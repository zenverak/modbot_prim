import discord
from discord.ext import commands
import asyncio
import time
import globals
import logging
from modbot import Mod_Commands
import database
import ticket
from logging.handlers import RotatingFileHandler
from discord.utils import get



bot = commands.Bot(command_prefix='$', description='description here')
bot.remove_command('help')


handler = RotatingFileHandler('modbot.log', maxBytes=10000000, backupCount=10)
logging.basicConfig(handlers=[handler], format='%(asctime)s %(message)s', level=logging.DEBUG)
bot.logger = logging.getLogger('bot')

evals = Mod_Commands()
extens = ['ticket','modbot']

    

@bot.event
async def on_ready():
    print("I'm in")
    print(bot.user)


@bot.event
async def on_message(message):
#    print (message.id)
    if message.channel.name in globals.channels:
        await evals.validate_message(message)
    elif message.channel.name in globals.group_chans:
        await evals.validate_group(message)
    else:
#        if trial in u_roles or mod in u_roles or admin in u_roles:      
        if 1 == 1:
            await bot.process_commands(message)




if __name__ == "__main__":
    for extension in extens:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

    bot.run(globals.TOKEN)
