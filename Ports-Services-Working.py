import os

with open('Domains-online.txt') as f:
	text = f.read().splitlines()
	for line in text:
		# print("Zero : " + os.getcwd())
		os.mkdir(line)
		os.chdir(line)
		os.system('dig +short ' + line + ' | grep -oE "\\b([0-9]{1,3}\\.){3}[0-9]{1,3}\\b" | head -1 >> IP.txt')


		with open('IP.txt') as fs:
			# print("First : " + os.getcwd())
			text1 = fs.read().splitlines()
			for line1 in text1:
				# print("Second : " + os.getcwd())
				os.system("sudo masscan " + line1 + " -p0-10001 --rate 1000 --wait 3 2> /dev/null | grep -o -P '(?<=port ).*(?=/)' | tee Open.txt")

		

			with open("Open.txt") as fsp:
				# print("Last : " + os.getcwd())
				text2 = fsp.read().replace("\n",",").rstrip(",")
				os.system('nmap -p' + text2 + ' ' + line1 + ' | tee Services.txt')
				os.chdir('..')
				# print("Last Final Dir: " + os.getcwd())
				# print(os.chdir('..'))
		