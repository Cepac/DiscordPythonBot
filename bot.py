import os
import discord
from discord.ext import commands


import botVariables
from Cogs.Autoban import autoban
from Cogs.Cerrar import cerrar
from Cogs.Voicehub import voicehub
#from Cogs.Saludos import saludos
from Cogs.Banderas import banderas
from Cogs.CogUtils import CogUtils
from Cogs.PptGame import pptCog

intents = discord.Intents.default()
intents.members=True
activity = CogUtils.getBotActivity(
    botVariables.BOT_ACTIVITY_TYPE, botVariables.BOT_ACTIVITY_MSG, url=botVariables.BOT_STREAMING_URL)
status = CogUtils.getBotStatus(botVariables.BOT_STATUS)
bot = commands.Bot(command_prefix=commands.when_mentioned_or(botVariables.BOT_PREFIX),
                   activity=activity, status=status, help_command=None, intents=intents)
print("Iniciando el bot")

#intents = discord.Intents.default()
#intents.members=True
#bot = commands.Bot(command_prefix = "$", intents=intents, help_command=None)


@bot.event
async def on_ready():
    print('------')
    print('Sesion iniciada')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

    await bot.change_presence(activity=discord.Streaming(name='en Selis13', url='https://twitch.tv/selis13'))

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        msg = f"<@{ctx.author.id}> comando no reconocido."
        #await ctx.send("calla bobo")

# add Autoban bot
bot.add_cog(autoban.Autoban(bot))

# add Cerrar bot
bot.add_cog(cerrar.Cerrar(bot))

# add Voicehub bot
bot.add_cog(voicehub.Voicehub(bot))

# add Saludos bot
#bot.add_cog(saludos.Saludos(bot))

# add Banderas bot
bot.add_cog(banderas.Banderas(bot))

# add juego ppt
bot.add_cog(pptCog.PptCog(bot))

#bot.run(botVariables.BOT_TOKEN)
bot.run('')