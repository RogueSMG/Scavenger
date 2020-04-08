import os
import fileinput
import re

fnames = ["Domains-online.txt", "altdns.txt", "Level1-Domains.txt", "altdns-2.txt", "Level2-Domains.txt"]

flag = 1	
n = 3 
def rec(a):
	# print(a,b)
	global flag
	while flag < 3:
		os.system('altdns -i ' + fnames[a] + ' -w ../altdns_words.txt -o ' + fnames[a+1])

		
		# Resolving again for AltDns Domains 
		# print('MassDns')
		os.system('massdns -r ~/massdns/lists/resolvers.txt -q -t A -o S -w "' + fnames[a+2] + '" "' + fnames[a+1] + '"')
		# print('Done Once')
		# Save Only Domains Names
		with open('Level1-Domains.txt', 'r+') as f:
			text = f.readlines()
			for line in text:
				# print(line)
				print(line.split()[0].rstrip('.')+"\n")
				# f.seek(0)
				# f.truncate()
			exit(0)
			
		flag += 1
		print(flag)
		rec(a+2)
		


rec(0)
