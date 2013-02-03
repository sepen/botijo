#!/usr/bin/env python -tt
#
# botijo: IRC Bot written in python with modules suppot

import os
import sys
import socket
import string
import ConfigParser

class Botijo:
	
	debug, verbose = None, None
	config = None
	home, mods = None, None
	host, port, channels = None, None, None
	nick, ident, realname = None, None, None
		
	def __init__ (self, verbose, config, host, port, channels, nick):

		self.debug = 0  # 0 disabled, 1/2/3 enabled
		self.verbose = verbose
		self.config = config.strip('"')
		self.config = os.path.expanduser(self.config)
		self.home = "~/.botijo"
		self.mods = "log, sysinfo, notes"
		self.admins = ""
		self.host, self.port, self.channels = host, port, channels
		self.nick, self.ident, self.realname = nick, nick, nick
		
		if os.path.exists(self.config):
			conf = ConfigParser.ConfigParser()
			conf.readfp(file(self.config))
			self.verbose = conf.get("config", "verbose")
			self.home = conf.get("config", "home")
			self.mods = conf.get("config", "mods")
			self.admins = conf.get("config", "admins")
			self.host = conf.get("config", "host")
			self.port = conf.get("config", "port")
			self.channels = conf.get("config", "channels")
			self.nick = conf.get("config", "nick")
			if (self.debug >= 1):
				print "[DEBUG] config file loaded: " + self.config

		self.home = self.home.strip('"')
		self.home = os.path.expanduser(self.home)
		if not os.access(self.home, os.F_OK | os.W_OK):
			os.mkdir(self.home)  # create prefs directory
		self.host = self.host.strip('"')
		self.port = int(self.port)
		self.channels = self.channels.strip('"')
		self.channels = self.channels.split(",")
		self.nick = self.nick.strip('"')
		self.registered = False
		self.inChannels = {}
		for channel in self.channels:
			if (self.debug >= 1):
				print "[DEBUG] channel: " + channel
			self.inChannels[channel] = False

	def main(self):
		
		if (self.verbose == 1):
			print "==> Connecting to server " + self.host + " on port " + str(self.port)

		# connect to a server
		self.readbuffer = ""
		self.socket = socket.socket( )
		self.socket.connect((self.host, self.port))

		# register user
		if (self.verbose == 1):
			print "==> Registering nick/user information"
		self.socket.send("NICK %s\r\n" % self.nick)
		self.socket.send("USER %s %s * :%s\r\n" % (self.ident, self.host, self.realname))

		# some modules require an extra initialization
		if "log" in self.mods:
			import log
			log = log.Log(self.config)

		if "notes" in self.mods:
			import notes
			notes = notes.Notes(self.home + "/notes")
			if not os.access(self.home + "/notes", os.F_OK | os.W_OK):
				os.mkdir(self.home + "/notes")  # create prefs directory

		# main loop
		while 1:
			# join to channels
			if self.registered:
				for channel in self.channels:
					if not self.inChannels[channel]:
						self.socket.send("JOIN %s\r\n" % channel)

			# read buffer from server
			self.readbuffer = self.readbuffer + self.socket.recv(1024)
			data = self.readbuffer.split("\n")
			self.readbuffer = data.pop( )

			# process every line
			for line in data:
				
				if (self.debug >= 2): print "[DEBUG] " + line

				# get sanitized string
				line = string.rstrip(line)
				line = string.split(line)
				
				# server ping pong
				if (line[0] == "PING"):
					self.socket.send("PONG %s\r\n" % line[1])

				# 433 Nickname is already in use
				elif (line[1] == "433"): # :server.domain 433 * botijo :Nickname is already in use.
					self.socket.close()
					if (self.verbose == 1):
						print "==> Nickname is already in use."
					sys.exit()

				# 376 End of MOTD
				if line[1] == '376':
					if (self.verbose == 1):
						print "==> Successfully registered with nickname: %s." % self.nick
					self.registered = True

				# 366 End of /NAMES list
				if line[1] == '366':
					if (self.verbose == 1):
						print "==> Successfully joined channel: %s." % line[3]
					self.inChannels[line[3]] = True

				# private messages
				elif (line[1] == "PRIVMSG"):
					user = line[0].lstrip(":")
					nick = line[0].split("!")[0].lstrip(":")
					msg = " ".join(line[3:]).lstrip(":")
					tmp = msg.split(" ")
					sendto = ""
					petition = ""
					response = ""
					mod = ""

					# PRIVMSG from user to bot
					if (line[2] == self.nick):
						sendto = nick
						mod = tmp[0]
						petition = " ".join(tmp[1:])

					# PRIVMSG from user to channel
					elif (line[2] in self.inChannels):
						sendto = line[2]
						if (msg[0] == "!"):
							mod = tmp[0].lstrip("!")
							petition = " ".join(tmp[1:])

					# search and execute the module petition
					if mod in self.mods:
						if (mod == 'log'):
							response = "module '" + mod + "' not available for users"
						elif (len(petition) > 0):
							tmp = petition.split(" ")
							cmd = tmp[0]
							args = " ".join(tmp[1:])
							if (mod == "sysinfo"):
								import sysinfo
								mod_sysinfo = sysinfo.Sysinfo()
								response = mod_sysinfo.doCommand(cmd, args)
							elif (mod == "notes"):
								if user in self.admins:
									response = notes.doCommand(cmd, args)
								else:
									response = "you are not authorized to use this module"
							else:
								response = "available modules are: " + self.mods
						elif (mod is not  ""):
							response = "module '" + mod + "' requires more arguments to be passed"
					else:
						response = "available modules are: " + self.mods

					#  return the response with a prefix depending on PRIVMSG origin
					if (sendto is not "") and (response is not ""):
						if (sendto != nick):
							response = nick + ": " + response
						self.socket.send("PRIVMSG %s :%s\r\n" % (sendto, response))
						if (self.verbose == 1):
							print "==> PRIVMSG " + sendto + " :" + response

					# save last line if log module is enabled
					if "log" in self.mods:
						if (self.debug >= 1):
							print "[DEBUG] log.write(" + nick + ", " + msg + ", " + sendto + ")"
						log.write(nick, msg, sendto)

				# debug not managed command codes from server
				else:
					if (self.debug >= 3):
						print "[DEBUG] NOT MATCHED LINE"

def version():
	print "botijo 0.2 by Jose V Beneyto, <sepen@crux.nu>"
	sys.exit()

def usage():
	print "Usage: botijo <options>"
	print "Where options are:"
	print " -h, --help           Show this help information"
	print " -V, --version        Show version information"
	print " -v, --verbose        Print verbose messages"
	print " --conf=CONFIG        Use alternate config file"
	print " --host=SERVER        IRC server to connect"
	print " --port=PORT          Port number of the server to connect"
	print " --channels=CHANNELS  List of channels to join (separated by commas)"
	print " --nick=NICK          Nick name you want to use"
	sys.exit()


if __name__ == "__main__":
	
	verbose = 0
	host, port = 'irc.freenode.net', 6667
	channels = '#botijotest1', '#botijotest2'
	nick = 'botijo'
	config = '~/.botijo.conf'

	for opt in sys.argv[1:]:

		if opt in ("-h", "--help"):
			usage()
		elif opt in ("-V", "--version"):
			version()
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
			elif (key == "--channels"):
				channels = val.split(",")
			elif (key == "--nick"):
				nick = val
			else:
				usage()
		else:
			usage()

	bot = Botijo(verbose, config, host, port, channels, nick)
	bot.main()

# End of file
