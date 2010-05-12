#!/usr/bin/env python

import hashlib
import storage
import twitter

db = storage.Couch('tweetd')

def hexhash(val):
	return hashlib.sha256(val).hexdigest()
