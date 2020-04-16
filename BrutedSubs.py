import os
from ReconPY import dom



fnames = ["Domains-online.txt", "dnsgen.txt", "Level1-Domains.txt", "dnsgen-2.txt", "Level2-Domains.txt", "dnsgen-3.txt", 
			"Level3-Domains.txt", "dnsgen-4.txt", "Level4-Domains.txt"]

flag = 1

def rec(a):
	# print(a,b)
	global dom, flag
	while flag < 5:
		print(str(flag)+"\n")
		os.system("dnsgen " + fnames[a] + " -w ../altdns_words.txt >> " + fnames[a+1])

		
		# Resolving again for AltDns Domains 
		# print('MassDns')
		os.system("shuffledns -silent -d " + dom + " -list " + fnames[a+1] + " -r /home/r00t/massdns/lists/resolvers.txt -o " + fnames[a+2])
		# print('Done Once')
		# Save Only Domains Names
		
		with open(fnames[a+2]) as f:
			text = f.read().splitlines()
		with open(fnames[a+2], 'w') as fp:	
			for line in text:
				# print(line)
				fp.write(line.split()[0].rstrip('.')+"\n")
				# exit(0)
		
		flag += 1
		rec(a+2)
		os.system('cat Domains-online.txt Level1-Domains.txt Level2-Domains.txt Level3-Domains.txt Level4-Domains.txt | sort -u >> Subdomains.txt')
		os.system('cat Domains.txt | httprobe -c 50 >> Web-Domains.txt')

rec(0)


# "shuffledns -d " + args.domain + " -list " fnames[a+1]" + " -r /home/r00t/massdns/lists/resolvers.txt -o " + fnames[a+2]
# "dnsgen " + fnames[a] + " -w ../altdns_words.txt >> " + fnames[a+1]"