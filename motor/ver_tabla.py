import sqlite3
miConexion=sqlite3.connect("monitoreo.sqlite3")
miCursor=miConexion.cursor()
miCursor.execute("PRAGMA table_info(periodos)")
print(miCursor.fetchall())
miConexion.close()
#deberia borarr esto despues de usarlo? 