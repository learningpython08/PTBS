#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import re
import errno
import requests
from bs4 import BeautifulSoup


class CSNParser:
    def __init__(self, url):
        self.url = url

    def __get_mp3_url(self, regex):
        ''' Get html page and parse it to get .mp3 url '''
        urls = []
        try:
            get_html = requests.get(self.url)
            soup = BeautifulSoup(get_html.text, 'html.parser')
            for url in soup.findAll('a', href=re.compile(regex)):
                urls.append(url['href'])
        except requests.exceptions.RequestException as e:
            print "Error detected: {}".format(e)
            sys.exit(1)

        return urls

    def __get_song_mp3(self):
        ''' Get .mp3 url of the song '''
        url_tmp = self.url.rsplit('.', 1)
        self.url = url_tmp[0] + '_download.' + url_tmp[1]
        mp3_url = self.__get_mp3_url('320kbps')

        return mp3_url

    def __get_album_title(self):
        ''' Get the title of album to create store dir '''
        try:
            get_html = requests.get(self.url)
            soup = BeautifulSoup(get_html.text, 'html.parser')
            for title in soup.findAll('span', class_='maintitle'):
                return str(title.text).replace(' ', '_')
        except requests.exceptions.RequestException as e:
            print "Error detected: {}".format(e)
            sys.exit(1)

    def __get_album_mp3(self):
        ''' Get all .mp3 urls of an album '''
        mp3_urls = []
        download_urls = self.__get_mp3_url('download')
        for song_url in set(download_urls):
            self.url = song_url
            mp3_urls.append(self.__get_mp3_url('320kbps'))

        return mp3_urls

    def __download_mp3(self, store_dir):
        ''' Download .mp3 file '''
        BLOCK_SIZE = 4096
        url = str(''.join(self.url))
        file_name = ''.join(url).split('/')[-1].replace('%20', ' ')
        file_path = os.path.join(store_dir, file_name)
        req = requests.get(url, stream=True)
        file_size = int(req.headers['content-length'])
        if os.path.isfile(file_path) and \
                file_size == os.path.getsize(file_path):
            print "%s already existed" % file_name
        else:
            with open(file_path, 'wb') as f:
                downloaded = 0
                print "Downloading '%s' to %s" % (file_name, store_dir)
                for chunk in req.iter_content(chunk_size=BLOCK_SIZE):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        done = int(downloaded * 100 / file_size)
                        sys.stdout.write("\r%d%%...done" % done)
                        sys.stdout.flush()
                print "\n"

    def __mkdir_p(self, path):
        try:
            if not os.path.isdir(path):
                os.makedirs(path)
                print "%s created!" % (path)
        except OSError as e:
            if e.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else:
                print "Error detected: {}".format(e)
                sys.exit(1)

    def download_album(self, store_dir):
        ''' Download all mp3 in album '''
        album_title = self.__get_album_title()
        p = os.path.join(store_dir, 'CSN-Albums', album_title)
        self.__mkdir_p(p)
        urls = self.__get_album_mp3()
        for u in urls:
            self.url = u
            self.__download_mp3(p)

    def download_song(self, store_dir):
        ''' Download single song '''
        p = os.path.join(store_dir, 'CSN-Songs')
        self.__mkdir_p(p)
        self.url = self.__get_song_mp3()
        self.__download_mp3(p)
