#!/usr/bin/env python

import datetime

class Log:

	dir = "."
	
	def __init__ (self, dir):
		self.dir = dir
		
	def write (self, user, text):
		dt = datetime.datetime.now()
		(date, time) = str(dt).split()
		(time, prec) = time.split(".")
		file = self.dir + "/" + date
		f = open(file, "a")
		f.write("%s [%s] %s\n" % (time, user, text))
		f.close()

# End of file
