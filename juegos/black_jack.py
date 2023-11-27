import tkinter as tk
from tkinter import messagebox
import random

baraja = [
    '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A',
    '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A',
    '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A',
    '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'
]

baraja_inicial = baraja.copy()

cartas_jugador = []
cartas_dealer = []
cartas_cpu1 = []
cartas_cpu2 = []
cartas_cpu3 = []
jugadores_plantados = []

cartas_ganadas = {'Jugador': 0, 'Dealer': 0, 'CPU1': 0, 'CPU2': 0, 'CPU3': 0}
rondas_ganadas = {'Jugador': 0, 'Dealer': 0, 'CPU1': 0, 'CPU2': 0, 'CPU3': 0}
numero_ronda = 1

# Crear la ventana principal
root = tk.Tk()
root.title("Blackjack Game")
root.geometry("800x600")
root.configure(bg="#001a4d")  # Color de fondo de neon

# Variables globales
baraja = baraja_inicial.copy()
cartas_jugador = []
cartas_dealer = []
cartas_cpu1 = []
cartas_cpu2 = []
cartas_cpu3 = []
cartas_ganadas = {'Jugador': 0, 'Dealer': 0, 'CPU1': 0, 'CPU2': 0, 'CPU3': 0}
rondas_ganadas = {'Jugador': 0, 'Dealer': 0, 'CPU1': 0, 'CPU2': 0, 'CPU3': 0}
numero_ronda = 1

# Interfaz gráfica
titulo_font = ("Arial", 20, "bold")
label_font = ("Arial", 14)
small_label_font = ("Arial", 10)
button_font = ("Arial", 12)

label_jugador = tk.Label(root, text="Cartas del Jugador:", font=titulo_font, bg="#001a4d", fg="white")
label_jugador.pack()

label_cartas_jugador = tk.Label(root, text="", font=label_font, bg="#001a4d", fg="white")
label_cartas_jugador.pack()

label_dealer = tk.Label(root, text="Cartas del Dealer:", font=titulo_font, bg="#001a4d", fg="white")
label_dealer.pack()

label_cartas_dealer = tk.Label(root, text="", font=label_font, bg="#001a4d", fg="white")
label_cartas_dealer.pack()

label_cpu1 = tk.Label(root, text="Cartas de CPU 1:", font=titulo_font, bg="#001a4d", fg="white")
label_cpu1.pack()

label_cartas_cpu1 = tk.Label(root, text="", font=label_font, bg="#001a4d", fg="white")
label_cartas_cpu1.pack()

label_cpu2 = tk.Label(root, text="Cartas de CPU 2:", font=titulo_font, bg="#001a4d", fg="white")
label_cpu2.pack()

label_cartas_cpu2 = tk.Label(root, text="", font=label_font, bg="#001a4d", fg="white")
label_cartas_cpu2.pack()

label_cpu3 = tk.Label(root, text="Cartas de CPU 3:", font=titulo_font, bg="#001a4d", fg="white")
label_cpu3.pack()

label_cartas_cpu3 = tk.Label(root, text="", font=label_font, bg="#001a4d", fg="white")
label_cartas_cpu3.pack()

# Etiqueta para el número de ronda
label_numero_ronda = tk.Label(root, text=f"Ronda: {numero_ronda}", font=label_font, bg="#001a4d", fg="white")
label_numero_ronda.place(x=10, y=10)  # Posición en la esquina superior izquierda

# Tabla de cartas ganadas
tabla_cartas_ganadas = tk.Text(root, height=10, width=30, font=small_label_font, bg="#001a4d", fg="white")
tabla_cartas_ganadas.pack(side=tk.RIGHT, padx=10, pady=10)

def nueva_partida():
    global baraja, cartas_jugador, cartas_dealer, cartas_cpu1, cartas_cpu2, cartas_cpu3, cartas_ganadas, rondas_ganadas, numero_ronda
    if numero_ronda == 30:
        messagebox.showinfo("Fin de juego", "Se han completado 30 rondas. Juego terminado.")
        root.quit()
    else:
        baraja = baraja_inicial.copy()
        cartas_jugador = []
        cartas_dealer = []
        cartas_cpu1 = []
        cartas_cpu2 = []
        cartas_cpu3 = []
        cartas_ganadas = {'Jugador': 0, 'Dealer': 0, 'CPU1': 0, 'CPU2': 0, 'CPU3': 0}
        rondas_ganadas = {'Jugador': 0, 'Dealer': 0, 'CPU1': 0, 'CPU2': 0, 'CPU3': 0}
        numero_ronda += 1
        habilitar_botones()
        repartir_cartas_iniciales()
        ocultar_cartas_cpu()  # Nueva línea para ocultar las cartas de los CPU
        actualizar_labels()

