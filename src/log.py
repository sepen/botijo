#!/usr/bin/env python

import os, datetime

class Log:

	dir = "."
	
	def __init__ (self, basedir):
		self.basedir = basedir
		
	def write (self, user, text, channel):
		dt = datetime.datetime.now()
		(date, time) = str(dt).split()
		(time, prec) = time.split(".")
		logdir = self.basedir + "/" + channel
		if not os.access(logdir, os.F_OK | os.W_OK):
			os.mkdir(logdir)
		logfile = logdir + "/" + date
		f = open(logfile, "a")
		f.write("%s [%s] %s\n" % (time, user, text))
		f.close()

# End of file
