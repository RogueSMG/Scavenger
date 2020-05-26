import os
import subprocess
import glob
from requests import post



def rec(a,dom):
	# print(a,b)
	global flag
	while flag < 5:
		print("Iteration Number: " + str(flag))
		
		# Generating Permutations with Dnsgen
		with open(fnames[a+1], 'w') as f:
			subprocess.run(['timeout', '30', 'dnsgen', fnames[a], '-w', '/root/Wordlists/words.txt'], text=True, stdout=f)
		
		# Resolving again for AltDns Domains 
		subprocess.check_output(["shuffledns", "-d", dom, "-list", fnames[a+1], "-r", "/root/tools/findomain/massdns/lists/resolvers.txt", "-t", "15000", "-o", fnames[a+2]], stderr=subprocess.STDOUT)

		flag += 1
		rec(a+2, dom)
	
	
def Catting(slack):

	p1 = subprocess.run(['cat', 'Domains-Online.txt', 'Level1-Domains.txt', 'Level2-Domains.txt', 'Level3-Domains.txt', 'Level4-Domains.txt'], text=True, capture_output=True)
	with open('Subdomains.txt', 'w') as fp:
		subprocess.run(['sort', '-u'], text=True, input=p1.stdout, stdout=fp)

	os.remove('Domains-Online.txt')
	
	for path in glob.glob('dnsgen*'):
		os.remove(path)

	for path in glob.glob('Level*'):
		os.remove(path) 


	send = "\n\n[***] TOTAL " + str(sum(1 for line in open('Subdomains.txt'))) + " LIVE DOMAINS...! [***]"
	print(send)
	post(slack, data="{'text': '"  + send + "'}", headers={'Content-Type': 'application/json'})


def Probing(slack):
	
	p1 = subprocess.run(['cat', 'Subdomains.txt'], text=True, capture_output=True)
	with open('Web-Domains.txt', 'w') as fps:
		subprocess.run(['httprobe', '-c', '50'], text=True, input=p1.stdout, stdout=fps)

	send = "[+++] Total " + str(sum(1 for line in open('Web-Domains.txt'))) + " WEB Domains...! [+++]"
	print(send)
	post(slack, data="{'text': '"  + send + "'}", headers={'Content-Type': 'application/json'})





def main(domssss,slax):
	
	global flag, fnames
	fnames = ["Domains-Online.txt", "dnsgen.txt", "Level1-Domains.txt", "dnsgen-2.txt", "Level2-Domains.txt", "dnsgen-3.txt", 
			"Level3-Domains.txt", "dnsgen-4.txt", "Level4-Domains.txt"]
	flag = 1
	
	# Calling the Functions
	rec(0,domssss)
	Catting(slax)
	Probing(slax)





if __name__ == '__main__':
	main(sites,slk)