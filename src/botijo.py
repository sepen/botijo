#!/usr/bin/env python -tt
#
# botijo: IRC Bot written in python with modules suppot

import os
import sys
import socket
import string
import ConfigParser

class Botijo:

	config = None
	debug, verbose = None, None
	home, mods, admins = None, None, None
	host, port, channels = None, None, None
	nick, ident, realname = None, None, None

	def __init__ (self, config, debug, verbose, home, mods, admins, host, port, channels, nick):

		self.config = config
		self.debug, self.verbose = debug, verbose
		self.home, self.mods, self.admins = home, mods, admins
		self.host, self.port, self.channels = host, port, channels
		self.nick, self.ident, self.realname = nick, nick, nick

		# sanitize vars
		self.home = self.home.strip('"')
		self.home = os.path.expanduser(self.home)
		if not os.access(self.home, os.F_OK | os.W_OK):
			os.mkdir(self.home)  # create prefs directory
		self.mods = self.mods.strip('"')
		self.mods = self.mods.split(" ")
		self.admins = self.admins.strip('"')
		self.admins = self.admins.split(" ")
		self.host = self.host.strip('"')
		self.port = int(self.port)
		self.channels = self.channels.strip('"')
		self.channels = self.channels.split(" ")
		self.inChannels = {}
		for channel in self.channels:
			if (self.debug >= 1):
				print "[DEBUG] channel: " + channel
			self.inChannels[channel] = False
		self.nick = self.nick.strip('"')
		self.registered = False

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

					# print some debug messages
					if (self.debug >= 2):
						print "[DEBUG] mods: " + " ".join(self.mods)
						print "[DEBUG] sendto: " + sendto
						print "[DEBUG] mod: " + mod
						print "[DEBUG] petition: " + petition

					# search and execute the module petition
					if (len(mod) > 0):
						if mod in self.mods:
							if (len(petition) > 0):
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
								response = "module '" + mod + "' requires more arguments to be passed"

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
	print " --conf=CONFIG        Use alternate config file (default: ~/.botijo.conf)"
	print " --host=SERVER        IRC server to connect"
	print " --port=PORT          Port number of the server to connect"
	print " --channels=CHANNELS  List of channels to join (separated by spaces)"
	print " --nick=NICK          Nick name you want to use"
	print "Example:"
	print "  botijo --host=localhost --channels='#test1 #test2' --nick=foo"
	sys.exit()


if __name__ == "__main__":

	debug = 0 # disabled: 0, enabled: 1, 2 or 3

	# check for 'show functions'
	for opt in sys.argv[1:]:
		if opt in ("-h", "--help"):
			usage()
		elif opt in ("-V", "--version"):
			version()

	# default values in config variables
	verbose = 0
	conf = '~/.botijo.conf'
	home = '~/.botijo'
	mods = ''
	admins = ''
	host = 'localhost'
	port = 6667
	channels = '#botijo'
	nick = 'botijo'

	# check for alternate config file
	for opt in sys.argv[1:]:
		if "=" in opt:
			(key, val) = (opt.split("="))
			if (key == "--conf"):
				conf = val
				# remove opt from sys.argv array
				sys.argv.remove(opt)

	# overlay config variables with values from config file
	conf = conf.strip('"')
	conf = os.path.expanduser(conf)
	config = ConfigParser.ConfigParser()
	if os.path.exists(conf):
		# read config file
		config.readfp(file(conf))
		for cname,cvalue in config.items("botijo"):
			if (cname == "verbose"):
				verbose = cvalue
			elif (cname == "home"):
				home = cvalue
			elif (cname == "mods"):
				mods = cvalue
			elif (cname == "admins"):
				admins = cvalue
			elif (cname == "host"):
				host = cvalue
			elif (cname == "port"):
				port = cvalue
			elif (cname == "channels"):
				channels = cvalue
			elif (cname == "nick"):
				nick = cvalue
		if (debug >= 1):
			print "[DEBUG] config file loaded: " + conf

	# overaly config variables with values from command line args
	for opt in sys.argv[1:]:
		if opt in ("-v", "--verbose"):
			verbose = 1
		elif "=" in opt:
			(key, val) = (opt.split("="))
			if (key == "--host"):
				host = val
			elif (key == "--port"):
				port = val
			elif (key == "--channels"):
				channels = val
			elif (key == "--nick"):
				nick = val
			else:
				usage()
		else:
			usage()

	# create main object
	bot = Botijo(config, debug, verbose, home, mods, admins, host, port, channels, nick)
	bot.main()

# End of file
