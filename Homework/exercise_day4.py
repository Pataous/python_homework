import os
import warnings

# Since I could not manage to get sh in Windows, I am using a python module called webbrowser.py
import webbrowser

# I use expanduser to get the path to the "home" folder because that is the simplest way I could find in Windows
home = os.path.expanduser("~")
os.chdir(home)

class Song(object):
	"""A class that decribes musical songs"""
	#good_song = True
	def __init__(self, title = "dring", artist = "lambda", duration = None): #constructor
		self.title = title
		self.artist = artist
		self.duration = duration

	def description(self):
		'''print the basic info about that song'''
		print "title: ", self.title
		print "artist: ", self.artist
		print "duration: ", self.duration

	def pretty_duration(self):
		'''print the duration of a song in a nice way'''
		hours = self.duration / 3600
		minutes = (self.duration - hours * 3600) / 60
		seconds = (self.duration - hours *3600 - minutes * 60)

		return "%02i hours %02i minutes %02i seconds" %(hours, minutes, seconds)

	def play(self):
		'''Open a web browser window/tab with a youtube search for the title of the song'''

		webbrowser.open_new("https://www.youtube.com/results?search_query=%s" % self.title)



in_path = ("lulu_mix_16.csv")

""" Open the document and extracts the data line by line. First the data is extracted in a list of lists called l_songs. 
The headers are removed."""
l_songs = [s.strip('\n').split(',') for s in open(in_path)][1:]

"""songs will contain the data extracted from the .csv file in a different format. 
It will be a list of instances of the class Song."""
songs = []

for l in range(len(l_songs)):
	song = Song()
	song.title = l_songs[l][0]
	song.artist = l_songs[l][1]

	# if the duration of a song cannot be converted into an integer, it is set to 0 and a warning is returned
	# if the duration of a song is negative (after conversion to integer), an exception is raised and the program stops 
	try:
		song.duration = int(l_songs[l][2])
	except ValueError :
		warnings.warn("The duration of the song number %i, entitled \" %s \" is not a number." % (l+1,song.title))
		song.duration = 0

	if song.duration > 0 :
		songs.append(song)

	# Removed that part to be able to run the test lines below	
	#else:	
		#raise Exception("The duration of the song number %i, entitled \" %s \" is negative! Please check the data file." % (l+1,song.title))

# test routine	
for s in songs: print s.artist
for s in songs: print s.pretty_duration()
print sum(s.duration for s in songs), "seconds in total"
songs[6].play()

# Annnnnnnd it works :).





