import discord
from discord.ext import commands

class Cerrar(commands.Cog, name="Cerrar"):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def cerrar(self, ctx):
        overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
        if overwrite.send_messages == False:
          await ctx.send("El canal ya está cerrado ¿sos bobo o qué?")
          print(f'{ctx.author.display_name} ha intentado cerrar el canal {ctx.channel.name}')
        else:
          embed=discord.Embed(title=f" ", description=" ", color=15158332)

          embed.add_field(name="Atención", value="Canal cerrado temporalmente.", inline=False)

          embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)

          await ctx.message.delete()
          await ctx.send(embed=embed)
          await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
          print(f'{ctx.author.display_name} ha cerrado el canal {ctx.channel.name}')

    @cerrar.error
    async def cerrar_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
          await ctx.send("Me la mamas (te falta rol)")

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def abrir(self, ctx):
        overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
        if overwrite.send_messages == True:
          await ctx.send("El canal ya está abierto ¿sos bobo o qué?")
          print(f'{ctx.author.display_name} ha intentado abrir el canal {ctx.channel.name}')
        else:        
          embed=discord.Embed(title=f" ", description=" ", color=3066993)

          embed.add_field(name="Atención", value="Canal reabierto correctamente.", inline=False)

          embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)

          await ctx.message.delete()
          await ctx.send(embed=embed)
          await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
          print(f'{ctx.author.display_name} ha abierto el canal {ctx.channel.name}')

    @abrir.error
    async def abrir_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
          await ctx.send("Me la mamas (te falta rol)")
          
    #Abrir/cerrar Mudae
    @commands.command()
    @commands.has_role(866343582323179521)
    async def cerrarmudae(self, ctx):
        if ctx.channel.id == 838090228291993620:
          overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
          if overwrite.send_messages == False:
              await ctx.send("El canal ya está cerrado ¿sos bobo o qué?")
              print(f'{ctx.author.display_name} ha intentado cerrar el canal {ctx.channel.name}')
          else:
              embed=discord.Embed(title=f" ", description=" ", color=15158332)

              embed.add_field(name="Atención", value="Canal cerrado temporalmente.", inline=False)

              embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)

              await ctx.message.delete()
              await ctx.send(embed=embed)
              await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
              print(f'{ctx.author.display_name} ha cerrado el canal {ctx.channel.name}')
        else:
              await ctx.send("Te has equivocado de canal bobo")

    @cerrarmudae.error
    async def cerrar_error(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            await ctx.send("Me la mamas (te falta rol)")

    @commands.command()
    @commands.has_role(866343582323179521)
    async def abrirmudae(self, ctx):
        if ctx.channel.id == 838090228291993620:
          overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
          if overwrite.send_messages == True:
              await ctx.send("El canal ya está abierto ¿sos bobo o qué?")
              print(f'{ctx.author.display_name} ha intentado abrir el canal {ctx.channel.name}')
          else:        
              embed=discord.Embed(title=f" ", description=" ", color=3066993)

              embed.add_field(name="Atención", value="Canal reabierto correctamente.", inline=False)

              embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)

              await ctx.message.delete()
              await ctx.send(embed=embed)
              await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
              print(f'{ctx.author.display_name} ha abierto el canal {ctx.channel.name}')
        else:
              await ctx.send("Te has equivocado de canal bobo")

    @abrirmudae.error
    async def abrir_error(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            await ctx.send("Me la mamas (te falta rol)")


def setup(bot):
    bot.add_cog(Cerrar(bot))