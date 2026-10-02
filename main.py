import flet as ft
import sqlite3
import calendar as pycalendar
from datetime import datetime, timedelta

from motor import basededatos  # al importarlo, crea las tablas si no existen
from motor.dolor_y_alertas import registrar_dolor
from motor.emociones_flujo import registrar_Emociones, registrar_tipodeflujo
from motor.modulo_de_consejos import que_es, consejos_higiene, mitos, origen
from motor.predicciones import predecir
from motor.notificaciones_recordatorios import dias_faltantes
from plyer import notification #esto es para las notificaciones reales
try:
    from flet_android_notifications import FletAndroidNotifications #esto e para que no tire error si se ejecuta el de windows en android, si no va a explotar todo
except ImportError:
    FletAndroidNotifications = None

def enviar_notificacion_real(titulo, mensaje):
    try:
        notification.notify(title=titulo, message=mensaje, app_name="Monitoreo Menstrual", timeout=10)
    except Exception as ex:
        print("No se pudo enviar la notificación:", ex)

COLOR_FONDO = "#FFFFD5"
COLOR_BOTON = "#C6FFFF"
COLOR_CAJA_PROXIMO = "#F7C6D9"
COLOR_TITULO = "#B71C4A"
COLOR_ENCABEZADO_DIA = "#F7C6D9"

