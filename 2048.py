import os
import random
import tkinter as tk
from tkinter import messagebox


TITULO = "2048 by Katerine"
ANCHO, ALTO = 700, 580

ventanaMenu = tk.Tk()
anchoPantalla= ventanaMenu.winfo_screenwidth()
altoPantalla= ventanaMenu.winfo_screenheight()

POS_X = int ((anchoPantalla/2)-(ANCHO/2))
POS_Y = int ((altoPantalla/2)-(ALTO/2))

grid = []
ventanaMenu.title (TITULO)
ventanaMenu.geometry ("{}x{}+{}+{}".format(ANCHO, ALTO, POS_X, POS_Y))

reloj = 0
timer = 0

horas = 0
minutos = 0
segundos = 0

configTimerClock = tk.IntVar()
configTimerClock.set(1)

# Ubicacion del archivo de juego actual
archivo_datos = "src\\files\\2048juegoactual.dat"
# Ubicacion archivo top 10
archivo_top = "src\\files\\2048top10.dat"
# Bandera que inidca si el juego inicio o no
jugando = False
hayclock = False
haytimer = False
#Variable donde se guarda el nombre del jugador
nombre_jugador = ""
gameboard = []
# Crea un diccionario para poner colores segun el numero en las casillas
colores = {2: '#e08a89', 4: '#f0a951', 8: '#e8e54a', 16: '#a4e647', 32: '#e34257', 64: '#33cc6b', 128: '#33cca1', 256: '#1e8eba', 512: '#9d42e3', 1024: '#bf3dd9', 2048: '#e62e7a'}

imagen = tk.PhotoImage(file="src\\imgs\\Imagenjuego.png")
fondo = tk.Label(ventanaMenu, image=imagen)
fondo.config(image=imagen)
fondo.place(x=185, y=50)

