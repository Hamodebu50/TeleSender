# TeleSender
A Windows GUI program that utilizes the Telethon library to send private 1-on-1 bulk message to a list of numbers. I was frustrated with the current landscape of available programs that do the same thing, but are charging rediculous fees and subscriptions. This is the solution.

# Pre-requisites

Make sure you have installed Python on your machine, and open GitBash by searching from the start menu. Type in the following:

```pip install tkinter```
```pip install telethon```

That's it! Download the .py file from this repo and double click on it to start.

# Setup
You'll need your to create your own Telegram bot using your registered number. Head to https://my.telegram.org/auth, verify your number, create the bot and you'll be given two important values: *API ID* and *API Hash.* Keep those values a secret, don't share it with anybody.

Enter those values within the program, along with your bulk message to be sent and the list of numbers. Hit Send, and the program will send a request for access to your account. Telegram will send you the codem Take it and enter it within the command window and press enter. Once you are done, the program will send a private message, using your account, to the list of numbers provided. Happy marketing!

# Notes

Make sure to use the Delay function. Sending 100s of messages all at once will get you throttled, if not flagged by Telegram for abuse. A delay of 60 seconds sounds reasonable. 

Disclaimer: I'm not resposible for what you do with this program!

This program is open-source, MIT licensed and everyone is free to fork, modify, change or build upon. All I ask is for credit :D. 
