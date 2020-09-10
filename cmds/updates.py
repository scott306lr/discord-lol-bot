import discord
from discord.ext import commands
from core.classes import Cog_Extension
import asyncio
from bs4 import BeautifulSoup
import urllib.request as req
import ssl
import json


class Updates(Cog_Extension):   
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        async def interval():
            await self.bot.wait_until_ready()
            with open('settings.json','r',encoding='utf8') as jfile:
                jdata = json.load(jfile)
            CHANNEL_ID =  jdata['NEWS_UPDATE_CHANNEL_ID']
            self.channel = self.bot.get_channel(int(CHANNEL_ID))
            while not self.bot.is_closed():
                with open(r'updateCheck.json','r', encoding='utf-8') as load_f:
                    udc = json.load(load_f)
                ######Check News###########################################
                page=1
                found=False
                ssl._create_default_https_context = ssl._create_unverified_context
                for page in range(1,2):
                    with req.urlopen(f"https://lol.garena.tw/news/?page={page}") as response:
                        data = response.read().decode("utf-8")
                    root = BeautifulSoup(data,"html.parser")
                    allhref = root.find_all("a",class_="newslist-item__link")
                    alltext = root.find_all("h2",class_="newslist-item__txt-title")
                    for i in range(0,10) :
                        if found == True: break   
                        text = alltext[i].get_text()
                        href = allhref[i].get('href')
                        if (text.rfind('版本更新') != -1 and text.rfind('聯盟戰棋') == -1 and text.rfind('TFT') == -1 and text.rfind('時刻表') == -1) :
                            if udc['newestNews'] != href :
                                udc['newestNews'] = href
                                found = True 
                                embed = discord.Embed(title="New Update!", description=f"[{text}](https://lol.garena.tw{href})" ,colour=discord.Colour(0xb8b8b8))
                                await self.channel.send(embed=embed)
                                print('Updated news!')
                ######Check ChampData##################################
                ssl._create_default_https_context = ssl._create_unverified_context
                with req.urlopen("https://ddragon.leagueoflegends.com/realms/tw.json") as response:
                    data = json.load(response)
                    version = data['v']
                if udc['version'] != version:
                    udc['version'] = version
                    with req.urlopen(f"http://ddragon.leagueoflegends.com/cdn/{version}/data/zh_TW/champion.json") as response:
                        champInf = json.load(response)
                    with open(r'champion.json', 'w') as dump_f:
                        json.dump(champInf, dump_f)

                    champTrans = {}
                    for champ in champInf['data']:
                        champEng = champInf['data'][champ]['name']
                        champTrans[champEng] = champ
                    with open(r'champTrans.json', 'w') as dump_f:
                        json.dump(champTrans, dump_f)
                    print(f'Updated champion data!')
                    print(f'Current Version: {version}')

                ###write updateCheck###
                with open(r'updateCheck.json', 'w') as dump_f:
                    json.dump(udc, dump_f)

                await asyncio.sleep(86400)
        self.bg_task = self.bot.loop.create_task(interval())

def setup(bot):
    bot.add_cog(Updates(bot))