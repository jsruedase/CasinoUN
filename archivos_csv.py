import config as cf
import time
import datetime
import csv
import pandas as pd
import matplotlib.pyplot as plt
csv.field_size_limit(2147483647)

file = cf.file_dir + "base_datos.csv"
input_file = list(csv.DictReader(open(file, encoding="utf-8")))

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
    num_registros = len(input_file)
    editor = csv.writer(open(file, "a", encoding="utf-8"), delimiter=",")
    editor.writerow([num_registros, nombre, cedula, fecha, 5000, 0, 0, 0, 0, 0])

def obtener_id():
    #print(len(input_file))
    return len(input_file)+1


def modificar_csv(columna, valor):
    num_registros = len(input_file)
    df = pd.read_csv(file) #usando la libreria pandas se crea un dataframe, una estructura de datos que organiza los datos en una matriz.
    df.loc[num_registros, columna] = valor #modifica la columna que entra por parámetro de la última fila
    df.to_csv(file, index=False)  

def calcular_din_final(id_jugador):
    dinero_astronaut = float(input_file[id_jugador-1]["Dinero_astronaut"])
    dinero_sicBO = float(input_file[id_jugador-1]["Dinero_SicBo"])
    dinero_21 = float(input_file[id_jugador-1]["Dinero_21"])
    dinero_final = round(5000 + dinero_astronaut + dinero_sicBO + dinero_21, 2)
    ganancia_neta = round(dinero_final - 5000,2)
    
    df = pd.read_csv(file)
    df.loc[id_jugador-1, "Dinero_final"] = dinero_final
    df.loc[id_jugador-1, "Ganancia_neta"] = ganancia_neta
    df.to_csv(file, index=False)  

def actualizar():
    num_registros = len(input_file)
    for i in range(1, num_registros+1):
        calcular_din_final(i)

def mostrar_estadisticas(cedula):
    df = pd.read_csv(file)  
    
    df['Cedula'] = df['Cedula'].astype(str).str.strip() #Ajustar a un formato para que se pueda filtrar el DataFrame
    cedula = str(cedula).strip()
    print(df)
    
    datos_filtrados = df.loc[df["Cedula"] == cedula] #Se filtran los datos del DataFrame por la cedula del jugador
    print(datos_filtrados)
    
    plt.figure(figsize=(10, 6))  # Ajusta el tamaño del gráfico 
    plt.plot(datos_filtrados['Fecha'], datos_filtrados['Ganancia_neta'], marker='o', linestyle='-')
    plt.title('Ganancia Neta a lo largo del Tiempo')
    plt.xlabel('Fecha')
    plt.ylabel('Ganancia Neta')
    plt.tight_layout()  # Ajustar el diseño del gráfico
    plt.show()

actualizar()