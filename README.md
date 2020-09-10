# discord-lol-bot
a bot for discord written by python

## Required Libraries

discord
googleapiclient
json
bs4
urllib
ssl

### Getting Started

To get the program working, you will have to fill up the data inside _**settings.json**_ which looks like this:
``` 
{
   	"TOKEN":"YourTokenHere",
	"DEVELOPER_KEY":"YourDeveloperKeyHere",
	"NEWS_UPDATE_CHANNEL_ID":"DiscordChannelID"
}
```
TOKEN is from [discord developers console](https://discord.com/developers/applications/),\
DEVELOPER_KEY is from [google apis console](https://console.developers.google.com/apis/credentials),\
NEWS_UPDATE_CHANNEL_ID can be gotten by right clicking a channel in discord and select "copy ID".\
\

### install libraries:

```
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
pip install discord.py
pip install bs4
```

start the program by executing _**bot.py**_ .


## Instructions: 

(In lol.py) 

**!news** 
* Lists out the newest 5 update news. 
 
**!list [level]** :\
ex: 
``` 
!list 8
``` 
* List the top 6 champions of each stats on the current level. 
 
**!champ [championName] [level]** :\
ex: 
``` 
!champ 卡特蓮娜 5
``` 
* Shows the rank of each stats of the certain champion on the current level. \
\
the program checks for new updates every 6 hours. It will show the newest update if found. \

When you type in certain words, the bot will print out some images and texts. (In fun.py)
