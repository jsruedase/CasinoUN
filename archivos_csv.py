import config as cf
import time
import datetime
import csv
import pandas as pd
csv.field_size_limit(2147483647)

file = cf.file_dir + "base_datos.csv"
input_file = list(csv.DictReader(open(file, encoding="utf-8")))
num_registros = len(input_file)

def inicio_usuario(nombre, cedula):
    fecha = datetime.date.today()
    fecha = fecha.strftime("%Y-%m-%d")
    lista_cedulas = []
    for jugador in input_file:
        lista_cedulas.append(jugador["Cedula"])
        
    if cedula not in lista_cedulas:
        meter_jugador(nombre, cedula, fecha)
        return "Usuario añadido correctamente"
    else:
        jugo = False
        for jugador in input_file:
            if jugador["Cedula"] == cedula and jugador["Fecha"] == fecha:
                jugo = True
                return "El día de hoy ya ha jugado, vuelva otro día"
        if not jugo:
            meter_jugador(nombre, cedula, fecha)
            return f"Usuario encontrado correctamente, bienvenido de vuelta, {nombre}"
    
    
def meter_jugador(nombre, cedula, fecha):
    editor = csv.writer(open(file, "a", encoding="utf-8"), delimiter=",")
    editor.writerow([num_registros + 1,nombre, cedula, fecha, 500, 0, 0, 0, 0, 0])

def obtener_saldo_inicial(cedula):
    for jugador in input_file:
        if jugador["Cedula"] == cedula:
            return jugador["Dinero_inicial"]

def modificar_csv(columna, valor, id_jugador):
    df = pd.read_csv(file) #usando la libreria pandas se crea un dataframe, una estructura de datos que organiza los datos en una matriz.

    df.loc[id_jugador, columna] = valor #modifica a la fila 
    
    df.to_csv(file, index=False)  
    