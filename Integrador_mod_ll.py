#AUTORES
from operator import ne
import time, os, sqlite3
from tabulate import tabulate
from tkinter import *
from tkinter import messagebox, StringVar, IntVar, simpledialog, PhotoImage

#ESPACIO PARA FUNCIONES
def encargado():
    nom=valida_string(enc.get())
    mov.set(time.asctime())
    if nom is not False:
        etiqueta=Label(frame0,text="Hamburguesas IT").place(x=260,y=5)
        etiqueta_1=Label(frame0,text="Encargad@ ->" + nom).place(x=260,y=35,width='150')
        etiqueta_2=Label(frame0,text="Recuerda, siempre hay que recibir al cliente con una sonrisa :)").place(x=260,y=65)
        boton1 = Button(frame0,text="Iniciar Pedido",command=pedidos).place(x=260,y=100,width=120,height=25)
        if nom_aux.get() != nom and flag.get() == 0:
            nom_aux.set(nom)
            grabar_encargado(nom_aux.get(),mov.get(),"IN",total_caja.get())
            flag.set(1)
        else:
            if nom_aux != nom and flag.get() == 1:
                mov.set(time.asctime())
                grabar_encargado(nom_aux.get(),mov.get(),"OUT",total_caja.get())
                nom_aux.set(nom)
                flag.set(0)
                total_caja.set(0)
                grabar_encargado(nom,mov.get(),"IN",total_caja.get())

def valida_string(n):
    if not n.replace(" ","").isalpha():    
        messagebox.showwarning("Ingreso datos","El nombre debe contener\n caracteres alfabeticos")
        return False
    return n.title()

def convierte(dato):
    if not dato.isdecimal():
        messagebox.showwarning("Ingreso datos","El pedido debe contener\n caracteres numericos")
        return "Error"
    return int(dato)

def pedidos():
   
    titulo=Label(frame1,text="Ingrese los datos para el pedido").place(x=5,y=20)
    enc.delete(0,'end')
    enc.place(x=5,y=40,width=120,height=20)
    boton = Button(frame0,text="Cambio Encargado",command=encargado).place(x=6,y=70,width=110,height=25)

    ncli=Label(frame1,text="Nombre Cliente").place(x=5,y=60)
    clin=Entry(frame1)
    clin.place(x=100,y=60,width=120,height=20)

    combs=Label(frame1,text="ComboS").place(x=5,y=90)
    scomb=Entry(frame1)
    scomb.place(x=100,y=90,width=120,height=20)

    combd=Label(frame1,text="ComboD").place(x=5,y=120)
    dcomb=Entry(frame1)
    dcomb.place(x=100,y=120,width=120,height=20)

    combt=Label(frame1,text="ComboT").place(x=5,y=150)
    tcomb=Entry(frame1)
    tcomb.place(x=100,y=150,width=120,height=20)

    post=Label(frame1,text="Mcflury").place(x=5,y=180)
    pos=Entry(frame1)
    pos.place(x=100,y=180,width=120,height=20)    

    label0 = Label(frame1,image=img).pack(anchor="se",ipady=40)

    boton2 = Button(frame1,text="Confirma",command=lambda:confirma_pedido(clin,scomb,dcomb,tcomb,pos))
    boton2.place(x=5,y=230,width=120,height=25)

