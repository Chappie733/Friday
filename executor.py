from urllib.parse import quote
import webbrowser
import wikipedia
import os
from video_scraper import VideoScraper
from PIL import ImageGrab
from win32api import GetSystemMetrics

def search(*args):
	cmd_index = args[0][1]
	query = wikipedia.search(' '.join(args[0][0][cmd_index+1:]))[0]
	return wikipedia.summary(query, sentences=2)

def google(*args):
	cmd_index = args[0][1]
	if "youtube" not in args[0][0]:
		success = webbrowser.open("http://www.google.com/?#q=" + quote(' '.join(args[0][0][cmd_index+1:])))
	else:
		idx = args[0][0].index("youtube")
		success = webbrowser.open("https://www.youtube.com/results?search_query=" + quote(' '.join(args[0][0][cmd_index+1:idx-1])))
	return "There you go" if success else "Could not access the browser"

def play_music(*args):
	if 'stop' in ' '.join(args[0][0]):
		scraper = args[0][2].scraper
		scraper.stop()
	else: 
		success = webbrowser.open('https://www.youtube.com/results?search_query=music')
		return "There you go" if success else "Could not access the browser"

def play_playlist(*args):
	scraper = args[0][2].scraper
	words = args[0][0]
	if 'playlist' in words:
		playlists_folder = os.path.join(os.path.dirname(__file__), 'playlists')
		playlists = os.listdir(playlists_folder)
		found = False

		for word in words:
			if word + '.txt' in playlists:
				scraper.load_playlist(os.path.join(playlists_folder, word +'.txt')) 
				scraper.play_playlist()
				found = True
		return "There you go" if found else "Could not find the playlist"

def skip(*args):
	args[0][2].scraper.playlist_next()

def set_volume(*args):
	scraper = args[0][2].scraper
	words = args[0][0]
	volume = 100
	for word in words:
		if str.isnumeric(word):
			volume = int(word) if (int(word) >= 0 and int(word) <= 100) else 100
	scraper.set_volume(volume)

def screenshot(*args):
	image = ImageGrab.grab(bbox=(0,0,GetSystemMetrics(0), GetSystemMetrics(1)))
	screenshots_dir = os.path.join(os.path.dirname(__file__), 'screenshots')
	image.save(os.path.join(screenshots_dir, 'screenshot_%i.png' % len(os.listdir(screenshots_dir))))

def pause(*args):
	args[0][2].scraper.toggle()

def set_wiki_language(lang_id='en'):
	wikipedia.set_lang(lang_id)

# container class for all of the commands
class Executor:
	commands = [search, 
				google, 
				play_music, 
				play_playlist,
				pause, # pause
				pause, # resume
				skip,
				set_volume,
				screenshot]

	def __init__(self, lang):
		self.lang = lang
		self.scraper = VideoScraper()

	def process(self, words):
		feedback = ""

		cmd_id = -1
		cmd_index = 0
		# TODO: add support for multiple commands in one sentence? (stop reading a command when an another keyword is found perhaps)
		for idx in range(len(words)):
			if self.lang.is_command(words[idx]):
				cmd_id = self.lang.get_command_id(words[idx])
				cmd_index = idx
				print("Command found: " + str(words[idx]))
				break
		if cmd_id != -1:
			feedback = self.execute(words, cmd_index, self, cmd_id=cmd_id)
			
		return feedback if feedback != None else "", cmd_id != -1


	def execute(self, *args, **kwargs):
		try:
			return self.commands[kwargs['cmd_id']](args)
		except IndexError:
			print("Index out of bounds exception occurred whilst trying to call the command with id: " + str(cmd_id))
		return ""