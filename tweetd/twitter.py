#!/usr/bin/env python

import datetime
import tweepy
import tweetd

class Search:
	classid = 'twitter.search'
	def __init__(self, q):
		self.q = q
		self.dbid = '%s.%s' % (self.classid, tweetd.hexhash(q))
		if not self.dbid in tweetd.db:
			tweetd.db[self.dbid] = {'q': q}
		self.dbdoc = tweetd.db[self.dbid]

	def fetch(self):
		results = tweepy.api.search(q=self.q)
		maxid = 0
		for result in results:
			del result.from_user_id
			tweet = Tweet(result, retriever=[self.classid, self.q])
			if tweet.ID > maxid:
				maxid = tweet.ID
		self.dbdoc['since_id'] = maxid

class Tweet:
	mappings = {'from_user': 'from_name', 'from_user_id': 'from_id', 'id': 'ID',
	            'text': 'text'}
	additional = ['created', 'retriever']
	def __init__(self, data, retriever=None):
		for (a, b) in self.mappings.iteritems():
			if hasattr(data, a):
				setattr(self, b, getattr(data, a))
		if not self.ID:
			raise Exception('no ID given')
		if hasattr(data, 'created_at'):
			c = data.created_at
			if isinstance(c, datetime.datetime):
				self.created = c.isoformat()
				if c.utcoffset() is None:
					self.created += '+00:00'
		if retriever is not None:
			self.retriever = [retriever,]
		self.dbid = 'twitter.tweet.' + str(self.ID)
		self.save()

	def save(self):
		attrs = self.mappings.values()
		attrs.extend(self.additional)
		t = {}
		for x in attrs:
			if hasattr(self, x):
				t[x] = getattr(self, x)
		if not self.dbid in tweetd.db:
			tweetd.db[self.dbid] = t
		# TODO: Else, update.
		self.dbdoc = tweetd.db[self.dbid]
