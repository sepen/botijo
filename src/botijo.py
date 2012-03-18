#!/usr/bin/env python
#
# botijo: IRC Bot written in python with modules suppot

import os
import sys
import socket
import string
import ConfigParser

class Botijo:
	
	debug, verbose = None, None
	home, mods = None, None
	host, port, channel = None, None, None
	nick, ident, realname = None, None, None
		
	def __init__ (self, verbose, config, host, port, channel, nick):

		self.debug = 0
		self.verbose = 0
		self.home = "~/.botijo"
		self.mods = "log", "sysinfo", "notes"
		self.admins = ""
		self.host, self.port, self.channel = host, port, channel
		self.nick, self.ident, self.realname = nick, nick, nick
		
		if os.path.exists(config):
			conf = ConfigParser.ConfigParser()
			conf.readfp(file(config))
			self.verbose = conf.get("config", "verbose")
			self.home = conf.get("config", "home")
			self.mods = conf.get("config", "mods")
			self.admins = conf.get("config", "admins")
			self.host = conf.get("config", "host")
			self.port = conf.get("config", "port")
			self.channel = conf.get("config", "channel")
			self.nick = conf.get("config", "nick")
		
		self.home = self.home.strip('"')
		self.home = os.path.expanduser(self.home)
		if not os.access(self.home, os.F_OK | os.W_OK):
			os.mkdir(self.home)  # create prefs directory
		self.host = self.host.strip('"')
		self.port = int(self.port)
		self.channel = self.channel.strip('"')
		self.nick = self.nick.strip('"')
	

	def main(self):
		
		if (self.verbose == 1):
			print ">>> Connecting to server " + self.host + " on port " + str(self.port)
			print ">>> Using nickname " + self.nick + " on channel " + self.channel
		
		readbuffer = ""
		s = socket.socket( )
		s.connect((self.host, self.port))
		s.send("NICK %s\r\n" % self.nick)
		s.send("USER %s %s * :%s\r\n" % (self.ident, self.host, self.realname))
		s.send("JOIN %s\r\n" % self.channel)
	
		if "log" in self.mods:
			import log
			log = log.Log(self.home + "/log/" + self.channel)
			if not os.access(self.home + "/log", os.F_OK | os.W_OK):
				os.mkdir(self.home + "/log")  # create prefs directory
			if not os.access(self.home + "/log/" + self.channel, os.F_OK | os.W_OK):
				os.mkdir(self.home + "/log/" + self.channel)  # create prefs directory

		if "notes" in self.mods:
			import notes
			notes = notes.Notes(self.home + "/notes/" + self.channel)
			if not os.access(self.home + "/notes", os.F_OK | os.W_OK):
				os.mkdir(self.home + "/notes")  # create prefs directory
			if not os.access(self.home + "/notes/" + self.channel, os.F_OK | os.W_OK):
				os.mkdir(self.home + "/notes/" + self.channel)  # create prefs directory

		while 1:
			readbuffer = readbuffer + s.recv(1024)
			temp = string.split(readbuffer, "\n")
			readbuffer = temp.pop( )
			
			for line in temp:
				
				if (self.debug == 1): print line
				
				line = string.rstrip(line)
				line = string.split(line)
				
				# server ping pong
				if (line[0] == "PING"):
					s.send("PONG %s\r\n" % line[1])

				# server codes
				elif (line[1] == "433"): # :server.domain 433 * botijo :Nickname is already in use.
					s.close()
					print "Nickname is already in use"
					sys.exit()

				# private messages
				elif (line[1] == "PRIVMSG"):
					user = line[0].split("!")
					user = user[0].lstrip(":")
					text = " ".join(line[3:]).lstrip(":")
					sendto = ""
					petition = ""
					response = ""
					mod = ""
					
					tmp = text.split()
					# user to bot
					if (line[2] == self.nick):
						sendto = user
						mod = tmp[0]
						petition = " ".join(tmp[1:])
					# user to channel
					elif (line[2] == self.channel) and (text[0] == "!"):
						sendto = self.channel
						mod = tmp[0].lstrip("!")
						petition = " ".join(tmp[1:])
					
					if mod in self.mods:
						if (mod == "log"):
							response = "module '" + mod + "' not available for users"
						elif len(petition) > 0:
							if (mod == "sysinfo"):
								import sysinfo
								mod_sysinfo = sysinfo.Sysinfo()
								response = mod_sysinfo.getresponse(petition)
							elif (mod == "notes"):
								if user in self.admins:
									response = notes.doCommand(petition)
								else:
									response = "you are not authorized to use this module"
							else:
								response = "module '" + mod + "' not implemented"
						else:
							response = "module '" + mod + "' requires more arguments to be passed"
					else:
						response = "unknown module '" + mod + "'"
					
					if (sendto is not "") and (response is not ""):
						if (sendto != user):
							response = user + ": " + response
						s.send("PRIVMSG %s :%s\r\n" % (sendto, response))
						if (self.verbose == 1):
							print ">>> PRIVMSG " + sendto + " :" + response
					
					if "log" in self.mods:
						log.write(user, text)



def usage() :

	print "botijo 0.1 by Jose V Beneyto, <sepen@crux.nu>"
	print "Usage: botijo <options>"
	print "Where options are:"
	print " -h, --help         Show this help information"
	print " -v, --verbose      Print verbose messages"
	print " --conf=CONFIG      Use a config file"
	print " --host=SERVER      IRC server to connect"
	print " --port=PORT        Port number of the server to connect"
	print " --channel=CHANNEL  Name for the server channel"
	print " --nick=NICK        Nick name you want to use"
	sys.exit()


if __name__ == "__main__":
	
	verbose = 0
	host, port = "irc.dyndns.org", 6667
	channel, nick = "#botijo", "botijo"
	config = "~/.botijo.conf"

	for opt in sys.argv[1:]:

		if opt in ("-h", "--help"):
			usage()
		elif opt in ("-v", "--verbose"):
			verbose = 1
		elif "=" in opt:
			(key, val) = (opt.split("="))
			if (key == "--conf"):
				config = val
			elif (key == "--host"):
				host = val
			elif (key == "--port"):
				port = int(val)
			elif (key == "--channel"):
				channel = val
			elif (key == "--nick"):
				nick = val
			else:
				usage()
		else:
			usage()
		
	bot = Botijo(verbose, config, host, port, channel, nick)
	bot.main()

# End of file
