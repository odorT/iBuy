#!/usr/bin/env bash

sudo apt-get update -y && sudo apt-get install python3 python3-venv python3-pip

wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install ./google-chrome-stable_current_amd64.deb -y
sudo apt --fix-broken install -y

git clone https://github.com/odorT/iBuy.git && cd iBuy/ || exit

python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt

python3 application.py
