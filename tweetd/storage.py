#!/usr/bin/env python

import couchdb

class Couch(object):
	def __init__(self, dbname):
		self.server = couchdb.Server()
		try:
			self.db = self.server[dbname]
		except couchdb.client.ResourceNotFound:
			self.db = self.server.create(dbname)

	def __getitem__(self, key):
		try:
			return self.db[key]
		except couchdb.client.ResourceNotFound:
			return None

	def __setitem__(self, key, value):
		self.db[key] = value

	def __contains__(self, key):
		return key in self.db
