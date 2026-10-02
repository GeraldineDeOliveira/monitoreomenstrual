import sqlite3
from dolor_y_alertas import registrar_dolor
from predicciones import mostrarprediccion
from notificaciones_recordatorios import verificar
from calendario import consultar_por_fecha, modificar_registro, historial_completo
from emociones_flujo import registrar_Emociones,registrar_tipodeflujo
from modulo_de_consejos import mostrar_consejos
#aca se importan todos los modulos y bibliotecas usadas
def mostrar_menu():
    print("=====================================")
    print("      MONITOREO MENSTRUAL")
    print("=====================================")
    print("1 - Registrar inicio de período")
    print("2 - Registrar dolor y ver alerta")
    print("3 - Ver consejos y educación")
    print("4 - Registrar emoción")
    print("5 - Registrar flujo")
    print("6 - Ver predicción del próximo período")
    print("7 - Ver recordatorio")
    print("8 - Consultar un día (calendario)")
    print("9 - Ver historial de períodos")
    print("10 - Modificar un registro")
    print("0 - Salir")
    print("=====================================")
#aca dependiendo el numero que ingresas te muestra uno de los temas
def registrar_periodo():
    fecha=input("Ingresá la fecha del inicio (AÑO-MES-DIA): ")
    miConexion=sqlite3.connect("monitoreo.sqlite3")
    miCursor=miConexion.cursor()
    sql_a_ejecutar="INSERT INTO periodos (fecha_de_inicio) VALUES (?)"
    miCursor.execute(sql_a_ejecutar,(fecha,))
    miConexion.commit() #confirmo la inserción - IMPORTANTE
    miConexion.close()
    print("Período registrado correctamente.")
#esto usa el predicciones.py, y registra el periodo en la base de datos
def registrar_dolor_menu():
    fecha=input("Ingresá la fecha (AÑO-MES-DIA): ")
    nivel=int(input("Elegí el nivel de dolor (0-5): "))
    resultado=registrar_dolor(fecha, nivel)
    print(resultado)
#esto registra el dolor, se guarda en  dolor_alertas.py y ese lo guarda en la base

def registrar_emocion_menu():
    fecha=input("Ingresá la fecha (AÑO-MES-DIA): ")
    print("¿Cómo te sentís hoy?")
    print("1 = Muy triste")
    print("2 = Triste")
    print("3 = Normal")
    print("4 = Contento")
    print("5 = Muy feliz")
    print("6 = Rabia")
    print("7 = Sensible")
    print("8 = Sin Control")
    emocion=int(input("Elegí una opción (1-5): "))
    resultado=registrar_Emociones(fecha, emocion)
    print(resultado)
#este registra las emociones
def registrar_flujo_menu():
    fecha=input("Ingresá la fecha (AÑO-MES-DIA): ")
    print("¿Cómo es tu flujo hoy?")
    print("1 = Leve")
    print("2 = Moderado")
    print("3 = Abundante")
    tipo=int(input("Elegí una opción (1-3): "))
    resultado=registrar_tipodeflujo(fecha, tipo)
    print(resultado)
#esto registra el flujo, enviandolo al modulo y del modulo a base, auqnue todas funcionan asi

def modificar_menu():
    print("¿Qué querés modificar?")
    print("1 - Período")
    print("2 - Emoción")
    print("3 - Flujo")
    print("4 - Dolor")
    opcion=input("Elegí una opción: ")
    fecha=input("Ingresá la fecha del registro (AÑO-MES-DIA): ")

    if opcion=="1":
        nuevo=input("Nueva fecha de inicio (AÑO-MES-DIA): ")
        modificar_registro("periodos", fecha, nuevo)
    elif opcion=="2":
        nuevo=input("Nueva emoción (1-5): ")
        modificar_registro("emociones", fecha, nuevo)
    elif opcion=="3":
        nuevo=input("Nuevo flujo (1-3): ")
        modificar_registro("flujo", fecha, nuevo)
    elif opcion=="4":
        nuevo=input("Nuevo nivel de dolor (0-5): ")
        modificar_registro("dolor", fecha, nuevo)
    else:
        print("Opción no válida.")

def main():
    while True:
        mostrar_menu()
        opcion=input("Elegí una opción: ")

        if opcion=="1":
            registrar_periodo()
        elif opcion=="2":
            registrar_dolor_menu()
        elif opcion=="3":
            fecha=input("Ingresá la fecha del dolor (AÑO-MES-DIA): ")
            miConexion=sqlite3.connect("monitoreo.sqlite3")
            miCursor=miConexion.cursor()
            miCursor.execute("SELECT nivel FROM dolor WHERE fecha=?", (fecha,))
            resultado=miCursor.fetchall()
            miConexion.close()
            if len(resultado)>0:
                mostrar_consejos(resultado[0][0])
            else:
                print("No hay dolor registrado para esa fecha. Registrá el dolor primero.")
        elif opcion=="4":
            registrar_emocion_menu()
        elif opcion=="5":
            registrar_flujo_menu()
        elif opcion=="6":
            mostrarprediccion()
        elif opcion=="7":
            verificar()
        elif opcion=="8":
            fecha=input("Ingresá la fecha a consultar (AÑO-MES-DIA): ")
            consultar_por_fecha(fecha)
        elif opcion=="9":
            historial_completo()
        elif opcion=="10":
            modificar_menu()
        elif opcion=="0":
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida. Intentá de nuevo.")

        input("Presioná Enter para continuar...")
#esta parte configura los numeros de arriba, de la priemra funcion para que te manden a la funcion que queres
if __name__ == "__main__":
    main()