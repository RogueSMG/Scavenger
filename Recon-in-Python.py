import os
import sys
import argparse


parser = argparse.ArgumentParser(description='Recon Testing')
parser.add_argument("--domain", dest='domain', help='Domain Name for the Recon!', required=True)
args = parser.parse_args()
dom = args.domain

#						"""	Part 1: GATHERING SUBDOMAINS """


# Passive Amass Scanning
print('\n[*] Gathering Passive Subdomains using Amass...\n\n')
os.system('amass enum --passive -d ' + args.domain + ' -o amass.txt')
print('\n[+] Done')




# Findomain Scanning
os.system('findomain --target ' + dom +' --threads 50 -o')


# Assetfinder Scanning
os.system('assetfinder --subs-only ' + dom + ' > assetfinder.txt')


# Subfinder Scanning
os.system('subfinder -silent -d ' + dom + ' -o subfinder.txt')


#Commomspeak2 Brute Forcing
print('\n\n[*] Bruting Subs using commonspeak2 subdomain wordlist...')
wordlist = open('/home/r00t/commonspeak2-wordlists/subdomains/subdomains.txt').read().split('\n')

for word in wordlist:
    if not word.strip(): 
        continue
    f = open("CommonSpeak_Bruted.txt", "a+" )
    f.write('{}.{}\n'.format(word.strip(), args.domain))
    # print('{}.{}\n'.format(word.strip(), scope))
f.close()
print('[+] File Closed!')
print('[+] Done')



# Combining the Subdomain Lists
print()
os.system('cat amass.txt findomain.txt assetfinder.txt subfinder.txt >> Potential-Domains.txt')


# Resolving with MassDns
print()
os.system('massdns -r ~/massdns/lists/resolvers.txt -q -t A -o S -w "Domains-online.txt" "Potential-Domains.txt"')


# AltDns Smart Brute-Forcing --> Need to implement Recurssion here
# filenames = ["Domains-online.txt", "altdns.txt", "Level1-Domains.txt", "Level2-Domains.txt"]

"""
flag = 1	

def rec(a):
	# print(a,b)
	global flag
	while flag < 3:
		os.system('altdns -i ' + str(a) + '.txt -w ../altdns_words.txt -o ' + str(a+1) + '.txt')

		
		#Resolving again for AltDns Domains 
		print('MassDns')
		os.system('massdns -r ~/massdns/lists/resolvers.txt -q -t A -o S -w "' + str(a+2) + '.txt" "' + str(a+1) + '.txt"')
		print('Done Once')
		flag += 1
		print(flag)
		rec(a+2)
		

rec(0)
"""