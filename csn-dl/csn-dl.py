#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import argparse
from CSNParser import CSNParser


def get_args():
    ''' Parses and returns arguments passed in '''
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--song', action='store_true',
                        help="Make script to download songs instead album")
    parser.add_argument('-f', '--filename',
                        help="Specify input file contains album urls")
    parser.add_argument('-d', '--directory',
                        help="Specify directory to store songs.")
    parser.add_argument('-u', '--url', nargs='+', default=None,
                        help="Specify url(s) of song/album")
    args = parser.parse_args()
    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(1)
    else:
        return args.song, args.filename, args.directory, args.url


def main():
    get_song_only, file_name, store_dir, urls = get_args()
    if store_dir is None:
        store_dir = 'Downloaded'
    ''' Get urls input directly from CLI '''
    if urls:
        try:
            if get_song_only:
                for url in urls:
                    CSNParser(url).download_song(store_dir)
            else:
                for url in urls:
                    CSNParser(url).download_album(store_dir)
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
                        CSNParser(url).download_song(store_dir)
                else:
                    for url in [line.strip('\n') for line in f]:
                        CSNParser(url).download_album(store_dir)
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
