#!/usr/bin/env python

import os
#import decimal

class Sysinfo:
	
	uname = None

	def __init__ (self):

		self.uname = " ".join(os.uname())
					
	def getresponse (self, text):

		t = text.split()
		cmd = t[0]
		arg = t[1:]

		if (cmd == "uname"):
			return self.uname

		elif (cmd == "free"):
			# mem
			pipe_mem = os.popen('{ free -tom | grep ^Mem; } 2>&1', 'r')
			line_mem = pipe_mem.read()
			pipe_mem.close()
			mem = line_mem.split()
			mem_percent_tmp = float(mem[3]) / float(mem[1])
			mem_percent = str(float(mem_percent_tmp)*100)
			mem_percent = mem_percent[:2]

			# swap
			pipe_swap = os.popen('{ free -tom | grep ^Swap; } 2>&1', 'r')
			line_swap = pipe_swap.read()
			pipe_swap.close()
			swap = line_swap.split()
			if (swap[1] == swap[3]):
				swap_percent = "100"
			else:
				swap_percent_tmp = float(swap[3]) / float(swap[1])
				swap_percent = str(float(swap_percent_tmp)*100)
				swap_percent = swap_percent[:2]

			# total
			pipe_total = os.popen('{ free -tom | grep ^Total; } 2>&1', 'r')
			line_total = pipe_total.read()
			pipe_total.close()
			total = line_total.split()
			total_percent_tmp = float(total[3]) / float(total[1])
			total_percent = str(float(total_percent_tmp)*100)
			total_percent = total_percent[:2]

			# output
			output = "Mem " + mem[3] + "/" + mem[1] + "M (" + mem_percent + "%), "
			output = output + "Swap " + swap[3] + "/" + swap[1] + "M (" + swap_percent + "%), "
			output = output + "Total " + total[3] + "/" + total[1] + "M (" + total_percent + "%)"

			return output

		else: return "'" + cmd + "' is not available"
		

# End of file
