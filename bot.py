import discord
from discord.ext import commands
import json
import os
with open('settings.json','r',encoding='utf8') as jfile:
    jdata = json.load(jfile)
bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print('>>Bot is online<<')
    
@bot.command()
async def reload(ctx,name=None):
    if (name == None) : 
        await ctx.send('!reload {name}')
        return
    try:
        bot.reload_extension(f'cmds.{name}')
        print(f'Reloaded \"{name}\" !')
        await ctx.send(f'Reloaded \"{name}\" !')
    except:
        await ctx.send('Failed!')

@bot.command()
async def load(ctx,name=None):
    if (name == None) : 
        await ctx.send('!reload {name}')
        return
    try:
        bot.load_extension(f'cmds.{name}')
        print(f'Loaded \"{name}\" !')
        await ctx.send(f'Loaded \"{name}\" !')
    except:
        await ctx.send('Failed!')

@bot.command()
async def unload(ctx,name=None):
    if (name == None) : 
        await ctx.send('!reload {name}')
        return
    try:
        bot.unload_extension(f'cmds.{name}')
        print(f'Unloaded \"{name}\" !')
        await ctx.send(f'Unloaded \"{name}\" !')
    except:
        await ctx.send('Failed!')
    
for filename in os.listdir('./cmds'):
    if filename.endswith('.py'):
        bot.load_extension(f'cmds.{filename[:-3]}')
    

if __name__ == "__main__":
    bot.run(jdata['TOKEN'])
