import matplotlib.pyplot as plt
import numpy as np
import hashlib
import random
import string
import hmac


"""
Para la creación de este juego se toma la implementación del juego Crash del casino virtual Roobet, el cual tiene
como modelo un sistema de encriptamiento usando un hash del bloque de bitcoin #610546 al cual se le hizo commit
antes de que fuese minado, creando los hashes de todos los juegos, lo que garantiza que el juego no es manipulado
manualmente dependiendo de lo que apuesten los jugadores, sino que sigue un orden inalterable. Como no se saben los
hashes posteriores al ultimo conocido, lo que se hará será crear una lista con múltiples hashes ya conocidos y por cada
sesión de juego seleccionar un número aleatorio y coger los siguientes hashes en la lista desde ese número
para simularlo.

"""
"""
from hashlib import blake2b
from hmac import compare_digest

SECRET_KEY = b'pseudorandomly generated server secret key'
AUTH_SIZE = 16

def sign(cookie):
    h = blake2b(digest_size=AUTH_SIZE, key=SECRET_KEY)
    h.update(cookie)
    return h.hexdigest().encode('utf-8')

def verify(cookie, sig):
    good_sig = sign(cookie)
    return compare_digest(good_sig, sig)

cookie = b'user-alice'
sig = sign(cookie)
print("{0},{1}".format(cookie.decode('utf-8'), sig))
user-alice,b'43b3c982cf697e0c5ab22172d1ca7421'
verify(cookie, sig)
True
verify(b'user-bob', sig)
False
verify(cookie, b'0102030405060708090a0b0c0d0e0f00')
False

"""
salt = "0000000000000000000fa3b65e43e4240d71762a5bf397d5304b2596d116859c" #Hash del bloque de bitcoin #610546
game_hash = "2c3025c09639326bd284c258882a28dae1cb169c0fb0d925149baa34c3e06cd1" #ultimo hash del sitio web 22-10
game_hash3 = "4469ecc88f39a0db18ac6823c81147ae6d083c7fbf43867d0d6c28d7b2aade4a" #ultimo hash del sitio web 23-10
primer_hash = "77b271fe12fca03c618f63dfb79d4105726ba9d4a25bb3f1964e435ccf9cb209"
print(len(game_hash))



def get_result(game_hash):
    hm = hmac.new(str.encode(game_hash), b'', hashlib.sha256)
    hm.update(salt.encode("utf-8"))
    h = hm.hexdigest()
    if (int(h, 16) % 33 == 0):
        return 1
    h = int(h[:13], 16)
    e = 2**52
    return (((100 * e - h) / (e-h)) // 1) / 100.0 , hm.hexdigest()


def get_prev_game(game_hash):
    m = hashlib.sha256()
    m.update(game_hash.encode("utf-8"))
    return m.hexdigest()

def crear_lista_hashes():
    hash_game = game_hash3
    lista_hashes = []
    while hash_game != game_hash:
        lista_hashes.append(hash_game)
        hash_game = get_prev_game(hash_game)


print(get_result("2c3025c09639326bd284c258882a28dae1cb169c0fb0d925149baa34c3e06cd1"))
print(get_prev_game("ae51878b60ee20546553002a841a6567c6b16d02231f8c894d3e94b0d494914a"))