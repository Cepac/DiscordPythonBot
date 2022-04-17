import asyncio
import csv
import os.path
from datetime import datetime
import os
import discord
from discord.errors import Forbidden


async def send_embed(ctx, embed):
    """
    Function that handles the sending of embeds
    -> Takes context and embed to send
    - tries to send embed in channel
    - tries to send normal message when that fails
    - tries to send embed private with information abot missing permissions
    If this all fails: https://youtu.be/dQw4w9WgXcQ

    Parameters
    ---------------
    ctx : discord.ext.commands.Context
    embed : discord.Embed
    """
    try:
        msg = await ctx.send(embed=embed)
        return msg
    except Forbidden:
        try:
            await ctx.send("Hey, seems like I can't send embeds. Please check my permissions :)")
        except Forbidden:
            await ctx.author.send(
                f"Hey, seems like I can't send any message in {ctx.channel.name} on {ctx.guild.name}\n"
                f"May you inform the server team about this issue? :slight_smile: ", embed=embed)


def getBotActivity(activityType, msg, url=None):
    """
    Returns the bot activity and its content based on the input parameters

    Parameters
    ---------------
    activityType : str
    msg : str
    url : str
    """
    if activityType.lower() == "playing":
        activity = discord.Game(name=msg)
    elif activityType.lower() == "streaming":
        activity = discord.Streaming(
            name=msg, url=url)
    elif activityType.lower() == "listening":
        activity = discord.Activity(
            type=discord.ActivityType.listening, name=msg)
    elif activityType.lower() == "watching":
        activity = discord.Activity(
            type=discord.ActivityType.watching, name=msg)
    else:
        activity = None

    return activity


def getBotStatus(status):
    """
    Returns the discord bot status

    Parameters
    ---------------
    status : str
    """
    if status.lower() == "dnd":
        return discord.Status.dnd
    elif status.lower() == "invisible":
        return discord.Status.invisible
    elif status.lower() == "idle":
        return discord.Status.idle
    else:
        return discord.Status.online


def errorEmbed(title):
    """
    Returns a discord.Embed with red color and the title specified

    Parameters
    -----------
    title : srt
    """
    return discord.Embed(
        title=title, color=0xff0000)


def successEmbed(title):
    """
    Returns a discord.Embed with green color and the title specified

    Parameters
    -----------
    title : srt
    """
    return discord.Embed(
        title=title, color=0x00ff00)


def infoEmbed(title):
    """
    Returns a discord.Embed with blue color and the title specified

    Parameters
    -----------
    title : srt
    """
    return discord.Embed(
        description=title, color=discord.Color.blue())


def pptEmbed(text, color, title):
    """
    Returns a discord.Embed with the color, footer and the title specified
    To prepare the ppt msg

    Parameters
    -----------
    title : srt
    color : str
    footer: str
    """
    embed = discord.Embed(
        description=text, color=color, title=title)
    # embed.set_footer(text=title)

    return embed


def removeMatches(theList, toDelete):
    """
    Returns a new list with with the items in theList that are not in toDelete

    Parameters
    -----------
    theList : list
    toDelete : list
    """
    newList = []
    for item in theList:
        if item not in toDelete:
            newList.append(item)
    return newList


def parsePossesive(name):
    """
    Returns the name + the posseive 's or '

    Parameters
    -----------
    name : srt
    """
    if name[-1].lower() == "s":
        return name + "\'"
    else:
        return name + "\'s"


def getFolderSize(start_path='.'):
    """
    Gets the total size of a folder in kB

    Parameters
    -----------
    start_path : str
    """
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)

    return total_size


def paginateEmbeds(pages):
    """
    Sets the footer of a list of embeds, paginating them

    Parameters
    ---------------
    pages : list
        list of embeds to paginate
    """
    numOfPages = len(pages)
    for x in range(1, numOfPages+1):
        pages[x-1].set_footer(text="Page {} of {}".format(x, numOfPages))
    return pages


