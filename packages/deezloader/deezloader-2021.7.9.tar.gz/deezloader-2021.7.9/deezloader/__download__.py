#!/usr/bin/python3

from tqdm import tqdm
from copy import deepcopy
from os.path import isfile
from .__dee_api__ import API
from .__deegw_api__ import API_GW
from .__taggers__ import write_tags
from .__others_settings__ import answers
from .__deezer_settings__ import qualities
from .__download_utils__ import genurl, decryptfile
from .exceptions import TrackNotFound, QualityNotFound

from .models import (
	Track, Album, Playlist,
	Preferences,
)

from .__utils__ import (
	set_path, check_md5_song,
	trasform_sync_lyric, create_zip
)

class Download_JOB:
	def __init__(self, gw_api: API_GW, api: API):
		self.gw_api = gw_api
		self.api = api

class EASY_DW:
	def __init__(
		self,
		download_job: Download_JOB,
		preferences: Preferences,
		infos_dw: dict
	) -> None:
		self.__gw_api = download_job.gw_api
		self.__api = download_job.api

		self.__infos_dw = infos_dw

		self.__link = preferences.link
		self.__ids = preferences.ids
		self.__song_metadata = preferences.song_metadata
		self.__output_dir = preferences.output_dir
		self.__method_save = preferences.method_save
		self.__recursive_download = preferences.recursive_download
		self.__recursive_quality = preferences.recursive_quality
		self.__quality_download = preferences.quality_download
		self.__not_interface = preferences.not_interface

		self.__c_quality = qualities[self.__quality_download]
		self.__num_quality = self.__c_quality['n_quality']
		self.__file_format = self.__c_quality['f_format']
		self.__song_quality = self.__c_quality['s_quality']

		self.__song_path = set_path(
			self.__song_metadata,
			self.__output_dir,
			self.__song_quality,
			self.__file_format,
			self.__method_save
		)

	def easy_dw(self) -> Track:
		pic = self.__infos_dw['ALB_PICTURE']
		image = self.__api.choose_img(pic)
		self.__song_metadata['image'] = image
		song = f"{self.__song_metadata['music']} - {self.__song_metadata['artist']}"

		if not self.__not_interface:
			msg = f"Downloading: {song}"
			print(msg)

		try:
			track = self.download_try()
		except TrackNotFound:
			ids = self.__api.not_found(song, self.__song_metadata['music'])
			self.__infos_dw = self.__gw_api.get_song_data(ids)
			track = self.download_try()

		track.md5_image = pic

		return track

	def download_try(self) -> Track:
		self._c_track = Track(
			self.__song_metadata, self.__song_path,
			self.__file_format, self.__song_quality,
			self.__link, self.__ids
		)

		if isfile(self.__song_path):
			if self.__recursive_download:
				return self._c_track

			ans = input(
				f"Track {self.__song_path} already exists, do you want to redownload it?(y or n):"
			)

			if not ans in answers:
				return self._c_track

		song_md5, version = check_md5_song(self.__infos_dw)
		song_hash = genurl(song_md5, self.__num_quality, self.__ids, version)

		if len(song_md5) == 0:
			raise TrackNotFound

		md50 = song_md5[0]

		try:
			crypted_audio = self.__gw_api.song_exist(md50, song_hash)
		except TrackNotFound:
			if not self.__recursive_quality:
				song = self.__song_metadata['music']
				artist = self.__song_metadata['artist']
				not_found_str = f"{song} - {artist}"
				msg = f"The {not_found_str} can't be downloaded in {self.__quality_download} quality :("
				raise QualityNotFound(msg = msg)

			for c_quality in qualities:
				if self.__c_quality == c_quality:
					continue

				self.__c_quality = qualities[c_quality]
				self.__num_quality = self.__c_quality['n_quality']
				self.__file_format = self.__c_quality['f_format']
				self.__song_quality = self.__c_quality['s_quality']

				song_hash = genurl(
					song_md5, self.__num_quality, self.__ids,
					self.__infos_dw['MEDIA_VERSION']
				)

				try:
					crypted_audio = self.__gw_api.song_exist(md50, song_hash)
				except TrackNotFound:
					raise TrackNotFound("Error with this song", self.__link)

		c_crypted_audio = crypted_audio.iter_content(2048)

		decryptfile(c_crypted_audio, self.__ids, self.__song_path)
		self.__add_more_tags()
		write_tags(self.__song_path, self.__song_metadata, self.__file_format)

		return self._c_track

	def __add_more_tags(self) -> None:
		contributors = self.__infos_dw['SNG_CONTRIBUTORS']

		if "author" in contributors:
			self.__song_metadata['author'] = " & ".join(
				contributors['author']
			)
		else:
			self.__song_metadata['author'] = ""

		if "composer" in contributors:
			self.__song_metadata['composer'] = " & ".join(
				contributors['composer']
			)
		else:
			self.__song_metadata['composer'] = ""

		if "lyricist" in contributors:
			self.__song_metadata['lyricist'] = " & ".join(
				contributors['lyricist']
			)
		else:
			self.__song_metadata['lyricist'] = ""

		if "composerlyricist" in contributors:
			self.__song_metadata['composer'] = " & ".join(
				contributors['composerlyricist']
			)
		else:
			self.__song_metadata['composerlyricist'] = ""

		if "version" in self.__infos_dw:
			self.__song_metadata['version'] = self.__infos_dw['VERSION']
		else:
			self.__song_metadata['version'] = ""

		self.__song_metadata['lyric'] = ""
		self.__song_metadata['copyright'] = ""
		self.__song_metadata['lyricist'] = ""
		self.__song_metadata['lyric_sync'] = []

		if self.__infos_dw['LYRICS_ID'] != 0:
			need = self.__gw_api.get_lyric(self.__ids)

			if "LYRICS_SYNC_JSON" in need:
				self.__song_metadata['lyric_sync'] = trasform_sync_lyric(
					need['LYRICS_SYNC_JSON']
				)

			self.__song_metadata['lyric'] = need['LYRICS_TEXT']
			self.__song_metadata['copyright'] = need['LYRICS_COPYRIGHTS']
			self.__song_metadata['lyricist'] = need['LYRICS_WRITERS']

