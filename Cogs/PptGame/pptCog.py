import discord
from discord.ext import commands
from Cogs.CogUtils import CogUtils
from . import ppt


class PptCog(commands.Cog, name="Ppt"):
    """
    Game related commands
    """
    def getDescriptions():
        descriptions = {}
        descriptions["ppt"] = "Juega a piedra, papel y tijera conmigo ;)"
        descriptions["ranking"] = "Muestra el ranking del server en PPT"
        descriptions["puntos"] = "Muestra tus puntos en el ranking del server en PPT"
        return descriptions
    descriptions = getDescriptions()

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ppt', aliases=['rockpaperscissors'], brief="<rock/paper/scissors>", description=descriptions.get("ppt"), pass_context=True)
    async def rps(self, ctx, choice= ""):
        if choice == "":
            await ctx.send(embed=CogUtils.infoEmbed("Para jugar al piedra, papel o tijera debes usar el comando !rps <opcion> y en opcion escribir tu mano con la que vas a jugar ya sea piedra/papel/tijera, sencillo verdad?"))
        else:
            await ppt.lucha(ctx, choice)

    # Ranking de piedra papel tijera
    @commands.command(name='topppt', description=descriptions.get("ranking"), pass_context=True)
    async def ranking(self, ctx):
        await ppt.rankppt(self, ctx)
        
    # Puntos de piedra papel tijera
    @commands.command(name='puntosppt', description=descriptions.get("puntos"), pass_context=True)
    async def puntos(self, ctx):
        await ppt.puntosppt(ctx)

def setup(bot):
    bot.add_cog(PptCog(bot))