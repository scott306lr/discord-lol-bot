# discord-lol-bot
a bot for discord written by python

## Required Libraries

discord
googleapiclient
json
bs4
urllib
ssl

### install libraries:

* pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
* pip install discord.py
* pip install bs4

start the program by executing _**bot.py**_ .


## Instructions: 

(In lol.py) 

**!news:** 
* Lists out the newest 5 update news. 
 
**!list [level]:** 
* List the top 6 champions of each stats on the current level. 
 
**!champ [championName] [level]:**
* Shows the rank of each stats of the certain champion on the current level. 
ex: 
``` 
!champ 卡特蓮娜 5
``` 
 

**In the background:** 
the program checks for new updates every 6 hours. It will show the newest update if found. 
 
**Some extra Easter eggs:** 
(In fun.py) When you type in certain words, the bot will print out some images and texts. 
