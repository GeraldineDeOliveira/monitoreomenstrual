import sqlite3
def registrar_Emociones(fecha,emocion):
    miConexion=sqlite3.connect("monitoreo.sqlite3")
    miCursor=miConexion.cursor()

    sqlejecutar="INSERT INTO emociones (fecha, emocion) VALUES (?,?)"
    miCursor.execute(sqlejecutar,(fecha,emocion))

    miConexion.commit()
    miConexion.close()
    return "Emoción registrada correctamente."

def consultar_Emociones(fecha):
    miConexion=sqlite3.connect("monitoreo.sqlite3")
    miCursor=miConexion.cursor()
    miCursor.execute("SELECT emocion FROM emociones WHERE fecha=?", (fecha,))
    resultado=miCursor.fetchall()
    miConexion.close()

    if len(resultado)==0:
        return f"No hay emoción registrada para {fecha}."
    else:
        return f"Emoción del {fecha}: {resultado[0][0]} de 5"

def registrar_tipodeflujo(fecha, tipo):
    miConexion=sqlite3.connect("monitoreo.sqlite3")
    miCursor=miConexion.cursor()
    sql_a_ejecutar="INSERT INTO flujo (fecha, tipo) VALUES (?,?)"
    miCursor.execute(sql_a_ejecutar,(fecha,tipo))
    miConexion.commit()
    miConexion.close()
    return "Flujo registrado correctamente."