async def showPages(ctx, bot, pages):
    """
    Sends a message with the first page of the list of embeds and changes it acording to the reactions in the message

    Parameters
    -----------
    ctx : discord.ext.commands.Context
    bot : discord.ext.commands.Bot
    pages : list
        list of discord.Embed
    """
    current = 0
    msg = await ctx.send(embed=pages[current])
    buttons = [u"\u23EA", u"\u25C0", u"\u25B6", u"\u23E9"]
    current = 0
    for button in buttons:
        await msg.add_reaction(button)

    while True:
        try:
            reaction, user = await bot.wait_for(
                "reaction_add",
                timeout=30,
                check=lambda reaction, user: user.id == ctx.author.id and
                reaction.emoji in buttons and reaction.message.id == msg.id
                # and isinstance(reaction.channel, discord.channel.DMChannel),
            )
        except asyncio.TimeoutError:
            await msg.clear_reactions()
            break
        else:
            previous_page = current
            if reaction.emoji == u"\u23EA":
                current = 0
                await reaction.remove(user)

            elif reaction.emoji == u"\u25C0":
                if current > 0:
                    current -= 1
                    await reaction.remove(user)

            elif reaction.emoji == u"\u25B6":
                if current < len(pages) - 1:
                    current += 1
                    await reaction.remove(user)
            elif reaction.emoji == u"\u23E9":
                current = len(pages) - 1
                await reaction.remove(user)
            # for button in buttons:
            # await msg.remove_reaction(button, ctx.author)
            if current != previous_page:
                await msg.edit(embed=pages[current])


async def elementsInPages(bot, ctx, elementEmbeds):
    if len(elementEmbeds) == 1:
        await send_embed(ctx, elementEmbeds[0])
        return
    reactions = {"⬛": "Non-element", "🟥": "Fire", "🟦": "Water",
                 "🟩": "Wind", "🟫": "Earth", "🟨": "Holy", "🟪": "Dark"}
    elements = {element.title: element for element in elementEmbeds}
    msgReactions = {}
    for emoji, element in reactions.items():
        if element in elements.keys():
            msgReactions[emoji] = element
    msg = await send_embed(ctx, elementEmbeds[0])

    for reaction in msgReactions.keys():
        await msg.add_reaction(reaction)
    cache_msg = discord.utils.get(bot.cached_messages, id=msg.id)
    emojistr = str(cache_msg.reactions[0])
    while True:
        try:
            reaction, user = await bot.wait_for(
                "reaction_add",
                timeout=25,
                check=lambda reaction, user: str(
                    reaction.emoji) in msgReactions.keys()
                and user.id != bot.user.id
                and reaction.message.id == msg.id
            )
        except asyncio.TimeoutError:
            embed = elements[msgReactions[emojistr]]
            embed.set_footer(text="Timed Out!")
            await msg.edit(embed=embed)
            await msg.clear_reactions()
        else:
            previous = emojistr
            emojistr = str(reaction.emoji)
            pg = msgReactions.get(element)
            await reaction.remove(user)
            if previous != emojistr:
                await msg.edit(embed=elements[msgReactions[emojistr]])


def addToLog(time, author, authorid, server, serverid, content):
    """
    Adds a command to the day's csv in logs/ 

    Parameters
    -----------
    time : datetime.datetime
    author : str
    authorid : int
    server : str
    serverid : int
    content : str
    """
    headers = ["Time (UTC)", "Author", "Author ID", "Server",
               "Server ID", "Message content"]
    time = datetime.utcnow().strftime('%Y-%m-%d')
    if os.path.isfile(f'logs/{time}.log.csv'):
        with open(f'logs/{time}.log.csv', 'a') as log:
            writer = csv.writer(log)
            writer.writerow(
                [datetime.utcnow().strftime('%Y-%m-%d-%H:%M:%S'), author, authorid, server, serverid, content])
    else:
        with open(f'logs/{time}.log.csv', 'w') as log:
            writer = csv.writer(log)
            writer.writerow(headers)
            writer.writerow(
                [datetime.utcnow().strftime('%Y-%m-%d-%H:%M:%S'), author, authorid, server, serverid, content])
