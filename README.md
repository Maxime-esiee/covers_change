# covers_change
As simple as possible, a small script to organise the cover of albums from flac files.

It can be used in order to show the illustrations of the music in Recordbox, when the musics readers read them but recordbox don't.

When the python program is added in the directory where you want to change the covers, it will update the covers from the flac files.
By "update the covers", I mean it will simply change the tag for the covers of the id3 metadata. It basically change the "Other" tag associated to a image (usually used for a cover), to the "Cover" tag.

How to use :
1. Make shure python is installed on your device.
2. Install if needed the "mutagen" python library.
3. Place the main program in the directory you wish to have your covers adjusted. 
4. Run the program. It should go down the subdirectories to change the tag of the music.

Credits : 
Maxime-esiee, Cascade
