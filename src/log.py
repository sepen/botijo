#!/usr/bin/env python

import os, datetime
import ConfigParser

class Log:

	# default values
	logdir = "~/.botijo/logs"
	logtype = "text"
	
	def __init__ (self, config):
		# read from config file
		if os.path.exists(config):
			conf = ConfigParser.ConfigParser()
			conf.readfp(file(config))
			self.logdir = conf.get("module log", "logdir")
			self.logtype = conf.get("module log", "logtype")
		# check for logdir
		self.logdir = self.logdir.strip('"')
		self.logdir = os.path.expanduser(self.logdir)
		if not os.access(self.logdir, os.F_OK | os.W_OK):
			os.mkdir(self.logdir)
		# check for logtype
		if (self.logtype == "sqlite"):
			import sqlite3 as lite
			self.bbddconn = lite.connect(self.logdir + '/log.db')

	def write (self, nick, message, channel):
		dt = datetime.datetime.now()
		(date, time) = str(dt).split()
		(time, prec) = time.split(".")
		if (self.logtype == "sqlite"):
			self.write_sqlite(date, time, nick, message, channel)
		else:
			self.write_text(date, time, nick, message, channel)

	def write_text (self, date, time, nick, message, channel):
		logdir = self.logdir + "/" + channel
		if not os.access(logdir, os.F_OK | os.W_OK):
			os.mkdir(logdir)
		logfile = logdir + "/" + date
		f = open(logfile, "a")
		f.write("%s [%s] %s\n" % (time, nick, message))
		f.close()

	def write_sqlite (self, date, time, nick, message, channel):
		print channel + " - " + date + " [" + nick + "] " + message
		with self.bbddconn:
			cur = self.bbddconn.cursor()
			cur.execute("CREATE TABLE IF NOT EXISTS '" + channel + "' (date TEXT, time TEXT, nick TEXT, message TEXT)")
			cur.execute("INSERT INTO '" + channel + "' VALUES('" + date + "','" + time +"','" + nick + "','" + message + "')")
			self.bbddconn.commit()

# End of file
