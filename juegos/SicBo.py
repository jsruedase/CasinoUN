import tkinter as tk
from tkinter import messagebox
import pandas as pd
import random

def main(raiz_view, saldo,cedula):
    base_datos = pd.read_csv('base_datos.csv')
    jugadores = {cedula: {'Nombre': nombre, 'Dinero_inicial': dinero_inicial, 'Dinero_SicBo': 0} for _, nombre, cedula, _, dinero_inicial, _, _, _, _, _ in base_datos.itertuples(index=False)}

    ronda_actual = 1

    def lanzar_dados():
        dados = [random.randint(1, 6) for _ in range(3)]
        resultado = sum(dados)
        return resultado

    def realizar_apuesta():
        nonlocal saldo
        try:
            apuesta_dinero = float(apuesta_entry_dinero.get().strip())
            if 0 <= apuesta_dinero <= float(saldo):
                resultado = lanzar_dados()
                dados_label.config(text=f"¡Resultado de los dados: {resultado}!")
                apuesta = int(apuesta_entry.get().strip())
                if apuesta == resultado:
                    saldo += 3*apuesta_dinero
                    
                    messagebox.showinfo("¡Felicidades!", f"Has acertado en los dados. Triplicaste tu apuesta!")
                else:
                    saldo-= apuesta_dinero
                    
                    messagebox.showinfo("¡Lo siento!", "No has acertado en los dados. Pierdes tu apuesta.")
                mostrar_puntuaciones()
            else:
                messagebox.showerror("Error", "La apuesta de dinero debe estar entre 40000 y 160000.")
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingresa números válidos.")

    def mostrar_puntuaciones():
        nonlocal saldo
        saldo_label.config(text=f"Saldo: ${saldo}")

    def salir():
        nonlocal saldo
        root.destroy()

    root = tk.Toplevel(raiz_view)
    root.title("Sic Bo Game")
    root.geometry("400x400")

    dados_label = tk.Label(root, text="¡Bienvenido a Sic Bo!")
    dados_label.pack()

    saldo_label = tk.Label(root, text=f"Saldo: ${saldo}", font=("Arial", 12))
    saldo_label.pack()

    apuesta_label_dinero = tk.Label(root, text="Ingrese su apuesta de dinero:")
    apuesta_label_dinero.pack()

    apuesta_entry_dinero = tk.Entry(root)
    apuesta_entry_dinero.pack()

    apuesta_label = tk.Label(root, text="Apuesta en dados (1-18):")
    apuesta_label.pack()

    apuesta_entry = tk.Entry(root)
    apuesta_entry.pack()

    apostar_button = tk.Button(root, text="Apostar", command=realizar_apuesta)
    apostar_button.pack()

    salir_button = tk.Button(root, text="Salir", command=salir)
    salir_button.pack()

    def aplicar_estilos_casino():
        root.configure(bg='#1E2124')
        etiquetas = [dados_label, apuesta_label_dinero, apuesta_label]
        for etiqueta in etiquetas:
            etiqueta.configure(fg='white', bg='#1E2124')

        entradas = [apuesta_entry_dinero, apuesta_entry]
        for entrada in entradas:
            entrada.configure(fg='black', bg='white')

        botones = [apostar_button, salir_button]
        for boton in botones:
            boton.configure(fg='white', bg='#4CAF50')

    aplicar_estilos_casino()
    root.wait_window()
