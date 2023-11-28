import tkinter as tk
from tkinter import messagebox
import random

def main(raiz_view, saldo):
    baraja = [
        '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A',
        '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A',
        '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A',
        '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'
    ]

    baraja_inicial = baraja.copy()

    # Crear la ventana principal
    root = tk.Toplevel(raiz_view)
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
    global cartas_ganadas
    cartas_ganadas = {'Jugador': 0, 'Dealer': 0, 'CPU1': 0, 'CPU2': 0, 'CPU3': 0}
    rondas_ganadas = {'Jugador': 0, 'Dealer': 0, 'CPU1': 0, 'CPU2': 0, 'CPU3': 0}
    global numero_ronda
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

    label_saldo = tk.Label(root, text=f"Saldo: {saldo}", font=label_font, bg="#001a4d", fg="white")
    label_saldo.place(x= 680, y= 10)

    # Etiqueta para el número de ronda
    label_numero_ronda = tk.Label(root, text=f"Ronda: {numero_ronda}", font=label_font, bg="#001a4d", fg="white")
    label_numero_ronda.place(x=10, y=10)  # Posición en la esquina superior izquierda

    # Tabla de cartas ganadas
    tabla_cartas_ganadas = tk.Text(root, height=10, width=30, font=small_label_font, bg="#001a4d", fg="white")
    tabla_cartas_ganadas.pack(side=tk.RIGHT, padx=10, pady=10)

    def nueva_partida():
        global baraja, cartas_jugador, cartas_dealer, cartas_cpu1, cartas_cpu2, cartas_cpu3, cartas_ganadas, rondas_ganadas, numero_ronda
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

        determinar_ganador_ronda()

    def jugar_cpu():
        while sumar_cartas(cartas_cpu1) < 17:
            cartas_cpu1.append(extraer_carta())
        while sumar_cartas(cartas_cpu2) < 17:
            cartas_cpu2.append(extraer_carta())
        while sumar_cartas(cartas_cpu3) < 17:
            cartas_cpu3.append(extraer_carta())

        actualizar_labels()

        determinar_ganador_ronda()

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

    def determinar_ganador_ronda():
        global cartas_jugador, cartas_dealer, cartas_cpu1, cartas_cpu2, cartas_cpu3, cartas_ganadas, rondas_ganadas, numero_ronda

        puntajes = {
            'Jugador': sumar_cartas(cartas_jugador),
            'Dealer': sumar_cartas(cartas_dealer),
            'CPU1': sumar_cartas(cartas_cpu1),
            'CPU2': sumar_cartas(cartas_cpu2),
            'CPU3': sumar_cartas(cartas_cpu3)
        }

        max_puntaje = max(puntajes.values())
        ganadores = [jugador for jugador, puntaje in puntajes.items() if puntaje == max_puntaje]

        mensaje_ganadores = f"Ganador(es) de la ronda {numero_ronda}: {', '.join(ganadores)}"
        messagebox.showinfo("Ganador de la ronda", mensaje_ganadores)

        for ganador in ganadores:
            cartas_ganadas[ganador] += 1
            rondas_ganadas[ganador] += 1

        actualizar_tabla_cartas_ganadas()
        actualizar_labels()

        if numero_ronda == 30:
            messagebox.showinfo("Fin de juego", "Se han completado 30 rondas. Juego terminado.")
            root.quit()
        else:
            messagebox.showinfo("Nueva ronda", "Comienza una nueva ronda.")
            nueva_partida()

    def actualizar_tabla_cartas_ganadas():
        tabla_cartas_ganadas.delete(1.0, tk.END)
        for jugador, cartas in cartas_ganadas.items():
            tabla_cartas_ganadas.insert(tk.END, f"{jugador}: {cartas}\n")

    # Crear botones
    button_pedir = tk.Button(root, text="Pedir Carta", font=button_font, command=pedir_carta, bg="#2ECC71")  # Verde
    button_pedir.pack(side=tk.LEFT, padx=10, pady=10)

    button_plantarse = tk.Button(root, text="Plantarse", font=button_font, command=plantarse, bg="#FF5733")  # Rojo menos brillante
    button_plantarse.pack(side=tk.LEFT, padx=10, pady=10)

    button_nueva_partida = tk.Button(root, text="Nueva Partida", font=button_font, command=nueva_partida, bg="#3498DB")  # Azul
    button_nueva_partida.pack(side=tk.LEFT, padx=10, pady=10)

    # Inhabilitar el botón de nueva partida al inicio
    button_nueva_partida["state"] = "disabled"

    # Iniciar el juego
    repartir_cartas_iniciales()
    ocultar_cartas_cpu()
    actualizar_labels()

    # Bucle principal de la interfaz gráfica
    root.mainloop()

