#!/usr/bin/env python

class Notes:

	dir = "."
	
	def __init__ (self, dir):

		self.dir = dir

	def msgUsage (self):

		return "available commands for notes module are: help, add"
		
	def doCommand (self, cmd, args):

		if (cmd == "help"):
			self.msgUsage()

		elif (cmd == "add"):
			if (len(args) > 1):
				filename = args[0]
				note = args[1:]
				file = self.dir + "/" + filename
				f = open(file, "a")
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
