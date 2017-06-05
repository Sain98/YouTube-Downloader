# YouTube-Downloader
by _Sain

### About this project:
This is a small toy project i used to get a few video's i wanted off youtube.
later i added another library so i was able to convert these videos to '.mp3' files
I currently am working on a second version that has more options for how to download etc.

### Requirements:
YouTube library used: https://github.com/nficano/pytube
Audio Library used: https://github.com/Zulko/moviepy
also required FFMPEG for the audio library (MoviePy installed it for me or search it trough google)

### How it works:
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

### Example for a file:
https://www.youtube.com/watch?v=dQw4w9WgXcQ : Not RickRoll
