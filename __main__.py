from urllib.parse import urljoin
import re
import pdb

import requests
from bs4 import BeautifulSoup

import scrapit


BASE_URL = 'http://www.chordie.com/'


class Song:
    def __init__(self, title, artist):
        self.title = title
        self.artist = artist        


def construct_rel_url(song):
    """Return the relative URL used to search for the song parameter by title
    and artist.
    """

    return '?q=' + song.artist.replace(' ', '+') + '+' \
        + song.title.replace(' ', '+') \
        + '&np=0&ps=10&wf=2221&s=RPD&wf=2221&wm=wrd&type=&sp=1&sy=1&cat=&ul=&np=0'


def construct_url(song):
    """Return the full URL used to search for the song parameter by title
    and artist.
    """

    return urljoin(BASE_URL, construct_rel_url(song))


def parse_songlist_file():
    """Return an array of Song objects from plaintext file 'songlist', 
    located in root dir.  File must have the following format:

    @artist1
    song1 by artist1
    song2 by artist1
    song3 by artist1

    @artist2
    song1 by artist2
    song2 by artist2
    song3 by artist2        
    """

    # Need more error-checking and punctuation replacement
    f = open('songlist', 'r')
    t1 = f.read().lower().split('@')[1:]
    songs = []
    for each1 in t1:
        t2 = each1.split('\n')
        for each2 in t2[1:-1]:
            if each2 != '':
                songs.append(Song(each2.lower(), t2[0].lower()))
    return songs


def process_songlist(songlist):
    """Iterate through Song objects in songlist."""

    for song in songlist:
        process(song)
        scrapit.delay()
        

def process(song):
    """Attempt to retrieve chopro data and output to chopro file in 
    /chopro/ dir.
    """

    # Search Chordie
    song_url = get_song_url(song)
    if song_url == None:
        print ('Song not found on Chordie: ' + song.title + ' - ' + song.artist)
        return

    # Retrieve chopro
    chopro = get_chopro(song_url)
    if chopro == None:
        print ('Chopro retrieval failed for: ' + song.title + ' - ' + song.artist)
        return

    # Write to disk
    write_chopro(song, chopro)
    print (song.title + ' - ' + song.artist + ' successfully retrieved!')


def get_song_url(song):
    """Search for song on Chordie and return the relative URL of a result with a
    chopro file.
    """

    url = construct_url(song)
    content = scrapit.get_content(url)
    soup = BeautifulSoup(content)
    soup_a = soup.find('a', {'title':"formatted guitar chord file"})
    if soup_a != None:
        href = soup_a.get('href')
        return href
    else:
        return None


def get_chopro(song_url):
    """Return chopro file based on relative song URL."""

    url = urljoin(BASE_URL, song_url)
    content = scrapit.get_content(url)
    soup = BeautifulSoup(content)
    chopro = soup.find('form', {'action':'/chopro.php'}).find('input').get('value')
    return chopro
   

def write_chopro(song, chopro):
    """Write out chopro file to disk in /chopro/ dir."""

    filename = song.artist.replace(' ', '_') + '-' + song.title.replace(' ', '_') + '.chopro'
    f = open('chopro/' + filename, 'w')
    f.write(chopro)
    f.close()


if __name__ == '__main__':

    # Read desired songlist into an array
    songlist = parse_songlist_file()

    # Attempt to retrieve chopro files
    process_songlist(songlist)




# ------------------------------------------------------------------------
# DEBUG
# ------------------------------------------------------------------------
    # Output html file
    #
    # f = open('ex/chopro.html', 'w')
    # f.write(soup.prettify())
    # f.close()

    # pdb.set_trace()
# ------------------------------------------------------------------------
