#!/usr/bin/env python

import os

class Sysinfo:
	
	uname = None

	def __init__ (self):

		self.uname = " ".join(os.uname())
					
	def getresponse (self, text):

		t = text.split()
		cmd = t[0]
		arg = t[1:]

		if (cmd == "uname"): return self.uname
		else: return "'" + cmd + "' is not available"
		

# End of file
