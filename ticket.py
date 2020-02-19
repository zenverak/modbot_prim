import discord
from discord.ext import commands
import asyncio
import time
import globals
import logging
from discord.utils import get


class Ticket(commands.Cog):


    def __init__(self, bot):
        self.bot = bot


    @commands.command(pass_context=True)
    async def ticket_open(self,ctx):
    #    await ctx.message.channel.send('Bitch be patient im working')
        ticket_answerers = ['Pregnancy Tests XD']
    
        f = open(globals.COUNT_FILE,'r')
        count = int(f.read())
        f.close()
        f = open(globals.COUNT_FILE, 'w')
        
        if count == 100:
            f.write(str(1))
        else:
            f.write(str(count+1))
        f.close()
        message = ctx.message.content
        server = ctx.message.guild
        author = ctx.message.author
        chan_name = ('{}-{}'.format(message,count)).replace('$ticket_open','ticket').replace(' ','-')
        cat_name = '????????????????'
    #    c_id = 611748344649351199
        c_id = globals.TICKET_CATEGORY
        category = discord.utils.get(ctx.guild.categories, id=c_id)
        print (category)
        everyone = server.roles[0]
        trial = get(server.roles,id=642345026264760329)
        mod = get(server.roles,id=611134565733498881)
        admin = get(server.roles,id=604801999866822686)
        overwrites = {author: discord.PermissionOverwrite(read_messages=True,send_messages=True),
                      everyone: discord.PermissionOverwrite(read_messages=False),
                      trial: discord.PermissionOverwrite(read_messages=True,send_messages=True),
                      mod: discord.PermissionOverwrite(read_messages=True,send_messages=True),
                      admin: discord.PermissionOverwrite(read_messages=True,send_messages=True)}
        await category.create_text_channel(chan_name, overwrites=overwrites)
        print(server.channels)
        print(chan_name)
        chan = get(server.channels, name=chan_name.lower())
        print(chan)
        alert_message = "{}, this is your ticket. {}, {}, {} a ticket has been opened".format(author.mention,trial.mention, mod.mention, admin.mention)
        print(alert_message)
        await chan.send(alert_message)
        print(author)
        print(server)
    
    @commands.command(pass_context=True)
    async def ticket_close(self,ctx):
        chan = ctx.message.channel
        if ctx.channel.name.find('ticket') != 0:
            await ctx.message.channel.send('Please use this command inside the ticket you wish to close')
        else:
            await chan.delete(reason=ctx.message.content)
     
     
    @commands.command(pass_contest=True)
    async def add_user(self,ctx):
        if is_ticket(ctx.channel.name):
            mess = ctx.message
            check1 = mess.content.find('<@!')
            check2 = mess.content.find('<@')
            if check1 != -1 or check2 != -1:
                for name in mess.mentions:
                    await ctx.channel.set_permissions(name, send_messages=True, read_messages=True)
            else:
                await mess.channel.send('{}, please include a user'.format(ctx.message.author.mention))
        else:
            ctx.message.channel.send('You can only add users this way in a ticket channel')
    
    @commands.command(pass_context=True)
    async def help(self,ctx):
        chan = ctx.message.channel
        await ctx.message.channel.send('type **$ticket_open <reason for opening>** to open ticket\ntype **$ticket_close <reason for closing>** to close the ticket.\n to add users to the ticket, type **$add_user @user_name1 @user_name2 etc** . If you only need one user then only use one username.\n do not use the brackets when running commands')
           
        
    
    @commands.command(pass_context=True)
    @commands.has_any_role(globals.t_id, globals.a_id, globals.m_id)
    async def show_channels(self,ctx):
        server = ctx.message.guild
        print(server.channels)
    
    
    @commands.command(pass_context=True)
    @commands.has_any_role(globals.t_id, globals.a_id, globals.m_id)
    async def show_roles(self,ctx):
        server = ctx.message.guild
        count = 0
        for i in server.roles:
            print('{}   {}'.format(count, i))
            count += 1
        count += 1
    
    
    def is_ticket(chan):
        if chan.find('ticket') == 0:
            return True
        return False

def setup(bot):
    bot.add_cog(Ticket(bot))
