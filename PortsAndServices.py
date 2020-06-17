import os
import subprocess
from requests import post



def fetch():
	global text
	for line in text:
		
		os.mkdir(line.replace("://","-"))
		os.chdir(line.replace("://","-"))
		
		mod = line.strip("https://" or "http://")
		mod = mod.rstrip("\n")
		
		p1 = subprocess.run(['dig', '+short', mod], capture_output=True, text=True)
		p2 = subprocess.run(['grep', '-oE', '\\b([0-9]{1,3}\\.){3}[0-9]{1,3}\\b'], capture_output=True, text=True, input=p1.stdout)
		
		if p2.returncode != 1:
			with open("IP.txt","w") as ips:
				subprocess.run(['head', '-1'], text=True, stdout=ips, input=p2.stdout)
		else:
			os.chdir('..')
			subprocess.run(['rm', '-r', line.replace("://","-")])
			continue

		

		with open('IP.txt') as fs:
			text1 = fs.read()
			mod = text1.rstrip("\n")
			print("\n" + mod)

			p1 = subprocess.run(['sudo', 'masscan', mod, '-p0-65535', '--rate', '100000', '--wait', '3', '2'], capture_output=True, text=True)

			if p1.stdout != '':
				with open("Open.txt","w") as out:
					subprocess.run(['grep', '-o', '-P', '(?<=port ).*(?=/)'], text=True, input=p1.stdout, stdout=out)
			else:
				print("No Open Ports!\n")
				os.chdir('..')
				continue

			
			with open("Open.txt") as fsp:

				mod1 = fsp.read().replace("\n",",").rstrip(",")

				with open("Services.txt", "w") as serv:
					subprocess.run(['nmap', '-Pn', '-p' + mod1, mod], text=True, stdout=serv)

				os.chdir('..')
				
			print("Services Scanned!\n")	


def main(slack):
	global text
	os.mkdir('Port-Scans')
	os.chdir('Port-Scans')

	with open('../Subdomains.txt') as f:
		text = f.read().splitlines()

	fetch()
	
	os.chdir('..')

	send = "\nPortScans Done...!"
	print(send)
	post(slack, data="{'text': '"  + send + "'}", headers={'Content-Type': 'application/json'})



if __name__ == '__main__':
	main(slx)
	
