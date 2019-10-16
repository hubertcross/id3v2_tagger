import os
import re
import subprocess

# This script adds id3v2 tags to mp3s organized in the following manner:
# Artist/YEAR-ALBUM/TRACKNUMBER_TRACKNAME.mp3
# i.e. (/Users/hubert/Music/) Radiohead/1995-The_Bends/01_Planet_Telex.mp3
# It does NOT correct case.
# My need to tag my mp3 collection came from realizing the iOS version of VLC does NOT let you simply browse directories
# to play music. It organizes all your mp3s by "Album", "Artist" etc using the damn id3v2 tags. Untagged mp3s turn into
# horrid mess. This is probably useful for iTunes as well.

# TODO: Clean up the code, check for existing id3v2 tags in an album's mp3's and skip processing if they're already tagged

# TODO: check for id3v2 program on system and bail if not present

# this probably does not need to be global
my_struct = {}


# TODO: Implement and use
def check_for_existing_id3v2_tags(path):
    pass

def run_clear_tag_cmd(path):
    clear_tag_cmd = ["id3v2", "-D", path]
    subprocess.call(clear_tag_cmd)
    # pass

def run_write_tag_cmd(struct):
    write_tag_cmd = ["id3v2", "-2", "-A", struct['album_name'], "-a", struct['artist'], "-t", struct['songname'], "-y",
                     struct['year'], "-T", struct['tracknum'], struct['full_path_to_song']]
    subprocess.call(write_tag_cmd)
    # pass

for root, dir, file in os.walk("/Users/hubert/Music"):
    # if re.match('\[0-9\]\{4\}-\[a-zA-Z_ \]', dir):
    # print("dir: %s" % dir)
    for album in dir:
        if re.match('^[0-9]{4}-[0-9a-zA-Z_\s]{1,}$', album): # re.match('\[0-9\]\{4\}-\[a-zA-Z_ \]', album):
            artist = os.path.basename(root)
            print("| %s %s" % (artist, album))
            songs = os.listdir(os.path.join(root, album))

            if not re.match('.*mp3$', songs[0]):
                continue

            songs.sort()
            for song in songs:
                print("Song: %s" % song)

                print("Full path to song: %s" % os.path.join(root, album, song))

                full_path_to_song = os.path.join(root, album, song)
                year = album.split('-')[0]
                songname = song.split("_", 1)[1]
                songname = songname.replace('.mp3', '')
                tracknum = song.split("_")[0]
                album_name = album.split("-")[1]
                print("Artist: %s | Album Name: %s | Year: %s | songname: %s | tracknum: %s" % (artist, album_name, year, songname, tracknum))


                my_struct = { "artist" : artist,
                            "album_name" : album_name,
                            "year" : year,
                            "songname" : songname,
                            "tracknum" : tracknum,
                            "full_path_to_song": full_path_to_song }

                print("Stop")
                run_clear_tag_cmd(full_path_to_song)
                run_write_tag_cmd(my_struct)

"""
dictionary structure:
{ artist: "radiohead", "album" : "the_bends", "year": "1995", "track" : "01", "songname" : "planex_telex" } }

# id3v2 program commands (you can get this program by using 'brew install id3v2' on MacOS)
# -2 write id3v2
# -A album
# -a artist
# -t songname
# -y year
# -T tracknum

"""