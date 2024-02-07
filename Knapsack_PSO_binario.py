import random
import numpy as np
import matplotlib.pyplot as plt

# Definición de la clase Partícula para representar una partícula en el enjambre
class Particula:
    def __init__(self, dimension):
        self.xi = np.random.randint(2, size=dimension)
        self.velocidad = np.random.rand(dimension)
        self.mejor_posicion = np.copy(self.xi)
        self.mejor_valor = -np.inf

    # Actualización de la velocidad mediante la ecuación original de PSO
    def actualizaVelocidad(self, mejor_posicion_global, w=0.5, c1=1.5, c2=1.5):
        r1, r2 = random.random(), random.random()
        self.velocidad = (w * self.velocidad +
                          c1 * r1 * (self.mejor_posicion - self.xi) +
                          c2 * r2 * (mejor_posicion_global - self.xi))

    # Actualización de la posición mediante el criterio de probabilidad
    # 0 -> rand() > S(v(t+1))
    # 1 -> rand() < S(v(t+1))
    def actualizaPosicion(self):
        self.xi = np.where(np.random.rand(len(self.velocidad)) < sigmoide(self.velocidad), 1, 0)

    # Evalúa la aptitud de la posible solución
    def fitness(self, valores, pesos, peso_mochila):
        valor_total = np.dot(self.xi, valores)
        peso_total = np.dot(self.xi, pesos)
        if peso_total <= peso_mochila:
            if valor_total > self.mejor_valor:
                self.mejor_valor = valor_total
                self.mejor_posicion = np.copy(self.xi)
            return valor_total
        return 0


# Función sigmoide para la actualización de la posición
# S = 1 / (1 + e^(v(t + 1)))
def sigmoide(x):
    return 1 / (1 + np.exp(-x))


# Función para ejecutar el algoritmo BPSO
def PSOBinario(valores, pesos, peso_mochila, particulas=30, iteraciones=100):
    numero_elementos = len(valores)
    particulas = [Particula(numero_elementos) for _ in range(particulas)]
    mejor_valor_global = -np.inf
    mejor_posicion_global = None

    for _ in range(iteraciones):
        for particula in particulas:
            valor = particula.fitness(valores, pesos, peso_mochila)
            if valor > mejor_valor_global:
                mejor_valor_global = valor
                mejor_posicion_global = np.copy(particula.xi)

            particula.actualizaVelocidad(mejor_posicion_global)
            particula.actualizaPosicion()

    return mejor_posicion_global, mejor_valor_global


if __name__ == "__main__":
    # Datos del problema de la mochila
    valores = [
        # Valores de los elementos
        360, 83, 59, 130, 431, 67, 230, 52, 93, 125, 670, 892, 600, 38, 48, 147,
        78, 256, 63, 17, 120, 164, 432, 35, 92, 110, 22, 42, 50, 323, 514, 28,
        87, 73, 78, 15, 26, 78, 210, 36, 85, 189, 274, 43, 33, 10, 19, 389, 276,
        312
    ]

    pesos = [
        # Pesos de los elementos
        7, 3, 30, 22, 80, 94, 11, 81, 70, 64, 59, 18, 13, 36, 3, 8, 15, 42, 9, 12,
        42, 47, 52, 32, 26, 48, 55, 6, 29, 84, 2, 4, 18, 56, 7, 29, 93, 44, 71,
        3, 86, 66, 31, 65, 14, 79, 20, 65, 52, 13
    ]
    peso_mochila = 850

    valores_obtenidos = []

    for semilla in range(30):
        # 30 semillas diferentes
        random.seed(semilla)
        np.random.seed(semilla)

        # Ejecución del BPSO
        mejor_posicion, mejor_valor = PSOBinario(valores, pesos, peso_mochila)

        valores_obtenidos.append(mejor_valor)

        # Resultados
        print("Semilla: ", semilla)
        print("La mejor solución encontrada tiene un valor total de:", mejor_valor)
        print("Los elementos seleccionados son:", mejor_posicion)

    mas_alto = max(valores_obtenidos)
    print("Valores obtenidos de las 30 iteraciones: ", valores_obtenidos)
    print("Mejor valor: ", mas_alto)

    plt.figure()
    plt.boxplot(valores_obtenidos)
    plt.suptitle("Mejores valores obtenidos")
    plt.title(mas_alto)
    plt.show()


