#!/usr/bin/env python

class Notes:

	dir = "."
	
	def __init__ (self, dir):
		self.dir = dir
		
	def doCommand (self, text):
		t = text.split()
		cmd = t[0]
		if (cmd == "help"):
			return "available commands: help, add"
		elif (cmd == "add"):
			if (len(t) > 2):
				filename = t[1]
				note = t[2:]
				file = self.dir + "/" + filename
				f = open(file, "a")
				f.write(" ".join(note) + "\n")
				f.close()
				return "added to " + filename
			else:
				return "you must give filename and text args to this command"
		#elif (cmd == "ls"):
		#	TODO: print a list of notes
		else:
			return "'" + cmd + "' is not available, use 'notes help' to get a list"

# End of file
