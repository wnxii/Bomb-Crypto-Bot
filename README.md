# Bomb-Crypto-Bot
 
An automation sccript that is incorporated with P2E NFT game Bomb Crypto. I'm also using this as an opportunity to pick up more on Python.

This script was inspired and uses small sections of code from [mpcabete's script](https://github.com/mpcabete/bombcrypto-bot) but I have implemented my own script from scratch and the flow is targetted at being efficient, light-weight and optimized.

This bot/script is currently private and won't be public, thus source code has been removed.

## **Features**
- Automated script with the lowest downtime
- Sends only heroes that has green stamina bar to work
- Dynamic screen polling, does not do actions based on a fixed routine
- Able to recover from any type of error regardless
- Highly configuarable script with tons of settings in the config
- Logs are saved locally and/or sent to discord through webhook
- New maps are automatically screenshotted and saved
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

## **Screenshots**
![Script](https://github.com/mawenxi2112/Bomb-Crypto-Bot/blob/main/readme-images/login.png)
![Discord Log](https://github.com/mawenxi2112/Bomb-Crypto-Bot/blob/main/readme-images/log.png)
![Discord New Map](https://github.com/mawenxi2112/Bomb-Crypto-Bot/blob/main/readme-images/map.png)
![Discord Chest Profits](https://github.com/mawenxi2112/Bomb-Crypto-Bot/blob/main/readme-images/chest.png)


