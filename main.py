import tkinter as tk
import random

# Constantes para el juego
DIRECCIONES = {
    "Left": (-1, 0),
    "Right": (1, 0),
    "Up": (0, -1),
    "Down": (0, 1),
}

class MenuInicio:
    def __init__(self, root):
        self.root = root
        self.root.title("Menú de Inicio")

        # Variables para almacenar las opciones seleccionadas por el usuario
        self.tamaño = tk.StringVar()
        self.nivel = tk.IntVar()
        self.trampas = tk.BooleanVar()

        # Configuración inicial de las variables
        self.tamaño.set("300x300")
        self.nivel.set(5)
        self.trampas.set(False)

        # Crear elementos del menú
        tk.Label(root, text="Tamaño del tablero:").pack()
        tk.Radiobutton(root, text="300x300", variable=self.tamaño, value="300x300").pack()
        tk.Radiobutton(root, text="400x400", variable=self.tamaño, value="400x400").pack()
        tk.Radiobutton(root, text="500x500", variable=self.tamaño, value="500x500").pack()

        tk.Label(root, text="Nivel (1-10):").pack()
        tk.Scale(root, from_=1, to=10, orient="horizontal", variable=self.nivel).pack()

        tk.Checkbutton(root, text="Jugar con trampas", variable=self.trampas).pack()

        tk.Button(root, text="Iniciar Juego", command=self.iniciar_juego).pack()

    def iniciar_juego(self):
        # Obtener las opciones seleccionadas por el usuario y cerrar el menú
        tamaño = self.tamaño.get()
        nivel = self.nivel.get()
        trampas = self.trampas.get()
        self.root.destroy()

        # Iniciar el juego con las opciones seleccionadas
        root = tk.Tk()
        game = JuegoSerpiente(root, tamaño, nivel, trampas)
        root.mainloop()

