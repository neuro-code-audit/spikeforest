#!/usr/bin/env python

from mountaintools import client as mt
sha1_path = mt.saveFile('klusta.simg')
print(sha1_path)
mt.saveFile('klusta.simg', upload_to='spikeforest.public')
print(sha1_path)
