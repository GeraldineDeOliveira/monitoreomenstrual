#Información basada en:
#- Organización Mundial de la Salud (OMS). Guía de higiene menstrual.
#- UNICEF. (2020). Guía de higiene menstrual para adolescentes: Educación y empoderamiento.
#- De Sanctis, V., et al. (2019). Primary dysmenorrhea in adolescents. Acta Bio-Medica.
def que_es():
    return ("La menstruación es el sangrado mensual que ocurre cuando tu cuerpo elimina "
            "el revestimiento del útero que no se usó. Es un proceso natural y normal "
            "que le pasa a las personas que menstrúan, y cada cuerpo es diferente.")

def consejos_higiene():
    return ("CONSEJOS DE HIGIENE:\n"
            "- Cambiá tu toalla, tampón o copa cada 4 a 6 horas.\n"
            "- Lavate las manos antes y después de cada cambio.\n"
            "- Usá agua y jabón suave para lavar la zona íntima (solo por fuera).\n"
            "- No uses jabones perfumados ni duchas vaginales: irritan la zona.\n"
            "- Si usás toalla, cambiála con frecuencia para evitar mal olor e infecciones.\n"
            "- Tirá los residuos en el tacho, nunca en el inodoro.\n"
            "- Tené siempre un kit de emergencia (toalla, ropa interior extra) en tu mochila.")

def mitos():
    """Aclara mitos comunes sobre la menstruación."""
    return ("MITOS Y VERDADES:\n"
            "- Mito: 'No podés bañarte durante el período.' → Falso: podés bañarte normal, incluso ayuda con los cólicos.\n"
            "- Mito: 'Si tocás agua fría, te corta el período.' → Falso: el agua fría no corta nada.\n"
            "- Mito: 'El período es sucio o impuro.' → Falso: es un proceso natural del cuerpo.\n"
            "- Mito: 'Todas las personas tienen ciclos de 28 días exactos.' → Falso: cada ciclo es diferente y puede variar.\n"
            "- Mito: 'No podés hacer ejercicio.' → Falso: moverte suave puede aliviar los cólicos.")
  
def consejos_dolor(nivel):

    if nivel<=1:
        return "¡Qué bueno que no te duele mucho! Seguí con tu día normal. Si querés, una botella de agua tibia en la panza ayuda a prevenir cólicos."
    elif nivel==2:
        return "Dolor leve: probá con una compresa tibia en la panza y descansá un ratito. Tomar agua y moverte suave también ayuda."
    elif nivel==3:
        return "Dolor moderado: una bolsa de agua caliente en la panza, descansar y tomar té de manzanilla pueden aliviarlo. Evitá comidas muy pesadas."
    elif nivel==4:
        return "Dolor fuerte: te recomendamos descansar, usar calor en la panza,tomar un analgésico que ya hayas usado antes y puedes poner tus piernas en tu panza en posicion fetal, apretando suavemente la zona. Si el dolor no baja, consultá a un médico."
    else:
        return "Dolor muy intenso: esto NO es normal. Te recomendamos fuertemente consultar a un médico. No tenés que aguantar el dolor en silencio."

def origen():
    """Explica de forma sencilla por qué duelen los cólicos."""
    return ("Los cólicos vienen de tu útero, que se contrae para eliminar el revestimiento. "
            "Esas contracciones pueden apretar los vasos sanguíneos y causar dolor. "
            "Es un proceso natural, pero si el dolor es muy fuerte, no es normal y hay que consultar a un médico.")

def mostrar_consejos(nivel):
    """Muestra todo junto: qué es, higiene, mitos, origen y consejos según el dolor."""
    print(que_es())
    print("")
    print(consejos_higiene())
    print("")
    print(mitos())
    print("")
    print(origen())
    print("")
    print(consejos_dolor(nivel))
