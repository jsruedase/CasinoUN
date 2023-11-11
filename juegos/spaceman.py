import hashlib
import hmac         #Estas dos librerias sirven para encriptar usando hashes.
import random
import time
import random
from tkinter import *
from tkinter import messagebox      
from PIL import ImageTk, Image, ImageSequence #Este último es para hacer funcionar los gifs
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
                                                  #Tiene la propiedad de que la probabilidad de que salga un numero menor a n es de 1 - 1/n
        

def get_prev_game(game_hash):
    m = hashlib.sha256()
    m.update(game_hash.encode("utf-8"))
    return m.hexdigest()

def hashear(game_hash):
    hasheado = hashlib.sha256((game_hash).encode()).hexdigest()
    return hasheado

def crear_lista_hashes_y_results():

    #Creación de la lista de los hashes y de los juegos:
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
    
    return lista_resultados, lista_hashes

def main(raiz_view, saldo):

    lista_results, lista_hashes = crear_lista_hashes_y_results()
    #Creación de la interfaz gráfica del juego.
    raiz = Toplevel(raiz_view) #crea otra ventana, pero dando prioridad a la principal, que sería el menú.
    raiz.title("Astronaut")
    raiz.geometry("1280x720")
    frame = Frame(raiz, width=600, height=400)
    frame.pack()
    
    frame.place(anchor='center', relx=0.5, rely=0.5)
    img = ImageTk.PhotoImage(Image.open("space.jpg"))
    label = Label(frame, image = img)
    label.pack()
    
    img2 = ImageTk.PhotoImage(Image.open("astronauta_flotando.gif").resize((1280, 300)))
    label2 = Label(raiz, image=img2)
    label2.place(x=0, y=0)
    
    titulo = Label(raiz, text="Astronaut", bg="white", font="Inkfree 20 bold")
    titulo.place(x = 550, y = 680)
    informacion_usuario = Label(raiz, text= f"Saldo: {saldo}", bg="white", font="Inkfree 20 italic")
    informacion_usuario.place(x = 1100, y = 500)
    
    #Código que hace que muestra cuánto va el multiplicador y hace funcionar el gif del astronauta flotando mientras el multiplicador siga aumentando. Al finalizar muestra la explosión.
    global imagen
    imagen = Image.open("astronauta_flotando.gif")        
    label = Label(raiz)
    label.place(x= 0, y= 0)
    
    def mostrar_resultado():
        multiplicador = 1 
        contador_frame = 0
        multiplicador_label = Label(raiz, text= f"x{multiplicador}", bg="white", font="Inkfree 20 bold", width=5)
        multiplicador_label.place(x=580, y = 400)
        while multiplicador < lista_results[1]: #Mientras el multiplicador no supere el monto, el gif funciona y va aumentando 0.01
            frame = ImageSequence.Iterator(imagen)[contador_frame] #Se actualiza el frame dependiendo de la condición si sigue aumentando el multiplicador
            frame = imagen.resize((1280, 300)) #Se ajusta para que quede en la parte superior de la pantalla
            frame = ImageTk.PhotoImage(frame)
            label.config(image=frame)
            multiplicador += 0.01
            contador_frame+=1
            multiplicador = round(multiplicador, 2)
            multiplicador_label.config(text=f"x{multiplicador}")
            time.sleep(0.05)
            raiz.update() #Se actualiza tanto el frame del gif como el valor del multiplicador
        label2.place(x=0, y=0)
        raiz.update()
        
    mostrar_resultado()
    raiz.mainloop() 
