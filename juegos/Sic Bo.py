import random
import tkinter as tk
from tkinter import messagebox

class SicBoGame:
    def __init__(self, master, num_players):
        self.master = master
        self.master.title("Sic Bo Game")
        self.num_players = num_players
        self.jugadores = {f"Jugador {i+1}": 0 for i in range(num_players)}
        
        self.dados_label = tk.Label(master, text="¡Bienvenido a Sic Bo!")
        self.dados_label.pack()

        self.apuesta_label = tk.Label(master, text="Ingresa tu apuesta:")
        self.apuesta_label.pack()

        self.apuesta_entry = tk.Entry(master)
        self.apuesta_entry.pack()

        self.apostar_button = tk.Button(master, text="Apostar", command=self.realizar_apuesta)
        self.apostar_button.pack()

        self.tablero_label = tk.Label(master, text="----- Sic Bo -----")
        self.tablero_label.pack()

        self.tablero_text = tk.Text(master, height=5, width=40)
        self.tablero_text.pack()

        self.jugar_nuevamente_button = tk.Button(master, text="Jugar Nuevamente", command=self.jugar_nuevamente)
        self.jugar_nuevamente_button.pack()

        self.salir_button = tk.Button(master, text="Salir", command=self.salir)
        self.salir_button.pack()

    def lanzar_dados(self):
        self.dados = [random.randint(1, 6) for _ in range(3)]
        resultado = sum(self.dados)
        self.dados_label.config(text=f"¡Resultado de los dados: {self.dados[0]}, {self.dados[1]}, {self.dados[2]}!")
        return resultado

    def realizar_apuesta(self):
        try:
            apuesta = int(self.apuesta_entry.get())
            if 4 <= apuesta <= 18:
                resultado = self.lanzar_dados()
                self.verificar_apuestas(apuesta, resultado)
            else:
                messagebox.showerror("Error", "La apuesta debe estar entre 4 y 18.")
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingresa un número válido.")

    def verificar_apuestas(self, apuesta, resultado):
        self.tablero_text.delete(1.0, tk.END)
        for jugador in self.jugadores:
            if apuesta == resultado:
                self.jugadores[jugador] += 1
            self.tablero_text.insert(tk.END, f"{jugador}: {self.jugadores[jugador]} puntos\n")
        self.apuesta_entry.delete(0, tk.END)

    def jugar_nuevamente(self):
        self.dados_label.config(text="¡Bienvenido a Sic Bo!")
        self.tablero_text.delete(1.0, tk.END)

    def salir(self):
        self.master.destroy()

def main():
    root = tk.Tk()
    num_players = int(input("Ingrese el número de jugadores: "))
    juego = SicBoGame(root, num_players)
    root.mainloop()

if __name__ == "__main__":
