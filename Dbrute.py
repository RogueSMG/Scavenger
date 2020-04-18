import os




def brute():
		os.system("""xargs -P10 -I {} sh -c 'url="{}"; ffuf -c -H "X-Forwarded-For: 127.0.0.1" -H "User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0" -u "{}/FUZZ" -w ../../tools/ffufplus/wordlist/dicc.txt -t 50 -D -e js,php,bak,txt,asp,aspx,jsp,html,zip,jar,sql,json,old,gz,shtml,log,swp,yaml,yml,config,save,rsa,ppk -ac -se -o ffuf/${url##*/}-${url%%:*}.json' < Domains-online.txt""")


brute()


os.system("""cat ffuf/* | jq '[.results[]|{status: .status, length: .length, url: .url}]' | grep -oP "status\\":\\s(\\d{3})|length\\":\\s(\\d{1,7})|url\\":\\s\\"(http[s]?:\\/\\/.*?)\\"" | paste -d' ' - - - | awk '{print $2" "$4" "$6}' | sed 's/\\"//g' > result_beast.txt""")
