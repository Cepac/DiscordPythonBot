import discord
import random
from . import accionesPptDB
from Cogs.CogUtils import CogUtils


# Esta clase es la que procesa el juego de Piedra Papel Tijera

def sacarManoBot():
    return random.choice(['piedra', 'papel', 'tijera'])


async def existe(ctx):
    exi = accionesPptDB.existe(str(ctx.message.author), str(ctx.guild.id))
    await ctx.send(exi)


async def rankppt(self, ctx):
    lista = accionesPptDB.ranking(str(ctx.guild.id))

    embed = discord.Embed(
        title="Ranking del servidor",
        description="Puestos",
        color=discord.Color.blue()
    )
    
    lista_jugadores = list()
    i = 1

    embed=discord.Embed(title=f"Top 10 - Piedra/Papel/Tijera!", description="", color=0x5ce7ff)

    if lista != None:
        for jugador in lista:
            idusuario = self.bot.get_user(int(jugador[0]))
            #print(idusuario.name)
            #print(f"{idusuario.name}: {jugador[2]} puntos")
            #print(lista_jugadores)
            lista_jugadores.append(f"**{i}** - **{idusuario.name}**: {jugador[1]} puntos")
            i += 1

        lista_jugadores = '\n'.join(lista_jugadores)
        #print(lista_jugadores)
        
        embed.add_field(name="Jugadores", value=f"{lista_jugadores}", inline=False)
    else:
        embed.add_field(name="Jugadores", value="No hay jugadores en el top en este momento.", inline=False)
        embed.set_footer(text="Si se trata de un error, contacta con un Moderador.")

    #for i in range(len(lista)):
    #    embed.add_field(name=str(i + 1), value='**' + str(lista[i][0]) + '** - -' + (
    #        '-' * (20 - len(lista[i][0]))) + '- - Puntos: ' + str(lista[i][1]), inline=False)

    await ctx.send(embed=embed)

    # await ctx.send(lista)


async def puntosppt(ctx):
    puntos = accionesPptDB.puntos(str(ctx.author.id), str(ctx.guild.id))
    #print(f"puntos: {puntos}")
    embed = discord.Embed(
        title=f"{ctx.message.author.display_name}",
        description=f"Tienes {puntos[0]} puntos",
        color=discord.Color.blue()
    )
    #embed.add_field(title=f"{ctx.message.author.display_name}", description=f"Tienes {puntos[0]} puntos", color=0x5ce7ff)
    #embed.add_field(name=str(i + 1), value='Nombre: ' + str(lista[i][0]) + ' - -' + (
    #    '-' * (20 - len(lista[i][0]))) + '- - Puntos: ' + str(lista[i][1]), inline=False)

    await ctx.send(embed=embed)

async def lucha(ctx, miMano):
    if miMano in ["r", "rock", "piedra"]:
        miMano = "piedra"
    elif miMano in ["p", "paper", "papel"]:
        miMano = "papel"
    elif miMano in ["s", "scissors", "tijera"]:
        miMano = "tijera"
    else:
        await ctx.send("Opcion no válida, ni al piedra/papel/tijera sabes jugar?")
        return
    puntos = 0

    manoBot = sacarManoBot()
    salida = 'Yo elegí: {}'.format(manoBot)

    if miMano == manoBot:
        salida += '\n Empate.'
        color = discord.Color.gold()
    elif miMano == 'piedra':
        if manoBot == 'papel':
            salida += '\n -1 punto'
            color = discord.Color.red()
            puntos = -1
        else:
            salida += '\n +2 puntos'
            color = discord.Color.green()
            puntos = 2
    elif miMano == 'papel':
        if manoBot == 'tijera':
            salida += '\n -1 punto'
            color = discord.Color.red()
            puntos = -1
        else:
            salida += '\n +2 puntos'
            color = discord.Color.green()
            puntos = 2
    elif miMano == 'tijera':
        if manoBot == 'piedra':
            salida += '\n -1 punto'
            color = discord.Color.red()
            puntos = -1
        else:
            salida += '\n +2 puntos'
            color = discord.Color.green()
            puntos = 2
    title = 'Partida de ' + str(ctx.message.author.display_name)

    await ctx.send(embed=CogUtils.pptEmbed(salida,color,title))

    accionesPptDB.meterPuntos(str(ctx.message.author.id),
                              str(ctx.guild.id), puntos, str(ctx.message.author))
