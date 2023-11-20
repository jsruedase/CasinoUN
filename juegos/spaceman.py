import hashlib
import hmac         #Estas dos librerias sirven para encriptar usando hashes.
import random
import time
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
    #Creación de la interfaz gráfica del juego, se crean los labels, botones y entries.
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
    
    informacion_usuario = Label(raiz, text=f"Saldo: ${saldo}", bg="white", font="Inkfree 20 italic")
    informacion_usuario.place(x = 1100, y = 500)
    
    celda_entry = Entry(raiz, width=20)
    celda_multiplicador = Entry(raiz, width=20)
    
    #Código que hace que funcione el gif de la explosion
    def gif_explosion():
        global img_explosion
        img_explosion = Image.open("explosión.gif")
        label_explosion = Label(raiz)
        label_explosion.place(x= 500, y= 50)

        for frame in ImageSequence.Iterator(img_explosion): #Se itera por el numero de frames que tiene el gif
            #frame = img.resize((1280, 300)) #Se ajusta para que quede en la parte superior de la pantalla
            frame = ImageTk.PhotoImage(frame)
            
            label_explosion.config(image=frame)
            time.sleep(0.05)
            raiz.update() #Se actualiza en cada iteracion del frame el fondo
        label_explosion.destroy()


 #Código que hace que muestra cuánto va el multiplicador y hace funcionar el gif del astronauta flotando mientras el multiplicador siga aumentando. Al finalizar muestra la explosión.
    def mostrar_resultado(pos):
        global imagen
        global multiplicador_global
        global isrunning
        global resultado 
        global boolean
        resultado = lista_results[pos]
        imagen = Image.open("astronauta_flotando.gif")        
        gif_label = Label(raiz)
        gif_label.place(x= 0, y= 0)
        previous_label = Label(raiz,  text=f"Anterior juego: \n x{resultado}", bg="white", font="Inkfree 20 bold")
        multiplicador = 0
        contador_frame = 0
        multiplicador_label = Label(raiz, text= f"x{multiplicador}", bg="white", font="Inkfree 20 bold", width=5)
        multiplicador_label.place(x=580, y = 320)
        isrunning = True
        while multiplicador <= resultado and isrunning: #Mientras el multiplicador no supere el monto, el gif funciona y va aumentando 0.01
            if contador_frame == 150:   #Si se alcanza el numero de frames, que vuelva a empezar el gif
                contador_frame = 0
            if not boolean:
                break
            frame = ImageSequence.Iterator(imagen)[contador_frame] #Se actualiza el frame dependiendo de la condición si sigue aumentando el multiplicador
            frame = imagen.resize((1280, 300)) #Se ajusta para que quede en la parte superior de la pantalla
            frame = ImageTk.PhotoImage(frame)
            gif_label.config(image=frame)
            multiplicador_global = multiplicador
            multiplicador += 0.01
            contador_frame+=1
            multiplicador = round(multiplicador, 2)
            multiplicador_label.config(text=f"x{multiplicador}")
            if multiplicador <= 2:
                time.sleep(0.07)
            elif multiplicador > 2 and multiplicador <= 5:
                time.sleep(0.05)
            elif multiplicador > 5 and multiplicador <= 10:
                time.sleep(0.03)
            else:
                time.sleep(0.01)
            isrunning = True
            raiz.update() #Se actualiza tanto el frame del gif como el valor del multiplicador
        multiplicador_global = 1
        gif_label.destroy()
        previous_label.place(x= 200, y=500)
        previous_label.update()
        gif_explosion()
        isrunning = False
        raiz.update()

    #Configuraciones de la jugabilidad del juego:
    def manual():
        boton_manual.destroy()
        boton_automatico.destroy()
        ingrese_apuesta = Label(raiz, text="Ingrese su apuesta:", bg="white", font="Inkfree 20 bold")
        ingrese_apuesta.place(x=480, y=450)
        celda_entry.place(x= 550, y = 500)
        boton_stop.place(x= 550, y = 550)
        boton_confirmar.place(x=700, y=500)
        global modo_juego
        modo_juego = "Manual"

        
    def automatico():   
        boton_automatico.destroy()
        boton_manual.destroy()
        ingrese_apuesta = Label(raiz, text="Ingrese su apuesta y\ndebajo el multiplicador:", bg="white", font="Inkfree 20 bold")
        ingrese_apuesta.place(x=480, y=450)
        celda_multiplicador.place(x= 550, y = 560)
        celda_entry.place(x= 550, y = 530)
        boton_listo.place(x= 550, y = 590)
        global modo_juego
        modo_juego = "Automatico"

    def confirmar():
        nonlocal saldo
        global multiplicador_global
        if float(celda_entry.get()) < 0 or float(celda_entry.get()) > saldo:
            celda_entry.insert(1, "")
            messagebox.showwarning("ERROR", "Ingrese un valor entre 0 y su saldo actual")
        else:
            if multiplicador_global >= 1:
                messagebox.showwarning("ERROR", "Ya ha pasado el tiempo de apuesta")
                boton_skip.place(x= 700, y = 550)
            else:
                saldo -= float(celda_entry.get())
                informacion_usuario.config(text=f"Saldo: ${saldo}")
                raiz.update()
                boton_stop.config(state=NORMAL)
                boton_confirmar.config(state=DISABLED)
            
    def stop():
        nonlocal saldo #Con global no funcionaba
        global multiplicador_global
        global isrunning
        boton_stop.config(state=DISABLED)
        saldo+=float(celda_entry.get())
        boton_skip.place(x= 700, y = 550)
        if float(celda_entry.get()) < 0 or float(celda_entry.get()) > saldo:
            celda_entry.insert(1, "")
            messagebox.showwarning("ERROR", "Ingrese un valor entre 0 y su saldo actual")
        else:
            if isrunning:
                saldo-=float(celda_entry.get())
                saldo+= round(float(celda_entry.get())*multiplicador_global,2)

            else:
                saldo -= float(celda_entry.get())
                
    def listo():
        nonlocal saldo #Con global no funcionaba
        global resultado
        global isrunning
        global multiplicador_global
        boton_listo.config(state=DISABLED)
        boton_skip.place(x= 700, y = 550)
        if float(celda_entry.get()) < 0 or float(celda_entry.get()) > saldo:
            messagebox.showwarning("ERROR", "Ingrese un valor entre 0 y su saldo actual")
        else:
            if multiplicador_global >= 1:
                messagebox.showwarning("ERROR", "Ya ha pasado el tiempo de apuesta")
            elif float(celda_multiplicador.get()) <= resultado:
                saldo-=float(celda_entry.get())
                saldo+= round(float(celda_entry.get())*float(celda_multiplicador.get()),2)
                
            else:
                saldo -= float(celda_entry.get())
    
    def skip():
        global isrunning
        isrunning = False
    

    def juego():
        nonlocal saldo
        global boolean
        boolean = True
        i = 0
        while i < len(lista_results)-1 and boolean:
                boton_listo.config(state=NORMAL)
                boton_stop.config(state=DISABLED)
                boton_confirmar.config(state=NORMAL)
                boton_skip.place_forget() #Oculta el skip
                mostrar_resultado(i)
                informacion_usuario.config(text=f"Saldo: ${saldo}")
                raiz.update()

    def fin():
        nonlocal saldo
        global boolean
        boolean = False
        

    boton_manual = Button(raiz, text="MANUAL", command=manual, height=5, width=20)
    boton_manual.place(x=400, y=550)
    
    boton_automatico = Button(raiz, text="AUTOMATICO", command=automatico, height=5, width=20)
    boton_automatico.place(x= 700, y = 550)
    
    boton_stop = Button(raiz, text="STOP", command=stop, height=5, width=15)
    boton_listo = Button(raiz, text="LISTO", command=listo, height=5, width=15)
    boton_confirmar = Button(raiz, text="Confirmar apuesta", command=confirmar)
    boton_skip = Button(raiz, text="Skip", command=skip)
    boton_salir = Button(raiz, text="Salir del juego", command=fin, height=5, width=15)
    boton_salir.place(x= 1100, y = 320)
    
    
    juego()
    raiz.destroy()
    print("Listo")
    return saldo 
    raiz.wait_window(raiz)

