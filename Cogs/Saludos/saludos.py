import discord
from discord.ext import commands

class Saludos(commands.Cog, name="Saludos"):
    
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        if "hola" in message.content.lower():
            await message.channel.send(f"Pa ti mi cola <@{message.author.id}>, te falta calle")

def setup(bot):
    bot.add_cog(Saludos(bot))