import tkinter as tk
from tkinter import messagebox
import pandas as pd
import random

# Cargar la base de datos
base_datos = pd.read_csv('base_datos.csv')

# Crear el diccionario de jugadores
jugadores = {cedula: {'Nombre': nombre, 'Dinero_inicial': dinero_inicial, 'Dinero_juego2': 0} for _, nombre, cedula, _, dinero_inicial, _, _, _, _, _ in base_datos.itertuples(index=False)}

# Crear listas para cédulas y nombres ordenadas por cédula
cedulas_ordenadas = sorted(jugadores.keys())
nombres_ordenados = [jugadores[cedula]['Nombre'] for cedula in cedulas_ordenadas]

num_jugador_actual = 0
rondas_totales = 10
ronda_actual = 1

def salir():
  # Actualizar la base de datos antes de salir
  for cedula in jugadores:
      base_datos.loc[base_datos['Cedula'] == int(cedula), 'Dinero_inicial'] = jugadores[cedula]['Dinero_inicial']
      base_datos.loc[base_datos['Cedula'] == int(cedula), 'Dinero_juego2'] = jugadores[cedula]['Dinero_juego2']
  base_datos.to_csv('base_datos.csv', index=False)
  root.destroy()
  
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
            jugadores[cedula]['Dinero_inicial'] -= apuesta_dinero
            jugadores[cedula]['Dinero_juego2'] += apuesta_dinero
            apuesta = int(apuesta_entry.get().strip())
            if 4 <= apuesta <= 18:
                jugadores[cedula]['Apuesta'] = apuesta
                resultado = lanzar_dados()
                verificar_apuestas(resultado)
                ronda_actual += 1
                if ronda_actual > rondas_totales:
                    finalizar_juego()
                else:
                    actualizar_labels()
            else:
                messagebox.showerror("Error", "La apuesta debe estar entre 4 y 18.")
        else:
            messagebox.showerror("Error", "La apuesta de dinero debe estar entre 40000 y 160000.")
    except ValueError:
        messagebox.showerror("Error", "Por favor, ingresa números válidos.")

def verificar_apuestas(resultado):
    tablero_text.delete(1.0, tk.END)
    ganadores = [cedula for cedula in jugadores if jugadores[cedula]['Apuesta'] == resultado]
    total_apuesta = sum(jugadores[cedula]['Apuesta'] for cedula in jugadores)

    if ganadores:
        monto_por_ganador = total_apuesta / len(ganadores)
        for ganador in ganadores:
            jugadores[ganador]['Dinero_inicial'] += monto_por_ganador
            jugadores[ganador]['Dinero_juego2'] -= monto_por_ganador
            tablero_text.insert(tk.END, f"{jugadores[ganador]['Nombre']} gana {monto_por_ganador} puntos en la ronda {ronda_actual}!\n")
    else:
        tablero_text.insert(tk.END, f"Nadie ha acertado en esta ronda, no hay ganadores.\n")

    mostrar_puntuaciones()

def jugar_nuevamente():
  global ronda_actual, num_jugador_actual
  ronda_actual = 1
  num_jugador_actual = 0
  for cedula in jugadores:
      jugadores[cedula]['Dinero_inicial'] = 5000  # Reinicia el dinero inicial a 5000
      jugadores[cedula]['Dinero_juego2'] = 0
  actualizar_labels()
  apuesta_entry_dinero.delete(0, tk.END)
  apuesta_entry.delete(0, tk.END)
  tablero_text.delete(1.0, tk.END)
  iniciar_juego()
  
def mostrar_puntuaciones():
    tablero_text.insert(tk.END, "\nTabla de Puntuaciones:\n")
    for cedula in jugadores:
        tablero_text.insert(tk.END, f"{jugadores[cedula]['Nombre']} - Dinero Inicial: {jugadores[cedula]['Dinero_inicial']} - Dinero Juego 2: {jugadores[cedula]['Dinero_juego2']}\n")

def finalizar_juego():
    tablero_text.insert(tk.END, "\nJuego finalizado. Puntuaciones finales:\n")
    mostrar_puntuaciones()
    apostar_button["state"] = tk.DISABLED

def actualizar_labels():
    apuesta_label.config(text=f"Apuesta - Ronda {ronda_actual}:")

# Crear la ventana principal
root = tk.Tk()
root.title("Sic Bo Game")
root.geometry("400x400")

# Etiquetas
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

salir_button = tkimport archivos_csv                 #Importa el archivo donde se trabaja la base de datos
from tkinter import *               #Importa la interfaz grafica
from tkinter import messagebox      
from PIL import ImageTk, Image      #Importa una libreria para abrir imágenes   
from juegos import spaceman

