import config as cf
import model
import time
import datetime
import csv
csv.field_size_limit(2147483647)

file = cf.file_dir + "base_datos.csv"
input_file = list(csv.DictReader(open(file, encoding="utf-8")))
#print(input_file)

def inicio_usuario(nombre, cedula):
    fecha = datetime.date.today()
    lista_cedulas = []
    for jugador in input_file:
        lista_cedulas.append(jugador["Cedula"])
        
    if cedula not in lista_cedulas:
        meter_jugador(nombre, cedula, fecha)
        return "Usuario añadido correctamente"
    else:
        return f"Usuario encontrado correctamente, bienvenido de vuelta, {nombre}"
    
    
def meter_jugador(nombre, cedula, fecha):
    editor = csv.writer(open(file, "a", encoding="utf-8"), delimiter=",")
    editor.writerow([nombre, cedula, fecha, 500, 0, 0, 0, 0, 0])

#inicio_usuario("Juan", "1014861797")
#inicio_usuario("Juan", "1014861796")