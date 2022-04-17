import mysql.connector
from configparser import ConfigParser

#Read config.ini file
config_object = ConfigParser()
config_object.read("resources/config.ini")

#Load variables from config.ini file
dbinfo = config_object["MYSQLINFO"]
#Esta clase es la que realiza las interacciones con la base de datos

def existe(idCliente, idServer):
    mydb = mysql.connector.connect(host=dbinfo["host"],user=dbinfo["user"],password=dbinfo["password"],db=dbinfo["db"])
    c = mydb.cursor()

    #sql="SELECT * FROM ppt WHERE tag = '" + str(tag) + "' and idserver = '" + str(server) + "'"
    #c.execute("SELECT * FROM ppt WHERE tag = %s and server = %s", (tag, server))
    c.execute("SELECT * FROM ppt WHERE iduser = %s and idserver = %s", (idCliente, idServer))
    items = c.fetchall()

    #print(items)

    c.close()
    mydb.commit()
    mydb.close()

    if len(items) == 1:
        return True
    else:
        return False


def meterPuntos(idCliente, idServer, punt, user):
    if existe(idCliente, idServer):
        mydb = mysql.connector.connect(host=dbinfo["host"],user=dbinfo["user"],password=dbinfo["password"],db=dbinfo["db"])
        c = mydb.cursor()

        c.execute("SELECT puntos FROM ppt WHERE iduser = %s and idserver = %s", (idCliente, idServer))

        # conexion.commit()

        # print(c.fetchone()[0])

        puntuacion = int(c.fetchone()[0]) + int(punt)
        #print(puntuacion)  
        c.execute("UPDATE ppt SET puntos = %s WHERE iduser = %s and idserver = %s", (puntuacion, idCliente, idServer))

        mydb.commit()
        mydb.close()
    else:
        mydb = mysql.connector.connect(host=dbinfo["host"],user=dbinfo["user"],password=dbinfo["password"],db=dbinfo["db"])
        c = mydb.cursor()

        puntuacion = int(punt)
        #print(idCliente)
        #print(idServer)
        #print(puntuacion)
        #print(user)
        c.execute("INSERT INTO ppt VALUES (%s, %s, %s, %s)", (idCliente, idServer, puntuacion, user))

        mydb.commit()
        mydb.close()


def ranking(idServer):
    mydb = mysql.connector.connect(host=dbinfo["host"],user=dbinfo["user"],password=dbinfo["password"],db=dbinfo["db"])
    c = mydb.cursor()

    c.execute("SELECT iduser, puntos FROM ppt WHERE idserver = %s order by puntos desc LIMIT 10", (idServer,))

    items = c.fetchall()

    #print(items)

    c.close()
    mydb.commit()
    mydb.close()

    return items

def puntos(idCliente, idServer):
    mydb = mysql.connector.connect(host=dbinfo["host"],user=dbinfo["user"],password=dbinfo["password"],db=dbinfo["db"])
    c = mydb.cursor()

    c.execute("SELECT puntos FROM ppt WHERE iduser = %s AND idserver = %s", (idCliente, idServer,))

    items = c.fetchone()

    #print(items)

    c.close()
    mydb.commit()
    mydb.close()

    return items
