import discord
import globals
import re
from discord.utils import get
from discord.ext import commands
import logging
import asyncio


class Mod(commands.Cog):


    def __init__(self, bot):
        self.bot = bot
        


    @commands.command(pass_context=True)
    @commands.has_any_role(globals.t_id, globals.a_id, globals.m_id)
    async def show_words(self,ctx):
        await ctx.message.channel.send(globals.bad_words)

    
    @commands.command(pass_context=True)
    @commands.has_any_role(globals.t_id, globals.a_id, globals.m_id)
    async def add_words(self,ctx):
        words =  ctx.message.content.replace('$add_words','').split(' ')
        words.pop(0)
        words_to_add = []
        words_already_added = []
        for word in words:
            if word in globals.bad_words:
                words_already_added.append(word)
            else:
                words_to_add.append(word)
                globals.bad_words.append(word)
        await ctx.message.channel.send("adding the following: {}\n The following were already added: {}".format(words_to_add, words_already_added ))
        f = open(globals.bad_file, 'a')
        for word in words_to_add:
          f.write('{}\n'.format(word))
        f.close()
        
        
    @commands.command(pass_context=True)
    @commands.has_any_role(globals.t_id, globals.a_id, globals.m_id)
    async def remove_words(self,ctx):
        try:
            words =  ctx.message.content.replace('$add_words','').split(' ')
            words.pop(0)
            for word in words:
                index = globals.bad_words.index(word)
                globals.bad_words.pop(index)
            f = open(globals.bad_file, 'w')
            for word in globals.bad_words:
                f.write('{}\n'.format(word))
            f.close()
            await ctx.message.channel.send('deleted {}'.format(words))
        except:
            await ctx.message.channel.send('could not delete words')
        
    @commands.command(pass_context=True)
    @commands.has_any_role(globals.t_id, globals.a_id, globals.m_id)
    async def toggle_delete(self,ctx):
        if globals.DEL == False:
            globals.DEL = True
        else:
            globals.DEL = False
            

    @commands.command()
    @commands.has_any_role(globals.t_id, globals.a_id, globals.m_id)
    async def show_delete_mode(self, ctx):
        await ctx.message.channel.send("Delete mode is {}. When False no messages will be deleted".format(globals.DEL))
        
        
    @commands.command(pass_context=True)
    @commands.has_any_role(globals.t_id, globals.a_id, globals.m_id)
    async def reload_words(self,ctx):
         f = open(globals.bad_file, 'r')
         globals.bad_words = []
         for line in f.readlines():
             globals.bad_words.append(line.replace('\n',''))


    @commands.command()
    @commands.has_any_role(globals.t_id, globals.a_id, globals.m_id)
    async def mod_help(self, ctx):
        await ctx.message.channel.send("**$show_words** to show the list of words that will trigger nsfw warning\n**$add_words *word1*...*wordn* .** will add words. Just seperate them by a space\n**$delete_words *word1*...*wordn* .**will delete all words listed\n**$toggle_delete** will stop the bot from deleting any posts that are too short\n**$show_delete_mode** will show you if it is deleting short posts or not")
        
    
        
    
class Mod_Commands():

    def format_nsfw_message(self,message):
        author = message.author
        content = message.content
        log_message = "message in {}\n\n {}".format(message.channel.mention, content)
    #    emb = {'author':{'name':message.author.name,'icon_url': message.author.avatar},'title':log_message}
        embed = discord.Embed()
        if len(log_message) > 1024:
            embed.add_field(name="Questionable Message", value=log_message[0:1024], inline=True)
            embed.add_field(name="Continued", value=log_message[1024::], inline=False)
        else:
            embed.add_field(name="Questionable Message", value=log_message, inline=True)
        embed.add_field(name="Time of Message", value=message.created_at, inline=False)
        embed.set_author(name=author, icon_url=message.author.avatar_url)
        return embed
    
    
    def check_nsfw(self,message):
        mess = message.content
        words = []
        for word in globals.bad_words:
            loc = mess.lower().find(word)
            if loc >= 0:
                if word == 'dom':
                  if loc in (0,1,2):
                      words.append(word)
                  else:
                      if mess[loc-3:loc] == 'fan':
                          pass
                      else:
                          words.append(word)
                else:
                    words.append(word)
        if len(words) > 0:
            logging.debug('{} had a message with these bad words {}'.format(message.author,words))
            return True, words
        else:
            return False, ''
    
    
    def get_alternate_pair(self,channel_1):
        name = ''
        for chan in globals.channel_pairs:
            if channel_1['name'] != chan['name'] and channel_1['group'] == chan['group']:
                name = chan['name']
                break
        return name
    
    
    def get_chan(self,message, name):
        return get(message.guild.channels, name=name)
    
    
    def check_length(self,message):