# Creación de la interfaz gráfica usando Tkinter
raiz = Tk() 
raiz.title("Casino")
raiz.geometry("1280x720")
frame = Frame(raiz, width=600, height=400)
frame.pack()
frame.place(anchor='center', relx=0.5, rely=0.5)
img = ImageTk.PhotoImage(Image.open("fondo-casino.jpg"))
label = Label(frame, image = img)
label.pack()
titulo = Label(raiz, text="CASINO UN", bg="dark blue", font="Inkfree 20 bold")
titulo.place(x = 550, y = 0)
#Inicializa la ventana y crea un frame, el fondo

nombre_e = Entry(raiz, width=20)
nombre_e.place(x = 550, y = 50)
nombre_e.insert(0, "Ingrese su nombre: ")

cedula_e = Entry(raiz, width=20)
cedula_e.place(x = 550, y = 90)
cedula_e.insert(1, "Ingrese su cédula: ")

edad_e =Entry(raiz, width=20)
edad_e.place(x = 550, y = 130)
edad_e.insert(2, "Ingrese su edad: ")

#Se piden datos al usuario y se recopilan

def click():
    if nombre_e.get() == "" or cedula_e.get() == "" or edad_e.get() == "":
        messagebox.showwarning("ERROR", "Por favor ingrese todos los datos correctamente")
    elif int(edad_e.get()) < 18:
        messagebox.showwarning("ERROR", "Debe ser mayor de edad para acceder")
    else:
        texto = archivos_csv.inicio_usuario(nombre_e.get(), cedula_e.get())
        if texto != "El día de hoy ya ha jugado, vuelva otro día":
            messagebox.showinfo("SUCCESS", texto)
            boton_iniciar_sesion.destroy()
            boton_listo.place(x = 550, y = 210)
        else:
            messagebox.showwarning("ERROR", texto)
            raiz.destroy()

def astronaut():
    global saldo
    saldo = spaceman.main(raiz, saldo)
    archivos_csv.modificar_csv("Dinero_astronaut", round(saldo-saldoi,2))
    informacion_usuario.config(text= f"Usuario: {cedula} \n Saldo: {round(saldo, 2)}")

def listo():
    global saldo  #Como después de que se inicialice sesión los juegos deben acceder al saldo, se declara como global.
    global cedula
    cedula = cedula_e.get()
    informacion_usuario.config(text= f"Usuario: {cedula} \n Saldo: {saldo}")
    informacion_usuario.place(x = 900, y = 20)
    nombre_e.destroy()
    edad_e.destroy()
    cedula_e.destroy()
    boton_listo.destroy()
    boton_astronaut = Button(raiz, text="Astronaut", command=astronaut, height=5, width=20)
    boton_astronaut.place(x = 550, y = 200)
    boton_mostrar_stats.place(x = 1000, y = 200)
    boton_mostrar_stats_juego.place(x = 1000, y = 300)

def salir():
    raiz.destroy()

def stats():
    archivos_csv.mostrar_estadisticas(cedula)

def stats_juego():
    archivos_csv.mostrar_ganancia_media_juego()

saldo = 5000    #Variable que va a ir cambiando en el menu
saldoi = 5000   #Todos los jugadores empiezan con 5000
informacion_usuario = Label(raiz, text="", bg="dark red", font="Inkfree 20 italic")
boton_iniciar_sesion = Button(raiz, text="Iniciar sesión", command=click)
boton_iniciar_sesion.place(x = 550, y = 170)
boton_listo = Button(raiz, text="Listo", command=listo)
boton_salir = Button(raiz, text="SALIR", command=salir, height=5, width=20, bg="red")
boton_mostrar_stats = Button(raiz, text="Ver tus \nestadísticas", command=stats, height=5, width=20)
boton_mostrar_stats_juego = Button(raiz, text="Ver el promedio\nde ganancia por juego", command=stats_juego, height=5, width=20)
boton_salir.place(x = 100, y = 100)
boton_listo.place(x = 550, y = 210) ##############################################

raiz.mainloop() #Hace que la ventana siga abierta.Button(root, text="Salir", command=salir)
salir_button.pack()

# Función para aplicar estilos de casino
def aplicar_estilos_casino():
    root.configure(bg='#1E2124')  # Color de fondo oscuro
    etiquetas = [dados_label, apuesta_label_dinero, apuesta_label]
    for etiqueta in etiquetas:
        etiqueta.configure(fg='white', bg='#1E2124')  # Texto blanco sobre fondo oscuro

    entradas = [apuesta_entry_dinero, apuesta_entry]
    for entrada in entradas:
        entrada.configure(fg='black', bg='white')  # Texto negro sobre fondo claro

    botones = [apostar_button, jugar_nuevamente_button, salir_button]
    for boton in botones:
        boton.configure(fg='white', bg='#4CAF50')  # Texto blanco sobre fondo verde

    tablero_text.configure(fg='white', bg='#1E2124')  # Texto blanco sobre fondo oscuro

# Aplicar estilos de casino
aplicar_estilos_casino()

# Iniciar el bucle principal
root.mainloop()
