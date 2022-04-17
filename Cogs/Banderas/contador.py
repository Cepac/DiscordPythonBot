import discord
import mysql.connector
from configparser import ConfigParser
from . import cdbandera
#import time
#import sys
#sys.path.append('/home/container/lib/asyncio')

import asyncio

#Read config.ini file
config_object = ConfigParser()
config_object.read("resources/config.ini")

#Load variables from config.ini file
dbinfo = config_object["MYSQLINFO"]

mydb = mysql.connector.connect(host=dbinfo["host"],user=dbinfo["user"],password=dbinfo["password"],db=dbinfo["db"], autocommit=True)

cursor = mydb.cursor()

async def editembed(ctx, seconds, bandera, msg, ans, puntos):
    newembed = discord.Embed(title=f"Adivina la bandera!", description="Tienes 10 segundos para acertar. **¡Que comience el juego!** ", color=0x5ce7ff)
    if seconds == 0:
        newembed.add_field(name="Resultado", value="**Se ha terminado el tiempo!** Más suerte la próxima vez.", inline=False)
        #cdbandera.newcd(0)
    elif seconds == 100:
        newembed.add_field(name="Resultado", value=f"¡<@{ans.author.id}> ha acertado! +{puntos} puntos", inline=False)
        #print(ans.author.id)
        #print(ans.guild.id)

        sql=f"UPDATE `banderas_ranking` SET `puntos` = `puntos` + {puntos} WHERE `iduser` = '" + str(ans.author.id) + "' AND `guild` = '" + str(ans.guild.id) + "';"
        #print(sql)
        cursor.execute(sql)
        
    newembed.set_thumbnail(url=f"https://www.worldometers.info/img/flags/{bandera[0]}-flag.gif")
    cdbandera.newcd(0)
    return await msg.edit(embed=newembed)

async def nuevocontador(self, ctx, msg, bandera):
    
    seconds = 10 
    #print("contador")
    def check(msg):
        return msg.channel == ctx.channel
    while seconds != 0 and seconds != 100:
        seconds -= 1
        try:
            ans = await self.bot.wait_for("message", timeout=10, check=check)
            #print(f"R U: {ans.content}")
            #print(f"R: {bandera[1]}")
            if ans.content == f"{bandera[1]}":
                puntos = 5
                seconds = 100
                sql="INSERT IGNORE INTO banderas_ranking VALUES ('" + str(ans.author.id) + "','" + str(ans.guild.id) + "', '0');"
                #print(sql)
                cursor.execute(sql)
                #print("bobo")
                await editembed(ctx, seconds, bandera, msg, ans, puntos)
                break
        except asyncio.TimeoutError:
            seconds=0
            await editembed(ctx, seconds, bandera, msg, ans="", puntos="")
            break