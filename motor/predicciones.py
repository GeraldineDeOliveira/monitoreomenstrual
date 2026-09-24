import sqlite3 #esto es para la base de datos
from datetime import datetime,timedelta #estas son librerias para poder poner fechas
def obtener_periodos():
    miConexion=sqlite3.connect("monitoreo.sqlite3") #conecta la base de datos para poder mostrar las fechas ya registradas.
    miCursor=miConexion.cursor()
    miCursor.execute("SELECT fecha_de_inicio FROM periodos ORDER BY fecha_de_inicio ASC")

    periodos=miCursor.fetchall()
    miConexion.close()
    return periodos

def duracion():
    periodos=obtener_periodos()

    if len(periodos) < 2:
        return 28

    fechas=[]
    for p in periodos:
        fechas.append(datetime.strptime(p[0], "%Y-%m-%d"))

    diferencias=[]
    for i in range(len(fechas)-1):
        diferencias.append((fechas[i+1]-fechas[i]).days)

    promedio=sum(diferencias)//len(diferencias)
    return promedio


def mostrarprediccion():
    proximo,promedio=predecir()
    if proximo is None:
        print("Registra el inicio de tu ultimo periodo")
        return

    periodos=obtener_periodos()
    if len(periodos)<2:
        print("Primer periodo registrado")

    else:
        print("Registrado")

    print(f"Proximo periodo estimado:{proximo.strftime('%d/%m/%Y')}")

def predecir():
    periodos=obtener_periodos()
    if len(periodos)==0:
        return None, None

    ultimo=datetime.strptime(periodos[-1][0], "%Y-%m-%d")

    proximo=ultimo+timedelta(days=duracion())
    return proximo, duracion()

