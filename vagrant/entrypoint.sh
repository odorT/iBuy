#!/usr/bin/env bash

sudo apt purge python3-venv
sudo apt install python3-venv

sudo apt-get update -y
sudo apt-get install python3 python3-venv python3-pip -y

wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install ./google-chrome-stable_current_amd64.deb -y
sudo apt --fix-broken install -y

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

git_resolve https://github.com/odorT/iBuy.git

sudo cp /vagrant/.env .env

python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt

sleep 5;

python3 application.py
