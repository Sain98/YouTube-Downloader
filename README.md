# YouTube-Downloader
by _Sain

### About this project:
This is a small toy project i used to get a few video's i wanted off youtube. 

Python version 2.7.13

### Requirements:
YouTube library used: [PyTube](https://github.com/nficano/pytube)

Audio/Video Library used: [MoviePy](https://github.com/Zulko/moviepy)
(for converting to mp3's)

also required FFMPEG for the audio library 

(MoviePy installed it for me or search it through google if it doesnt)

### Features:
Currently in its 2nd version which has support for different types off input such as:

+ direct link
+ link(s) from file
+ link(s) from a YouTube playlist (TODO)

#### Downloading links from a file:
for every line on the file it checks or the user gave a custom title

uses the link to download the file and if given saves it under the custom title

if no custom title is given it will save it under a generated one

##### Example for a file (any_name.txt):
https://www.youtube.com/watch?v=dQw4w9WgXcQ : My video title

#### Note for custom title's:
any reserved characters will be removed from the custom title
This is because of how filenames work in windows

reserved characters: 
['<', '>', ':', '"', '/', '\\', '|', '?', '*']
