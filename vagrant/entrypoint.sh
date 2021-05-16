#!/usr/bin/env bash

YELLOW='\033[1;33m'

echo "${YELLOW}Installing required dependencies"

sudo apt-get update -y
sudo apt purge python3-venv
sudo apt-get install python3 python3-venv python3-pip -y

if [ -f "google-chrome-stable_current_amd64.deb" ]; then
  echo "${YELLOW}google-chrome exists."
else
  wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
  sudo apt install ./google-chrome-stable_current_amd64.deb -y
  sudo apt --fix-broken install -y
fi

function git_resolve {
    dir=$(basename "$1" .git)
    echo "$dir"
    if [[ -d "$dir" ]]; then
      cd "$dir" || exit
      git pull
    else
      git clone "$1" && cd "$dir" || exit
    fi
}

echo "${YELLOW}Cloning the source code"
git_resolve https://github.com/odorT/iBuy.git

echo "${YELLOW}Setting .env file"
sudo cp /vagrant/.env .env

echo "${YELLOW}Installing pip dependencies"
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt

sleep 5;

echo "${YELLOW}Running application"
python3 application.py
