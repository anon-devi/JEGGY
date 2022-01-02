import discord
from discord import colour
from discord import guild
from discord import mentions
from discord import channel
from discord import message
from discord.abc import Messageable
from discord.colour import Color
from discord.ext import commands
from discord.ext.commands.core import command
import youtube_dl
import os
from discord_slash import SlashCommand
import requests
import random
import aiohttp
import asyncio
#import replit
from flask import Flask
#import keep_alive
from dotenv import load_dotenv
import datetime



client = commands.Bot(command_prefix=">")
client.remove_command('help')

@client.event
async def on_ready():
      await client.change_presence(activity=discord.Game(name='http://jeggy.xyz/'))
      print('We have logged in as {0.user}'.format(client))


#----------------------
#general commands

slash = SlashCommand(client, sync_commands=True)

@client.event
async def on_message(message):
    message.content = message.content.lower()
    if message.author == client.user:
        return
    
    if message.content.startswith("hello"):
        await message.channel.send("hello!!")
    await client.process_commands(message)
    


@client.command()
async def invite(ctx):
    invite = await ctx.channel.create_invite()
    await ctx.send(invite)




#@client.command()
#async def server(ctx):
#    await ctx.send("https://discord.gg/AnmC8djr5Z")

@client.command()
async def bot(ctx):
    await ctx.send("https://discord.com/api/oauth2/authorize?client_id=825576242530615326&permissions=8&scope=bot%20applications.commands")



#@slash.slash(description="displays the bot's website")
#async def web(ctx):
   #await ctx.send("http://jeggy.xyz/")




#music commands







#admin commands


@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, user: discord.Member, *, reason = None):
    if not reason:
        await user.kick()
        await ctx.send(f"{user} has been kicked for an **unspecified reason**.")
    else:
        await user.kick(reason=reason)
        await ctx.send(f"**{user}** has been kicked for **{reason}**.")


@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, user: discord.Member, *, reason = None):
    if not reason:
        await user.ban()
        await ctx.send(f"**{user}** has been banned for an **unspecified reason**.")
    else:
        await user.ban(reason=reason)
        await ctx.send(f"**{user}** has been banned for **{reason}**.")


#@client.command()
#@commands.has_permissions(manage_messages=True)
#async def mute(ctx, member: discord.Member, *, reason=None):
#    guild = ctx.guild
#    mutedRole = discord.utils.get(guild.roles, name="Muted")
#
#    if not mutedRole:
#        mutedRole = await guild.create_role(name=Muted)
#
#        for channel in guild.channels:
#            await channel.set_permissions(mutedRole, speak=False, #send_messages=False, read_message_history=True, read_messages=True)
#    if not reason:
#        await member.add_roles(mutedRole, reason=reason)
#        await ctx.send(f"{member.mention} was muted for an **unspecified #reason** 🔇.")
#        await member.send(f"You were muted in the server **{guild.name}** for #an **unspecified reason** 🔇")
#    else:
#        await member.add_roles(mutedRole, reason=reason)
#        await ctx.send(f"{member.mention} was muted for **{reason}** 🔇.")
#        await member.send(f"You were muted in the server **{guild.name}** for #{reason} 🔇.")
#

#@client.command()
#@commands.has_permissions(manage_messages=True)
#async def unmute(ctx, member: discord.Member):
#    mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")
#
#    await member.remove_roles(mutedRole)
#    await ctx.send(f"Successfully unmuted {member.mention} 🔊")
#    await member.send(f"You were unmuted in the server **{ctx.guild.name}** 🔊")
#

@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=100):
    channel = ctx.message.channel
    messages = []
    async for message in channel.history(limit=amount + 1):
        messages.append(message)

    await channel.delete_messages(messages)
    #await ctx.send(f'{amount} messages have been deleted by {ctx.message.author.mention}')


@client.command()
@commands.has_permissions(manage_channels=True)
async def slowmode(ctx, seconds: int):
    await ctx.channel.edit(slowmode_delay=seconds)
    await ctx.send(f"Set the slowmode in this channel to `{seconds}` seconds!")



#help command(slash)



#mod command list(help_mod)




#giveaway command(beta)
#@client.command()
#@commands.has_permissions(manage_messages=True)
#async def create(ctx, mins: int, *, prize: str):
    #embed = discord.Embed(title="Giveaway!",
    #description=f"{prize}",
    #color=ctx.author.color)

    #end = datetime.datetime.utcnow() + datetime.timedelta(seconds=mins * 60)

    #embed.add_field(name="Ends at:", value=f"{end} UTC")

    #my_msg = await ctx.send(embed=embed)
    #await my_msg.add_reaction("🎉")

    #await asyncio.sleep(mins)

    #new_msg = await ctx.channel.fetch_message(my_msg.id)

    #users = await new_msg.reactions[0].users().flatten()

    #users.pop(users.index(client.user))

    #winner = random.choice(users)

    #await ctx.send(f"Congratulations! {winner.mention} won {prize}!")


