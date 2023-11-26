import tkinter as tk
from tkinter import messagebox
import pandas as pd
import random

# Cargar la base de datos
base_datos = pd.read_csv('base_datos.csv')

# Crear el diccionario de jugadores
jugadores = {cedula: {'Nombre': nombre, 'Dinero_inicial': dinero_inicial, 'Dinero_juego2': 0} for _, nombre, cedula, _, dinero_inicial, _, _, _, _, _, _ in base_datos.itertuples(index=False)}

# Crear listas para cédulas y nombres ordenadas por cédula
cedulas_ordenadas = sorted(jugadores.keys())
nombres_ordenados = [jugadores[cedula]['Nombre'] for cedula in cedulas_ordenadas]

num_jugador_actual = 0
rondas_totales = 10
ronda_actual = 1

def registrar_jugadores():
  global num_jugador_actual, num_jugadores_registrados, jugadores_registrados
  try:
      num_jugadores_registrados = int(num_players_entry.get())
      jugadores_registrados = []
      registrar_button.config(state=tk.NORMAL)  # Habilitar el botón de registrar jugador
      registrar_jugador()
  except ValueError:
      messagebox.showerror("Error", "Por favor, ingresa un número válido para el número de jugadores.")

def registrar_jugador():
  global num_jugador_actual, num_jugadores_registrados, jugadores_registrados
  if num_jugador_actual < num_jugadores_registrados:
      cedula = cedula_entry.get().strip()
      if cedula in jugadores and cedula not in jugadores_registrados:
          jugadores_registrados.append(cedula)
          num_jugador_actual += 1
          cedula_entry.delete(0, tk.END)
          if num_jugador_actual == num_jugadores_registrados:
              iniciar_juego()
          else:
              registrar_jugador()
      else:
          messagebox.showerror("Error", "La cédula no está registrada o ya se ha registrado. Inténtalo de nuevo.")
  else:
      messagebox.showinfo("Información", "Todos los jugadores han sido registrados.")
      registrar_button.config(state=tk.DISABLED)  # Inhabilitar el botón de registrar jugador cuando todos están registrados


def iniciar_juego():
    global num_jugador_actual
    actualizar_labels()
    apostar_button.config(state=tk.NORMAL)

def lanzar_dados():
    dados = [random.randint(1, 6) for _ in range(3)]
    resultado = sum(dados)
    dados_label.config(text=f"¡Resultado de los dados: {dados[0]}, {dados[1]}, {dados[2]}!")
    return resultado

def realizar_apuesta():
    global num_jugador_actual, ronda_actual
    try:
        apuesta_dinero = int(apuesta_entry_dinero.get().strip())
        if 40000 <= apuesta_dinero <= 160000:
            jugadores[jugadores_registrados[num_jugador_actual]]['Dinero_inicial'] -= apuesta_dinero
            jugadores[jugadores_registrados[num_jugador_actual]]['Dinero_juego2'] += apuesta_dinero
            apuesta = int(apuesta_entry.get().strip())
            if 4 <= apuesta <= 18:
                jugadores[jugadores_registrados[num_jugador_actual]]['Apuesta'] = apuesta
                num_jugador_actual += 1

                if num_jugador_actual == len(jugadores_registrados):
                    resultado = lanzar_dados()
                    verificar_apuestas(resultado)
                    num_jugador_actual = 0
                    ronda_actual += 1
                    if ronda_actual > rondas_totales:
                        finalizar_juego()
                    else:
                        actualizar_labels()
                else:
                    apuesta_entry.delete(0, tk.END)
                    apuesta_label.config(text=f"Apuesta {jugadores_registrados[num_jugador_actual]} - Ronda {ronda_actual}:")
            else:
                messagebox.showerror("Error", "La apuesta debe estar entre 4 y 18.")
        else:
            messagebox.showerror("Error", "La apuesta de dinero debe estar entre 40000 y 160000.")
    except ValueError:
        messagebox.showerror("Error", "Por favor, ingresa números válidos.")

