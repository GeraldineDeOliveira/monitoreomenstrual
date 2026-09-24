import sqlite3 #importo la libreria
miConexion=sqlite3.connect("monitoreo.sqlite3")
print(miConexion)

miCursor=miConexion.cursor()
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
            emocion INTEGER
    )
'''
miCursor.execute(sqlejecutar)
sqlejecutar='''
    CREATE TABLE IF NOT EXISTS flujo(
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha TEXT NOT NULL,
        tipo INTEGER
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

print("Tablas creadas :3")

