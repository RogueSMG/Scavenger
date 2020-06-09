#!/bin/bash

sudo apt update
sudo apt -y upgrade
sudo apt -y dist-upgrade


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


# Install RUST for Findomain
curl https://sh.rustup.rs -sSf | sh
source ~/.profile
source ~/.cargo/env


# Make a tools directory
mkdir -p ~/tools
cd ~/tools

# Install Findomain
git clone https://github.com/Edu4rdSHL/findomain.git
cd findomain
cargo build --release
sudo cp target/release/findomain /usr/bin
cd ..

# Install Masscan
sudo apt-get install git gcc make libpcap-dev
git clone https://github.com/robertdavidgraham/masscan
cd masscan
make
mv masscan /usr/bin

cd ..

# Install Subfinder
wget -c "https://github.com/projectdiscovery/subfinder/releases/download/v2.3.2/subfinder-linux-amd64.tar"
tar -xvf subfinder-linux-amd64.tar
mv subfinder-linux-amd64 /usr/bin/subfinder
rm subfinder-linux-amd64.tar


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
go get -u github.com/tomnomnom/httprobe
go get -u github.com/tomnomnom/assetfinder
go get -u github.com/ffuf/ffuf
go get -u github.com/tomnomnom/httprobe