class JuegoSerpiente:
    def __init__(self, root, tamaño, nivel, trampas):
        self.root = root
        self.root.title("Juego de la Serpiente")
        self.canvas = tk.Canvas(root, width=int(tamaño.split('x')[0]), height=int(tamaño.split('x')[1]), bg="black")
        self.canvas.pack()

        # Configurar variables del juego
        self.ancho = int(tamaño.split('x')[0])
        self.alto = int(tamaño.split('x')[1])
        self.tamaño_serpiente = 10
        self.tamaño_comida = 10
        self.velocidad_base = 550 - nivel * 50  # Ajustar la velocidad según el nivel
        self.trampas = trampas
        self.velocidad = self.velocidad_base

        # Resto del código del juego...
        
        # Marcador de velocidad
        self.velocidad_label = tk.Label(root, text=f"Velocidad: {self.velocidad}")
        self.velocidad_label.pack()

        # Marcador de puntuación
        self.puntuacion_label = tk.Label(root, text="Puntuación: 0")
        self.puntuacion_label.pack()

        self.serpiente = [(self.ancho // 2, self.alto // 2)]  # Posición inicial de la serpiente
        self.direccion = "Right"  # Dirección inicial
        self.comida = self.crear_comida()  # Crear la primera comida

        self.en_ejecucion = True  # El juego está en ejecución
        self.puntuacion = 0  # Puntuación inicial

        # Vincular las teclas de dirección al método de cambio de dirección
        self.root.bind("<KeyPress>", self.cambiar_direccion)

        self.actualizar()  # Iniciar la actualización del juego
        
    def crear_comida(self):
        # Crear comida en una posición aleatoria dentro del canvas
        x = random.randint(0, (self.ancho - self.tamaño_comida) // self.tamaño_serpiente) * self.tamaño_serpiente
        y = random.randint(0, (self.alto - self.tamaño_comida) // self.tamaño_serpiente) * self.tamaño_serpiente
        return (x, y)

    def cambiar_direccion(self, event):
        # Cambiar la dirección de la serpiente según la tecla presionada
        tecla = event.keysym  # Obtener la tecla presionada
        if tecla in DIRECCIONES:
            nueva_direccion = DIRECCIONES[tecla]
            direccion_actual = DIRECCIONES[self.direccion]

            # Evitar moverse en dirección opuesta a la actual
            if (
                nueva_direccion[0] != -direccion_actual[0]
                or nueva_direccion[1] != -direccion_actual[1]
            ):
                self.direccion = tecla

    def actualizar(self):
        if self.en_ejecucion:
            self.mover_serpiente()  # Mover la serpiente en la dirección actual
            if self.comprobar_colision():  # Verificar colisiones
                self.en_ejecucion = False
                self.fin_del_juego()  # Mostrar mensaje de fin del juego
            else:
                self.canvas.delete("all")  # Limpiar el canvas
                self.dibujar_serpiente()  # Dibujar la serpiente
                self.dibujar_comida()  # Dibujar la comida
                self.velocidad_label.config(text=f"Velocidad: {self.velocidad}")  # Actualizar la etiqueta de la velocidad
                self.root.after(self.velocidad, self.actualizar)  # Llamar de nuevo después de un retraso

    def mover_serpiente(self):
        dx, dy = DIRECCIONES[self.direccion]  # Obtener el cambio en x e y según la dirección
        cabeza_x, cabeza_y = self.serpiente[0]  # Obtener la posición de la cabeza de la serpiente
        nueva_cabeza = (cabeza_x + dx * self.tamaño_serpiente, cabeza_y + dy * self.tamaño_serpiente)

        # Si se juega con trampas, manejar las salidas de la serpiente por los bordes
        if self.trampas:
            cabeza_x, cabeza_y = nueva_cabeza
            if cabeza_x < 0:
                nueva_cabeza = (self.ancho - self.tamaño_serpiente, cabeza_y)
            elif cabeza_x >= self.ancho:
                nueva_cabeza = (0, cabeza_y)
            elif cabeza_y < 0:
                nueva_cabeza = (cabeza_x, self.alto - self.tamaño_serpiente)
            elif cabeza_y >= self.alto:
                nueva_cabeza = (cabeza_x, 0)

        # Verificar si la serpiente comió la comida
        if nueva_cabeza == self.comida:
            self.serpiente.insert(0, nueva_cabeza)  # Agregar a la cabeza
            self.comida = self.crear_comida()  # Crear nueva comida
            self.puntuacion += 1  # Incrementar la puntuación
            self.puntuacion_label.config(text=f"Puntuación: {self.puntuacion}")  # Actualizar la etiqueta de la puntuación
            self.velocidad -= 50  # Aumentar la velocidad
            if self.velocidad < 50:  # Evitar que la velocidad sea menor que 50
                self.velocidad = 50
        else:
            # Si no comió, mover la cabeza y mantener la cola
            self.serpiente.pop()  # Eliminar la cola
            self.serpiente.insert(0, nueva_cabeza)

            # Si se juega con trampas, verificar nuevamente las salidas de la serpiente por los bordes
            if self.trampas:
                cabeza_x, cabeza_y = nueva_cabeza
                if cabeza_x < 0:
                    nueva_cabeza = (self.ancho - self.tamaño_serpiente, cabeza_y)
                elif cabeza_x >= self.ancho:
                    nueva_cabeza = (0, cabeza_y)
                elif cabeza_y < 0:
                    nueva_cabeza = (cabeza_x, self.alto - self.tamaño_serpiente)
                elif cabeza_y >= self.alto:
                    nueva_cabeza = (cabeza_x, 0)

                self.serpiente[0] = nueva_cabeza

    def comprobar_colision(self):
        cabeza_x, cabeza_y = self.serpiente[0]

        # Verificar colisiones con los bordes del canvas si no se juega con trampas
        if not self.trampas:
            if cabeza_x < 0 or cabeza_x >= self.ancho or cabeza_y < 0 or cabeza_y >= self.alto:
                return True

        # Verificar colisiones consigo misma
        if self.serpiente[0] in self.serpiente[1:]:
            return True

        return False

    def dibujar_serpiente(self):
        for x, y in self.serpiente:
            self.canvas.create_rectangle(x, y, x + self.tamaño_serpiente, y + self.tamaño_serpiente, fill="green")

    def dibujar_comida(self):
        x, y = self.comida
        self.canvas.create_rectangle(x, y, x + self.tamaño_comida, y + self.tamaño_comida, fill="red")

    def fin_del_juego(self):
        # Mostrar mensaje de fin del juego en el canvas
        self.canvas.create_text(
            self.ancho // 2, self.alto // 2,
            text="Game Over",
            fill="white",
            font=("Helvetica", 16)
        )
        print(f"Game Over. Puntuación: {self.puntuacion}")

# Crear y mostrar el menú de inicio
root_menu = tk.Tk() 
menu = MenuInicio(root_menu)
root_menu.mainloop()
