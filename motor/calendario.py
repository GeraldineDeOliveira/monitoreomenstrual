import sqlite3

def consultar_por_fecha(fecha):
    miConexion=sqlite3.connect("monitoreo.sqlite3")
    miCursor=miConexion.cursor()

    miCursor.execute("SELECT * FROM periodos WHERE fecha_de_inicio=?", (fecha,))
    periodos=miCursor.fetchall()

    miCursor.execute("SELECT * FROM emociones WHERE fecha=?", (fecha,))
    emociones=miCursor.fetchall()

    miCursor.execute("SELECT * FROM flujo WHERE fecha=?", (fecha,))
    flujo=miCursor.fetchall()

    miCursor.execute("SELECT * FROM dolor WHERE fecha=?", (fecha,))
    dolor=miCursor.fetchall()

    miConexion.close()

    print(f"=== REGISTROS DEL {fecha} ===")
    if len(periodos)>0:
        print(f"Período: {periodos[0][1]}") #fecha_inicio
    else:
        print("Período: sin registro")

    if len(emociones)>0:
        print(f"Emoción: {emociones[0][2]}") #nivel de emoción
    else:
        print("Emoción: sin registro")

    if len(flujo)>0:
        print(f"Flujo: {flujo[0][2]}") #tipo de flujo
    else:
        print("Flujo: sin registro")

    if len(dolor)>0:
        print(f"Dolor: {dolor[0][2]} de 5") #nivel de dolor
    else:
        print("Dolor: sin registro")

def modificar_registro(tabla, fecha, nuevo_valor):
    miConexion=sqlite3.connect("monitoreo.sqlite3")
    miCursor=miConexion.cursor()

    if tabla=="periodos":
        sql_a_ejecutar="UPDATE periodos SET fecha_de_inicio=? WHERE fecha_de_inicio=?"
        miCursor.execute(sql_a_ejecutar,(nuevo_valor,fecha))
    elif tabla=="emociones":
        sql_a_ejecutar="UPDATE emociones SET emocion=? WHERE fecha=?"
        miCursor.execute(sql_a_ejecutar,(nuevo_valor,fecha))
    elif tabla=="flujo":
        sql_a_ejecutar="UPDATE flujo SET tipo=? WHERE fecha=?"
        miCursor.execute(sql_a_ejecutar,(nuevo_valor,fecha))
    elif tabla=="dolor":
        sql_a_ejecutar="UPDATE dolor SET nivel=? WHERE fecha=?"
        miCursor.execute(sql_a_ejecutar,(nuevo_valor,fecha))
    else:
        print("Tabla no válida.")
        return

    miConexion.commit() 
    miConexion.close()
    print(f"Registro de {tabla} modificado correctamente.")

def eliminar_registro(tabla, fecha):
    miConexion=sqlite3.connect("monitoreo.sqlite3")
    miCursor=miConexion.cursor()

    if tabla=="periodos":
        sql_a_ejecutar="DELETE FROM periodos WHERE fecha_de_inicio=?"
    elif tabla=="emociones":
        sql_a_ejecutar="DELETE FROM emociones WHERE fecha=?"
    elif tabla=="flujo":
        sql_a_ejecutar="DELETE FROM flujo WHERE fecha=?"
    elif tabla=="dolor":
        sql_a_ejecutar="DELETE FROM dolor WHERE fecha=?"
    else:
        print("Tabla no válida.")
        return

    miCursor.execute(sql_a_ejecutar,(fecha,))
    miConexion.commit()
    miConexion.close()
    print(f"Registro de {tabla} eliminado correctamente.")
    
def historial_completo():
    miConexion=sqlite3.connect("monitoreo.sqlite3")
    miCursor=miConexion.cursor()
    miCursor.execute("SELECT fecha_de_inicio FROM periodos ORDER BY fecha_de_inicio ASC")
    periodos=miCursor.fetchall()
    miConexion.close()

    print("=== HISTORIAL DE PERÍODOS ===")
    if len(periodos)==0:
        print("No hay períodos registrados todavía.")
    else:
        for periodo in periodos:
            print(f"- {periodo[0]}")