#@client.command()
#@commands.has_permissions(kick_members=True)
#async def reroll(ctx, channel: discord.TextChannel, id_: int):
    #try:
   #     new_msg = await channel.fetch_message(id_)
    #except:
     #   await ctx.send(
      #      "The ID that was entered was incorrect, make sure you have entered the correct giveaway message ID."
       # )
    #users = await new_msg.reactions[0].users().flatten()
    #users.pop(users.index(client.user))

    #winner = random.choice(users)

    #await channel.send(
     #   f"Congratulations the new winner is: {winner.mention} for the giveaway rerolled!"
    #)



#meme command
meme_colour=[0xE8FF45,0x00FF1F,0x14B5B8,0x0859B9,0x9504B2,0xE70C0C]
@client.command(pass_context=True)
async def meme(ctx):
    embed=discord.Embed(description="",colour=random.choice(meme_colour))
    async with aiohttp.ClientSession() as cs:
        async with cs.get('https://www.reddit.com/r/dankmemes/new.json?sort=hot') as r:
            res = await r.json()
            embed.set_image(url=res['data']['children'] [random.randint(0, 25)]['data']['url'])
            await ctx.send(embed=embed)


#("okay, Jeggy is ready to help! first you need to know the prefix which is > then you can type >commands")


#help guide
@client.command()
async def help(ctx):
  embed = discord.Embed(description='okay, Jeggy is ready to help! first you need to know the prefix which is > then you can type >commands')
  await ctx.send(embed=embed)



#help commands
@client.command()
async def commands(ctx):
        embed=discord.Embed(title="Commands")
        embed.set_author(name="By Dxrk & Coder")
        embed.add_field(name=">meme", value="Displays random memes", inline=True)
        #embed.add_field(name=">help", value="shows this command", inline=False)
        embed.add_field(name=">kick", value="kicks selected member (only for mods)", inline=False)
        embed.add_field(name=">ban", value="bans selected member(only for mods)", inline=False)
        #embed.add_field(name=">_8ball", value="ask a question", inline=True)
        embed.add_field(name=">bot", value="displays jeggie's invite link", inline=False)
        embed.add_field(name=">server", value="displays main server invite link", inline=True)
        embed.add_field(name='>commands', value='displays this embed', inline=False)
        #embed.add_field(name='>poll', value='creates a poll (must include a question and 2 options,)', inline=False)
        #embed.add_field(name='>mute', value='mutes a targeted member', inline=False)
        #embed.add_field(name='>unmute', value='unmutes a muted member (must ping member you want to unmute)', inline=False)
        embed.add_field(name='>clear', value='deletes messages on a channel(must include amount or it will delete every message in the channel)', inline=False)
        embed.add_field(name='>slowmode', value='adds slowmode to chat (must include time as seconds)', inline=False)
        embed.add_field(name='>ball', value='answers questions with yes/no format', inline=False)
        await ctx.send(embed=embed)




#8ball command
@client.command()
async def ball(ctx, *, question):
  responses = [
  discord.Embed(title='It is certain.'),
  discord.Embed(title='It is decidedly so.'),
  discord.Embed(title='Without a doubt.'),
  discord.Embed(title='Yes - definitely.'),
  discord.Embed(title='You may rely on it.'),
  discord.Embed(title='Most likely.'),
  discord.Embed(title='Outlook good.'),
  discord.Embed(title='Yes.'),
  discord.Embed(title='Signs point to yes.'),
  discord.Embed(title='Reply hazy, try again.'),
  discord.Embed(title='Ask again later.'),
  discord.Embed(title='Better not tell you now.'),
  discord.Embed(title='Cannot predict now.'),
  discord.Embed(title='Concentrate and ask again.'),
  discord.Embed(title="Don't count on it."),
  discord.Embed(title='My reply is no.'),
  discord.Embed(title='My sources say no.'),
  discord.Embed(title='Outlook not very good.'),
  discord.Embed(title='Very doubtful.')
    ]
  responses = random.choice(responses)
  await ctx.send(content=f'Question: {question}\nAnswer:', embed=responses)


#poll command
@client.command()
async def poll(ctx, question, option1=None, option2=None):
  if option1==None and option2==None:
    await ctx.channel.purge(limit=1)
    message = await ctx.send(f"```New poll: \n{question}```\n**✅ = Yes**\n**❎ = #No**")
    await message.add_reaction('❎')
    await message.add_reaction('✅')
  elif option1==None:
    await ctx.channel.purge(limit=1)
    message = await ctx.send(f"```New poll: \n{question}```\n**✅ = {option1}#**\n**❎ = No**")
    await message.add_reaction('❎')
    await message.add_reaction('✅')
  elif option2==None:
    await ctx.channel.purge(limit=1)
    message = await ctx.send(f"```New poll: \n{question}```\n**✅ = Yes**\n**❎ = #{option2}**")
    await message.add_reaction('❎')
    await message.add_reaction('✅')
  else:
    await ctx.channel.purge(limit=1)
    message = await ctx.send(f"```New poll: \n{question}```\n**✅ = {option1}#**\n**❎ = {option2}**")
    await message.add_reaction('❎')
    await message.add_reaction('✅')








if __name__ == '__main__':
    import config
    client.run(config.token)
