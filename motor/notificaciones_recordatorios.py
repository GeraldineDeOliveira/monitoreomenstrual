from datetime import datetime, timedelta
from predicciones import predecir #voy a usar el modilo de predicciones para las notificaciones

def dias_faltantes():
    proximo,periodo=predecir()
    if proximo is None:
        return None
    hoy=datetime.now().date()
    faltan=(proximo.date()-hoy).days
    return faltan
def verificar():
    faltan=dias_faltantes()
    if faltan is None:
        print("primero registra tu periodo para poder avisarte")
        return

    if faltan<=3:
        print(f"Recordatorio:tu periodo se acerca. faltan´{faltan} dias")
    elif faltan==1:
        print("el periodo puede llegarte mañana")
    elif faltan<0:
        print(f"tu periodo ya deberia haber empezado hace {abs(faltan)} dias")
        print("si no empezo, puede ser normal,pero si tienes dudas cpnsulta a tu medico")
    else:
        print(f"Te aviso cuadno falten 3 dias para tu periodo. aun faltan {faltan}")
