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
hashes posteriores al ultimo conocido, lo que se hará será crear una lista con múltiples hashes ya conocidos y por cada
sesión de juego seleccionar un número aleatorio y coger los siguientes hashes en la lista desde ese número
para simularlo.

En este caso, se hará el encriptamiento mediante un string que será modificado cada vez que se abra el juego por parte 
del usuario y se hasheará 200 veces para generar una lista de hashes, los cuales serán los game hashes que se darán al usuario
para que luego se puedan comprobar con la función de que efectivamente el juego no está manipulado.
"""
def get_result(game_hash, string_original):
    hm = hmac.new(str.encode(game_hash), b'', hashlib.sha256)
    hm.update(string_original.encode("utf-8"))
    h = hm.hexdigest()
    if (int(h, 16) % 33 == 0):
        return 1                    #Hay un 3% aproximadamente de que se pierda el juego instantáneamente
    h = int(h[:13], 16)
    e = 2**52
    return (((100 * e - h) / (e-h)) // 1) / 100.0 , hm.hexdigest()
        

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
    string_original = f"Mendivelso es {lista_variaciones_string_original[num_random]}" 
    hashi = hashear(string_original)
    lista_hashes = []
    i = 0
    while i < 10:
        hashi = hashear(hashi)
        lista_hashes.append(hashi)
        i+= 1
    lista_hashes = lista_hashes[::-1] #Reversa la lista
    return lista_hashes

print(main())
print(get_prev_game('07fb2d908e0e9041dd8f5425e64857c4aef957daf7d87bac40534c871b606db2'))
