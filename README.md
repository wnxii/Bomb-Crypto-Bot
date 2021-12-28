# Bomb-Crypto-Bot
 
An automation sccript that is incorporated with P2E NFT game Bomb Crypto. I'm also using this as an opportunity to pick up more on Python.

This script was inspired and uses small sections of code from [mpcabete's script](https://github.com/mpcabete/bombcrypto-bot) but I have implemented my own script from scratch and the flow is targetted at being efficient, light-weight and optimized.

## **Features**
- Automated script with the lowest downtime
- Sends only heroes that has green stamina bar to work
- Dynamic screen polling, does not use a routine check like mpcabete's
- Able to recover from any type of error regardless
- Highly configuarable script with tons of settings in the config
- Logs are saved locally or sent to discord through webhook
- Errors are automatically screenshotted and saved
- Chest profits are periodically screenshotted, saved and sent to discord webhook
- Searching multiple image positions that takes about 0.3s~ on a 4k resolution monitor

## **How to use the script**

Setup config in config.yaml, add in your own discord ID and webhooks.

Download and install python 3.9.x and make sure to tick "Add Python 3.9 to PATH"

Run the following commands in terminal

```
pip install -r requirements.txt
```

```
python main.py
```
