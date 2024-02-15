#!/bin/bash

sudo apt update


# Install Golang if not already installed
if [[ -z "$GOPATH" ]];then
echo "It looks like go is not installed, would you like to install it now"
PS3="Please select an option : "
choices=("yes" "no")
select choice in "${choices[@]}"; do
        case $choice in
                yes)

					echo "Installing Golang"
					wget -c https://dl.google.com/go/go1.14.3.linux-amd64.tar.gz
					sudo tar -xvf go1.14.2.linux-amd64.tar.gz
					sudo mv go /usr/local
					export GOROOT=/usr/local/go
					export GOPATH=$HOME/go
					export PATH=$GOPATH/bin:$GOROOT/bin:$PATH
					echo 'export GOROOT=/usr/local/go' >> ~/.bash_profile
					echo 'export GOPATH=$HOME/go'	>> ~/.bash_profile			
					echo 'export PATH=$GOPATH/bin:$GOROOT/bin:$PATH' >> ~/.bash_profile	
					echo 'export PATH=$PATH:/snap/bin' >> ~/.bash_profile
					source ~/.bash_profile
					sleep 1
					break
					;;
				no)
					echo "Please install go and rerun this script"
					echo "Aborting installation..."
					exit 1
					;;
	esac	
done
fi



# Make a tools directory
mkdir -p ~/tools
cd ~/tools

# Install Findomain
wget https://github.com/Findomain/Findomain/releases/latest/download/findomain-linux.zip
unzip findomain-linux.zip
chmod +x findomain
mv findomain /usr/bin/findomain


# Install Masscan
sudo apt-get install git gcc make libpcap-dev
git clone https://github.com/robertdavidgraham/masscan
cd masscan
make
mv bin/masscan /usr/bin/

cd ..


# Wordlists
mkdir -p ~/Wordlists
cd ~/Wordlists
wget https://raw.githubusercontent.com/assetnote/commonspeak2-wordlists/master/subdomains/subdomains.txt
wget https://raw.githubusercontent.com/dark-warlord14/ffufplus/master/wordlist/dicc.txt
wget https://raw.githubusercontent.com/infosec-au/altdns/master/words.txt
cd ..


# Install amass and nmap
sudo snap install amass
sudo apt install nmap

# Installing the required GO based tools
go install github.com/tomnomnom/assetfinder@latest
go install github.com/ffuf/ffuf@latest
go install github.com/tomnomnom/httprobe@latest
go install github.com/projectdiscovery/subfinder/cmd/subfinder@latest