class DW_TRACK:
	def __init__(
		self,
		download_job: Download_JOB,
		preferences: Preferences
	):
		self.__download_job = download_job
		self.__gw_api = download_job.gw_api
		self.__preferences = preferences

	def dw(self) -> Track:
		ids = self.__preferences.ids
		infos_dw = self.__gw_api.get_song_data(ids)

		track = EASY_DW(
			self.__download_job, self.__preferences, infos_dw
		).easy_dw()

		return track

class DW_ALBUM:
	def __init__(
		self,
		download_job: Download_JOB,
		preferences: Preferences
	):
		self.__download_job = download_job
		self.__gw_api = download_job.gw_api
		self.__api = download_job.api

		self.__preferences = preferences
		self.__song_metadata = self.__preferences.song_metadata
		self.__not_interface = self.__preferences.not_interface
		self.__make_zip = self.__preferences.make_zip
		self.__output_dir = self.__preferences.output_dir
		self.__method_save = self.__preferences.method_save

		self.__song_metadata_items = self.__song_metadata.items()

	def dw(self) -> Album:
		c_song_metadata = {}
		ids = self.__preferences.ids
		infos_dw = self.__gw_api.get_album_data(ids)['data']
		md5_image = infos_dw[0]['ALB_PICTURE']
		image = self.__api.choose_img(md5_image)
		self.__song_metadata['image'] = image
		album = Album(ids)
		album.image = image
		album.md5_image = md5_image
		album.nb_tracks = self.__song_metadata['nb_tracks']
		album.album_name = self.__song_metadata['album']
		album.upc = self.__song_metadata['upc']
		tracks = album.tracks

		for key, item in self.__song_metadata_items:
			if type(item) is not list:
				c_song_metadata[key] = self.__song_metadata[key]

		t = tqdm(
			range(
				len(infos_dw)
			),
			desc = c_song_metadata['album'],
			disable = self.__not_interface
		)

		for a in t:
			for key, item in self.__song_metadata_items:
				if type(item) is list:
					c_song_metadata[key] = self.__song_metadata[key][a]

			c_infos = infos_dw[a]
			song = f"{c_song_metadata['music']} - {c_song_metadata['artist']}"
			t.set_description_str(song)
			c_preferences = deepcopy(self.__preferences)
			c_preferences.song_metadata = c_song_metadata
			c_preferences.ids = c_infos['SNG_ID']

			try:
				track = EASY_DW(
					self.__download_job, c_preferences, c_infos
				).download_try()

				tracks.append(track)
			except TrackNotFound:
				try:
					ids = self.__api.not_found(song, c_song_metadata['music'])
					song_info = self.__gw_api.get_song_data(ids)

					track = EASY_DW(
						self.__download_job, c_preferences, song_info
					).download_try()

					tracks.append(track)
				except TrackNotFound:
					track = Track(
						c_song_metadata,
						None, None,
						None, None, None,
					)

					track.success = False
					tracks.append(track)
					print(f"Track not found: {song} :(")
					continue

		if self.__make_zip:
			song_quality = tracks[0].quality

			zip_name = create_zip(
				tracks,
				output_dir = self.__output_dir,
				song_metadata = self.__song_metadata,
				song_quality = song_quality,
				method_save = self.__method_save
			)

			album.zip_path = zip_name

		return album

class DW_PLAYLIST:
	def __init__(
		self,
		download_job: Download_JOB,
		preferences: Preferences
	) -> Playlist:
		self.__download_job = download_job
		self.__gw_api = download_job.gw_api

		self.__preferences = preferences
		self.__make_zip = self.__preferences.make_zip
		self.__output_dir = self.__preferences.output_dir

	def dw(self):
		ids = self.__preferences.ids
		infos_dw = self.__gw_api.get_playlist_data(ids)['data']
		playlist = Playlist()
		tracks = playlist.tracks

		for a in range(
			len(infos_dw)
		):
			c_infos_dw = infos_dw[a]
			c_preferences = deepcopy(self.__preferences)
			c_preferences.song_metadata = self.__preferences.song_metadata[a]
			c_song_metadata = c_preferences.song_metadata

			if type(c_song_metadata) is not dict:
				not_found_str = f"Track not found {c_song_metadata['title']} :("
				print(not_found_str)
				continue

			track = EASY_DW(
				self.__download_job, c_preferences, c_infos_dw
			).easy_dw()

			tracks.append(track)

		if self.__make_zip:
			zip_name = f"{self.__output_dir}/playlist [{ids}]"
			create_zip(tracks, zip_name = zip_name)
			playlist.zip_path = zip_name

		return playlist