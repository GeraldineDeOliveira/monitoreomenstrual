import sqlite3 #esto es para la base de datos
from datetime import datetime,timedelta #estas son librerias para poder poner fechas
def obtener_periodos():
    miConexion=sqlite3.connect("monitoreo.sqlite3") #conecta la base de datos para poder mostrar las fechas ya registradas.
    miCursor=miConexion.cursor()
    miCursor.execute("SELECT DISTINCT fecha_de_inicio FROM periodos ORDER BY fecha_de_inicio ASC") #tuve que cambiar esta parte  pq si registro dos veces la misma fecha explota todo y me muestra que mi periodo debio empezar hace 23 dias :(

    periodos=miCursor.fetchall()
    miConexion.close()
    return periodos
#toma la fecha ingresada, si esla primera fecha,usa 28 dias para la duracion, si no cuenta para los dias para saber cuento dura tu ciclo,para eso toma la ultima fecha regidtrada y la nueva registrada, con eso sacaria los dias de duracion
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

    if len(diferencias) == 0:
        return 28

    promedio=sum(diferencias)//len(diferencias)
    return promedio


#toma los dias de duracion que estaan guardados en la variable
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
#esto es medio al pedo pq solo te dice que esta registrado y ya, te muestra la prediccion realizada
def predecir():
    periodos=obtener_periodos()
    if len(periodos)==0:
        return None, None

    ultimo=datetime.strptime(periodos[-1][0], "%Y-%m-%d")

    proximo=ultimo+timedelta(days=duracion())
    return proximo, duracion()
#esto es lo que predice
