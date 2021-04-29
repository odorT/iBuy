## **iBuy** is a multi-search engine for 3 (amazon.com, aliexpress.com, tap.az) e-commerce websites
### Installation

#### Get the source code
`git clone https://github.com/odorT/iBuy.git`

### In order to prevent dependency version problems, create virtualenv and install dependencies under venv
`python3 -m venv venv`  

### For Windows
`venv/Scripts/activate`  
### For Linux
`source venv/bin/activate`  

### Install dependencies
`pip3 install -r requirements.txt`  

### Run the application
`python3 application.py`  

### After finishing deactivate the venv with
`deactivate`

### Notes
* iBuy only supports Chrome webbrowser, therefore you should have already installed Chrome to be able to run the application
* The current version of the website uses paid Aliexpress Product search API from [magic-aliexpress-rapidapi](https://rapidapi.com/b2g.corporation/api/magic-aliexpress1).
If you want to search Aliexpress too, register at [rapidapi.com](https://rapidapi.com/marketplace) and subscribe to [magic-aliexpress-rapidapi](https://rapidapi.com/b2g.corporation/api/magic-aliexpress1).
Then copy the **X-RapidAPI-Key** from the website. Then you will need to create `.env` file in the iBuy/ folder with following content:  
```
X_RAPIDAPI_KEY=<YOUR PERSONAL RAPIDAPI KEY>
X_RAPIDAPI_HOST_500_MO=magic-aliexpress1.p.rapidapi.com
```  
Replace the <YOUR PERSONAL RAPIDAPI KEY> with the token that you copied before. After that just run the application.  
Or contact [odorlesstangerine@gmail.com](https://mail.google.com/mail/u/0/#inbox?compose=DmwnWrRlQhgRCFlmTNcPXNfFqhVfGsBSXZsjqMFNhsNBqdjtwMcwfKtglvSQLBrDbpDVVcSTqjTL)