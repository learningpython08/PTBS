#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import re
import argparse
import errno
import requests
from bs4 import BeautifulSoup


def parse_url(url, regex):
    ''' Parse url to html object and get actual .mp3 url '''
    links = []
    try:
        get_html = requests.get(url)
        soup = BeautifulSoup(get_html.text, 'html.parser')
        for link in soup.findAll('a', href=re.compile(regex)):
            links.append(link['href'])
    except requests.exceptions.RequestException as e:
        print "Error detected: {}".format(e)
        sys.exit(1)

    return links


def parse_album_title(url):
    try:
        get_html = requests.get(url)
        soup = BeautifulSoup(get_html.text, 'html.parser')
        for title in soup.findAll('span', class_='maintitle'):
            return str(title.text).replace(' ', '_')
    except requests.exceptions.RequestException as e:
        print "Error detected: {}".format(e)
        sys.exit(1)


def parse_song_url(url):
    ''' Convert song url to download url and get .mp3 url '''
    url = url.rsplit('.', 1)[0] + '_download.' + url.rsplit('.', 1)[1]
    song_url = parse_url(url, '320kbps')

    return song_url


def parse_album_url(url):
    ''' Get list of .mp3 url of each song in album '''
    mp3_urls = []
    download_urls = parse_url(url, 'download')
    for song_url in set(download_urls):
        mp3_urls.append(parse_url(song_url, '320kbps'))

    return mp3_urls


def get_mp3(url, store_dir):
    BLOCK_SIZE = 4096
    ''' Actually download .mp3 file'''
    url = str(''.join(url))
    file_name = ''.join(url).split('/')[-1].replace('%20', ' ')
    file_path = os.path.join(store_dir, file_name)
    req = requests.get(url, stream=True)
    file_size = int(req.headers['content-length'])
    if os.path.isfile(file_path) and file_size == os.path.getsize(file_path):
        print "%s already existed" % file_name
    else:
        with open(file_path, 'wb') as f:
            downloaded = 0
            print "Downloading '%s' to %s " % (file_name, store_dir)
            for chunk in req.iter_content(chunk_size=BLOCK_SIZE):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    done = int(downloaded * 100 / file_size)
                    sys.stdout.write("\r%d%%...done" % done)
                    sys.stdout.flush()
            print "\n"


def create_dir(path):
    try:
        if not os.path.isdir(path):
            os.makedirs(path)
            print "%s created!" % path
    except OSError as e:
        if e.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            print "Error: {}".format(e)
            sys.exit(1)


def download_album(url, store_dir):
    album_dir = parse_album_title(url)
    store_dir = os.path.join(store_dir, 'CSN-Albums', album_dir)
    create_dir(store_dir)
    urls = parse_album_url(url)
    for url in urls:
        get_mp3(url, store_dir)


def download_song(url, store_dir):
    store_dir = os.path.join(store_dir, 'CSN-Songs')
    create_dir(store_dir)
    url = parse_song_url(url)
    get_mp3(url, store_dir)


def get_args():
    ''' Parses and returns arguments passed in '''
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--song', action='store_true',
                        help="Make script to download songs instead album")
    parser.add_argument('-f', '--filename',
                        help="Specify input file contains album urls")
    parser.add_argument('-d', '--directory',
                        help="Specify directory to store songs.")
    parser.add_argument('-u', '--URL', nargs='+', default=None,
                        help="Specify url(s) of song/album")
    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit()
    args = parser.parse_args()
    return args.song, args.filename, args.directory, args.link


def main():
    get_song_only, file_name, store_dir, links = get_args()
    if store_dir is None:
        store_dir = 'Downloaded'
    ''' Get urls input directly from CLI '''
    if links:
        try:
            if get_song_only:
                for url in links:
                    download_song(url, store_dir)
            else:
                for url in links:
                    download_album(url, store_dir)
        except KeyboardInterrupt as e:
            print "OK, terminating..."
            sys.exit(1)
        except:
            print "Unexpected error: ", sys.exc_type()[0]
            raise
    ''' Get urls from file '''
    if file_name:
        try:
            with open(file_name) as f:
                if get_song_only:
                    for url in [line.strip('\n') for line in f]:
                        download_song(url, store_dir)
                else:
                    for url in [line.strip('\n') for line in f]:
                        download_album(url, store_dir)
        except IOError as e:
            print "I/O error '{0}' : {1}".format(e.filename, e.strerror)
        except KeyboardInterrupt as e:
            print "OK, terminating..."
            sys.exit(1)
        except:
            print "Unexpected error: ", sys.exc_type()[0]
            raise


if __name__ == '__main__':
        main()
