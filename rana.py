import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import csv
import tkinter as tk
from tkinter import filedialog
import time
from PIL import Image, ImageTk 
from itertools import product

class SimuladorRana:
    def __init__(self, ventana_principal):
        """
        Inicializa el simulador de la rana.
        Args:
            ventana_principal: La ventana principal de la interfaz gráfica.
        """
        self.ventana_principal = ventana_principal
        self.configurar_ventana_principal()

    def configurar_ventana_principal(self):
        """
        Configura la ventana principal de la interfaz gráfica.
        """
        self.ventana_principal.title("Menú")
        self.ventana_principal.attributes('-fullscreen', True)
        self.cargar_imagen_fondo()
        self.mostrar_etiqueta_bienvenida()
        self.mostrar_imagen_rana()
        self.mostrar_botones_menu()

    def cargar_imagen_fondo(self):
        """
        Carga y muestra una imagen de fondo en la ventana.
        """
        fondo_imagen = Image.open("fondo.jpg")
        fondo_imagen = fondo_imagen.resize((self.ventana_principal.winfo_screenwidth(), self.ventana_principal.winfo_screenheight()), Image.ADAPTIVE)
        self.fondo_imagen = ImageTk.PhotoImage(fondo_imagen)
        
        self.canvas_fondo = tk.Canvas(self.ventana_principal, width=self.ventana_principal.winfo_screenwidth(), height=self.ventana_principal.winfo_screenheight())
        self.canvas_fondo.pack(fill="both", expand=True)
        self.canvas_fondo.create_image(0, 0, anchor="nw", image=self.fondo_imagen)

    def mostrar_etiqueta_bienvenida(self):
        """
        Muestra una etiqueta de bienvenida en la ventana.
        """
        etiqueta = tk.Label(self.canvas_fondo, text="BIENVENIDO AL SIMULADOR DE LA RANA", font=("Times new roman", 50), fg='#000000')
        etiqueta.place(relx=0.5, rely=0.1, anchor="center")
        etiqueta.config(bg="green")

    def mostrar_imagen_rana(self):
        """
        Muestra una imagen de una rana en la ventana.
        """
        imagen_rana = Image.open("rana4.jpg")
        imagen_rana = imagen_rana.resize((200, 200), Image.ADAPTIVE)
        imagen_rana = ImageTk.PhotoImage(imagen_rana)
        
        etiqueta_rana = tk.Label(self.canvas_fondo, image=imagen_rana)
        etiqueta_rana.image = imagen_rana
        etiqueta_rana.place(relx=0.5, rely=0.3, anchor="center")

    def mostrar_botones_menu(self):
        """
        Muestra los botones del menú principal en la ventana.
        """
        colores_botones = ['#FFD700', '#FFD700', '#FFD700', '#FFD700']
        opciones_menu = [
            ("Hacer simulación para una dimensión", self.mostrar_simulacion_dim1, colores_botones[0]),
            ("Hacer simulación para dos dimensiones", self.mostrar_simulacion_dim2, colores_botones[1]),
            ("Hacer simulación para tres dimensiones", self.mostrar_simulacion_dim3, colores_botones[2]),
            ("Salir", self.ventana_principal.destroy, colores_botones[3])
        ]
        for i, (opcion_texto, funcion_opcion, color) in enumerate(opciones_menu):
            boton = tk.Button(self.canvas_fondo, text=opcion_texto, command=funcion_opcion, font=("Helvetica", 16), bg=color, fg='#333333')  
            boton.place(relx=0.5, rely=0.5 + i * 0.1, anchor="center")

    def leer_csv(self, nombre_archivo):
        """
        Lee un archivo CSV y devuelve los números pseudoaleatorios.
        Args:
            nombre_archivo: El nombre del archivo CSV.

        Returns:
            Una lista de números pseudoaleatorios.
        """
        numeros_pseudoaleatorios = []
        with open(nombre_archivo, 'r') as archivo_csv:
            lector_csv = csv.reader(archivo_csv)
            for fila in lector_csv:
                numeros_pseudoaleatorios.append(float(fila[0]))
        return numeros_pseudoaleatorios

    def asignar_valor_segun_rango_1dim(self, valor):
        """
        Asigna un valor según un rango para una dimensión.
        Args:
            valor: El valor a asignar.

        Returns:
            El valor asignado según el rango.
        """
        if 0 <= valor < 0.5:
            return -1
        elif 0.5 <= valor <= 1:
            return 1
        else:
            raise ValueError("El valor debe estar en el rango [0, 1]")    

    def simulate_frog_from_data(self, data):
        """
        Simula el movimiento de la rana a partir de los datos.
        Args:
            data: Los datos de los saltos de la rana.

        Returns:
            Una lista de posiciones de la rana en la recta numérica.
        """
        positions = [0]
        for jump in data:
            new_position = positions[-1] + jump
            positions.append(new_position)
        return positions
    
    def calcular_probabilidades(self):
        """
        Calcula las probabilidades de regresar al origen en el segundo, tercer y cuarto salto.
        Returns:
            Una lista de probabilidades.
        """
        movimientos_posibles = ['izquierda', 'derecha']
        secuencias_posibles = list(product(movimientos_posibles, repeat=4))

        # Cuenta el número de secuencias que resultan en el regreso al origen en el segundo, tercer y cuarto salto
        regreso_segundo_salto = sum(1 for secuencia in secuencias_posibles if secuencia[0] != secuencia[1])
        regreso_tercer_salto = 0
        regreso_cuarto_salto = sum(1 for secuencia in secuencias_posibles if secuencia.count('izquierda') == 2 )

        # Calcula las probabilidades
        probabilidad_segundo_salto = regreso_segundo_salto / len(secuencias_posibles)
        probabilidad_tercer_salto = regreso_tercer_salto / len(secuencias_posibles)
        probabilidad_cuarto_salto = regreso_cuarto_salto / len(secuencias_posibles)

        return [0, probabilidad_segundo_salto, probabilidad_tercer_salto, probabilidad_cuarto_salto]


    def volver_al_menu(self, ventana_graficos):
        """
        Vuelve al menú principal.
        Args:
            ventana_graficos: La ventana de gráficos actual.
        """
        ventana_graficos.destroy()
        self.ventana_principal.deiconify()

    def mostrar_simulacion_dim1(self):
        """
        Muestra la simulación en una dimensión.
        """
        # Crea una ventana de gráficos
        ventana_graficos = tk.Toplevel(self.ventana_principal)
        ventana_graficos.title("Simulación de Movimiento de la Rana")
        ventana_graficos.attributes('-fullscreen', True)

        # Configura el espacio vertical entre los gráficos
        ventana_graficos.geometry("1200x800")

        archivo_csv = 'numeros_ri_final.csv'
        datos = self.leer_csv(archivo_csv)
        datos_asignados = [self.asignar_valor_segun_rango_1dim(valor) for valor in datos]

        # Crea un solo Figure para contener ambas subtramas
        fig, (ax1, ax2) = plt.subplots(nrows=2, figsize=(10, 5), constrained_layout=True)

        # Gráfico de posiciones
        posiciones = self.simulate_frog_from_data(datos_asignados)
        ax1.plot(self.simulate_frog_from_data(datos_asignados))
        ax1.set_title('Simulación de Movimiento de la Rana')
        ax1.set_xlabel('Número de Saltos')
        ax1.set_ylabel('Posición en la Recta Numérica')

        # Histograma de frecuencia de posiciones de salida
        posiciones_salida = self.simulate_frog_from_data(datos_asignados)[1:]
        ax2.hist(posiciones_salida, bins=range(min(posiciones_salida), max(posiciones_salida) + 2),
                 align='left', color='skyblue', edgecolor='black')
        ax2.set_title('Frecuencia de Posiciones de Salida de la Rana')
        ax2.set_xlabel('Posición de Salida')
        ax2.set_ylabel('Frecuencia')

        # Crea el widget FigureCanvasTkAgg
        canvas = FigureCanvasTkAgg(fig, master=ventana_graficos)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Calcula y muestra las probabilidades de volver al origen en el segundo, tercer y cuarto salto
        probabilidades = self.calcular_probabilidades()
        etiqueta_probabilidades = tk.Label(ventana_graficos, text=f"Probabilidades:\nSegundo salto: {probabilidades[1]:.2%}\nTercer salto: {probabilidades[2]:.2%}\nCuarto salto: {probabilidades[3]:.2%}", font=("Helvetica", 12))
        etiqueta_probabilidades.pack()

        # Agrega etiquetas para mostrar el último valor y el número total de datos
        etiqueta_ultimo_valor = tk.Label(ventana_graficos, text=f"Posición de la rana después del millonesimo salto: {posiciones[-1]}", font=("Helvetica", 12))
        etiqueta_ultimo_valor.pack()
        
        etiqueta_total_datos = tk.Label(ventana_graficos, text=f"Número total de datos: {len(posiciones)-1}", font=("Helvetica", 12))
        etiqueta_total_datos.pack()       

        # Agrega un botón para volver al menú
        boton_volver = tk.Button(ventana_graficos, text="Volver al Menú", command=lambda: self.volver_al_menu(ventana_graficos))
        boton_volver.pack(side="bottom", pady=10)

        self.ventana_principal.withdraw()

        # Muestra la ventana de gráficos
        ventana_graficos.wait_window(ventana_graficos)

    def distancia_euclidiana(self, punto_actual, punto_objetivo):
        """
        Calcula la distancia euclidiana entre dos puntos en un espacio n-dimensional.

        Args:
            punto_actual: Una lista que representa las coordenadas del punto actual.
            punto_objetivo: Una lista que representa las coordenadas del punto objetivo.

        Returns:
            La distancia euclidiana entre los dos puntos.
        """
        return np.linalg.norm(np.array(punto_objetivo) - np.array(punto_actual))
    
    def asignar_valor_segun_rango_2dim(self, valor):
        """
        Asigna un vector de dirección según un rango para dos dimensiones.

        Args:
            valor: El valor a asignar.

        Returns:
            Una lista que representa la dirección en el plano XY.
        """
        if 0 <= valor < 0.25:
            return [1, 0]  # Asignar 1 en X
        elif 0.25 <= valor < 0.5:
            return [0, 1]  # Asignar 1 en Y
        elif 0.5 <= valor < 0.75:
            return [-1, 0]  # Asignar -1 en X
        elif 0.75 <= valor <= 1:
            return [0, -1]  # Asignar -1 en Y
        else:
            raise ValueError("El valor debe estar en el rango [0, 1]")
        
    def asignar_valor_segun_rango_3dim(self, valor):
        """
        Asigna un vector de dirección según un rango para tres dimensiones.

        Args:
            valor: El valor a asignar.

        Returns:
            Una lista que representa la dirección en el espacio XYZ.
        """
        if 0 <= valor < 0.167:
            return [1, 0, 0]  # Asignar 1 en X
        elif 0.167 <= valor < 0.333:
            return [-1, 0, 0]  # Asignar -1 en X
        elif 0.333 <= valor < 0.5:
            return [0, 1, 0]  # Asignar 1 en Y
        elif 0.5 <= valor < 0.667:
            return [0, -1, 0]  # Asignar -1 en Y
        elif 0.667 <= valor < 0.833:
            return [0, 0, 1]  # Asignar 1 en Z
        elif 0.833 <= valor <= 1:
            return [0, 0, -1]  # Asignar -1 en Z
        else:
            raise ValueError("El valor debe estar en el rango [0, 1]")

    def simular_hasta_posicion_objetivo(self, dimensions, objetivo, numeros_pseudoaleatorios):
        """
        Simula el movimiento de la rana en un espacio bidimensional hasta alcanzar el objetivo.

        Args:
            dimensions: El número de dimensiones (en este caso, 2).
            objetivo: Una lista que representa las coordenadas del punto objetivo.
            numeros_pseudoaleatorios: Una lista de números pseudoaleatorios.

        Returns:
            El número de saltos realizados y una lista de posiciones de la rana.
        """
        posicion_actual = [0] * dimensions
        brincos = 0
        posiciones = [posicion_actual.copy()]  

        while self.distancia_euclidiana(posicion_actual, objetivo) > 0:
            if not numeros_pseudoaleatorios:
                break  # Si no hay más números pseudoaleatorios disponibles, sal del bucle
            brinco = self.asignar_valor_segun_rango_2dim(numeros_pseudoaleatorios[0])
            numeros_pseudoaleatorios = numeros_pseudoaleatorios[1:] 
            posicion_actual = [posicion_actual[i] + brinco[i] for i in range(dimensions)]
            brincos += 1
            posiciones.append(posicion_actual)  
            #print(posicion_actual)

        return brincos, posiciones
    
    def simular_hasta_posicion_objetivo_3dim(self, dimensions, objetivo, numeros_pseudoaleatorios):
        """
        Simula el movimiento de la rana en un espacio tridimensional hasta alcanzar el objetivo.

        Args:
            dimensions: El número de dimensiones (en este caso, 3).
            objetivo: Una lista que representa las coordenadas del punto objetivo.
            numeros_pseudoaleatorios: Una lista de números pseudoaleatorios.

        Returns:
            El número de saltos realizados y una lista de posiciones de la rana.
        """
        # Inicializa la posición actual de la rana en el espacio tridimensional
        posicion_actual = [0] * dimensions
        brincos = 0
        # Inicializa una lista de posiciones con la posición inicial de la rana
        posiciones = [posicion_actual.copy()]  
        # Inicia un bucle mientras la rana no haya alcanzado el objetivo
        while self.distancia_euclidiana(posicion_actual, objetivo) > 0:
            if not numeros_pseudoaleatorios:
                break  # Si no hay más números pseudoaleatorios disponibles, sal del bucle
            # Genera un salto aleatorio para la rana en el espacio tridimensional
            brinco = self.asignar_valor_segun_rango_3dim(numeros_pseudoaleatorios[0])
            # Elimina el primer número pseudoaleatorio utilizado de la lista
            numeros_pseudoaleatorios = numeros_pseudoaleatorios[1:]  
             # Actualiza la posición actual de la rana sumando el salto generado
            posicion_actual = [posicion_actual[i] + brinco[i] for i in range(dimensions)]
            brincos += 1
            # Añade la nueva posición de la rana a la lista de posiciones
            posiciones.append(posicion_actual)  
            #print(posicion_actual)
        # Retorna el número total de saltos realizados y la lista de posiciones de la rana
        return brincos, posiciones


    def mostrar_simulacion_dim2(self):
        """
        Muestra la simulación en dos dimensiones.
        """
        dimensiones_2D = 2
        posicion_objetivo_2D = [250, 300]

        # Obtiene los números pseudoaleatorios
        archivo_csv = 'numeros_ri_final.csv'
        numeros_pseudoaleatorios = self.leer_csv(archivo_csv)

        #Empieza a medir el tiempo de procesamiento
        start_time = time.time()

        # Simulación
        brincos_2D, posiciones = self.simular_hasta_posicion_objetivo(dimensiones_2D, posicion_objetivo_2D, numeros_pseudoaleatorios)

        # Termina de medir el tiempo de procesamiento
        tiempo_procesamiento = time.time() - start_time

        # Crea una nueva ventana de gráficos
        ventana_graficos = tk.Toplevel(self.ventana_principal)
        ventana_graficos.title("Simulación 2D - Rana")
        ventana_graficos.attributes('-fullscreen', True)

        # Configura el espacio vertical entre los gráficos
        ventana_graficos.geometry("1200x800")

        # Gráfico de posiciones
        fig, ax = plt.subplots(figsize=(8, 6))
        for punto in posiciones:
            ax.scatter(punto[0], punto[1], color='blue')  # Scatter para cada punto
        ax.plot(*zip(*posiciones), color='red', linestyle='-', marker='')  # Unir los puntos con una línea roja

        # Configuración del gráfico
        ax.set_title('Movimiento de la Rana en 2D')
        ax.set_xlabel('Eje X')
        ax.set_ylabel('Eje Y')
        ax.axhline(y=posicion_objetivo_2D[1], color='r', linestyle='--', label='Objetivo Y')
        ax.axvline(x=posicion_objetivo_2D[0], color='g', linestyle='--', label='Objetivo X')
        ax.legend()

        # Crea el widget FigureCanvasTkAgg
        canvas = FigureCanvasTkAgg(fig, master=ventana_graficos)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Agrega las etiquetas para mostrar información
        etiqueta_total_datos = tk.Label(ventana_graficos, text=f"Número total de datos: {len(posiciones)-1}", font=("Helvetica", 12))
        etiqueta_total_datos.pack()

        # Se decide que mensaje mostrar, de acuerdo a si se llego al punto o no
        if self.distancia_euclidiana(posiciones[len(posiciones)-1], posicion_objetivo_2D) == 0:
            etiqueta_brincos = tk.Label(ventana_graficos, text=f"Saltos para llegar a: {posicion_objetivo_2D} en 2D: {brincos_2D}", font=("Helvetica", 12))
            etiqueta_brincos.pack()
        else:
            etiqueta_brincos = tk.Label(ventana_graficos, text=f"No llego a: {posicion_objetivo_2D} en 2D con: {brincos_2D} saltos, llego a {posiciones[len(posiciones)-1]}", font=("Helvetica", 12))
            etiqueta_brincos.pack()

        etiqueta_tiempo_procesamiento = tk.Label(ventana_graficos, text=f"Tiempo de procesamiento: {tiempo_procesamiento} segundos", font=("Helvetica", 12))
        etiqueta_tiempo_procesamiento.pack()

        # Agrega un botón para volver al menú
        boton_volver = tk.Button(ventana_graficos, text="Volver al Menú", command=lambda: self.volver_al_menu(ventana_graficos))
        boton_volver.pack(side="bottom", pady=10)

        self.ventana_principal.withdraw()

        # Muestra la ventana de gráficos
        ventana_graficos.mainloop()  


    def mostrar_simulacion_dim3(self):
        """
        Muestra la simulación en tres dimensiones.
        """
        dimensiones_3D = 3
        posicion_objetivo_3D = [45, 23, 17]

        # Obtiene los números pseudoaleatorios
        archivo_csv = 'numeros_ri_final.csv'
        numeros_pseudoaleatorios = self.leer_csv(archivo_csv)

        # Empieza a medir el tiempo de procesamiento
        start_time = time.time()

        # Simulación
        brincos_3D, posiciones = self.simular_hasta_posicion_objetivo_3dim(dimensiones_3D, posicion_objetivo_3D, numeros_pseudoaleatorios)

        # Termina de medir el tiempo de procesamiento
        tiempo_procesamiento = time.time() - start_time

        # Crea una nueva ventana de gráficos
        ventana_graficos = tk.Toplevel(self.ventana_principal)
        ventana_graficos.title("Simulación 3D - Rana")
        ventana_graficos.attributes('-fullscreen', True)

        # Configura el espacio vertical entre los gráficos
        ventana_graficos.geometry("1200x800")

        # Gráfico de posiciones en 3D
        fig = plt.figure(figsize=(8, 6))
        ax = fig.add_subplot(111, projection='3d')

        # Desempaqueta las coordenadas x, y, z
        x, y, z = zip(*posiciones)

        # Scatter para cada punto, asignando el color azul
        ax.scatter(x, y, z, color='blue')

        # Une los puntos con una línea roja
        ax.plot(x, y, z, color='red', linestyle='-', marker='')

        # Configuración del gráfico
        ax.set_title('Movimiento de la Rana en 3D')
        ax.set_xlabel('Eje X')
        ax.set_ylabel('Eje Y')
        ax.set_zlabel('Eje Z')
        ax.scatter(posicion_objetivo_3D[0], posicion_objetivo_3D[1], posicion_objetivo_3D[2], color='green', marker='x', label='Objetivo 3D')
        ax.legend()

        # Crea el widget FigureCanvasTkAgg
        canvas = FigureCanvasTkAgg(fig, master=ventana_graficos)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Agrega etiquetas para mostrar información
        
        # Se decide que mensaje mostrar, de acuerdo a si se llego al punto o no
        if self.distancia_euclidiana(posiciones[len(posiciones)-1], posicion_objetivo_3D) == 0:
            etiqueta_brincos = tk.Label(ventana_graficos, text=f"Brincos para llegar a: {posicion_objetivo_3D} en 3D: {brincos_3D}", font=("Helvetica", 12))
            etiqueta_brincos.pack()
        else:
            etiqueta_brincos = tk.Label(ventana_graficos, text=f"No llego a: {posicion_objetivo_3D} en 3D con: {brincos_3D} saltos, llego a {posiciones[len(posiciones)-1]}", font=("Helvetica", 12))
            etiqueta_brincos.pack()

        
        etiqueta_tiempo_procesamiento = tk.Label(ventana_graficos, text=f"Tiempo de procesamiento: {tiempo_procesamiento} segundos", font=("Helvetica", 12))
        etiqueta_tiempo_procesamiento.pack()

        # Agrega un botón para volver al menú
        boton_volver = tk.Button(ventana_graficos, text="Volver al Menú", command=lambda: self.volver_al_menu(ventana_graficos))
        boton_volver.pack(side="bottom", pady=10)

        #Oculta la ventana principal
        self.ventana_principal.withdraw()

        # Muestra la ventana de gráficos
        ventana_graficos.mainloop() 


if __name__ == "__main__":
    # Crea una instancia de la clase Tk de tkinter para la ventana principal de la aplicación
    ventana_principal = tk.Tk()
    # Crea una instancia del simulador de la rana, pasando la ventana principal como argumento
    simulador = SimuladorRana(ventana_principal)
    # Inicia el bucle principal de la interfaz gráfica de usuario
    ventana_principal.mainloop()
