#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import argparse
from base64 import b64encode
import json
import requests

CLIENT_ID = os.getenv('IMGUR_CLIENT_ID', None)
CLIENT_SECRET = os.getenv('IMGUR_CLIENT_SECRET', None)
IMG_UPLOAD_API = 'https://api.imgur.com/3/upload.json'
ALBUM_CREATION_API = 'https://api.imgur.com/3/album.json'
AUTH_HEADER = {"Authorization": "Client-ID " + str(CLIENT_ID)}


def upload(img):
    ''' Return uploaded data info in dictionary '''
    try:
        fp = open(img, 'rb').read()
    except IOError as e:
        print "Error: {}".format(e)
        sys.exit()
    fp_b64 = b64encode(fp)
    payload = {
        'key': CLIENT_SECRET,
        'image': fp_b64,
        'type': 'base64',
    }
    r = requests.post(IMG_UPLOAD_API, data=payload, headers=AUTH_HEADER)

    return json.loads(r.text)


def upload_image(path):
    ''' Return uploaded url '''
    return upload(path)['data']['link']


def upload_album(imgs):
    ''' Upload multiple files into one album, return album url '''
    # Create album first and get 'deletehash', 'id' values
    r = requests.post(ALBUM_CREATION_API, headers=AUTH_HEADER)
    album_data = json.loads(r.text)
    deletehash = album_data['data']['deletehash']
    name = album_data['data']['id']
    ALBUM_ADD_API = 'https://api.imgur.com/3/album/' + deletehash + '/add'
    img_ids = []
    for img in imgs:
        img_data = upload(img)
        img_ids.append(str(img_data['data']['id']))
    payload = {
        'ids': '%s' % ','.join(img_ids)
    }
    r = requests.post(ALBUM_ADD_API, data=payload, headers=AUTH_HEADER)
    if json.loads(r.text)['status'] == 200:
        return 'https://imgur.com/a/' + name
    else:
        print "Album creation failed!"
        print json.loads(r.text)


def get_args():
    '''
    Parses and returns arguments.
    If there is no
    '''
    parser = argparse.ArgumentParser(usage='python pyimgur.py [files]')
    parser.add_argument('files', type=str, nargs='+',
                        help='List of images to upload')
    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit()

    parser.parse_args()


def main():
    if not (CLIENT_ID or CLIENT_SECRET):
        print """
CLIENT_ID or CLIENT_SECRET missing.
Export keys on your terminal first:
$ export IMGUR_CLIENT_ID='your_client_id'
$ export IMGUR_CLIENT_SECRET='your_secret'
        """
        sys.exit()

    get_args()
    if len(sys.argv) > 3:
        print upload_album(sys.argv[1:])
    else:
        print upload_image(sys.argv[1])


if __name__ == '__main__':
    main()
