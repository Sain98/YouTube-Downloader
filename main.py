# -*- coding: utf-8 -*-
# Python version 2.7.13
from pytube import YouTube
from pytube.utils import print_status
import moviepy.editor as mp
import sys
import os

API_KEY = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
API_URL = 'https://www.googleapis.com/youtube/v3/playlistItems'


# Download video from the given url
def download(url, destination, quality, filename=None):
	"""
	@params:
		URL: url to the video we want to download
			ex. 'https://www.youtube.com/watch?v=7kBiBrSlq3g'

		Destination: Where we will save the video
			ex. 'D:\Projects\Youtube Downloader\playlist1\'

		Quality: an array of which quality we want to try to download
			ex. ['1080p', '720p', '480p', '360p']
			will first try to get the video in 1080p
			if thats not available it will try 720p then 480p and at last 360p
			as soon as it gets a match for its quality it will start downloading
			and ignore the other quality's as they are no longer needed

		filename: What name we should save the downloaded video under
			default is None since it can copy the title from the video we are trying to download
	"""
	yt = YouTube(url)

	if filename == None:
		print (
			"[*] Generated Filename: %s" %
			unicode(yt.filename).encode(sys.stdout.encoding, errors="replace")
			)

		filename = unicode(yt.filename).encode(sys.stdout.encoding, errors="replace")


	filename = clean_filename(filename)

	yt.set_filename(filename)


	# ===== / Filters / ===

	print "[*] Trying filter..."

	for res in quality:
		vid_quality = yt.filter(resolution=res)
		if len(vid_quality) > 0:
			print "[*] Getting video | Quality: {}".format(res)
			vid = yt.get('mp4', resolution=res)
			break

	dir = os.getcwd() + "\\" + destination + "\\"

	if not os.path.isdir(dir):
		try:
			print "[Warning] Directory: [{}]\nDid not exist".format(dir)
			os.makedirs(dir)
		except OSError as err:
			print err

	print "[*] Downloading video to: %s" % dir

	try:
		vid.download(dir, on_progress=print_status)
		del vid
	except OSError:
		print "[Warning] File already exists\n[%s]" % (dir + filename)

	return


# Sanitize the given filename
def clean_filename(filename):
	"""
	@params:
		filename: any filename

	@function:
		This function checks the given filename and clears it of any bad characters
		as these characters can cause problems when trying to save the file
	"""
	reserved_chars = ['<','>',':','"', '/', '\\', '|', '?', '*']

	for ch in reserved_chars:
		for ch2 in filename:
			filename = filename.replace(ch, '')

	return filename


# Converting mp4 -> mp3, etc..
def convert(source, source_dir, dest_dir='mp3'):
	"""
	@params:
		source: The location off the source we want to convert
		source_dir: The source directory the file needs to be loaded from
		dest_dir: The destination directory the file needs to be saved to
			default (mp3) saves it to a folder called mp3
	"""
	source_vid = source_dir + source
	print "Attempting to load file @ " + str(source_vid)

	# Free up the used memory - WITHOUT THIS IT WILL MEMLEAK
	del vid.reader
	del vid

	return


# Main menu options:
def opt_filename():
	print "Option: Filename"
	print "Please enter the filename"

	filename = raw_input('Filename: ')

	quality = opt2_quality()

	try:
		f = open(filename, 'r')
	except Exception as ex:
		print ex

	urls = {}	# {0: [url, custom_filename], 1: ...}
	counter = 0

	# Get all the url's from file
	for line in f:
		a = line.split(" : ")

		print "Downloading: " + str(a[0])
		print "Destination: " + filename.split('.')[0]
		print "Target quality: " + str(quality)
		print "Video number: " + str(counter)

		if len(a) == 2:
			# URL, DESTINATION (folder), QUALITY, FILENAME (custom filename for the video)
			download(
				url=str(a[0]),
				destination=filename.split('.')[0], 
				quality=quality, 
				filename=str(a[1])
				)
		else:
			download(
				url=str(a[0]),
				destination=filename.split('.')[0], 
				quality=quality
				)

		counter += 1

	print "Finished"
	f.close()

def opt_playlist():
	# TODO:
	return


def opt_direct():
	print "Please enter a url from the video you would like to download"
	url = raw_input("URL: ")

	quality = opt2_quality()

	print "Custom filename? (y/n)"
	f = raw_input("Y/N: ").lower()



	if f[0] == 'y':
		# Using custom filename
		filename = raw_input("Filename: ")
		download(url, destination='downloads', quality=quality, filename=filename)
	elif f[0] == 'n':
		# No custom filename
		download(url, destination='downloads', quality=quality)

	else:
		print "Unexpected answer please type either: y for yes or n for no"
		opt_direct()

	return


def opt_convert():
	# TODO:
	return


# Secondary options
def opt2_quality():
	quality_arr = []

	# All possible video quality's
	all_qual = ['144p', '240p', '360p', '480p', '720p', '1080p', '1440p', '2160p']

	print "Please choose the desired quality"
	print "from high to low priority\n"

	print "Quality's:"
	print "1. HD > LD - [1080p > 720p > 480p > 360p]"
	print "2. LD > HD - [360p > 480p > 720p > 1080p]"
	print "3. Custom - Ex. 720p, 480p, 360p"

	opt = raw_input("Quality: ")

	if opt == '1':
		quality_arr = ['1080p', '720p', '480p', '360p']

	elif opt == '2':
		quality_arr = ['360p','480p','720p','1080p']

	elif opt == '3':
		# TODO
		print "Please enter a custom quality preset"
		print "From high to low priority seperated by ','"
		print "Possible quality's: [{}]".format(all_qual)
		quality_arr = raw_input("Quality: ")

		quality_arr = quality_arr.replace(' ', '').split(',')

	else:
		print "Unknown option please try again..."
		opt2_quality()

	return quality_arr


# == MAIN ==
def main():
	# DEBUG:
	download(
		'https://www.youtube.com/watch?v=0G1lZVCJuSQ',
		'downloads',
		['1080p', '720p', '480p', '360p']
		)

	quit()
	# ==========
	print "YouTube Downloader Version 2"
	print "Please select how you will be giving the URL's for the video's"
	print ""
	print "Options:"
	print "1. | Filename"
	print "2. | Playlist"
	print "3. | Direct link"
	print "5. | Convert file to mp3"
	print "9. | Exit"
	print ""

	option = raw_input("Option: ")

	if option == '1':
		opt_filename()

	elif option == '2':
		opt_playlist()

	elif option == '3':
		opt_direct()

	elif option == '5':
		opt_convert()

	elif option == '9':
		quit(0)

	else:
		print "\n" * 10
		print "Invalid option!"
		main()

	return


if __name__ == '__main__':
	main()