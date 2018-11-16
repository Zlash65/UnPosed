# -*- coding: utf-8 -*-
import sqlite3

class PhotoDB():
	def __init__(self):
		self.conn = sqlite3.connect("flickr.db")
		self.setup()

	def setup(self):
		self.create_group_table()
		self.create_photo_table()

	def create_group_table(self):
		self.conn.execute('''CREATE TABLE IF NOT EXISTS GROUPS
			(
				group_id CHAR(20) PRIMARY KEY NOT NULL,
				name CHAR(50) NOT NULL,
				topic_count INT,
				iconserver  INT,
				privacy CHAR(20),
				members INT,
				total_photos INT,
				iconfarm INT
			);
		''')

	def create_photo_table(self):
		self.conn.execute('''CREATE TABLE IF NOT EXISTS PHOTOS
			(
				photo_id CHAR(20) PRIMARY KEY NOT NULL,
				title CHAR(50) NOT NULL,
				group_id CHAR(20),
				views INT,
				datetaken DATETIME,
				dateuploaded TIMESTAMP,
				originalformat CHAR(10),
				iconserver  INT,
				iconfarm INT,
				location CHAR(30),
				nsid CHAR(20),
				tags TEXT,
				url text
			);
		''')

	def insert_group(self, group):
		# columns = ["group_id", "name", "topic_count", "iconserver", 
		# 	"privacy", "members", "total_photos", "iconfarm"]
		columns = list(group.keys())

		values = [str(group.get(d)).encode('ascii', 'ignore') for d in columns]

		try:
			self.conn.execute('''
				INSERT INTO GROUPS (%s)
				VALUES (%s)
			''' % (', '.join(columns), ','.join(['?'] * len(columns))), tuple(values))
			self.conn.commit()
			return True
		except Exception, e:
			print(e)
			return False

	def insert_photo(self, photo):
		# columns = ["photo_id", "title", "group_id", "views", "datetaken", "dateupload", 
		# 	"originalformat", "iconserver", "iconfarm", "location", "nsid", "tags"]
		columns = list(photo.keys())

		try:
			values = [str(photo.get(d)).encode('utf-8') for d in columns]

			self.conn.execute('''
				INSERT INTO PHOTOS (%s)
				VALUES (%s)
			''' % (', '.join(columns), ','.join(['?'] * len(columns))), tuple(values))
			self.conn.commit()
			return True
		except Exception, e:
			print(e, "hree")
			return False