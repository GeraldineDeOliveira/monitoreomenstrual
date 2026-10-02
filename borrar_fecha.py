import sqlite3

conexion = sqlite3.connect("monitoreo.sqlite3")
cursor = conexion.cursor()
cursor.execute("DELETE FROM periodos WHERE fecha_de_inicio = ?", ("2026-09-27",))
conexion.commit()
conexion.close()
print("Borrado correctamente.")

#no se si deberia borrar esto antes de entregar, es un modlulo por las dudas para borrar fechgas que pongo en las pruebas por accidentepy