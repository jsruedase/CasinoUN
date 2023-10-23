import archivos_csv
from tkinter import *               #Importa la interfaz grafica
from tkinter import messagebox      
from PIL import ImageTk, Image      #Importa una libreria para abrir imágenes   

# Creación de la interfaz gráfica usando Tkinter
raiz = Tk() 
raiz.title("Casino")
raiz.geometry("1280x720")
frame = Frame(raiz, width=600, height=400)
frame.pack()
frame.place(anchor='center', relx=0.5, rely=0.5)
img = ImageTk.PhotoImage(Image.open("fondo-casino.jpg"))
label = Label(frame, image = img)
label.pack()
titulo = Label(raiz, text="CASINO UN", bg="dark blue", font="Inkfree 20 bold")
titulo.place(x = 550, y = 0)
#Inicializa la ventana y crea un frame, el fondo

nombre_e = Entry(raiz, width=20)
nombre_e.place(x = 550, y = 50)
nombre_e.insert(0, "Ingrese su nombre: ")

cedula_e = Entry(raiz, width=20)
cedula_e.place(x = 550, y = 90)
cedula_e.insert(1, "Ingrese su cédula: ")

edad_e =Entry(raiz, width=20)
edad_e.place(x = 550, y = 130)
edad_e.insert(2, "Ingrese su edad: ")

#Se piden datos al usuario y se recopilan

def click():
    if nombre_e.get() == "" or cedula_e.get() == "" or edad_e.get() == "":
        messagebox.showwarning("ERROR", "Por favor ingrese todos los datos correctamente")
    elif int(edad_e.get()) < 18:
        messagebox.showwarning("ERROR", "Debe ser mayor de edad para acceder")
    else:
        texto = controller.inicio_usuario(nombre_e.get(), cedula_e.get())
        if texto != "El día de hoy ya ha jugado, vuelva otro día":
            messagebox.showinfo("SUCCESS", texto)
            boton_iniciar_sesion.destroy()
            boton_listo.place(x = 550, y = 210)
        else:
            messagebox.showwarning("ERROR", texto)
            raiz.destroy()

def listo():
    saldo = 500
    informacion_usuario = Label(raiz, text= f"Usuario: {cedula_e.get()} \n Saldo: {saldo}", bg="dark red", font="Inkfree 20 italic")
    informacion_usuario.place(x = 900, y = 20)
    nombre_e.destroy()
    edad_e.destroy()
    cedula_e.destroy()
    boton_listo.destroy()

boton_iniciar_sesion = Button(raiz, text="Iniciar sesión", command=click)
boton_iniciar_sesion.place(x = 550, y = 170)
boton_listo = Button(raiz, text="Listo", command=listo)

raiz.mainloop() #Hace que la ventana siga abierta