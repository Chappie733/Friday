import pafy
import vlc


class VideoScraper:
	DEFAULT_VOLUME = 75

	def __init__(self):
		self.Instance = vlc.Instance()
		self.player = self.Instance.media_player_new()
		self.curr_media = None
		self.volume = self.DEFAULT_VOLUME
		self.playlist = None
		self.curr_playlist_index = None

	def load_playlist(self, filename):
		with open(filename, 'r') as file:
			lines = file.readlines()

			for idx in range(len(lines)):
				lines[idx] = lines[idx].replace('\n', '')

			self.playlist = lines
			self.curr_playlist_index = 0

	def play_playlist(self, video=False):
		if self.curr_playlist_index == len(self.playlist):
			self.curr_playlist_index = 0
		self.play(self.playlist[self.curr_playlist_index], video=True)

	def playlist_next(self):
		self.player.stop()
		self.curr_playlist_index += 1
		self.play_playlist()

	def play(self, url, video=False):
		self.player.stop()

		vid = pafy.new(url)
		best = vid.getbest() if video else vid.getbestaudio()
		playurl = best.url

		self.curr_media = self.Instance.media_new(playurl)
		self.player.set_media(self.curr_media)
		self.player.play()

	def toggle(self):
		self.player.pause()

	def stop(self):
		self.player.stop()

	def set_volume(self, volume):
		self.volume = volume
		self.player.audio_set_volume(volume)