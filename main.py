from colorama import Fore, Back, Style
import random
import time
import json


iserp = [(0, 1), (0, 2), (0, 3)]
imanz = []
imatriz = []
jugadores = {}

for i in range(10):
    x = []
    for j in range(20):
        x.append(".")
    imatriz.append(x.copy())


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
    imanz.clear()
    print("## INICIO DEL JUEGO ##")
    time.sleep(0.5)
    x = input("Ingrese el nombre: ")
    correo = input("Ingrese su correo: ")
    jugadores[x] = {"puntaje": 0, "correo": correo}
    guardar_jugadores()
    nombre, puntaje = game(iserp.copy(), imatriz, x, 0, 0, 0)

    # Estas lineas son para ver si es necesario actualizar
    # En el caso que haya un jugador con puntajes mayores

    if puntaje > jugadores[nombre]["puntaje"]:
        jugadores[nombre]["puntaje"] = puntaje
        guardar_jugadores()
    return (nombre, puntaje)


def game(serp, mz, name, pj, sp, mov):
    if (sp == 1):
        print("Fin del juego")
        print("Puntaje total: " + str(pj))
        return (name, pj)
    k = (random.randint(0, 9), random.randint(0, 19))
    while mov % 20 == 0 and k in serp:
        k = (random.randint(0, 9), random.randint(0, 19))
    if mov % 20 == 0 or len(imanz) == 0:
        imanz.append(k)
    print("## SNAKE ##")
    print("Jugador: ", str(name))
    print("Puntaje: ", str(pj))
    for i in range(10):
        for j in range(20):
            if (i, j) in serp:
                print(Fore.BLUE+"-"+Style.RESET_ALL, end="")
                if (i, j) in imanz:
                    imanz.remove((i, j))
                    pj = pj+1
            elif (i, j) in imanz:
                print(Fore.RED+"@"+Style.RESET_ALL, end="")
            else:
                print(Fore.GREEN+mz[i][j]+Style.RESET_ALL, end="")
        print()
    if len(imanz) == 3:
        sp = 1
        print()
        print("Fin dej juego")
        print("Puntaje total: ", pj)

        return (name, pj)
    print("Arriba (w)")
    print("Abajo (s)")
    print("Izquierda (a)")
    print("Derecha (d)")
    print("Salir (exit)")
    ele = input("Seleccione un movimiento: ")
    while ele not in ["w", "s", "a", "d", "exit"]:
        ele = input("Seleccione nuevamente el movimiento: ")
    serp2 = serp.copy()
    new = (0, 0)
    last = serp2[len(serp2) - 1]
    if (ele == "w"):
        new = (last[0]-1, last[1])
        serp2.append(new)
    elif (ele == "s"):
        new = (last[0] + 1, last[1])
        serp2.append(new)
    elif (ele == "a"):
        new = (last[0], last[1]-1)
        serp2.append(new)
    elif (ele == "d"):
        new = (last[0], last[1]+1)
        serp2.append(new)
    elif (ele == "exit"):
        sp = 1
    if new not in imanz:
        serp2.pop(0)
    if new in imanz:
        pj = pj+1
        # lo pondremos para que funcione el mov%20
        imanz.remove(new)
        if (len(imanz) == 0):
            mov = -1
    for i in serp2:
        if i[0] < 0 or i[0] > 9:
            sp = 1
        if i[1] < 0 or i[1] > 19:
            sp = 1
        if len(set(serp2)) != pj+3:
            sp = 1
    return game(serp2, imatriz, name, pj, sp, mov+1)


def record():
    print("## RECORD ##")
    time.sleep(0.5)
    print()
    if not jugadores:
        print("Aun no hay historial de jugadores ni datos pasados :c")
        print()
    else:
        organizado = sorted(jugadores.items(),
                            key=lambda j: j[1]["puntaje"], reverse=True)
        for i, (name, datos) in enumerate(organizado, 1):
            print(
                f"{i}. {name} | Puntaje: {datos['puntaje']} | Correo: {datos['correo']}")
        print()
    x = input("Ingrese la opcion s para regresar al menu principal: ")
    while x != "s":
        x = input("Por favor, volver a ingresar la opcion s para regresar: ")
    return 0


def Pinicio():
    print("## MENU DE INICIO ##")
    time.sleep(0.5)
    print()
    print("1. Empezar el juego")
    time.sleep(0.5)
    print("2. Récord")
    time.sleep(0.5)
    print("3. Salir")
    time.sleep(0.5)
    print()
    print("####################")
    x = input("Seleccione una opcion: ")
    while x not in ["1", "2", "3"]:
        x = input("Por favor vuelva a selecionar la opcion: ")
    return x


def inicio():
    cargar_jugadores()
    x = Pinicio()
    x = int(x)
    if (x == 1):
        newgamers = prevgame()
        print(newgamers)
    elif (x == 2):
        record()
    elif (x == 3):
        print("Saliendo del juego...")
        time.sleep(1)
        print("Hasta luego!!!!")
        return 0
    return inicio()


inicio()
