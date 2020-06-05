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
 


# Passive Amass Scanning
def amass_scan():
	
	subprocess.check_output(["amass", "enum", "--passive", "-d", dom, "-o", "amass.txt"], stderr=subprocess.DEVNULL)
	send = "Amass found " + str(sum(1 for line in open('amass.txt'))) + " Domains"
	print(send)
	post(slack, data="{'text': '"  + send + "'}", headers={'Content-Type': 'application/json'})
	

# Findomain Scanning
def findomain_scan():
	
	subprocess.check_output(["findomain", "--target", dom, "--threads", "50", "-u", "findomain.txt"], stderr=subprocess.STDOUT)
	send = "Findomain found " + str(sum(1 for line in open('findomain.txt'))) + " Domains"
	print(send)
	post(slack, data="{'text': '"  + send + "'}", headers={'Content-Type': 'application/json'})
	

# Assetfinder Scanning
def assetfinder_scan():
	
	with open("assetfinder.txt", "w") as fp:
		subprocess.run(["assetfinder", "--subs-only", dom], text=True, stdout=fp)
	send = "Assetfinder found " + str(sum(1 for line in open('assetfinder.txt'))) + " Domains"
	print(send)
	post(slack, data="{'text': '"  + send + "'}", headers={'Content-Type': 'application/json'})
	


def subfinder_scan():
	
	subprocess.check_output(["subfinder", "-silent", "-t", "100", "-d", dom, "-o", "subfinder.txt"], stderr=subprocess.STDOUT)
	send = "Subfinder found " + str(sum(1 for line in open('subfinder.txt'))) + " Domains"
	print(send)
	post(slack, data="{'text': '"  + send + "'}", headers={'Content-Type': 'application/json'})
	

#Commomspeak2 Brute Forcing
def cspeak_brute():
	
	wordlist = open('/root/Wordlists/subdomains.txt').read().split('\n')

	for word in wordlist:
	    if not word.strip(): 
	        continue
	    f = open("CommonSpeak_Bruted.txt", "a+" )
	    f.write('{}.{}\n'.format(word.strip(), args.domain))
	    
	    
	f.close()
	
	send = 'CommomSpeak Generated ' + str(sum(1 for line in open('CommonSpeak_Bruted.txt'))) + ' Domains'
	print(send)
	post(slack, data="{'text': '"  + send + "'}", headers={'Content-Type': 'application/json'})
	



def Combine():
	p1 = subprocess.run(['cat', 'CommonSpeak_Bruted.txt', 'amass.txt', 'findomain.txt', 'assetfinder.txt', 'subfinder.txt'], text=True, capture_output=True)
	with open("Potential-Domains.txt", "w") as fp:
	 	subprocess.run(['sort', '-u'], text=True, input=p1.stdout, stdout=fp)

	subprocess.run(['rm', 'CommonSpeak_Bruted.txt', 'amass.txt', 'findomain.txt', 'assetfinder.txt', 'subfinder.txt'])
	send = "Total found " + str(sum(1 for line in open('Potential-Domains.txt'))) + " Domains"
	print(send)
	post(slack, data="{'text': '"  + send + "'}", headers={'Content-Type': 'application/json'})
	


def Resolve():
	subprocess.check_output(["shuffledns", "-silent", "-d", dom, "-list", "Potential-Domains.txt", "-r", "/root/tools/findomain/massdns/lists/resolvers.txt", "-t", "15000", "-o", "Domains-Online.txt"], stderr=subprocess.STDOUT)
	subprocess.run(['rm', 'Potential-Domains.txt'])
	send = "Total " + str(sum(1 for line in open('Domains-Online.txt'))) + " Live Passive Domains"
	print(send)
	post(slack, data="{'text': '"  + send + "'}", headers={'Content-Type': 'application/json'})
	


def Brute():
	import BrutedSubs
	BrutedSubs.main(dom,slack)



def PortScans():
	import PortsAndServices
	pscan = "\nRunning PortScans..."
	print(pscan)
	post(slack, data="{'text': '"  + pscan + "'}", headers={'Content-Type': 'application/json'})
	PortsAndServices.main(slack)



def DirBrute():
	import Dbrute
	bfuff = "\nDirectory BruteForcing..."
	print(bfuff)
	post(slack, data="{'text': '"  + bfuff + "'}", headers={'Content-Type': 'application/json'})
	Dbrute.main(slack)



def main():



	letsgo = "\n\n[+] Script Execution Started...\n\n"
	print(letsgo)
	post(slack, data="{'text': '"  + letsgo + "'}", headers={'Content-Type': 'application/json'})
	t1 = Thread(target=amass_scan)
	t2 = Thread(target=findomain_scan)
	t3 = Thread(target=assetfinder_scan)
	t4 = Thread(target=subfinder_scan)
	t5 = Thread(target=cspeak_brute)
	


	t1.start()
	t2.start()
	t3.start()
	t4.start()
	# t5.start()


	t1.join()
	t2.join()
	t3.join()
	t4.join()
	# t5.join()



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


	t6 = Thread(target=PortScans)
	t7 = Thread(target=DirBrute)

	t6.start()
	t7.start()

	t6.join()
	t7.join()



	fin = "\n\n[$$$] ALL THE BORING STUFF DONE, GO HACK NOW...! [$$$]"
	print(fin)
	post(slack, data="{'text': '"  + fin + "'}", headers={'Content-Type': 'application/json'})





if __name__ == '__main__':
	main()