ventanaMenu.resizable(width=False, height=False)
ventanaMenu.config(bg="#f1e6da")
lblTitle=tk.Label(ventanaMenu, text="Menu principal", bg="#f1e6da", fg="black", font=("Ubuntu Monospace", 18))
lblTitle.place(x=ANCHO//2, y=20, anchor="center")

frame = tk.Frame(ventanaMenu)
frame.place(x=220, y=45)

def verManual():
    os.system("src\\files\\manual_de_usuario_2048.pdf")

def salir():
    # Destruye la ventana
    ventanaMenu.destroy()

def empezarAJugar():
    global grid, reloj
    reloj = 0
    # Esconde la ventana principal
    ventanaMenu.withdraw()
    # Con top level se crea una ventana secundaria
    ventanaJuego = tk.Toplevel()
    # matrix inicia en 0
    def createMatrix(rows, cols):
        matrix = []
        # Me crea las filas
        for i in range(rows):
            row = []
            #me agrega ceros a mi matrix
            for j in range(cols):
                row.append(0)
            matrix.append(row)
        return matrix

    #Inicia la matriz con dos numeros aleatorios en pocisiones aleatorias
    def initMatrix(matrix):
        pos = []
        while len(pos) < 2:
            # Agrega un dos aleatorio
            newPos = [random.randint(0, 3), random.randint(0, 3)]
            # si la posicion no esta ocupada por un dos se agrega a esa posicion
            if newPos not in pos:
                pos.append(newPos)
        # Agrega los dos aleatorios, crea las "coordenadas" [x1,y1] [x2, y2] y coloca el 2
        matrix[pos[0][0]][pos[0][1]] = random.choice([2, 2, 2, 4])
        matrix[pos[1][0]][pos[1][1]] = random.choice([2, 2, 2, 4])
        # matrix -> [[0, 0, 0, 0], [0, 0, 0, 2], [0, 2, 0, 0], [0, 0, 0, 0]]
        return matrix

    # Verifica si hay espacios vacios en la matriz
    def terminoElJuego(matrix):
        for i in range (len(matrix)):
            for j in range (len(matrix[i])):
                if matrix[i][j] == 0:
                    return False
        return True

    # Si se encuentra un 2048 en la matriz el juego  termina tambien
    def termina2048(matrix):
        for i in range (len(matrix)):
            for j in range (len(matrix[i])):
                if matrix[i][j] == 2048:
                    return True
        return False

    #  Aparecen numeros aleatorios en diferentes pocisiones
    def colocarNumerosRandom(matrix):
        # Genera una posicion random en la matriz (fila, columna)
        newPos = [random.randint(0, 3), random.randint(0, 3)]
        # El ciclo se cumple Si la pocision esta ocupada
        while matrix[newPos[0]][newPos[1]] != 0:
            # Si encuentra que esta ocupada genera otra posicion
            newPos = [random.randint(0, 3), random.randint(0, 3)]
            # Agrega un dos o un 4 en la posicion x y
        matrix[newPos[0]][newPos[1]] = random.choice([2, 2, 2, 4])
        return matrix

    # Mueve los numeros a la izquierda
    def move_left(matrix):
        newmatrix=[]
        # Saca cada fila de la matrix
        for row in matrix:
            newrow=[]
            # Evalua cada columna de cada fila y agrega en una nueva los valores diferentes de cero
            for cols in row:
                # Agrega el numero a izquierda
                if cols!=0:
                    newrow.append(cols)
            # Aniade los ceros que le hace falta a la derecha
            amountOfZeros = 4-len(newrow)
            # agrega ceros a la derecha
            newrow +=[0]*amountOfZeros
            newmatrix.append (newrow)
        return newmatrix

    def move_right(matrix):
        newmatrix=[]
        # Saca cada fila de la matrix
        for row in matrix:
            newrow=[]
            # Evalua cada columna de cada fila y agrega en una nueva los valores diferentes de cero
            for cols in row:
                # Agrega el numero a la derecha
                if cols != 0:
                    newrow.append(cols)
            #añade los ceros que le hace falta a la derecha
            amountOfZeros = 4 - len(newrow)
            # Agrega primero el numero y luego los ceros
            newrow=[0]*amountOfZeros+newrow  
            newmatrix.append (newrow)
        return newmatrix

    # Mueve los numeros hacia la derecha
    def move_up(matrix):
        # Crea la matriz con ceros de 4x4
        newMatrix = createMatrix(4, 4)
        # Recorre las columnas
        for j in range(len(matrix)):
            # Indica el espacio que esta vacio
            count = 0
            # Recorrer las filas
            for i in range(len(matrix)):
                # Si la posicion es diferente de cero  la  agrego a la nueva matriz
                if (matrix[i][j] != 0):
                    # Se guarda en la posicion fila que guarda el contador
                    newMatrix[count][j] = matrix[i][j]
                    # Aumenta el contador para que se vaya moviendo en la matriz buscando espacios
                    count += 1
        return newMatrix

    def move_down(matrix):
        newMatrix = createMatrix(4, 4)
        # Recorre las columnas
        for j in range(len(matrix)):
            # Indica el espacio que esta vacio
            count = -1
            # Recorre las filas desde la ultima posicion hasta la primera, va de menos 1 en menos 1 (porque va en reversa)
            for i in range(-1, -len(matrix) - 1, -1):
                if (matrix[i][j] != 0):
                    newMatrix[count][j] = matrix[i][j]
                    # Aumenta el contador para que se vaya moviendo en la matriz buscando espacios desde abajo
                    count -= 1
        return newMatrix

    # Suma izquierda
    def add_left(matrix):
        for fila in matrix:
            # Entra a la columna hasta un elemento antes para no salirme de la columna
            for j in range (len(fila)-1):
                # Si fila en pocision j es igual a la posicion siguiente y es diferente de cero, m
                if fila[j] == fila[j+1] and fila[j] != 0:
                    # Se actualiza mi fila con la suma del numero mas el siguiente
                    fila[j] = fila[j] + fila[j + 1]
                    # Reinicia en 0 la posicion sumada
                    fila[j + 1] = 0
        return matrix

    # Suma derecha
    def add_right(matrix):
        for fila in matrix:
            # Recorre las filas desde la ultima posicion hasta la segunda para que no se salga del rango
            for j in range (-1,-len(fila), -1):
                #Si en la posicion que tengo , el numero anterior es igual, lo sumo a la derecha
                if fila[j] == fila[j-1] and fila[j] != 0:
                    fila[j] = fila[j] + fila[j - 1]
                    # Reinicio mi numero anterior
                    fila[j - 1] = 0
        return matrix

    # Suma arriba
    def add_up(matrix):
        for j in range(len(matrix)):
            # Sumo hacia arriba pero  no puede llegar hasta la de mas arriba, sino una fila antes
            for i in range(len(matrix)-1):
                #
                if (matrix[i][j] == matrix[i+1][j] and matrix[i][j] != 0):
                    matrix[i][j] = matrix[i][j] + matrix[i+1][j]
                    matrix[i+1][j] = 0
        return matrix

    def add_down(matrix):
        for j in range(len(matrix)):
            for i in range(-1, -len(matrix), -1):
                if (matrix[i][j] == matrix[i-1][j] and matrix[i][j] != 0):
                    matrix[i-1][j] = matrix[i][j] + matrix[i-1][j]
                    matrix[i][j] = 0
        return matrix

    ventanaJuego.title (TITULO)
    ventanaJuego.geometry ("{}x{}+{}+{}".format(ANCHO, ALTO, POS_X, POS_Y))

    ventanaJuego.resizable(width=False, height=False)
    ventanaJuego.config(bg="#f1e6da")
    lblTitle=tk.Label(ventanaJuego, text="2048", bg="#f1e6da", fg="black", font=("Ubuntu Monospace", 24))
    lblTitle.place(x=ANCHO//2, y=20, anchor="center")

    frame = tk.Frame(ventanaJuego)
    frame.place(x=220, y=45)

    lblInstruc=tk.Label(ventanaJuego, text=" Use las teclas" + "\n"+ "de dirección" + "\n"+ "para mover" + "\n"+ "las fichas." , bd = 3, bg="#f0a951", fg="black", font=("Ubuntu Monospace", 11))
    lblInstruc.place(x= 535, y = 390)

    lblJugador=tk.Label(ventanaJuego, text="Nombre del jugador:", bd=3, bg="#f1e6da", fg="black", font=("Ubuntu Monospace", 11))
    lblJugador.place(x= 100, y = 410)

    lblClock = tk.Label(ventanaJuego, bg = "#f1e6da", font=("Ubuntu Monospace", 18))
    lblClock.place(x=500, y=20)

    lblTimer = tk.Label(ventanaJuego, bg = "#f1e6da", font=("Ubuntu Monospace", 18))
    lblTimer.place(x=500, y=70)
   
    #Label que dibuja  la matriz
    grid = [[tk.Label(frame, width=4, height=2, borderwidth=3, relief="solid", font=("Ubuntu Monospace", 18)) for i in range(4)] for j in range(4)]

    def convertir(n):
        horas= n//3600
        minutos= n%3600//60
        segundos= n%3600%60
        if minutos < 10:
            minutos = '0' + str(minutos)
        else:
            minutos = str(minutos)
           
        if segundos < 10:
            segundos = '0' + str(segundos)
        else:
            segundos = str(segundos)
        return str(horas) + ":" + minutos + ":" + str(segundos)

    # Dibuja el reloj en la pantalla
    def tic():
        global reloj, timer, configTimerClock
        if configTimerClock.get() == 1:
           lblClock['text'] = convertir(reloj)
        if configTimerClock.get() == 3:
           lblTimer['text'] = convertir(timer)
    # Llama solo una vez al reloj
    tic()

    # Actualiza el cronometro
    def tac():
        global reloj, configTimerClock, jugando
        # Sigue dibujando para estar actualizando el reloj
        tic()
        lblTimer.after(1000, tac)
        # Cada 1000 milisegundos llama a la funcion tac (after)
        if configTimerClock.get() == 1 and jugando:
            reloj += 1

    def run_timer():
        global timer, configTimerClock, jugando
        # Sigue dibujando para estar actualizando el reloj
        tic()
        # Cada 1000 milisegundos llama a la funcion tac (after)
        lblTimer.after(1000, run_timer)
        if configTimerClock.get() == 3 and jugando:
            timer-= 1

    # Llama a tac una vez para que aparezca en pantalla
    tac()
    run_timer()

    # Dibuja la matriz
    def draw(grid, matrix):
        for x in range(4):
            for y in range(4):
               # Si la matriz tiene un numero
                if (matrix[y][x]) != 0:
                   # Se modifica la matriz  y se coloca ese nuemro con el color respectivo
                    grid[x][y].config(text=str(matrix[y][x]), bg=colores[matrix[y][x]])
                else:
                    # Si la matriz tiene un cero, no se coloca un numero y se deja el fondo del mismo color
                    grid[x][y].config(text="", bg="#f1e6da")
                   # Acomoda los labels segun la cuadricula
                grid[x][y].grid(column=x, row=y)

    def iniciarPausarPartida():
        global jugando, nombre_jugador
        # Obtiene el nombre del jugador
        nombre_jugador = entryNombre.get()
        if nombre_jugador == "":
           # Envia mensaje de error si no se introduce el nombre
            messagebox.showerror("Nombre no asignado", "Debe ingresar el nombre del jugador antes de iniciar la partida")
        elif len(nombre_jugador) > 30:
           # Si el nombre ingresado es mayor a 30  retorna error
            messagebox.showerror("Nombre invalido", "El nombre del jugador debe contener maximo 30 caracteres")
        else:
           #  Disable : desabilita la ventana
            entryNombre.config(state='disabled')
            # Me niega el valor que tenga jugando
            jugando = not jugando
            # Si esta jugando muestre  el boton pausar
            if jugando:
                btnIniciarPartida.config(text="PAUSAR \n  PARTIDA  ")
            else:
               # Si no esta jugando muestre el boton de iniciar partida
                btnIniciarPartida.config(text="INICIAR \n  PARTIDA  ")

    def partidaNueva():
        MsgBox = messagebox.askquestion('Nueva partida','¿Esta seguro que desea iniciar partida?', icon='warning')
        if MsgBox == 'yes':
            # Llama a la funcion iniciar partida para que se despliegue matriz primero y luego mensaje
            iniciarPartida()
       
    def iniciarPartida():
        global grid, gameboard, jugando, nombre_jugador, reloj, timer, configTimerClock
        global horas, minutos, segundos
        jugando = False
        reloj = 0
        timer = horas * 3600 + minutos * 60 + segundos
        nombre_jugador = ""
        # Crear matriz 4x4
        gameboard = createMatrix(4, 4)
        # Inicia la matriz con numeros random
        gameboard = initMatrix(gameboard)
        # Dibuja la matriz
        draw(grid, gameboard)
        btnIniciarPartida.config(text="INICIAR \n  PARTIDA  ")
        #  Se habilita nuevamente el espacio para escribir el nombre
        entryNombre.config(state='normal')
        # Limpiar el entry, end=constante que va desde el inicio hasta el final
        entryNombre.delete(0, tk.END)

    def salir():
        # Se sale de la ventana
        ventanaJuego.destroy()
        # Restaura la ventana  del menu
        ventanaMenu.deiconify()

    def guardarJuego():
        global archivo_datos, nombre_jugador, gameboard, jugando
        # si se esta jugando
        if jugando:
           # Abre el archivo
            archivo = open(archivo_datos, 'w')
             # Escribe  el nombre del jugador
            archivo.write(nombre_jugador + '\n')
            # Escribe la matriz como string
            archivo.write(str(gameboard))
            # Se cierra el archivo
            archivo.close()
            messagebox.showinfo("Guardado", "Partida guardada")
        else:
            messagebox.showerror("Error", "No hay partida en curso")

    def cargarJuego():
        global archivo_datos, nombre_jugador, gameboard, jugando, grid
        # Lee los datos guardados
        archivo = open(archivo_datos, 'r')
        datos = archivo.read()
        # Si no hay datos muestra el error
        if datos == "":
            messagebox.showerror("Error", "No hay partida guardad")
        else:
            # Me devuelve los datos separados
            lineas = datos.split('\n')
            # El nombre del jugador va a ser el primer elemento del string
            nombre_jugador = lineas[0]
            # Devuelve la matriz en su estado  original
            gameboard = eval(lineas[1])
            # Se habilita el juego de nuevo
            jugando = True
            # Se dibuja la matriz de nuevo
            draw(grid, gameboard)
            # Se habilita espacio para esribir nombre
            entryNombre.config(state='normal')
            #  Limpia el entry
            entryNombre.delete(0, tk.END)
            # Se guarda el nombre desde la primera posicion del entry (por eso el cero)
            entryNombre.insert(0, nombre_jugador)
            # Se vuelve a desabilitar entry
            entryNombre.config(state='disabled')

    def top10():
        print("Mejores jugadores")

    # Agrega espacio donde se coloca el nombre del jugador
    entryNombre = tk.Entry(ventanaJuego, bd = 2, bg = "white", font = ("Ubuntu Monospace", 13) )
    entryNombre.place(x= 275, y=410)

    btnIniciarPartida=tk.Button(ventanaJuego, text="INICIAR \n  PARTIDA  ",
                                bg="#a4e647", fg="black",
                                font=("Ubunto Monospace", 12),
                                activebackground="#a4e647",
                                activeforeground="black",
                                command=iniciarPausarPartida)
    btnIniciarPartida.place(x=25, y=330)

    btnPartidaNueva=tk.Button(ventanaJuego, text="  PARTIDA  \n NUEVA ",
                                bg="#e34257", fg="black",
                                font=("Ubunto Monospace", 12),
                                activebackground="#e34257",
                                activeforeground="black",
                                command=partidaNueva)
    btnPartidaNueva.place(x=150, y=330)

    btnSalir=tk.Button(ventanaJuego, text= "      SALIR      \n",
                                bg="#33cca1", fg="black",
                                font=("Ubunto Monospace", 12),
                                activebackground="#33cca1",
                                activeforeground="black",
                                command= salir)
    btnSalir.place(x=275, y=330)

    btnCargarJuego=tk.Button(ventanaJuego, text="   CARGAR   \nJUEGO",
                                bg="#e8e54a", fg="black",
                                font=("Ubunto Monospace", 12),
                                activebackground="#e8e54a",
                                activeforeground="black",
                                command= cargarJuego)
    btnCargarJuego.place(x=407, y=480)

    btnGuardarJuego=tk.Button(ventanaJuego, text="  GUARDAR  \nJUEGO",
                                bg="#e08a89", fg="black",
                                font=("Ubunto Monospace", 12),
                                activebackground="#e08a89",
                                activeforeground="black",
                                command= guardarJuego)
    btnGuardarJuego.place(x=272, y=480)

    btnTop10=tk.Button(ventanaJuego, text= "        TOP        \n10",
                                bg="#9d42e3", fg="black",
                                font=("Ubunto Monospace", 12),
                                activebackground="#9d42e3",
                                activeforeground="black",
                                command=top10)
    btnTop10.place(x=407, y=330)

    # Crea el tablero inicial
    iniciarPartida()

    # Cuando se presiona a la derecha se llama a esta funcion
    def right_pressed(e):
        global gameboard, jugando
        # Si se esta jugando
        if jugando:
           # Mueve a la derecha los numeros, suma y vuelve a colocar a la derecha
            gameboard = move_right(gameboard)
            gameboard = add_right(gameboard)
            gameboard = move_right(gameboard)
            # Si no ha teminado el juego
            if not terminoElJuego(gameboard):
               # Se vuelven a colocar numeros random en el tablero
                gameboard = colocarNumerosRandom(gameboard)
                # Si se llega a 2048 muestra mensajd de ganó
                if termina2048(gameboard):
                     #Juego regresa a  ser false
                    jugando = False
                    draw(grid, gameboard)
                    messagebox.showinfo("Gano", "2048")
                # Se dibuja nueva,mente la matriz para que se actualice
                draw(grid, gameboard)
            else:
                jugando = False
                draw(grid, gameboard)
                # Mensaje de perdio si ya no se pueden hacer movimientos
                messagebox.showinfo("Perdio", "No hay casillas disponibles")

    def left_pressed(e):
        global gameboard, jugando
        # Mueve a la izquierda los numeros, suma y vuelve a colocar a la izquierda
        if jugando:
            gameboard = move_left(gameboard)
            gameboard = add_left(gameboard)
            gameboard = move_left(gameboard)
            # Si no ha teminado el juego
            if not terminoElJuego(gameboard):
               # Se vuelven a colocar numeros random en el tablero
                gameboard = colocarNumerosRandom(gameboard)
                # Si se llega a 2048 muestra mensajd de ganó
                if termina2048(gameboard):
                    messagebox.showinfo("Gano", "2048")
                    #Juego regresa a  ser false
                    jugando = False
                # Se dibuja nueva,mente la matriz para que se actualice
                draw(grid, gameboard)
            else:
                # Si no ha terminado  y no hay mas casillas vacias muestra mensaje
                messagebox.showinfo("Perdio", "No hay casillas disponibles")
                jugando = False
   
    def up_pressed(e):
        global gameboard, jugando
        if jugando:
           # Mueve hacia arriba los numeros, suma arriba y vuelve a colocar arriba
            gameboard = move_up(gameboard)
            gameboard = add_up(gameboard)
            gameboard = move_up(gameboard)
            # Si no ha terminado el juego coloca los numeros random de nuevo
            if not terminoElJuego(gameboard):
                gameboard = colocarNumerosRandom(gameboard)
                # Si llega a 2048 sale el mensaj e de gano
                if termina2048(gameboard):
                    messagebox.showinfo("Gano", "2048")
                    # Jugando vuelve a ser False
                    jugando = False
                    # Se actualiza la matriz
                draw(grid, gameboard)
            else:
                # Si se llenan las casillas y no se ha formado el 2048 sale el mensaje de perdio
                messagebox.showinfo("Perdio", "No hay casillas disponibles")
                jugando = False

    def down_pressed(e):
        global gameboard, jugando
        if jugando:
            # Mueve hacia abajo los numeros, suma abajo y vuelve a colocar abajo
            gameboard = move_down(gameboard)
            gameboard = add_down(gameboard)
            gameboard = move_down(gameboard)
            # Si no ha terminado el juego coloca los numeros random de nuevo
            if not terminoElJuego(gameboard):
                gameboard = colocarNumerosRandom(gameboard)
                # Si llega a 2048 sale el mensaj e de gano
                if termina2048(gameboard):
                    messagebox.showinfo("Gano", "2048")
                    # Jugando vuelve a ser False
                    jugando = False
                # Se actualiza nuevamente la matriz
                draw(grid, gameboard)
            else:
                # Si se llenan las casillas y no se ha formado el 2048 sale el mensaje de perdio
                messagebox.showinfo("Perdio", "No hay casillas disponibles")
                jugando = False
               
    # Permite usar las teclas direccionales y mover  hacia la direccion corresponidente
    ventanaJuego.bind("<Left>", left_pressed)
    ventanaJuego.bind("<Right>", right_pressed)
    ventanaJuego.bind("<Up>", up_pressed)
    ventanaJuego.bind("<Down>", down_pressed)

def config():
    global hayclock, haytimer, configTimerClock, horas, minutos, segundos
    ventanaMenu.withdraw()
    #Genera una ventana secundaria
    ventanaConfig = tk.Toplevel()
    ventanaConfig.title (TITULO)
    ventanaConfig.geometry ("{}x{}+{}+{}".format(ANCHO, ALTO, POS_X, POS_Y))
    ventanaConfig.resizable(width=False, height=False)
    ventanaConfig.config(bg="#f1e6da")

    lblhora=tk.Label(ventanaConfig, text="Ingrese hora:", bg="#f1e6da", fg="black", font=("Ubuntu Monospace", 16))
    lblhora.place(x=150, y=175 )

    lblminutos=tk.Label(ventanaConfig, text="Ingrese minutos:", bg="#f1e6da", fg="black", font=("Ubuntu Monospace", 16))
    lblminutos.place(x=150, y=250)

    lblsegundos=tk.Label(ventanaConfig, text="Ingrese segundos:", bg="#f1e6da", fg="black", font=("Ubuntu Monospace", 16))
    lblsegundos.place(x=150, y=325)

    entryHoras = tk.Entry(ventanaConfig, bd=2, bg = "white", font = ("Ubuntu Monospace", 13) )
    entryHoras.insert(0, str(horas))
    entryHoras.place(x= 350, y=175)

    entryMinutos = tk.Entry(ventanaConfig, bd=2, bg="white", font = ("Ubuntu Monospace", 13) )
    entryMinutos.insert(0, str(minutos))
    entryMinutos.place(x= 350, y=250)
   
    entrySegundos = tk.Entry(ventanaConfig, bd=2, bg="white", font = ("Ubuntu Monospace", 13) )
    entrySegundos.insert(0, str(segundos))
    entrySegundos.place(x= 350, y=325)

    def guardarConfig():
        global horas, minutos, segundos
        try:
            horas = int(entryHoras.get())
            minutos = int(entryMinutos.get())
            segundos = int(entrySegundos.get())
            ventanaMenu.deiconify()
            ventanaConfig.destroy()
        except ValueError:
            messagebox.showerror('Error', 'Los campos no deben estar vacios')

    def cancelarConfig():
        ventanaMenu.deiconify()
        ventanaConfig.destroy()

    btnGuardarConfig=tk.Button(ventanaConfig, text= "     Guardar     ",
                                bg="#e8e54a", fg="black",
                                font=("Ubunto Monospace", 12),
                                activebackground="#e8e54a",
                                activeforeground="black",
                                command=guardarConfig)
    btnGuardarConfig.place(x=150, y=400)

    btnCancelar=tk.Button(ventanaConfig, text= "     Cancelar     ",
                                bg="#33cc6b", fg="black",
                                font=("Ubunto Monospace", 12),
                                activebackground="#33cc6b",
                                activeforeground="black",
                                command=cancelarConfig)
    btnCancelar.place(x=380, y=400)
   
    rbtnSi = tk.Radiobutton(ventanaConfig, 
              text="Si",
              padx = 20, 
              variable=configTimerClock,
              bg = "#f1e6da",
              font=("Ubuntu Monospace", 16),
              value=1)
    rbtnSi.place(x= 150, y=80)
    
    rbtnNo=tk.Radiobutton(ventanaConfig, 
              text="No",
              padx = 20, 
              variable=configTimerClock,
              bg = "#f1e6da",
              font=("Ubuntu Monospace", 16),
              value=2)
    rbtnNo.place(x= 150, y=110)
    rbtnTimer=tk.Radiobutton(ventanaConfig, 
              text="Timer",
              padx = 20, 
              variable=configTimerClock,
              bg = "#f1e6da",
              font=("Ubuntu Monospace", 16),
              value=3)
    rbtnTimer.place(x=150, y=50)
    
    lblhora=tk.Label(ventanaConfig, text="¿Desea jugar con reloj?", bg="#f1e6da", fg="black", font=("Ubuntu Monospace", 16))
    lblhora.place(x=150, y=15 )


    

def acercaDe():
    ventanaAcercaDe = tk.Toplevel()
    ventanaAcercaDe.title (TITULO)
    ventanaAcercaDe.geometry ("{}x{}+{}+{}".format(ANCHO, ALTO, POS_X, POS_Y))

    ventanaAcercaDe.resizable(width=False, height=False)
    ventanaAcercaDe.config(bg="#f1e6da")
   
    lblnombreJuego=tk.Label(ventanaAcercaDe, text="2048", bg="#f1e6da", fg="black", font=("Ubuntu Monospace", 24))
    lblnombreJuego.place(x=ANCHO//2, y=100, anchor="center")

    lblversion=tk.Label(ventanaAcercaDe, text="version v1.0.0", bg="#f1e6da", fg="black", font=("Ubuntu Monospace", 24))
    lblversion.place(x=ANCHO//2, y=175, anchor="center")

    lblfecha=tk.Label(ventanaAcercaDe, text="02/10/2019", bg="#f1e6da", fg="black", font=("Ubuntu Monospace", 24))
    lblfecha.place(x=ANCHO//2, y=250, anchor="center")

    lblautora=tk.Label(ventanaAcercaDe, text="Katerine Guzman Flores", bg="#f1e6da", fg="black", font=("Ubuntu Monospace", 24))
    lblautora.place(x=ANCHO//2, y=325, anchor="center")
   

btnJugar=tk.Button(ventanaMenu, text="     Jugar     ",
                            bg="#a4e647", fg="black",
                            font=("Ubunto Monospace", 15),
                            activebackground="#a4e647",
                            activeforeground="black",
                            command=empezarAJugar)
btnJugar.place(x=80, y=390)

btnConfiguracion=tk.Button(ventanaMenu, text=" Configuración ",
                            bg="#e34257", fg="black",
                            font=("Ubunto Monospace", 15),
                            activebackground="#e34257",
                            activeforeground="black",
                            command=config)
btnConfiguracion.place(x=270, y=390)

btnAcercade=tk.Button(ventanaMenu, text= "   Acerca de   ",
                            bg="#33cca1", fg="black",
                            font=("Ubunto Monospace", 15),
                            activebackground="#33cca1",
                            activeforeground="black",
                            command=acercaDe)
btnAcercade.place(x=480, y=390)

btnAyuda=tk.Button(ventanaMenu, text= "    Ayuda    ",
                            bg="#9d42e3", fg="black",
                            font=("Ubunto Monospace", 15),
                            activebackground="#9d42e3",
                            activeforeground="black",
                            command=verManual)
btnAyuda.place(x=180, y=480)

btnSalir=tk.Button(ventanaMenu, text="     Salir     ",
                            bg="#e8e54a", fg="black",
                            font=("Ubunto Monospace", 15),
                            activebackground="#e8e54a",
                            activeforeground="black",
                            command=salir)
btnSalir.place(x=390, y=480)

ventanaMenu.mainloop()
