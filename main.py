# -*- coding: utf-8 -*-
"""
Youtube downloader by _Sain

YouTube library used: https://github.com/nficano/pytube
Audio Library used: https://github.com/Zulko/moviepy

also required FFMPEG for the audio library

How it works:
You have a file each line contains a link and if you want a custom title
the custom title will be used as a filename to save the downloaded video under
it will be stored inside a folder that will be made with the same name
as the file you enter that contains your url's
After it finished downloading all the youtube videos,
it will start converting them all into mp3's into a seperate folder named 'mp3'

Note for custom title's 
any reserved characters will be removed from the custom title
reserved characters: ['<', '>', ':', '"', '/', '\\', '|', '?', '*']

Content for the file containing the videos you want to download:
URL : Custom title (not required)

Example - playlist.txt:
https://www.youtube.com/watch?v=uEpfPVQy_Bc : Fire From The Gods - Excuse Me
https://www.youtube.com/watch?v=uk7OegsMOyM
"""
from pytube import YouTube
from pytube.utils import print_status
import moviepy.editor as mp
import sys
import os

def download(url, folder):
	if len(url) == 2:
		# URL has custom filename:
		custom_file = url[1]
	else:
		custom_file = None
		
	yt = YouTube(url[0])
	
	dir = folder.split('.')
	dir = dir[0]
	
	if custom_file == None:
		print (
			"[*] Generated filename: %s" %
			unicode(yt.filename).encode(sys.stdout.encoding, errors="replace")
			)
			
		file_name = unicode(yt.filename).encode(sys.stdout.encoding, errors="replace")
		
	elif custom_file != None:
		file_name = unicode(custom_file).encode(sys.stdout.encoding, errors="replace")
		
		
	# Reserved characters that we cant use for filenames
	reserved_chars = ['<','>',':','"', '/', '\\', '|', '?', '*']
	
	for ch in reserved_chars:
		if ch in file_name:
			file_name = file_name.replace(ch, "")
			
	print "[*] Cleaned filename: " + file_name
	yt.set_filename(file_name)	# Should stop the unicode errors
	
	print "[*] Trying filters"
	
	# ===== / Filters / ===
	
	uhd = yt.filter(resolution='1080p')
	if len(uhd) > 0:
		print uhd
		
	hd = yt.filter(resolution='720p')
	if len(hd) > 0:
		print hd
		
	ld = yt.filter(resolution='480p')
	if len(ld) > 0:
		print ld
		
	lld = yt.filter(resolution='360p')
	if len(lld) > 0:
		print lld
		
	# ===== / Filters / ===
	
	print "[*] Getting video"
		
	if len(uhd) > 0:
		print "[*] Got 1080p resolution video"
		vid = yt.get('mp4', '1080p')
	elif len(hd) > 0:
		print "[*] Got 720p resolution video"
		vid = yt.get('mp4', '720p')
	elif len(ld) > 0:
		print "Got 480p resolution video"
		vid = yt.get('mp4', '480p')
	elif len(lld) > 0:
		print "Got 360p resolution video"
		vid = yt.get('mp4', '360p')
		
	dir = os.getcwd() + "\\" + dir + "\\"
	print "[*] Downloading video to " + dir
	
	try:
		vid.download(dir, on_progress=print_status)
		
		del vid
	except OSError:
		print "[Warning] File [%s] already exists" % (dir + file_name)
		
	return file_name	# Need this part for converting them all to mp3's


def convert_to_mp3(dir, filename):
	dir = dir.split('.')[0]
	dir = os.getcwd() + "\\" + dir + "\\"
	
	try:
		os.makedirs(dir + 'mp3')
	except OSError:
		if not os.path.isdir(dir):
			raise
			
	if not os.path.exists(dir + "mp3\\" + filename.split('.')[0] + ".mp3"):
		print "[*] Directory: " + dir
		print "[*] Converting [%s] " % filename
		
		clip = mp.VideoFileClip(dir + filename + ".mp4")
		out = dir + "mp3\\" + filename.split('.')[0] + ".mp3"
		clip.audio.write_audiofile(out)
		
		print "\n[*] Finished new filename = " + out 
		print "=" * 25
		
		# Cleanup
		del clip.reader
		del clip
		
	else:
		file = dir + "mp3\\" + filename.split('.')[0] + ".mp3"
		print "[Warning] File [%s] already exists" % file
	
	
def get_links(file_loc):
	urls = {}	# {0: [url, custom_filename], 1: ...}
	custom_file = ""
	counter = 0
	
	try:
		f = open(file_loc, 'r')
	except Exception as ex:
		print ex
		quit(0)
	
	for line in f:
		a = line.split(" : ")
		if len(a) == 2:
			urls[counter] = [str(a[0]), str(a[1][:-1])]
		else:
			urls[counter] = [str(a[0])]
		counter += 1
		
	return urls, counter
	
	
def show_list(dict):
	for x in range(len(dict)):
		print "URL : " + str(dict[x][0])
		
		if len(dict[x]) == 2:
			print "Custom filename : %s\n" % dict[x][1]
		else:
			print ""
	
	
def main():
	print "Youtube downloader"
	print "Please enter the filename containing all the links"
	print "For the video's you would like to download\n"
	
	file_name = raw_input("Filename: ")
	
	# Converter vars;
	filename = []

	urls, vid_counter = get_links(file_name)
	
	print ""
	
	print "[*] %i URL'S RECEIVED" % vid_counter
	print "[*] URL LIST:"
	
	show_list(urls)
	dir = str(file_name).split('.')[0]
	
	try:
		print "[*] Trying to make directory: " + dir
		os.makedirs(dir)
	except OSError:
		if not os.path.isdir(dir):
			raise
	
	for x in range(vid_counter):
		if 'https://www.youtube.com/' in str(urls[x][0]):
			print "\nDownloading URL : " + str(urls[x][0])	
			
			if len(urls[x]) == 2:
				print "Custom title : " + str(urls[x][1])
				
			print "Progress: %i/%i" % (x, vid_counter)
				
			filename += [download(urls[x], file_name)]	# URL, (file_name = folder)
			
		else:
			print "URL [%s] does not contain 'https://www.youtube.com/'" % str(urls[x][0])

		
	for f in filename:
		convert_to_mp3(file_name, f)		# Confusing name here file_name = folder/directory
	
	return 0
	
	
if __name__ == "__main__":
	main()
	
