#!/usr/bin/env python

class Notes:

	dir = "."
	
	def __init__ (self, basedir):

		self.basedir = basedir

	def doCommand (self, cmd, args):

		if (cmd == "help"):
			return "available commands for notes module are: help add"

		elif (cmd == "add"):
			if (len(args) > 1):
				filename = args[0]
				note = args[1:]
				notefile = self.basedir + "/" + filename
				f = open(notefile, "a")
				f.write(" ".join(note) + "\n")
				f.close()
				return "added to " + filename
			else:
				self.msgUsage()

		#elif (cmd == "ls"):
		#	TODO: print a list of notes

		else:
			self.msgUsage()

# End of file