def verificar_apuestas(resultado):
    tablero_text.delete(1.0, tk.END)
    ganadores = [cedula for cedula in jugadores_registrados if jugadores[cedula]['Apuesta'] == resultado]
    total_apuesta = sum(jugadores[cedula]['Apuesta'] for cedula in jugadores_registrados)

    if ganadores:
        monto_por_ganador = total_apuesta / len(ganadores)
        for ganador in ganadores:
            jugadores[ganador]['Dinero_inicial'] += monto_por_ganador
            jugadores[ganador]['Dinero_juego2'] -= monto_por_ganador
            tablero_text.insert(tk.END, f"{jugadores[ganador]['Nombre']} gana {monto_por_ganador} puntos en la ronda {ronda_actual}!\n")
    else:
        tablero_text.insert(tk.END, f"Nadie ha acertado en esta ronda, no hay ganadores.\n")

    mostrar_puntuaciones()

def mostrar_puntuaciones():
    tablero_text.insert(tk.END, "\nTabla de Puntuaciones:\n")
    for cedula in jugadores_registrados:
        tablero_text.insert(tk.END, f"{jugadores[cedula]['Nombre']} - Dinero Inicial: {jugadores[cedula]['Dinero_inicial']} - Dinero Juego 2: {jugadores[cedula]['Dinero_juego2']}\n")

def finalizar_juego():
    tablero_text.insert(tk.END, "\nJuego finalizado. Puntuaciones finales:\n")
    mostrar_puntuaciones()
    apostar_button["state"] = tk.DISABLED

def jugar_nuevamente():
    global ronda_actual, num_jugador_actual
    ronda_actual = 1
    num_jugador_actual = 0
    jugadores.clear()
    actualizar_labels()
    num_players_entry.delete(0, tk.END)
    apuesta_entry_dinero.delete(0, tk.END)
    apuesta_entry.delete(0, tk.END)
    tablero_text.delete(1.0, tk.END)
    iniciar_registro()

def salir():
    # Actualizar la base de datos antes de salir
    for cedula in jugadores:
        base_datos.loc[base_datos['Cedula'] == int(cedula), 'Dinero_inicial'] = jugadores[cedula]['Dinero_inicial']
        base_datos.loc[base_datos['Cedula'] == int(cedula), 'Dinero_juego2'] = jugadores[cedula]['Dinero_juego2']
    base_datos.to_csv('base_datos.csv', index=False)
    root.destroy()

def actualizar_labels():
    apuesta_label.config(text=f"Apuesta {jugadores_registrados[num_jugador_actual]} - Ronda {ronda_actual}:")

def iniciar_registro():
    global num_jugador_actual
    num_jugador_actual = 0
    num_players_entry.config(state=tk.NORMAL)
    cedula_entry.config(state=tk.NORMAL)
    registrar_button.config(state=tk.NORMAL)
    registrar_button.pack()

# Crear la ventana principal
root = tk.Tk()
root.title("Sic Bo Game")
root.geometry("400x400")

# Etiquetas
num_players_label = tk.Label(root, text="Ingrese el número de jugadores:")
num_players_label.pack()

num_players_entry = tk.Entry(root)
num_players_entry.pack()

# Registro de jugadores
cedula_label = tk.Label(root, text="Ingrese su cédula:")
cedula_label.pack()

cedula_entry = tk.Entry(root)
cedula_entry.pack()

registrar_button = tk.Button(root, text="Registrar Jugador", command=registrar_jugador, state=tk.DISABLED)
registrar_button.pack()

# Botones adicionales
iniciar_registro_button = tk.Button(root, text="Iniciar Registro", command=iniciar_registro)
iniciar_registro_button.pack()

iniciar_juego_button = tk.Button(root, text="Iniciar Juego", command=registrar_jugadores, state=tk.DISABLED)
iniciar_juego_button.pack()

dados_label = tk.Label(root, text="¡Bienvenido a Sic Bo!")
dados_label.pack()

apuesta_label_dinero = tk.Label(root, text="Ingrese su apuesta de dinero (40000-160000):")
apuesta_label_dinero.pack()

apuesta_entry_dinero = tk.Entry(root)
apuesta_entry_dinero.pack()

apuesta_label = tk.Label(root, text="")
apuesta_label.pack()

apuesta_entry = tk.Entry(root)
apuesta_entry.pack()

apostar_button = tk.Button(root, text="Apostar", command=realizar_apuesta, state=tk.DISABLED)
apostar_button.pack()

# Área de texto
tablero_text = tk.Text(root, height=5, width=40)
tablero_text.pack()

# Botones adicionales
jugar_nuevamente_button = tk.Button(root, text="Jugar Nuevamente", command=jugar_nuevamente)
jugar_nuevamente_button.pack()

salir_button = tk.Button(root, text="Salir", command=salir)
salir_button.pack()

# Iniciar el bucle principal
root.mainloop()
