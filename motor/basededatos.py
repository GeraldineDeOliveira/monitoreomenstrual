import sqlite3 #importo la libreria
miConexion=sqlite3.connect("monitoreo.sqlite3")
print(miConexion)

miCursor=miConexion.cursor() #con eso de abajo se crean las tablas usando el sql o php no recuerdo cual era, pero nos lo enseñaron en cientifica
sqlejecutar= '''
    CREATE TABLE IF NOT EXISTS periodos(   
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha_de_inicio TEXT NOT NULL,
        duracion INTEGER
    )
'''
miCursor.execute(sqlejecutar)
sqlejecutar='''
    CREATE TABLE IF NOT EXISTS emociones(
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT NOT NULL,
            emocion TEXT
    )
'''
miCursor.execute(sqlejecutar)
sqlejecutar='''
    CREATE TABLE IF NOT EXISTS flujo(
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha TEXT NOT NULL,
        tipo TEXT
    )
'''
miCursor.execute(sqlejecutar)

sqlejecutar='''
    CREATE TABLE IF NOT EXISTS dolor(
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha TEXT NOT NULL,
        nivel INTEGER
    )
'''
miCursor.execute(sqlejecutar)

print("Tablas creadas :3") #esto avisa si las tablas se crearon

