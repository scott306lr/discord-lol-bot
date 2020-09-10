import discord
from discord.ext import commands
from core.classes import Cog_Extension
import json
import os

class Fun(Cog_Extension):   
    @commands.Cog.listener()
    async def on_message(self,message):
        if message.author.bot: return
        msg = message.content.upper()
        with open('funText.json','r',encoding='utf8') as jfile:
            jdata = json.load(jfile)

        try:
            sendtxt = jdata[msg]
            print(f'Found Keyword: {msg}')
            ch = message.channel
            await ch.send(sendtxt)

        except:
            for fileKeys in os.listdir('./picture'):
                keywords = (fileKeys[:-4]).split("&")
                for keyword in keywords:
                    if msg.rfind(keyword.upper()) !=-1:
                        print(f'Found Keyword: {keyword}')
                        ch = message.channel
                        sendFile = discord.File(f'picture/{fileKeys}')
                        await ch.send(file=sendFile)


def setup(bot):
    bot.add_cog(Fun(bot))
    