def confirma_pedido(c,s,d,t,p):
    cliente = valida_string(c.get())
    if cliente != False:
        combos = convierte(s.get())
        combod = convierte(d.get())
        combot = convierte(t.get())
        postre = convierte(p.get())
        if combos != "Error" and combod != "Error" and combod != "Error" and combot != "Error" and postre != "Error":
            fecha = time.asctime()
            total = (combos*5) + (combod*6) + (combot*7) + (postre*2)

            abono = None
            while abono is None or not abono.strip().replace(".", "").replace(".", "").isdigit(): 
                abono = (simpledialog.askstring("Dinero Cliente", "El total del pedido es $" + str(total) + "\nCon cuanto abona el cliente"))

            while float(abono) < total or not abono.replace(".", "").replace(".", "").isdigit():
                abono =  (simpledialog.askstring("Dinero Cliente", "No puede abonar menos que el total" + "\nEl total del pedido es $" + str(total) + "\nCon cuanto abona el cliente"))
                while abono is None or not abono.strip().replace(".", "").replace(".", "").isdigit(): 
                    abono = (simpledialog.askstring("Dinero Cliente", "El total del pedido es $" + str(total) + "\nCon cuanto abona el cliente"))

            vuelto = float(abono) - total
    
            res = cuadro_dialogo("El vuelto es $" + str(vuelto) + "\nConfirma Pedido","Confirmacion de Pedidos")
            if res:
                total_caja.set(total_caja.get() + total)
                grabar_ventas(cliente,fecha,combos,combod,combot,postre,total)
            c.delete(0,'end')
            s.delete(0,'end')
            d.delete(0,'end')
            t.delete(0,'end')
            p.delete(0,'end')

def grabar_ventas(cli,fec,s,d,t,p,total):
    conn = sqlite3.connect("comercio.sqlite")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO ventas (cli,fec,s,d,t,p,total) VALUES (?,?,?,?,?,?,?)", (cli,fec,s,d,t,p,total))
    except sqlite3.OperationalError:
        cursor.execute("CREATE TABLE if not exists ventas(id INTEGER PRIMARY KEY AUTOINCREMENT, cli TEXT, fec DATETIME, s TEXT, d TEXT, t TEXT, p TEXT, total NUMERIC)")
        cursor.execute("INSERT INTO ventas (cli,fec,s,d,t,p,total) VALUES (?,?,?,?,?,?,?)", (cli,fec,s,d,t,p,total))
    conn.commit()
    conn.close()

def grabar_encargado(enc,fec,eve,total):
    conn = sqlite3.connect("comercio.sqlite")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO registro (enc,fec,eve,total) VALUES (?,?,?,?)", (enc,fec,eve,total))
    except sqlite3.OperationalError:
        cursor.execute("CREATE TABLE if not exists registro(id INTEGER PRIMARY KEY AUTOINCREMENT, enc TEXT, fec DATETIME, eve TEXT, total NUMERIC)")
        cursor.execute("INSERT INTO registro (enc,fec,eve,total) VALUES (?,?,?,?)", (enc,fec,eve,total))
    conn.commit()
    conn.close()    

def cuadro_dialogo(m,t):
    cerrar = messagebox.askyesno(
        message=m,
        title=t
        )
    return cerrar

def salir():
    try:
        grabar_encargado(nom_aux.get(),mov.get(),"OUT",total_caja.get())
    except:
        pass
    cerrar = messagebox.askyesno(
        message="¿Está seguro de que quiere cerrar la aplicación?",
        title="Cierre de aplicacion"
        )
    if cerrar:
        panel.destroy()

#COMIENZO DE MAIN

panel = Tk()
panel.geometry("600x400")
panel.title("Bienvenidos a Hamburguesas IT")

panel.grid_rowconfigure(0, weight=2, uniform="rows_g1")
panel.grid_rowconfigure(1, weight=4, uniform="rows_g1")
panel.grid_columnconfigure(0, weight=4,  uniform="cols_g1")

total_caja = IntVar()
total_caja.set(0)
flag = IntVar()
flag.set(0)
nom_aux = StringVar()
nom_aux.set("")
mov = StringVar()

frame0 = Frame(panel)
frame0.grid(row=0, column=0,sticky='nsew')

frame1 = Frame(panel)
frame1.grid(row=1, column=0,columnspan=2,sticky='nsew')

etiqueta=Label(frame0,text="Ingrese nombre de encargado").place(x=5,y=10)

enc=Entry(frame0)
enc.place(x=5,y=40,width=120,height=20)

img = PhotoImage(file="HAM2.PNG")

boton = Button(frame0,text="Ingresar", command=encargado).place(x=6,y=70,width=70,height=25)

salir = Button(frame0,text="Salir",command=salir).place(x=6,y=100,width=70,height=25)

panel.mainloop()