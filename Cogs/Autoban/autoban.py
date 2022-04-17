import discord
from discord.ext import commands
from datetime import datetime

class Autoban(commands.Cog, name="Autoban"):
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        created = member.created_at
        now = datetime.today()

        timein = now - created
        hours = divmod(timein.total_seconds(), 3600)

        print('Usuario: ', member)
        print('Creada: ', created)
        print('Tiempo creada: ', int(hours[0]), 'horas')

        if int(hours[0]) < 24:
          embed=discord.Embed(title=f" ", description=" ", color=15105570)

          embed.add_field(name="Mensaje", value=f"Has recibido un baneo automático en {member.guild.name} ", inline=False)
          embed.add_field(name="Apelación", value=f"Si consideras que el baneo ha sido un error envia un mensaje a SelisMods#5312", inline=False)

          embed.set_author(name=member, icon_url=member.avatar_url)

          file = discord.File("img/selischibi.png", filename="image.png")
          embed.set_thumbnail(url="attachment://image.png")

          await member.send(file=file, embed=embed)

          await member.ban(reason="Baneo automático", delete_message_days=7)
          print(f"{member} ha sido baneado automaticamente!")

    
    #@commands.Cog.listener()
    #async def on_message(self, message: discord.Message):
    #    if message.author.bot:
    #        return

    #    if "hello" in message.content.lower():
    #        await message.channel.send("Hi!")

def setup(bot):
    bot.add_cog(Autoban(bot))