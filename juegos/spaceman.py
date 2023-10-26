import matplotlib.pyplot as plt
import numpy as np
import hashlib
import random
import string
import hmac
import random

"""
Para la creación de este juego se toma la implementación del juego Crash del casino virtual Roobet, el cual tiene
como modelo un sistema de encriptamiento usando un hash del bloque de bitcoin #610546 al cual se le hizo commit
antes de que fuese minado, creando los hashes de todos los juegos, lo que garantiza que el juego no es manipulado
manualmente dependiendo de lo que apuesten los jugadores, sino que sigue un orden inalterable. Como no se saben los
hashes posteriores al ultimo conocido, ya que no se sabe la manera de encriptarlo, el jugador no puede predecir el resultado
de los próximos juegos.

En este caso, se hará el encriptamiento mediante un string que será modificado cada vez que se abra el juego por parte 
del usuario y se hasheará 100 veces para generar una lista de hashes, los cuales serán los game hashes que se darán al usuario
para que luego se puedan comprobar con la función de que efectivamente el juego no está manipulado.
"""
def get_result(game_hash, string_original):
    hm = hmac.new(str.encode(game_hash), b'', hashlib.sha256)
    hm.update(string_original.encode("utf-8"))
    h = hm.hexdigest()
    if (int(h, 16) % 33 == 0):
        return 1                                  #Hay un 3% aproximadamente de que se pierda el juego instantáneamente
    h = int(h[:13], 16)
    e = 2**52
    return (((100 * e - h) / (e-h)) // 1) / 100.0 #Funcion matemática con la que se obtiene el resultado de un juego a partir del hash. 
                                                  #Tiene la propiedad de que la probabilidad de que salga un numero mayor a n es de 1 - 1/n
        

def get_prev_game(game_hash):
    m = hashlib.sha256()
    m.update(game_hash.encode("utf-8"))
    return m.hexdigest()

def hashear(game_hash):
    hasheado = hashlib.sha256((game_hash).encode()).hexdigest()
    return hasheado

def main():
    lista_variaciones_string_original = ["god", "genio", "inteligente", "prodigio", "pro"]
    num_random = random.randint(0, len(lista_variaciones_string_original)-1) #Da un numero aleatorio de 0 al numero de variaciones
    string_original = f"Mendivelso es {lista_variaciones_string_original[num_random]}" #Se hacen variaciones para que los juegos no sean siempre iguales
    hashi = hashear(string_original)
    lista_hashes = []
    i = 0
    while i < 100:
        hashi = hashear(hashi)
        lista_hashes.append(hashi)
        i+= 1
    lista_hashes = lista_hashes[::-1] #Reversa la lista
    
    lista_resultados = []
    for juego in lista_hashes:
        lista_resultados.append(get_result(juego, string_original))
    return lista_resultados

print(main())
