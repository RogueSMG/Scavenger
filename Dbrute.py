import os
import subprocess
from requests import post

os.mkdir('Directories')


def beast():

		subprocess.run(["""xargs -P10 -I {} sh -c 'url="{}"; ffuf -c -H "X-Forwarded-For: 127.0.0.1" -H "User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0" -u "{}/FUZZ" -w /root/Wordlists/dicc.txt -t 50 -D -e js,php,bak,txt,asp,aspx,jsp,html,zip,jar,sql,json,old,gz,shtml,log,swp,yaml,yml,config,save,rsa,ppk -ac -se -o Directories/${url##*/}-${url%%:*}.json' < Web-Domains.txt"""],shell=True, stdout=subprocess.DEVNULL)
		send = "Fuff Done!"
		print(send)


def main(slack):
	beast()
	subprocess.run(["""cat Directories/* | jq '[.results[]|{status: .status, length: .length, url: .url}]' | grep -oP "status\\":\\s(\\d{3})|length\\":\\s(\\d{1,7})|url\\":\\s\\"(http[s]?:\\/\\/.*?)\\"" | paste -d' ' - - - | awk '{print $2" "$4" "$6}' | sed 's/\\"//g' > Directories.txt"""], shell=True)
	subprocess.run(['rm', '-r', 'Directories'])
	send = "\nDirectories Bruteforced...!"
	print(send)
	post(slack, data="{'text': '"  + send + "'}", headers={'Content-Type': 'application/json'})



if __name__ == '__main__':
	main(slx)