#         '''
#    
#         Returns Pass, delete, and message
#      
#         if pass is True then the message was a good lenght for the channel it is in
#         if pass is false then there will be a message
#         If delete is True then we have set the message to be deleted
#          '''
        no_space = message.content.replace(' ','')
        ##check_length
        no_space_length = len(no_space)
        print('this message is {} long'.format(no_space_length))
        author = message.author
        chan = ''
        type_ = ''
        for channel in globals.channel_pairs:
            if channel['name'] == message.channel.name:
                type_ = channel['type']
                chan = channel
                break
        print(' You are in channel {}'.format(chan['name']))
        print(' Channel type is {}'.format(chan['type']))
        if type_ == 'short':
            if no_space_length >= 240 and no_space_length < globals.upper_min:
                return True,False, ''
            else:
                if no_space_length < 50:
                    return False ,True, '{}, Your post in {} is less than 50 characters and it should be a minimum of 250 characters (not counting spaces) long. Thanks\n\n'.format(author.mention, message.channel.mention)
                if no_space_length < 250:
                    if no_space_length < globals.lower_lin_lim:
                        return False, True,  '{}, Your post is too short for {} and it should be a minimum of 250 characters (not counting spaces) long. Thanks \n\n'.format(author.mention, message.channel.mention)
                    else:
                        return False, False,  '{}, Your post is too short for {} and it should be a minimum of 250 characters (not counting spaces) long. Thanks \n\n'.format(author.mention, message.channel.mention)
                else:
                    other_group = self.get_chan(message,self.get_alternate_pair(chan))
                    return False, False, '{}, Your post is too long to be in {}. Please move it to {}. Thanks\n\n'.format(author.mention,message.channel.mention,other_group.mention)
        if type_ == 'long':
            if no_space_length >= globals.upper_min:
                return True, False,  ''
            elif self.check_for_link(message):
                return True, False, ''
            elif no_space_length < globals.upper_lin_lim:
                other_group = self.get_chan(message,self.get_alternate_pair(chan))
                return False, True, '{}, Message is too short for {}, Please move it to {} and make sure that it less than {} characters (not counting spaces). Thanks\n\n'.format(author.mention,message.channel.mention,other_group.mention, globals.upper_min-1)
            else:
                other_group = self.get_chan(message,self.get_alternate_pair(chan))
                return False, False, '{}, Your post is too short for {} and it should be a minimum of {} characters (not counting spaces) long. Thanks\n\n'.format(author.mention,message.channel.mention, globals.upper_min-1)
    
        
    def check_for_link(self,message):
        url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message.content)
        if len(url) == 0:
            return False
        else:
            return True
    
    
    async def validate_message(self,message):
        mod_chan = self.get_chan(message,globals.MOD_CHAN)
        nsfw_chan = self.get_chan(message,globals.NSFW_CHAN)
        print("nsfw channel is {}".format(nsfw_chan.name))
        length_check, delete, length_message = self.check_length(message)
        print('{} .......{}'.format(length_check, length_message))
        is_bad_words, bads = self.check_nsfw(message)
        if is_bad_words:
            print("found bad words")
            embed = self.format_nsfw_message(message)
            try:
                await nsfw_chan.send(embed=embed)
            except:
                print("no exist")
        if not length_check:
            await mod_chan.send(length_message)
        print("deletign is {}".format(delete))
        if delete and globals.DEL:
            await message.author.send(content='This your deleted message')
            await message.author.send(content=message.content)
            await message.delete()
            
    async def validate_group(self, message):
        mod_chan = self.get_chan(message,globals.MOD_CHAN)
        nsfw_chan = self.get_chan(message,globals.NSFW_CHAN)
        is_bad_words, bads = self.check_nsfw(message)
        if is_bad_words:
            print("found bad words")
            embed = self.format_nsfw_message(message)
            try:
                await nsfw_chan.send(embed=embed)
            except:
                print("no exist")
        link = self.check_for_link(message)
        if not link and globals.DEL:
            link_message = "{}, your advertisement in {} did not have a link a group. Please try again after your cooldown".format(message.author.mention, message.channel.mention)
            await mod_chan.send(link_message)
            await message.author.send(content='This your deleted message')
            await message.author.send(content=message.content)
            await message.delete()
            


def setup(bot):
    bot.add_cog(Mod(bot))
