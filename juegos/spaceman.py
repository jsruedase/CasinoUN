import matplotlib.pyplot as plt
import numpy as np
import hashlib
import random
import string
import hmac

e = 2**52
salt = "0000000000000000000fa3b65e43e4240d71762a5bf397d5304b2596d116859c" #Hash del bloque de bitcoin #610546
print(len(salt))
game_hash = "2c3025c09639326bd284c258882a28dae1cb169c0fb0d925149baa34c3e06cd1" #ultimo hash del sitio web
game_hash2 = '100af1b49f5e9f87efc81f838bf9b1f5e38293e5b4cf6d0b366c004e0a8d9987' 
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
    return (((100 * e - h) / (e-h)) // 1) / 100.0


def get_prev_game(game_hash):
    m = hashlib.sha256()
    m.update(game_hash.encode("utf-8"))
    return m.hexdigest()

hash_game = game_hash
lista_hashes = []
while hash_game != game_hash2:
    lista_hashes.append(hash_game)
    hash_game = get_prev_game(hash_game)
    
print(len(lista_hashes))