def habilitar_botones():
    button_pedir["state"] = "active"
    button_plantarse["state"] = "active"
    if numero_ronda < 30:
        button_nueva_partida["state"] = "disabled"
    else:
        button_nueva_partida["state"] = "active"

def repartir_cartas_iniciales():
    global cartas_jugador, cartas_dealer, cartas_cpu1, cartas_cpu2, cartas_cpu3

    cartas_jugador = [extraer_carta(), extraer_carta()]
    cartas_dealer = [extraer_carta(), extraer_carta()]
    cartas_cpu1 = [extraer_carta(), extraer_carta()]
    cartas_cpu2 = [extraer_carta(), extraer_carta()]
    cartas_cpu3 = [extraer_carta(), extraer_carta()]

    if sumar_cartas(cartas_jugador) == 21 or sumar_cartas(cartas_dealer) == 21 or sumar_cartas(cartas_cpu1) == 21 or sumar_cartas(cartas_cpu2) == 21 or sumar_cartas(cartas_cpu3) == 21:
        determinar_ganador_21()

def determinar_ganador_21():
    global cartas_jugador, cartas_dealer, cartas_cpu1, cartas_cpu2, cartas_cpu3
    resultado = []

    if sumar_cartas(cartas_jugador) == 21:
        resultado.append("¡Has ganado! ¡Tienes 21!")
        cartas_ganadas['Jugador'] += 1

    if sumar_cartas(cartas_dealer) == 21:
        resultado.append("El dealer ha ganado. Tiene 21.")
        cartas_ganadas['Dealer'] += 1

    if sumar_cartas(cartas_cpu1) == 21:
        resultado.append("CPU 1 ha ganado. Tiene 21.")
        cartas_ganadas['CPU1'] += 1

    if sumar_cartas(cartas_cpu2) == 21:
        resultado.append("CPU 2 ha ganado. Tiene 21.")
        cartas_ganadas['CPU2'] += 1

    if sumar_cartas(cartas_cpu3) == 21:
        resultado.append("CPU 3 ha ganado. Tiene 21.")
        cartas_ganadas['CPU3'] += 1

    if resultado:
        messagebox.showinfo("Resultado", "\n".join(resultado))
        nueva_partida()

def pedir_carta():
    if sumar_cartas(cartas_jugador) < 21:
        carta = extraer_carta()
        cartas_jugador.append(carta)
        actualizar_labels()

        if sumar_cartas(cartas_jugador) > 21:
            messagebox.showinfo("Resultado", "Has perdido. ¡Te pasaste de 21!")
            determinar_ganador_21()
        else:
            jugar_cpu()
          
def mostrar_perdedor(perdedor):
  messagebox.showinfo("Perdedor", f"{perdedor} ha perdido. ¡Se pasó de 21!")
  
def plantarse():
    while sumar_cartas(cartas_dealer) < 17:
        cartas_dealer.append(extraer_carta())
    while sumar_cartas(cartas_cpu1) < 17:
        cartas_cpu1.append(extraer_carta())
    while sumar_cartas(cartas_cpu2) < 17:
        cartas_cpu2.append(extraer_carta())
    while sumar_cartas(cartas_cpu3) < 17:
        cartas_cpu3.append(extraer_carta())

    actualizar_labels()

    determinar_ganador(sumar_cartas(cartas_jugador), "Jugador")
    determinar_ganador(sumar_cartas(cartas_dealer), "Dealer")
    determinar_ganador(sumar_cartas(cartas_cpu1), "CPU 1")
    determinar_ganador(sumar_cartas(cartas_cpu2), "CPU 2")
    determinar_ganador(sumar_cartas(cartas_cpu3), "CPU 3")

def jugar_cpu():
    while sumar_cartas(cartas_cpu1) < 17:
        cartas_cpu1.append(extraer_carta())
    while sumar_cartas(cartas_cpu2) < 17:
        cartas_cpu2.append(extraer_carta())
    while sumar_cartas(cartas_cpu3) < 17:
        cartas_cpu3.append(extraer_carta())

    actualizar_labels()

    determinar_ganador(sumar_cartas(cartas_cpu1), "CPU 1")
    determinar_ganador(sumar_cartas(cartas_cpu2), "CPU 2")
    determinar_ganador(sumar_cartas(cartas_cpu3), "CPU 3")