MESES_ES = ["", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio",
            "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
DIAS_ES = ["Dom", "Lun", "Mar", "Mier", "Juev", "Vier", "Sab"]

OPCIONES_EMOCION = [
    ("Muy triste", "icono_myt_triste.png", "Muy triste"),
    ("Triste", "icono_triste.png", "Triste"),
    ("Normal", "icono_normal.png", "Normal"),
    ("Contento", "icono_contento.png", "Contento"),
    ("Muy feliz", "muy_feliz.png", "Muy feliz"),
    ("Rabia", "icono_rabia.png", "Rabia"),
    ("Sensible", "icono_sensible.png", "Sensible"),
    ("Sin Control", "icono_sin_control.png", "Sin Control"),
]
OPCIONES_FLUJO = [
    ("Leve", "icono_flujoleve.png", "Leve"),
    ("Moderado", "icono_flujo_moderado.png", "Moderado"),
    ("Abundante", "icono_flujo_fuerte.png", "Abundante"),
]


def boton_app(texto, on_click, ancho=320):
    return ft.Button(
        texto,
        width=ancho,
        height=45,
        on_click=on_click,
        style=ft.ButtonStyle(
            bgcolor=COLOR_BOTON,
            color="#000000",
            shape=ft.RoundedRectangleBorder(radius=6),
        ),
    )


def boton_app_icono(texto, icono, on_click, ancho=320):
    return ft.Container(
        content=ft.Row(
            [
                ft.Image(src=icono, width=28, height=28),
                ft.Text(texto, size=14),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,
        ),
        width=ancho,
        height=45,
        bgcolor=COLOR_BOTON,
        border_radius=6,
        alignment=ft.Alignment.CENTER,
        on_click=on_click,
    )


def consultar_dia_texto(fecha):
    conexion = sqlite3.connect("monitoreo.sqlite3")
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM periodos WHERE fecha_de_inicio=?", (fecha,))
    periodo = cursor.fetchall()
    cursor.execute("SELECT emocion FROM emociones WHERE fecha=?", (fecha,))
    emocion = cursor.fetchall()
    cursor.execute("SELECT tipo FROM flujo WHERE fecha=?", (fecha,))
    flujo = cursor.fetchall()
    cursor.execute("SELECT nivel FROM dolor WHERE fecha=?", (fecha,))
    dolor = cursor.fetchall()
    conexion.close()

    lineas = [f"Registros del {fecha}:"]
    lineas.append(f"Período: {'sí, inicio registrado' if periodo else 'sin registro'}")
    lineas.append(f"Emoción: {emocion[0][0] if emocion else 'sin registro'}")
    lineas.append(f"Flujo: {flujo[0][0] if flujo else 'sin registro'}")
    lineas.append(f"Dolor: {dolor[0][0] if dolor else 'sin registro'}")
    return "\n".join(lineas)


def fechas_con_periodo():
    conexion = sqlite3.connect("monitoreo.sqlite3")
    cursor = conexion.cursor()
    cursor.execute("SELECT fecha_de_inicio FROM periodos")
    resultado = {fila[0] for fila in cursor.fetchall()}
    conexion.close()
    return resultado


def main(page: ft.Page):
    page.title = "Monitoreo Menstrual"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = COLOR_FONDO
    page.window.width = 400
    page.window.height = 700
    page.scroll = ft.ScrollMode.AUTO

    hoy = datetime.now()
    estado_calendario = {"mes": hoy.month, "anio": hoy.year}
    estado_emocion = {"fecha": hoy.strftime("%Y-%m-%d"), "emocion": None, "flujo": None}

    notificaciones_android = FletAndroidNotifications() if (page.platform == ft.PagePlatform.ANDROID and FletAndroidNotifications) else None

    async def notificar_android():
        if not notificaciones_android:
            return
        await notificaciones_android.request_permissions()
        proximo, _ = predecir()
        if proximo:
            fecha_aviso = proximo - timedelta(days=3)
            await notificaciones_android.schedule_notification(
                notification_id=1,
                title="Monitoreo Menstrual",
                body="Tu período se acerca, faltan 3 días.",
                scheduled_time=fecha_aviso,
            )

    #lam primera pantalla que va a mostrar el periodo estimado, registrar emociones y dolor
    def mostrar_inicio(e=None):
        page.clean()
        if page.navigation_bar:
            page.navigation_bar.selected_index = 0
        proximo, promedio = predecir()
        texto_proximo = proximo.strftime("%d/%m/%Y") if proximo else "--/--/----"

        page.add(
            ft.Column(
                [
                    ft.Image(src="icono_de_la_app.png", width=80, height=80),
                    ft.Text("Mi Monitoreo", size=24, weight=ft.FontWeight.BOLD, color=COLOR_TITULO),
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text("Próximo periodo estimado:", size=14),
                                ft.Text(texto_proximo, size=16, weight=ft.FontWeight.BOLD),
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        bgcolor=COLOR_CAJA_PROXIMO,
                        padding=10,
                        border_radius=8,
                        width=320,
                    ),
                    boton_app_icono("+ Registrar Síntomas o Dolor", "icono_dolor.png", mostrar_dolor),
                    boton_app_icono("Registrar inicio de período", "registrar_ciclo.png", mostrar_periodo),
                    ft.TextButton("Salir", on_click=lambda e: page.window.close()),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=12,
            )
        )

    #segunda pantalla que muestra el registro del periodo y deja registrar mas
    def mostrar_periodo(e=None):
        page.clean()
        campo_fecha = ft.TextField(
            label="Fecha (AAAA-MM-DD)", value=hoy.strftime("%Y-%m-%d"), width=250, read_only=True
        )
        mensaje = ft.Text("")

        def fecha_elegida(e):
            if e.control.value:
                campo_fecha.value = e.control.value.strftime("%Y-%m-%d")
                page.update()

        def abrir_calendario(e):
            page.show_dialog(
                ft.DatePicker(
                    on_change=fecha_elegida,
                    first_date=datetime(2020, 1, 1),
                    last_date=datetime(2035, 12, 31),
                )
            )

        def guardar(e):
            if not campo_fecha.value:
                mensaje.value = "Ingresá la fecha."
                page.update()
                return
            conexion = sqlite3.connect("monitoreo.sqlite3")
            cursor = conexion.cursor()
            cursor.execute("INSERT INTO periodos (fecha_de_inicio) VALUES (?)", (campo_fecha.value,))
            conexion.commit()
            conexion.close()
            mensaje.value = "Período registrado correctamente."
            page.update()

        page.add(
            ft.Text("Registrar inicio de período", size=20, weight=ft.FontWeight.BOLD),
            ft.Row(
                [campo_fecha, ft.IconButton(ft.Icons.CALENDAR_MONTH, on_click=abrir_calendario)],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            boton_app("Guardar", guardar, ancho=200),
            mensaje,
            boton_app("Volver al inicio", mostrar_inicio, ancho=200),
        )

    #pantallla que registra el dolor uwu
    def mostrar_dolor(e=None):
        page.clean()
        campo_fecha = ft.TextField(label="Fecha (AAAA-MM-DD)", value=hoy.strftime("%Y-%m-%d"), width=300)
        nivel_texto = ft.Text("Nivel seleccionado: 1")
        mensaje = ft.Text("")

        def cambio_slider(e):
            nivel_texto.value = f"Nivel seleccionado: {int(e.control.value)}"
            page.update()

        slider = ft.Slider(min=0, max=5, divisions=5, value=1, on_change=cambio_slider, width=300)

        def guardar(e):
            resultado = registrar_dolor(campo_fecha.value, int(slider.value))
            mensaje.value = resultado
            mensaje.color = "red" if "ALERTA" in resultado else "black"
            page.update()

        page.add(
            ft.Text("Registrar Dolor", size=20, weight=ft.FontWeight.BOLD),
            campo_fecha,
            ft.Text("Intensidad del dolor o cólicos (0 al 5):"),
            slider,
            nivel_texto,
            boton_app("Guardar registro", guardar, ancho=250),
            mensaje,
            boton_app("Volver al inicio", mostrar_inicio, ancho=250),
        )

    #registra las emociones, ya con los iconos que hice
    def mostrar_emocion(e=None):
        page.clean()
        if page.navigation_bar:
            page.navigation_bar.selected_index = 3
        mensaje = ft.Text("")

        def cambiar_fecha(e):
            estado_emocion["fecha"] = e.control.value

        campo_fecha = ft.TextField(
            label="Fecha (AAAA-MM-DD)", value=estado_emocion["fecha"], width=300, on_change=cambiar_fecha
        )

        def elegir_emocion(valor):
            def handler(e):
                estado_emocion["emocion"] = valor
                mostrar_emocion()
            return handler

        def elegir_flujo(valor):
            def handler(e):
                estado_emocion["flujo"] = valor
                mostrar_emocion()
            return handler

        def icono_seleccionable(valor, archivo, etiqueta, seleccionado, on_click):
            return ft.Container(
                content=ft.Column(
                    [
                        ft.Image(src=archivo, width=48, height=48),
                        ft.Text(etiqueta, size=11, text_align=ft.TextAlign.CENTER),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=2,
                ),
                padding=6,
                border_radius=10,
                bgcolor=COLOR_CAJA_PROXIMO if seleccionado else COLOR_BOTON,
                border=ft.Border.all(2, COLOR_TITULO) if seleccionado else None,
                on_click=on_click,
            )

        fila_emocion = ft.Row(
            [
                icono_seleccionable(v, archivo, etiqueta, estado_emocion["emocion"] == v, elegir_emocion(v))
                for v, archivo, etiqueta in OPCIONES_EMOCION
            ],
            spacing=8,
            scroll=ft.ScrollMode.AUTO,
            width=320,
        )

        fila_flujo = ft.Row(
            [
                icono_seleccionable(v, archivo, etiqueta, estado_emocion["flujo"] == v, elegir_flujo(v))
                for v, archivo, etiqueta in OPCIONES_FLUJO
            ],
            spacing=8,
            scroll=ft.ScrollMode.AUTO,
            width=320,
        )

        def guardar_emocion(e):
            if estado_emocion["emocion"] is None:
                mensaje.value = "Elegí un estado de ánimo."
            else:
                mensaje.value = registrar_Emociones(estado_emocion["fecha"], estado_emocion["emocion"])
            page.update()

        def guardar_flujo(e):
            if estado_emocion["flujo"] is None:
                mensaje.value = "Elegí un tipo de flujo."
            else:
                mensaje.value = registrar_tipodeflujo(estado_emocion["fecha"], estado_emocion["flujo"])
            page.update()

        page.add(
            ft.Text("Emoción y Flujo", size=20, weight=ft.FontWeight.BOLD),
            campo_fecha,
            ft.Text("Estado de ánimo:", size=14),
            fila_emocion,
            boton_app("Guardar emoción", guardar_emocion, ancho=250),
            ft.Text("Tipo de flujo:", size=14),
            fila_flujo,
            boton_app("Guardar flujo", guardar_flujo, ancho=250),
            mensaje,
            boton_app("Volver al inicio", mostrar_inicio, ancho=250),
        )

    #aca hay consejos, no se si debo añadir mas o poner una en inicio que diga dependiendo del dolor
    def mostrar_consejos(e=None):
        page.clean()
        if page.navigation_bar:
            page.navigation_bar.selected_index = 1
        texto_mostrado = ft.Text("", size=13, selectable=True)

        def mostrar(texto):
            def handler(e):
                if texto_mostrado.value == texto:
                    texto_mostrado.value = ""
                else:
                    texto_mostrado.value = texto
                page.update()
            return handler

        page.add(
            ft.Text("Guía de Consejos y Salud", size=20, weight=ft.FontWeight.BOLD),
            boton_app("¿Qué es la menstruación?", mostrar(que_es())),
            boton_app("Higiene menstrual", mostrar(consejos_higiene())),
            boton_app("¿Por qué duelen los cólicos?", mostrar(origen())),
            boton_app("Mitos y verdades", mostrar(mitos())),
            ft.Container(
                content=texto_mostrado,
                bgcolor="#FFFFFF",
                padding=10,
                border_radius=8,
                width=320,
            ),
            boton_app("Volver al inicio", mostrar_inicio),
        )

    #recordatorios, deberia de hacer una prueba de como funcionan
    def mostrar_recordatorio(e=None):
        page.clean()
        if page.navigation_bar:
            page.navigation_bar.selected_index = 4
        faltan = dias_faltantes()
        if faltan is None:
            texto = "Primero registrá tu período para poder avisarte."
        elif faltan < 0:
            texto = f"Tu período ya debería haber empezado hace {abs(faltan)} días.\nSi no empezó, puede ser normal, pero si tenés dudas consultá a tu médico."
        elif faltan <= 3:
            texto = f"Recordatorio: tu período se acerca. Faltan {faltan} días."
        else:
            texto = f"Te avisamos cuando falten 3 días para tu período. Aún faltan {faltan} días."

        page.add(
            ft.Text("Recordatorio", size=20, weight=ft.FontWeight.BOLD),
            ft.Container(
                content=ft.Text(texto, size=15),
                bgcolor=COLOR_CAJA_PROXIMO,
                padding=15,
                border_radius=8,
                width=320,
            ),
            boton_app(
                "Probar notificación",
                lambda e: enviar_notificacion_real("Prueba", "¡Esto es una notificación de prueba!"),
                ancho=250,
            ),
            boton_app("Volver al inicio", mostrar_inicio),
        )

    #este es el calendario interactivo aunque aun no ineractua mucho, creo que le voy a poner un icono en el dia que menstruas
    def mostrar_calendario(e=None):
        page.clean()
        if page.navigation_bar:
            page.navigation_bar.selected_index = 2
        mes = estado_calendario["mes"]
        anio = estado_calendario["anio"]
        marcados = fechas_con_periodo()

        def cambiar_mes(delta):
            def handler(e):
                nuevo_mes = estado_calendario["mes"] + delta
                nuevo_anio = estado_calendario["anio"]
                if nuevo_mes > 12:
                    nuevo_mes = 1
                    nuevo_anio += 1
                elif nuevo_mes < 1:
                    nuevo_mes = 12
                    nuevo_anio -= 1
                estado_calendario["mes"] = nuevo_mes
                estado_calendario["anio"] = nuevo_anio
                mostrar_calendario()
            return handler

        def ver_dia(fecha_str):
            def handler(e):
                dlg = ft.AlertDialog(
                    title=ft.Text(fecha_str),
                    content=ft.Text(consultar_dia_texto(fecha_str)),
                )
                page.show_dialog(dlg)
            return handler

        cal = pycalendar.Calendar(firstweekday=6)  #lasemana empieza en domingo
        semanas = cal.monthdayscalendar(anio, mes)

        filas = [
            ft.Row(
                [ft.Container(ft.Text(d, size=12, weight=ft.FontWeight.BOLD), bgcolor=COLOR_ENCABEZADO_DIA,
                               width=44, height=30, alignment=ft.Alignment.CENTER) for d in DIAS_ES],
                spacing=2,
            )
        ]

        for semana in semanas:
            celdas = []
            for dia in semana:
                if dia == 0:
                    celdas.append(ft.Container(width=44, height=40))
                else:
                    fecha_str = f"{anio:04d}-{mes:02d}-{dia:02d}"
                    tiene_periodo = fecha_str in marcados
                    es_hoy = fecha_str == hoy.strftime("%Y-%m-%d")
                    celdas.append(
                        ft.Container(
                            content=ft.Text(
                                str(dia), size=13,
                                weight=ft.FontWeight.BOLD if es_hoy else ft.FontWeight.NORMAL,
                            ),
                            bgcolor=COLOR_CAJA_PROXIMO if tiene_periodo else COLOR_BOTON,
                            width=44,
                            height=40,
                            alignment=ft.Alignment.CENTER,
                            border_radius=4,
                            border=ft.Border.all(2, COLOR_TITULO) if es_hoy else None,
                            on_click=ver_dia(fecha_str),
                        )
                    )
            filas.append(ft.Row(celdas, spacing=2))

        page.add(
            ft.Row(
                [
                    ft.IconButton(ft.Icons.ARROW_BACK, on_click=cambiar_mes(-1)),
                    ft.Text(f"{MESES_ES[mes]} {anio}", size=18, weight=ft.FontWeight.BOLD),
                    ft.IconButton(ft.Icons.ARROW_FORWARD, on_click=cambiar_mes(1)),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            *filas,
            boton_app("Volver al inicio", mostrar_inicio),
        )

    #la barra de abajo que tienen todas las aplicaiones
    pantallas_nav = [mostrar_inicio, mostrar_consejos, mostrar_calendario, mostrar_emocion, mostrar_recordatorio]

    def cambiar_pantalla(e):
        indice = e.control.selected_index
        pantallas_nav[indice]()

    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.Image(src="icono_de_la_app.png", width=26, height=26), label="Inicio"),
            ft.NavigationBarDestination(icon=ft.Image(src="icono_guia.png", width=26, height=26), label="Consejos"),
            ft.NavigationBarDestination(icon=ft.Image(src="icono_calendario.png", width=26, height=26), label="Calendario"),
            ft.NavigationBarDestination(icon=ft.Image(src="icono_normal.png", width=26, height=26), label="Emoción"),
            ft.NavigationBarDestination(icon=ft.Image(src="icono_notificacion.png", width=26, height=26), label="Recordatorio"),
        ],
        on_change=cambiar_pantalla,
        bgcolor=COLOR_BOTON,
    )

    if page.platform == ft.PagePlatform.ANDROID:
        page.run_task(notificar_android)
    else:
        faltan_inicio = dias_faltantes()
        if faltan_inicio is not None and 0 <= faltan_inicio <= 3:
            enviar_notificacion_real("Monitoreo Menstrual", f"Tu período se acerca, faltan {faltan_inicio} días.")

    mostrar_inicio()


ft.run(main, assets_dir="assets")