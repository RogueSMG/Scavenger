import os
import sys
import re
import argparse
import subprocess
import configparser
from time import sleep
from threading import Thread
from requests import post


config = configparser.ConfigParser()
config.read('config.ini')
slack = config['default']['SLACKBB']


parser = argparse.ArgumentParser(description='Recon Testing')
parser.add_argument("--domain", "-D",  dest='domain', help='Domain Name for the Recon!', required=True)
args = parser.parse_args()
dom = args.domain


os.mkdir(dom)
os.chdir(dom)


#								Part 1: GATHERING SUBDOMAINS 


# Passive Amass Scanning
def amass_scan():
	# os.system('amass enum --passive -d ' + args.domain + ' -o amass.txt')
	subprocess.check_output(["amass", "enum", "--passive", "-d", dom, "-o", "amass.txt"], stderr=subprocess.DEVNULL)
	send = "Amass found " + str(sum(1 for line in open('amass.txt'))) + " Domains"
	print(send)
	post(slack, data="{'text': '"  + send + "'}", headers={'Content-Type': 'application/json'})
	# sleep(1)

# Findomain Scanning
def findomain_scan():
	# os.system('findomain --target ' + dom + ' --threads 50 -o')
	subprocess.check_output(["findomain", "--target", dom, "--threads", "50", "-u", "findomain.txt"], stderr=subprocess.STDOUT)
	send = "Findomain found " + str(sum(1 for line in open('findomain.txt'))) + " Domains"
	print(send)
	post(slack, data="{'text': '"  + send + "'}", headers={'Content-Type': 'application/json'})
	# sleep(1)

# Assetfinder Scanning
def assetfinder_scan():
	# os.system('assetfinder --subs-only ' + dom + ' > assetfinder.txt')
	with open("assetfinder.txt", "w") as fp:
		subprocess.run(["assetfinder", "--subs-only", dom], text=True, stdout=fp)
	send = "Assetfinder found " + str(sum(1 for line in open('assetfinder.txt'))) + " Domains"
	print(send)
	post(slack, data="{'text': '"  + send + "'}", headers={'Content-Type': 'application/json'})
	# sleep(1)

# Subfinder Scanning
def subfinder_scan():
	# os.system('subfinder -silent -d ' + dom + ' -o subfinder.txt')
	subprocess.check_output(["subfinder", "-silent", "-t", "100", "-d", dom, "-o", "subfinder.txt"], stderr=subprocess.STDOUT)
	send = "Subfinder found " + str(sum(1 for line in open('subfinder.txt'))) + " Domains"
	print(send)
	post(slack, data="{'text': '"  + send + "'}", headers={'Content-Type': 'application/json'})
	# sleep(1)

#Commomspeak2 Brute Forcing
def cspeak_brute():
	# print('\n\n[*] Bruting Subs using commonspeak2 subdomain wordlist...')
	wordlist = open('/root/Wordlists/subdomains.txt').read().split('\n')

	for word in wordlist:
	    if not word.strip(): 
	        continue
	    f = open("CommonSpeak_Bruted.txt", "a+" )
	    f.write('{}.{}\n'.format(word.strip(), args.domain))
	    # sleep(0.3)
	    # print('{}.{}\n'.format(word.strip(), scope))
	f.close()
	# print('[+] File Closed!')
	send = 'CommomSpeak Generated ' + str(sum(1 for line in open('CommonSpeak_Bruted.txt'))) + ' Domains'
	print(send)
	post(slack, data="{'text': '"  + send + "'}", headers={'Content-Type': 'application/json'})
	# sleep(1)



def Combine():
	p1 = subprocess.run(['cat', 'CommonSpeak_Bruted.txt', 'amass.txt', 'findomain.txt', 'assetfinder.txt', 'subfinder.txt'], text=True, capture_output=True)
	with open("Potential-Domains.txt", "w") as fp:
	 	subprocess.run(['sort', '-u'], text=True, input=p1.stdout, stdout=fp)

	subprocess.run(['rm', 'CommonSpeak_Bruted.txt', 'amass.txt', 'findomain.txt', 'assetfinder.txt', 'subfinder.txt'])
	send = "Total found " + str(sum(1 for line in open('Potential-Domains.txt'))) + " Domains"
	print(send)
	post(slack, data="{'text': '"  + send + "'}", headers={'Content-Type': 'application/json'})
	# sleep(1)


def Resolve():
	subprocess.check_output(["shuffledns", "-silent", "-d", dom, "-list", "Potential-Domains.txt", "-r", "/root/tools/findomain/massdns/lists/resolvers.txt", "-t", "15000", "-o", "Domains-Online.txt"], stderr=subprocess.STDOUT)
	subprocess.run(['rm', 'Potential-Domains.txt'])
	send = "Total " + str(sum(1 for line in open('Domains-Online.txt'))) + " Live Passive Domains"
	print(send)
	post(slack, data="{'text': '"  + send + "'}", headers={'Content-Type': 'application/json'})
	# sleep(1)


def Brute():
	import BrutedSubs
	BrutedSubs.main(dom,slack)



def PortScans():
	import PortsAndServices
	PortsAndServices.main(slack)



def DirBrute():
	import Dbrute
	Dbrute.main(slack)



def main():



	letsgo = "\n\n[+] Script Execution Started...\n\n"
	print(letsgo)
	post(slack, data="{'text': '"  + letsgo + "'}", headers={'Content-Type': 'application/json'})
	t1 = Thread(target=amass_scan)
	# sleep(0.2)
	t2 = Thread(target=findomain_scan)
	# sleep(0.4)
	t3 = Thread(target=assetfinder_scan)
	# sleep(0.6)
	t4 = Thread(target=subfinder_scan)
	# sleep(0.8)
	t5 = Thread(target=cspeak_brute)
	# sleep(0.9)
	# t6 = Thread(target=shit_combined).start()

	t1.start()
	# sleep(0.2)
	t2.start()
	# sleep(0.2)
	t3.start()
	# sleep(0.2)
	t4.start()
	#sleep(0.2)
	t5.start()


	t1.join()
	t2.join()
	t3.join()
	t4.join()
	t5.join()



	# Combining the Subdomain Lists
	send = "\nCombining files from all Tools..."
	print(send)
	post(slack, data="{'text': '"  + send + "'}", headers={'Content-Type': 'application/json'})
	Combine()



	# Resolving with Shuffledns
	shufl = "\nResolving Passive Domains...."
	print(shufl)
	post(slack, data="{'text': '"  + shufl + "'}", headers={'Content-Type': 'application/json'})
	Resolve()



	# Calling the BruteForcer
	bruf = "\nBruteForcing and Resolving to find more Domains..."
	print(bruf)
	post(slack, data="{'text': '"  + bruf + "'}", headers={'Content-Type': 'application/json'})
	Brute()



	# Calling the Beast Ffuf
	bfuff = "\nDirectory BruteForcing..."
	print(bfuff)
	post(slack, data="{'text': '"  + bfuff + "'}", headers={'Content-Type': 'application/json'})
	DirBrute()



	# Calling the PortScanner
	pscan = "\nRunning PortScans..."
	print(pscan)
	post(slack, data="{'text': '"  + pscan + "'}", headers={'Content-Type': 'application/json'})
	PortScans()




	fin = "\n\n[$$$] ALL THE BORING STUFF DONE, GO HACK NOW...! [$$$]"
	print(fin)
	post(slack, data="{'text': '"  + fin + "'}", headers={'Content-Type': 'application/json'})





if __name__ == '__main__':
	main()