def extraer_carta():
    carta = random.choice(baraja)
    baraja.remove(carta)
    return carta

def actualizar_labels():
    label_cartas_jugador.config(text=", ".join(cartas_jugador))
    label_cartas_dealer.config(text=", ".join(cartas_dealer))
    label_cartas_cpu1.config(text=", ".join(cartas_cpu1))
    label_cartas_cpu2.config(text=", ".join(cartas_cpu2))
    label_cartas_cpu3.config(text=", ".join(cartas_cpu3))
    actualizar_tabla_cartas_ganadas()

def sumar_cartas(cartas):
    suma = 0
    ases = 0

    for carta in cartas:
        if carta.isdigit():
            suma += int(carta)
        elif carta in ['J', 'Q', 'K']:
            suma += 10
        elif carta == 'A':
            ases += 1

    for _ in range(ases):
        if suma + 11 <= 21:
            suma += 11
        else:
            suma += 1

    return suma

def mostrar_cartas_fin_ronda():
    mostrar_cartas_dealer()
    mostrar_cartas_cpu('CPU1', cartas_cpu1)
    mostrar_cartas_cpu('CPU2', cartas_cpu2)
    mostrar_cartas_cpu('CPU3', cartas_cpu3)

def mostrar_cartas_dealer():
    messagebox.showinfo("Cartas del Dealer", f"Cartas del Dealer: {', '.join(cartas_dealer)}")

def mostrar_cartas_cpu(cpu, cartas):
    messagebox.showinfo(f"Cartas de {cpu}", f"Cartas de {cpu}: {', '.join(cartas)}")

def ocultar_cartas_cpu():
    global cartas_cpu1, cartas_cpu2, cartas_cpu3
    cartas_cpu1 = ["?"] * 2
    cartas_cpu2 = ["?"] * 2
    cartas_cpu3 = ["?"] * 2

def plantarse():
  global jugadores_plantados
  if not jugadores_plantados:
      jugadores_plantados.append("Jugador")
      while sumar_cartas(cartas_dealer) < 17:
          cartas_dealer.append(extraer_carta())
      while sumar_cartas(cartas_cpu1) < 17:
          cartas_cpu1.append(extraer_carta())
      while sumar_cartas(cartas_cpu2) < 17:
          cartas_cpu2.append(extraer_carta())
      while sumar_cartas(cartas_cpu3) < 17:
          cartas_cpu3.append(extraer_carta())

      actualizar_labels()

      determinar_ganador_ronda()

def jugar_cpu_auto(cartas_cpu, label_cartas_cpu):
  while sumar_cartas(cartas_cpu) < 17:
      cartas_cpu.append(extraer_carta())
      actualizar_labels()
      root.update_idletasks()  # Actualizar la interfaz gráfica durante el bucle para mostrar los movimientos
      root.after(1000)  # Esperar 1 segundo entre cada movimiento de CPU (ajustable según sea necesario)


def jugar_round_auto():
  global jugadores_plantados
  if not jugadores_plantados:
      # Jugador
      jugadores_plantados.append("Jugador")
      pedir_carta()
      root.update_idletasks()
      root.after(1000)

      # Dealer
      jugadores_plantados.append("Dealer")
      jugar_cpu_auto(cartas_dealer, label_cartas_dealer)
      root.update_idletasks()
      root.after(1000)

      # CPU 1
      jugadores_plantados.append("CPU1")
      jugar_cpu_auto(cartas_cpu1, label_cartas_cpu1)
      root.update_idletasks()
      root.after(1000)

      # CPU 2
      jugadores_plantados.append("CPU2")
      jugar_cpu_auto(cartas_cpu2, label_cartas_cpu2)
      root.update_idletasks()
      root.after(1000)

      # CPU 3
      jugadores_plantados.append("CPU3")
      jugar_cpu_auto(cartas_cpu3, label_cartas_cpu3)
      root.update_idletasks()
      root.after(1000)

      determinar_ganador_ronda()


