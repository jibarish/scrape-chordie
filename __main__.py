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
    return '?q=' + song.artist.replace(' ', '+') + '+' \
        + song.title.replace(' ', '+') \
        + '&np=0&ps=10&wf=2221&s=RPD&wf=2221&wm=wrd&type=&sp=1&sy=1&cat=&ul=&np=0'


def construct_url(song):
    return urljoin(BASE_URL, construct_rel_url(song))


def parse_songlist_file():
    """Return an array of Song objects from plaintext file called 'songlist' 
    located in root dir. File must have the following format:

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


if __name__ == '__main__':

    songlist = parse_songlist_file()

    # pdb.set_trace()
