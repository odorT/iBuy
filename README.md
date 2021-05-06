# **iBuy** is a multi-search engine for 3 (amazon.com, aliexpress.com, tap.az) e-commerce websites
## Installation  
You can run the application directly on host machine or with [Vagrant](https://www.vagrantup.com/)

### To install on host machine
#### Get the source code
`git clone https://github.com/odorT/iBuy.git`

#### In order to prevent dependency version problems, create virtualenv and install dependencies under venv
`python3 -m venv venv`  

#### For Windows
`venv/Scripts/activate`  
#### For Linux
`source venv/bin/activate`  

#### Install dependencies
`pip3 install -r requirements.txt`  

#### Run the application
`python3 application.py`  

#### After finishing deactivate the venv with
`deactivate`

### Vagrant  
Clone the repository and cd into vagrant folder. To search aliexpress, you should have .env in /vagrant folder too. 
Check Notes for more details about .env. To use this feature, you should have already installed virtualbox and
[vagrant](https://www.vagrantup.com/downloads). **Note that Vagrant uses NFS and NFS is supported only in Linux. 
To you nfs in windows, you can try vagrant-winnfsd plugin(which is not stable)**. Recommended to use in Linux OS.  
Inside vagrant/ folder, run following command:  
`vagrant up`

This will automatically create new virtual machine in virtualbox and provision the application inside it.
To access website hosted in VM, use `192.168.33.11:5000` or `localhost:5001`. You can change the ip address and port in Vagrantfile.

### Notes
* iBuy only supports Chrome webbrowser, therefore you should have already installed Chrome to be able to run the application
* The current version of the website uses paid Aliexpress Product search API from [magic-aliexpress-rapidapi](https://rapidapi.com/b2g.corporation/api/magic-aliexpress1).
If you want to search Aliexpress too, register at [rapidapi.com](https://rapidapi.com/marketplace) and subscribe to [magic-aliexpress-rapidapi](https://rapidapi.com/b2g.corporation/api/magic-aliexpress1).
Then copy the **X-RapidAPI-Key** from the website. Then you will need to create `.env` file in the iBuy/ folder with following content:  
```
X_RAPIDAPI_KEY=<YOUR PERSONAL RAPIDAPI KEY>
X_RAPIDAPI_HOST_500_MO=magic-aliexpress1.p.rapidapi.com
```  
Replace `<YOUR PERSONAL RAPIDAPI KEY>` with the token that you copied before. After that just run the application.  
Or contact [odorlesstangerine@gmail.com](https://mail.google.com/mail/u/0/#inbox?compose=DmwnWrRlQhgRCFlmTNcPXNfFqhVfGsBSXZsjqMFNhsNBqdjtwMcwfKtglvSQLBrDbpDVVcSTqjTL)