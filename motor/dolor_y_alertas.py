import sqlite3
def registrar_dolor(fecha,nivel):
    miConexion=sqlite3.connect("monitoreo.sqlite3")
    miCursor=miConexion.cursor()

    sqlejecutar="INSERT INTO dolor(fecha,nivel) VALUES(?,?)"
    miCursor.execute(sqlejecutar,(fecha,nivel))
    miConexion.commit()
    miConexion.close()

    if nivel>=5:
        return "ALERTA:no es normal sentir un dolor tan intenso. Te recomendamos consultar un medico"
    else:
        return "Dolor registrado correctamente"

    def consultar_dolor(fecha):
        miConexion=sqlite3.connect("monitoreo.sqlite3")
        miCursor=miConexion.cursor()
        miCursor.execute("SELECT nivel FROM dolor WHERE fceha=?",(fecha,))
        resultado=miCursor.fetchall()
        miConexion.close()
        if len(resultado)==0:
            return f"No hay dolor registrado para {fecha}."
        else:
            return f"Dolor del {fecha}: nivel {resultado[0][0]} de 5."
        def escala_dolor():
            print("¿Cuanto dolor sientes hoy")
            print("0-Sin dolor")
            print("1-Molestia leve")
            print("2-Dolor leve")
            print("3-Dolor moderado")
            print("4-Dolor fuerte")
            print("5-Dolor insoportable")