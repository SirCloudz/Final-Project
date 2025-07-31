import random
import pygame
import time
import json
from colorama import Fore, Style
import os


iserp = [(0, 1), (0, 2), (0, 3)]
imanz = []
imatriz = []
jugadores = {}
mv = []
meses = {"Enero": "01", "Febrero": "02", "Marzo": "03", "Abril": "04", "Mayo": "05", "Junio": "06",
         "Julio": "07", "Agosto": "08", "Septiembre": "09", "Octubre": "10", "Noviembre": "11", "Diciembre": "12"}

for i in range(10):
    x = []
    for j in range(20):
        x.append(".")
    imatriz.append(x.copy())

pygame.mixer.init()
pygame.mixer.music.load("cancion.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)


def limpieza_pantalla():
    os.system('cls' if os.name == 'nt' else "clear")


def guardar_jugadores():
    with open("jugadores.json", "w") as f:
        json.dump(jugadores, f)


def cargar_jugadores():
    global jugadores
    try:
        with open("jugadores.json", "r") as f:
            jugadores = json.load(f)
    except FileNotFoundError:
        jugadores = {}


def prevgame():
    limpieza_pantalla()
    imanz.clear()
    print()
    print("## INICIO DEL JUEGO ##")
    time.sleep(0.5)
    print()
    x = input("Ingrese su nombre: ")
    correo = input("Ingrese su correo: ")
    while "@" not in correo or "utec.edu.pe" not in correo:
        correo = input("Asegúrese de que su correo incluya @ y dominio utec: ")
    correo_cortado = correo.split("@")
    while correo_cortado[0] == "":
        correo_cortado[0] = input(
            "Ingrese un nombre (Ya no es necesario el dominio): ")
    fecha = input("Ingrese la fecha (MM/AA): ")
    fecha_dividida = fecha.split("/")
    while len(fecha_dividida) != 2 or int(fecha_dividida[0]) >= 13 or int(fecha_dividida[0]) <= 0 or int(fecha_dividida[1]) < 0:
        fecha = input("Ingrese nuevamente la fecha (MM/AA): ")
        fecha_dividida = fecha.split("/")
    print("\n####################")
    nuevo_id = f"SY{len(jugadores)+1}"
    jugadores[x] = {
        'id': nuevo_id,
        'puntaje': 0,
        'correo': correo,
        'fecha': fecha,
        'movimientos': 0
    }

    guardar_jugadores()

    nombre, puntaje, movimientos = game(iserp.copy(), imatriz, x, 0, 0, 0)

    if puntaje > jugadores[nombre]["puntaje"]:
        jugadores[nombre]["puntaje"] = puntaje

    jugadores[nombre]["movimientos"] = mv.copy()
    mv.clear()
    print(f"\n✔️ Juego guardado exitosamente. Tu ID es: {nuevo_id}")
    input("Presiona ENTER para continuar...")
    return (nombre, puntaje)


def game(serp, mz, name, pj, sp, mov):
    limpieza_pantalla()
    print(f"Cantidad de movimientos: {mov}")

    if sp == 1:
        print("Fin del juego")
        print("Puntaje total: " + str(pj))
        return (name, pj, mov)
    k = (random.randint(0, 9), random.randint(0, 19))
    while mov % 20 == 0 and k in serp:
        k = (random.randint(0, 9), random.randint(0, 19))
    if mov % 20 == 0 or len(imanz) == 0:
        imanz.append(k)
    print("## SNAKE ##")
    print("Jugador: ", str(name))
    print("Puntaje: ", str(pj))
    # MATRIZ
    for i in range(10):
        for j in range(20):
            if (i, j) in serp:
                if (i, j) == serp[-1]:
                    print(Fore.BLUE + ">" + Style.RESET_ALL, end="")
                else:
                    print(Fore.BLUE + "-" + Style.RESET_ALL, end="")
            elif (i, j) in imanz:
                print(Fore.RED + "@" + Style.RESET_ALL, end="")
            else:
                print(Fore.GREEN + mz[i][j] + Style.RESET_ALL, end="")
        print()
    if len(imanz) == 3:
        print()
        print("Fin del juego")
        print("Puntaje total: ", pj)
        return (name, pj, mov)
    print("Arriba (w)")
    print("Abajo (s)")
    print("Izquierda (a)")
    print("Derecha (d)")
    print("Salir (exit)")
    ele = input("Seleccione un movimiento: ")
    while ele not in ["w", "s", "a", "d", "exit"]:
        ele = input("Seleccione nuevamente el movimiento: ")
    if ele != "exit":
        mv.append(ele)
    serp2 = serp.copy()
    new = (0, 0)
    last = serp2[len(serp2) - 1]
    if ele == "w":
        new = (9, last[1]) if last[0] == 0 else (last[0] - 1, last[1])
    elif ele == "s":
        new = ((last[0] + 1) % 10, last[1])
    elif ele == "a":
        new = (last[0], 19) if last[1] == 0 else (last[0], last[1] - 1)
    elif ele == "d":
        new = (last[0], (last[1] + 1) % 20)
    elif ele == "exit":
        sp = 1
    serp2.append(new)
    if new not in imanz:
        serp2.pop(0)
    if new in imanz:
        pj += 1
        imanz.remove(new)
        if len(imanz) == 0:
            mov = -1
    return game(serp2, imatriz, name, pj, sp, mov + 1)


def record():
    limpieza_pantalla()
    print("## MENU RECORD ##")
    time.sleep(0.5)
    print()
    print("1. Ranking")
    time.sleep(0.2)
    print("2. Ganadores del mes")
    time.sleep(0.2)
    print()
    print("############")
    eleccion = input("Seleccione una opcion: ")
    if eleccion == "1":
        ranking()
        return
    elif eleccion == "2":
        ganadores_mes()
        return
    elif eleccion.lower() == "s":
        return inicio()

    while eleccion not in ("1", "2", "s", "S"):
        eleccion = input("Seleccione una de las opciones disponibles: ")
        if eleccion == "1":
            ranking()
            return
        elif eleccion == "2":
            ganadores_mes()
            return
        elif eleccion.lower() == "s":
            return inicio()


def Pinicio():
    limpieza_pantalla()
    print("## MENU DE INICIO ##")
    time.sleep(0.2)
    print()
    print("1. Empezar el juego")
    time.sleep(0.2)
    print("2. Récord")
    time.sleep(0.2)
    print("3. Info de Jugadores")
    time.sleep(0.2)
    print("4. Salir")
    time.sleep(0.2)
    print()
    print("####################")
    print()
    x = input("Seleccione una opcion: ")
    while x not in ["1", "2", "3", "4"]:
        x = input("Por favor vuelva a selecionar la opcion: ")
    return x


def inicio():
    limpieza_pantalla()
    cargar_jugadores()
    x = Pinicio()
    x = int(x)
    if (x == 1):
        newgamers = prevgame()
        print(newgamers)
    elif (x == 2):
        record()
    elif (x == 3):
        info_jugadores()
    elif (x == 4):
        print("Saliendo del juego...")
        time.sleep(1)
        print("Hasta luego!!!!")
        pygame.mixer.music.stop()
        return 0
    return inicio()


def info_jugadores():
    limpieza_pantalla()
    cargar_jugadores()
    target = input("Ingrese el ID del jugador: ")
    print("### INFORMACIÓN DE JUGADORES ###\n")
    time.sleep(0.3)

    user = None
    for nombre, datos in jugadores.items():
        if datos["id"] == target:
            user = nombre
            jugador = datos
            break

    if user:
        movimientos = jugador.get("movimientos", [])
        if isinstance(movimientos, list):
            movimientos = ", ".join(movimientos)

        ancho_columna = 15
        mov_lines = [movimientos[i:i + ancho_columna]
                     for i in range(0, len(movimientos), ancho_columna)]
        print("---------+---------------+------------+------------------------------+------------------")
        print("| ID     | NOMBRE        | PUNTAJE    | CORREO                       | MOVIMIENTOS     |")
        print("---------+---------------+------------+------------------------------+------------------")
        print(
            f"| {jugador['id']:<6} | {user:<13} | {jugador['puntaje']:<10} | {jugador['correo']:<28} | {mov_lines[0]:<15} |")
        for linea in mov_lines[1:]:
            print(f"| {'':<6} | {'':<13} | {'':<10} | {'':<28} | {linea:<15} |")
        print("----------------------------------------------------------------------------------------")
    else:
        print("No hay datos de jugadores con ese ID :( ")

    print()
    time.sleep(0.3)
    x = input("Ingrese la letra 's' para regresar al menú principal: ")
    while x.lower() != "s":
        x = input("Por favor, vuelva a ingresar la letra 's' para regresar: ")
    return 0


def ganadores_mes():
    limpieza_pantalla()
    cargar_jugadores()
    print("### GANADORES DEL MES ###\n")
    time.sleep(0.3)
    if not jugadores:
        print("Aún no hay historial de jugadores ni datos pasados :c\n")
    else:
        ganadores = {}
        for names, j in jugadores.items():
            fecha = j["fecha"].split('/')[0]
            puntaje = j["puntaje"]
            if fecha not in ganadores or puntaje > ganadores[fecha][1]:
                ganadores[fecha] = (names, puntaje)

        for mes, i in meses.items():  # retorna enero 01
            if i in ganadores:
                print(f"{mes}:    {ganadores[i][0]}")
            else:
                if mes in ["Enero", "Marzo", "Mayo", "Julio", "Septiembre", "Noviembre"]:
                    print(f"{mes}:  Ninguno ")
                else:
                    print(f"{mes}:  No existe")
            time.sleep(0.1)
    print()
    input("Presione \"s\" para volver al menú: ")


def ranking():
    limpieza_pantalla()
    print("### LISTA DE GANADORES ###")
    time.sleep(0.5)
    print()
    if not jugadores:
        print("Aún no hay historial de jugadores ni datos pasados :c\n")
    else:
        organizado = sorted(jugadores.items(),
                            key=lambda j: j[1]["puntaje"], reverse=True)
        print("----------+---------------+--------------------")
        print("| ID      | NOMBRE        | PUNTOS            |")
        print("----------+---------------+--------------------")
        for i, (name, datos) in enumerate(organizado, 1):
            print(
                f"| {datos['id']:<8}|{name:<12}   | {datos['puntaje']} PUNTOS          |")
            time.sleep(0.2)
        print("----------+---------------+--------------------")
        print()
    print("######################")
    x = input("Ingrese la letra 's' para regresar al menú principal: ")
    while x.lower() != "s":
        x = input("Por favor, vuelva a ingresar la letra 's' para regresar: ")
    return 0


inicio()
