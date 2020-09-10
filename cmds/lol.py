import discord
from discord.ext import commands
from core.classes import Cog_Extension
import json
from bs4 import BeautifulSoup
import urllib.request as req
import ssl
from googleapiclient.discovery import build

with open('settings.json','r',encoding='utf8') as jfile:
    jdata = json.load(jfile)
DEVELOPER_KEY =  jdata['DEVELOPER_KEY']

alist = ["hp","hpregen","mp","mpregen","attackdamage","armor","spellblock","attackspeed","attackrange","movespeed"]

def calculate(basic,g,lv:int=1):
    llv = lv-1
    A = g*llv*(0.7025+0.0175*llv)
    return (round(basic+A,3))

def searchByKeyword (keyword):
    youtube = build('youtube','v3',developerKey=DEVELOPER_KEY)
    req = youtube.search().list(q=f'lol {keyword}' , part='snippet' ,maxResults=5)
    return req.execute()

def compare(cds,cmp,lv:int=1):
    compare=[]
    for cd in cds['data']:
        name = cds['data'][cd]['name']
        stats = cds['data'][cd]['stats'] 
        if cmp =='attackrange'or cmp =='movespeed':
            result = stats[cmp]
        elif cmp == 'attackspeed':
            result = calculate(stats[cmp],stats[f'{cmp}perlevel']/100,lv)     
        else:
            result = calculate(stats[cmp],stats[f'{cmp}perlevel'],lv)
        compare.append((result,name))
        compare.sort(reverse=True)
    return (compare)

with open('champion.json','r',encoding='utf8') as champDatas:
    cds = json.load(champDatas)
with open('champTrans.json','r',encoding='utf8') as champTrans:
    cts = json.load(champTrans)
with open('statTrans.json','r',encoding='utf8') as statTrans:
    sts = json.load(statTrans)

class LOL(Cog_Extension):   
    @commands.command()
    async def list(self,ctx,lv=-1):
        print(f"Recieved Input: !list {lv}")
        if lv == -1 : 
            await ctx.send('`!list [lv]`')
        else :
            try:
                embed=discord.Embed(title=f"數值排行(等級{lv})", description='' ,colour=discord.Colour(0x573688))
                for a in alist :
                    cmplist = compare(cds,a,lv)
                    i=1
                    text= f'Rank 1: {cmplist[0][1]} {cmplist[0][0]}\n'
                    m=cmplist[0][0]
                    for x,y in cmplist[1:6]:
                        if(x<m):
                            m=x
                            i+=1
                        text= text+f'Rank {i}: {y} {x}\n'
                    embed.add_field(name=sts[a], value=text)
                await ctx.send(embed=embed)
            except:
                await ctx.send('Input Error!')
    @commands.command()
    async def champ(self,ctx,champ=None,lv=1):
        print(f"Recieved Input: !champ {champ} {lv}")
        if champ == None :
            ctx.send('`!champ [角色名稱] [lv]`')
        else :
            try:
                engChamp = cts[champ]   
                text=""         
                embed = discord.Embed(title=f'{champ} (等級{lv})', colour=discord.Colour(0x6b0c0c))
                embed.set_image(url=f"http://ddragon.leagueoflegends.com/cdn/img/champion/splash/{engChamp}_0.jpg") 
                for a in range(0,10):
                    cmplist = compare(cds,alist[a],lv)
                    i=1              
                    m=cmplist[0][0]
                    champDict = {cmplist[0][1]:(1,cmplist[0][0])}
                    for x,y in cmplist[1:] :
                        if(x<m):
                            m=x
                            i+=1
                        champDict.update({y:(i,x)})
                    embed.add_field(name=f'{sts[alist[a]]}: Rank {champDict[champ][0]}', value=f'{champDict[champ][1]}')
                await ctx.send(content="", embed=embed)
###################################################################################
                tKey = cts[champ]
                out = searchByKeyword(champ)
                i=0
                combine=[]
                for title in out['items']:
                    combine.append((title['snippet']['title'],title['id']['videoId']))
                    i+=1
                    if i==5 :
                        break
                        
                embed = discord.Embed(title="列出了最相關的幾部影片:", colour=discord.Colour(0x6b0c0c), description="")
                embed.set_thumbnail(url=f"http://ddragon.leagueoflegends.com/cdn/9.24.2/img/champion/{tKey}.png")
                for a in range(0,5):
                    embed.add_field(name=f'影片{a+1}:', value=f"[{combine[a][0]}](https://www.youtube.com/watch?v={combine[a][1]})",inline=False)
                await ctx.send(embed=embed)

            except:
                await ctx.send('Input Error!')
################################################################################### 
    @commands.command()
    async def news(self,ctx):
        print ('Recieved Input: "!news"')
        b = 0
        ssl._create_default_https_context = ssl._create_unverified_context
        embed = discord.Embed(title="近期更新資訊", colour=discord.Colour(0xb8b8b8))
        for a in range(1,5):
            with req.urlopen(f"https://lol.garena.tw/news/?page={a}") as response:
                data = response.read().decode("utf-8")
            root = BeautifulSoup(data,"html.parser")
            allhref = root.find_all("a",class_="newslist-item__link")
            alltext = root.find_all("h2",class_="newslist-item__txt-title")
            for i in range(0,10) :
                text = alltext[i].get_text()
                href = allhref[i].get('href')
                if text.rfind('版本更新') != -1 and text.rfind('聯盟戰棋') == -1 and text.rfind('TFT') == -1 and text.rfind('時刻表') == -1 :
                    embed.add_field(name=f'連結{b+1}:', value=f"[{text}](https://lol.garena.tw{href})",inline=False)
                    b += 1
                if b == 4:
                    break
            if b == 4:
                    break
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(LOL(bot))


 