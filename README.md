# covers_change
A simple (but limited for now) script to change the image tag for flac files.

It can be used in order to show the illustrations of the music in Recordbox, when the musics readers shows them but Recordbox don't.
I mean it will simply change the tag for the covers of the id3 metadata.
It basically change the "Other" tag associated to a image (usually used for a cover), to the "Cover" tag.

How to use :
1. Make shure python is installed on your device.
2. Install if needed the "mutagen" python library.
3. Place the main program in the directory you wish to have your covers adjusted. 
4. Run the program. It should go down the subdirectories to change the tag of the music.

Credits : 
Maxime-esiee, Cascade