def determinar_ganador_ronda():
    global cartas_jugador, cartas_dealer, cartas_cpu1, cartas_cpu2, cartas_cpu3, cartas_ganadas, rondas_ganadas

    puntajes = {
        'Jugador': sumar_cartas(cartas_jugador),
        'Dealer': sumar_cartas(cartas_dealer),
        'CPU1': sumar_cartas(cartas_cpu1),
        'CPU2': sumar_cartas(cartas_cpu2),
        'CPU3': sumar_cartas(cartas_cpu3)
    }

    max_puntaje = max(puntajes.values())
    ganadores = [jugador for jugador, puntaje in puntajes.items() if puntaje == max_puntaje]

    if 'Jugador' in ganadores:
        mostrar_resultado_ronda('Jugador', len(cartas_dealer) + len(cartas_cpu1) + len(cartas_cpu2) + len(cartas_cpu3))
    elif ganadores:
        mostrar_resultado_ronda(ganadores[0], len(cartas_dealer) // 2 + len(cartas_cpu1) // 2 + len(cartas_cpu2) // 2 + len(cartas_cpu3) // 2)

def mostrar_ganadores(ganadores):
    messagebox.showinfo("Ganadores", f"Los ganadores de la ronda son: {', '.join(ganadores)}")

def mostrar_resultado_ronda(ganador, cartas_repartidas):
  global rondas_ganadas, cartas_ganadas

  if ganador == 'Jugador':
      messagebox.showinfo("Resultado de la Ronda", f"¡Has ganado la ronda! +1 punto")
      rondas_ganadas['Jugador'] += 1
  else:
      messagebox.showinfo("Resultado de la Ronda", f"{ganador} ha ganado la ronda. +1 punto")

  cartas_ganadas[ganador] += cartas_repartidas
  actualizar_tabla_cartas_ganadas()

  nueva_partida()  # Agregar esta línea para iniciar una nueva partida después de la ronda

# Modificación de la función nueva_partida()
def nueva_partida():
  global baraja, cartas_jugador, cartas_dealer, cartas_cpu1, cartas_cpu2, cartas_cpu3, cartas_ganadas, rondas_ganadas, numero_ronda, jugadores_plantados
  jugadores_plantados = []  # Restablecer la lista de jugadores plantados

def determinar_ganador(puntaje, jugador):
  global cartas_jugador, cartas_dealer, cartas_cpu1, cartas_cpu2, cartas_cpu3

  if puntaje > 21:
      mostrar_perdedor(jugador)
  elif puntaje == 21:
      mostrar_ganadores([jugador])
  elif jugador == 'Jugador' and sumar_cartas(cartas_jugador) == 21:
      mostrar_ganadores(['Jugador'])
  elif jugador == 'Dealer' and sumar_cartas(cartas_dealer) == 21:
      mostrar_ganadores(['Dealer'])
  elif jugador == 'CPU1' and sumar_cartas(cartas_cpu1) == 21:
      mostrar_ganadores(['CPU1'])
  elif jugador == 'CPU2' and sumar_cartas(cartas_cpu2) == 21:
      mostrar_ganadores(['CPU2'])
  elif jugador == 'CPU3' and sumar_cartas(cartas_cpu3) == 21:
      mostrar_ganadores(['CPU3'])

def actualizar_tabla_cartas_ganadas():
  global cartas_ganadas, rondas_ganadas
  tabla_cartas_ganadas.delete("1.0", tk.END)
  for jugador in cartas_ganadas:
      tabla_cartas_ganadas.insert(tk.END, f"{jugador}: Cartas Ganadas: {cartas_ganadas[jugador]}, Rondas Ganadas: {rondas_ganadas[jugador]}\n")

# Crear etiquetas y botones
button_pedir = tk.Button(root, text="Pedir Carta", font=button_font, command=pedir_carta, bg="#b2f7e2", fg="#333333")  # Verde pastel
button_pedir.pack(side=tk.LEFT, padx=10)

button_plantarse = tk.Button(root, text="Plantarse", font=button_font, command=plantarse, bg="#f7b2b2", fg="#333333")  # Rojo pastel
button_plantarse.pack(side=tk.LEFT, padx=10)

button_nueva_partida = tk.Button(root, text="Nueva Partida", font=button_font, command=nueva_partida, bg="#b2b2f7", fg="#333333")  # Azul pastel
button_nueva_partida.pack(side=tk.LEFT, padx=10)


jugar_round_auto()

# Resto del código
root.mainloop()
