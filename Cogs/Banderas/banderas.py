import discord
from discord.ext import commands
import mysql.connector
from configparser import ConfigParser
from . import contador
from . import cdbandera


#Read config.ini file
config_object = ConfigParser()
config_object.read("resources/config.ini")

#Load variables from config.ini file
dbinfo = config_object["MYSQLINFO"]

mydb = mysql.connector.connect(host=dbinfo["host"],user=dbinfo["user"],password=dbinfo["password"],db=dbinfo["db"], autocommit= True)


class Banderas(commands.Cog, name="Banderas"):

    def __init__(self, bot):
        self.bot = bot
    
    global bandcd
    bandcd=cdbandera.cd
    
    @commands.command()
    @commands.cooldown(1, bandcd, commands.BucketType.user)
    async def bandera(self, ctx):
        #print(f"inicio: {cdbandera.cd}")
        do = cdbandera.cd

        if do == 10:
            msg = f"<@{ctx.author.id}> debes esperar a que termine la partida anterior antes de iniciar otra!"
            await ctx.send(msg)
        else:
            cdbandera.newcd(10)

            cursor = mydb.cursor()
            #print("bandera")

            sql="""SELECT * FROM banderas ORDER BY rand() LIMIT 1;"""
            cursor.execute(sql)
            bandera = cursor.fetchone()

            print(f"{bandera[0]} -> {bandera[1]}" )
            embed=discord.Embed(title=f"Adivina la bandera!", description="Tienes 10 segundos para acertar. **Que comience el juego!** ", color=0x5ce7ff)
            #embed.add_field(name="Tiempo", value="10 segundos", inline=False)
            embed.set_thumbnail(url=f"https://www.worldometers.info/img/flags/{bandera[0]}-flag.gif")
            msg = await ctx.send(embed=embed)
            
            await contador.nuevocontador(self, ctx, msg, bandera)
            cdbandera.newcd(0)
        
    
    @bandera.error
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            msg = f"<@{ctx.author.id}> debes esperar a que termine la partida anterior antes de iniciar otra!"
            await ctx.send(msg)

        if isinstance(error, commands.MissingPermissions):
          await ctx.send("No tengo banderas para ti :(")

    @commands.command()
    async def topband(self, ctx):
        cursor = mydb.cursor()
        #print(ctx.guild.id)
        
        sql="SELECT * FROM banderas_ranking WHERE guild = '" + str(ctx.guild.id) + "' ORDER BY puntos DESC LIMIT 10;"
        cursor.execute(sql)
        jugadores = cursor.fetchall()
        #print(jugadores)
        #print(self.bot.get_user(265137864533213185))
        lista_jugadores = list()
        i = 1

        embed=discord.Embed(title=f"Top 10 - Adivina la bandera!", description="", color=0x5ce7ff)

        if jugadores != None:
            for jugador in jugadores:
                idusuario = self.bot.get_user(int(jugador[0]))
                #print(f"{idusuario.name}: {jugador[2]} puntos")
                #print(lista_jugadores)
                lista_jugadores.append(f"**{i}** - **{idusuario.name}**: {jugador[2]} puntos")
                i += 1

            lista_jugadores = '\n'.join(lista_jugadores)
            #print(lista_jugadores)
            
            embed.add_field(name="Jugadores", value=f"{lista_jugadores}", inline=False)
        else:
            embed.add_field(name="Jugadores", value="No hay jugadores en el top en este momento.", inline=False)
            embed.set_footer(text="Si se trata de un error, contacta con un Moderador.")
        await ctx.send(embed=embed)

    @commands.command()
    async def puntosband(self, ctx):
        cursor = mydb.cursor()
        #print(ctx.guild.id)
        #print(ctx.message.author.id)

        sql="SELECT puntos FROM banderas_ranking WHERE iduser = '" + str(ctx.message.author.id) + "' AND guild = '" + str(ctx.guild.id) + "';"
        cursor.execute(sql)
        puntos = cursor.fetchone()
        #print(puntos)
        #print(self.bot.get_user(265137864533213185))
        lista_jugadores = list()
        i = 1

        if puntos != None:
            embed=discord.Embed(title=f"{ctx.message.author.display_name}", description=f"Tienes {puntos[0]} puntos", color=0x5ce7ff)
        else:
            embed=discord.Embed(title=f"{ctx.message.author.display_name}", description="No tienes puntos en el ranking. ¿A qué esperas para empezar a jugar?", color=0x5ce7ff)
            embed.set_footer(text="Si se trata de un error, contacta con un Moderador.")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def resetcd(self, ctx):
        print("reset")
        cdbandera.newcd(0)
        await ctx.send("Banderas reseteadas correctamente.")

    @resetcd.error
    async def cerrar_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
          await ctx.send("Me la mamas (te falta rol)")

def setup(bot):
    bot.add_cog(Banderas(bot))