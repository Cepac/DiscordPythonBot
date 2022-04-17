import discord
from discord.ext import commands
import mysql.connector
from configparser import ConfigParser

#Read config.ini file
config_object = ConfigParser()
config_object.read("resources/config.ini")

#Load variables from config.ini file
dbinfo = config_object["MYSQLINFO"]

mydb = mysql.connector.connect(host=dbinfo["host"],user=dbinfo["user"],password=dbinfo["password"],db=dbinfo["db"])

def execSQL(sql,param):
    cur = mydb.cursor()
    return cur.execute(sql,param)

class Voicehub(commands.Cog, name="Voicehub"):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before: discord.VoiceState, after: discord.VoiceState):
      cursor = mydb.cursor()

      sql="""SELECT creador, idcreador, idcanal FROM canal_temporal"""
      cursor.execute(sql)
      tempchans = cursor.fetchall()

      if before.channel != None and before.channel != after.channel and before.channel.id != 864060966974390292:
        #print(f'{member.display_name} ha salido de {before.channel}')
        userslist = before.channel.members
        #print(userslist)
        #print(f'Canal anterior: {before.channel.id}')

        for row in tempchans:
            #print(row)
            chanid = int(row[2])
            #print(chanid)
            #print(before.channel.id)
            #chan = discord.utils.get(member.guild.channels, name=before.channel)
            if before.channel.id == chanid and userslist == []:
                print(f'Canal temporal {before.channel} vacio')
                chan = discord.utils.get(member.guild.channels, id=before.channel.id)
                await chan.delete()
                
                sql = "DELETE FROM `canal_temporal` WHERE idcanal = '" + str(chanid) + "' "
                #param=(chanid,)
                #print(sql)
                #print(chanid)
                #print(sql)
                cursor.execute(sql)
                mydb.commit()

      if after.channel != None:
        if after.channel.id == 864060966974390292:
          channel = f'『🎮』Squad de {member.display_name}'

          hub = discord.utils.get(member.guild.channels, id=864060966974390292)
          #print(hub.position)
          #print(hub.category)
          chanpos = int(hub.position) + 1

          role_follower = discord.utils.get(member.guild.roles, id=695709727912493097)
          role_user = discord.utils.get(member.guild.roles, id=714751303250870331)
          perms = {
              member: discord.PermissionOverwrite(manage_channels=True),
              role_follower: discord.PermissionOverwrite(view_channel=True),
              role_user: discord.PermissionOverwrite(view_channel=False)
          }

          newchan = await member.guild.create_voice_channel(channel, overwrites=perms, position=chanpos, category=hub.category, user_limit=10)
          await member.move_to(newchan)
          
          #print(f'{member}: {member.id}')
          print(f'Se ha creado {newchan.name}')
          
          creator = member.name
          idmember = int(member.id)
          idchannel = int(newchan.id)

          #print(creator)
          #print(idmember)
          #print(idchannel)

          sql="""INSERT INTO canal_temporal (creador,idcreador,idcanal) values (%s,%s,%s)"""
          param=(creator,idmember,idchannel)
          execSQL(sql,param)
          
          mydb.commit()
        
def setup(bot):
    bot.add_cog(Voicehub(bot))
