#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
tarea_2.py
------------

Tarea 2a: Dibujar un grafo utilizando métodos de optimización

Si bien estos métodos no son los que se utilizan en el dibujo de gráfos por computadora (son
algoritmos realmente muy complejos lo que se usan actualmente). Si da una idea de la utilidad de
los métodos de optimización en un problema divertido.

Obviamente el problema se encuentra muy simplificado para poder ser visto dentro de una práctica.

Para realizar este problema es ecesario contar con el módulo PIL (Python Image Library) instalada.
Si instalaste EPD o EPD free, no hay problema, PIL viene ya incluido. Si no, hay que instalarlo.

Para que funcione, este modulo debe de encontrarse en la misma carpeta que blocales.py (incluida en piazza)

"""

__author__ = 'Juan Manuel Cruz Luque'

import blocales
import random
import itertools
import math
import Image
import ImageDraw
import time
from math import exp


class problema_grafica_grafo(blocales.Problema):

    """
    Clase para un grafo simple no dirigido, únicamente para fines de graficación

    """

    def __init__(self, vertices, aristas, dimension_imagen=400):
        """
        Un grafo se define como un conjunto de vertices, en forma de lista (no conjunto, el orden es importante
        a la hora de graficar), y un conjunto (tambien en forma de lista) de pares ordenados de vertices, lo que
        forman las aristas.

        Igualmente es importante indicar la resolución de la imagen a mostrar (por default de 400x400 pixeles).

        @param vertices: Lista con el nombre de los vertices.
        @param aristas: Lista con pares de vertices, los cuales definen las aristas.
        @param dimension_imagen: Entero con la dimension de la imagen en pixeles (cuadrada por facilidad).

        """
        self.vertices = vertices
        self.aristas = aristas
        self.dim = dimension_imagen

    def estado_aleatorio(self):
        """
        Devuelve un estado aleatorio.

        Un estado para este problema de define como s = [s(1), s(2), ..., s(2*len(vertices))] en donde:

        s(i) \in {10, 11, ..., 390} es la posición en x del nodo i/2 si i es par, o la posicion en y del
        nodo (i-1)/2 si i es non (osease las parejas (x,y)).

        @return: Una tupla con las posiciones (x1, y1, x2, y2, ...) de cada vertice en la imagen.

        """
        return tuple(random.randint(10, self.dim - 10) for _ in range(2 * len(self.vertices)))

    def vecino_aleatorio(self, estado, dispersion=None):
        """
        Encuentra un vecino en forma aleatoria. En estea primera versión lo que hacemos es tomar un valor aleatorio,
        y sumarle o restarle uno al azar.

        Este es un vecino aleatorio muy malo. Por lo que deberás buscar como hacer un mejor vecino aleatorio y comparar
        las ventajas de hacer un mejor vecino en el algoritmo de temple simulado.

        @param estado: Una tupla con el estado.
        @param dispersion: Un flotante con el valor de dispersión para el vertice seleccionado

        @return: Una tupla con un estado vecino al estado de entrada.

        """

        """
        vecino = list(estado)
        i = random.randint(0, len(vecino) - 1)
        vecino[i] = max(
            10, min(self.dim - 10, vecino[i] + random.choice([-1, 1])))
        return vecino

        """

        #######################################################################
        #                          20 PUNTOS
        #######################################################################
        # Por supuesto que esta no es la mejor manera de generar vecino para este problema.
        #
        # Modifica la funcion para generar vecinos de tal manera que el vecino aleatorio se realice de
        # la siguiente manera:
        #
        #   1. Selecciona un vertice al azar.
        #   2. Obten dos números aleatorios al azar entre -1 y 1.
        #   3. Multiplicalos por el valor de la dispersión.
        #   4. Sumale dichos valores (redondeados) a los valores originales de
        #      la posicion en x y y de la posicion de la arista. tomando en cuenta
        #      los límites que tiene la imagen (en numero máximo de pixeles).
        #
        #
        # -- Comenta la función ya programada, programa inmediatamenta despues de este comentario
        #    tu solución. ¿Como integras esta dispersión para utilizar la temperatura del temple simulado?
        #    ¿Que resultados obtienes con el nuevo método? Comenta tus resultados.
        #
        # RESULTADOS
        #
        # ¿Como integras esta dispersión para utilizar la temperatura del temple simulado?
        #
        # Para integrar la temperatura en la dispersion utilizo la operacion modulo y la i que va
        # iterando de la siguiente manera: temperatura * i % dimension asi siempre obtengo una dispersion
        # en el rango de 0 a el tamano de la dimension de la imagen.
        #
        # ¿Que resultados obtienes con el nuevo método?
        #
        # Pues parece que el nuevo metodo funciona mejor se ven los vertices un poco mas dispersos
        # pero igualmente aveces se obtienen resultados bastantes parecidos adjunto dos imagenes una
        # con la funcion ya programada y la otra con la que programe.
        # NOTA: La imagen vecinos1 es con la funcion ya programada.

        #"""
        vecino = list(estado)

        c = 0

        while (c == 0):

            # Selecciona un vertice al azar.
            i = random.randint(0, len(vecino) - 1)
            while i % 2 != 0:
                i = random.randint(0, len(vecino) - 1)

            # Obten dos números aleatorios al azar entre -1 y 1.
            r1 = random.uniform(-1,1)
            r2 = random.uniform(-1,1)

            # Multiplicalos por el valor de la dispersión.
            #print 'Multiplicacion'
            r1 = r1 * dispersion
            r2 = r2 * dispersion
            #print r1
            #print r2

            # Sumale dichos valores (redondeados) a los valores originales de
            # la posicion en x y y de la posicion de la arista. tomando en cuenta
            # los límites que tiene la imagen (en numero máximo de pixeles).
            s1 = vecino[i] + round(r1)
            s2 = vecino[i + 1] + round(r2)
            if (s1 < self.dim and s1 >= 0) and (s2 < self.dim and s2 >= 0):
                vecino[i] = s1
                vecino[i + 1] = s2
                c += 1

        return vecino

        #"""

    def costo(self, estado):
        """
        Encuentra el costo de un estado. En principio el costo de un estado es la cantidad de veces que dos
        aristas se cruzan cuando se dibujan. Esto hace que el dibujo se organice para tener el menor numero
        posible de cruces entre aristas.

        @param: Una tupla con un estado

        @return: Un número flotante con el costo del estado.

        """

        # Inicializa fáctores lineales para los criterios más importantes
        # (default solo cuanta el criterio 1)
        K1 = 100.0
        K2 = 30.0
        K3 = 100.0
        K4 = 70.0

        # Genera un diccionario con el estado y la posición para facilidad
        estado_dic = self.estado2dic(estado)

        return (K1 * self.numero_de_cruces(estado_dic) +
                K2 * self.separacion_vertices(estado_dic) +
                K3 * self.angulo_aristas(estado_dic) +
                K4 * self.criterio_propio(estado_dic))

        # Como podras ver en los resultados, el costo inicial propuesto no hace figuras particularmente
        # bonitas, y esto es porque lo único que considera es el numero de cruces.
        #
        # Una manera de buscar mejores resultados es incluir en el costo el angulo entre dos aristas conectadas
        # al mismo vertice, dandole un mayor costo si el angulo es muy pequeño (positivo o negativo). Igualemtente
        # se puede penalizar el que dos nodos estén muy cercanos entre si en la gráfica
        #
        # Así, vamos a calcular el costo en tres partes, una es el numero de cruces (ya programada), otra
        # la distancia entre nodos (ya programada) y otro el angulo entre arista de cada nodo (para programar) y cada
        # uno de estos criterios hay que agregarlo a la función de costo con un peso. Por último, puedes mejor el
        #

    def numero_de_cruces(self, estado_dic):
        """
        Devuelve el numero de veces que dos aristas se cruzan en el grafo si se grafica como dice estado

        @param estado_dic: Diccionario cuyas llaves son los vértices del grafo y cuyos valores es una
                           tupla con la posición (x, y) de ese vértice en el dibujo.

        @return: Un número.

        """
        total = 0

        # Por cada arista en relacion a las otras (todas las combinaciones de
        # aristas)
        for (aristaA, aristaB) in itertools.combinations(self.aristas, 2):

            # Encuentra los valores de (x0A,y0A), (xFA, yFA) para los vartices de una arista
            # y los valores (x0B,y0B), (x0B, y0B) para los vertices de la otra
            # arista
            (x0A, y0A), (xFA, yFA) = estado_dic[
                aristaA[0]], estado_dic[aristaA[1]]
            (x0B, y0B), (xFB, yFB) = estado_dic[
                aristaB[0]], estado_dic[aristaB[1]]

            # Utilizando la clasica formula para encontrar interseccion entre dos lineas
            # cuidando primero de asegurarse que las lineas no son paralelas (para evitar la
            # división por cero)
            den = (xFA - x0A) * (yFB - y0B) - (xFB - x0B) * (yFA - y0A) + 0.0
            if den == 0:
                continue

            # Y entonces sacamos el largo del cruce, normalizado por den. Esto significa que en 0
            # se encuentran en la primer arista y en 1 en la última. Si los puntos de cruce de ambas
            # lineas se encuentran en valores entre 0 y 1, significa que se
            # cruzan
            puntoA = (
                (xFB - x0B) * (y0A - y0B) - (yFB - y0B) * (x0A - x0B)) / den
            puntoB = (
                (xFA - x0A) * (y0A - y0B) - (yFA - y0A) * (x0A - x0B)) / den

            if 0 < puntoA < 1 and 0 < puntoB < 1:
                total += 1
        return total

    def separacion_vertices(self, estado_dic, min_dist=50):
        """
        A partir de una posicion "estado" devuelve una penalización proporcional a cada par de vertices que se
        encuentren menos lejos que min_dist. Si la distancia entre vertices es menor a min_dist, entonces calcula una
        penalización proporcional a esta.

        @param estado_dic: Diccionario cuyas llaves son los vértices del grafo y cuyos valores es una
                           tupla con la posición (x, y) de ese vértice en el dibujo.
        @param min_dist: Mínima distancia aceptable en pixeles entre dos vértices en el dibujo.

        @return: Un número.

        """
        total = 0
        for (v1, v2) in itertools.combinations(self.vertices, 2):
            # Calcula la distancia entre dos vertices
            (x1, y1), (x2, y2) = estado_dic[v1], estado_dic[v2]
            dist = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

            # Penaliza la distancia si es menor a min_dist
            if dist < min_dist:
                total += (1.0 - (dist / min_dist))
        return total

    def angulo_aristas(self, estado_dic):
        """
        A partir de una posicion "estado", devuelve una penalizacion proporcional a cada angulo entre aristas
        menor a pi/6 rad (30 grados). Los angulos de pi/6 o mayores no llevan ninguna penalización, y la penalizacion
        crece conforme el angulo es menor.

        @param estado_dic: Diccionario cuyas llaves son los vértices del grafo y cuyos valores es una
                           tupla con la posición (x, y) de ese vértice en el dibujo.

        @return: Un número.

        """
        #######################################################################
        #                          20 PUNTOS
        #######################################################################
        # Agrega el método que considere el angulo entre aristas de cada vertice. Dale diferente peso a cada criterio
        # hasta lograr que el sistema realice gráficas "bonitas"
        #
        # ¿Que valores de diste a K1, K2 y K3 respectivamente?
        #
        # K1 = 100.0
        # K2 = 30.0
        # K3 = 100.0
        #
        # Pienso que deben de tener mucho mas prioridad el numero de cruces y el angulo entre aristas ya
        # que la separacion de vertices el vecino aleatorio hace su trabajo y la mayoria de las veces
        # salen bastante dispersos.
        #
        # ------ IMPLEMENTA AQUI TU CÓDIGO ------------------------------------
        #

        costo = 0

        for v in self.vertices:
            lista_incidencias = []
            for a in self.aristas:
                if v == a[0] or v == a[1]:
                    lista_incidencias.append(a)
            #print 'Incide'
            for v1, v2 in itertools.combinations(lista_incidencias, 2):
                #print v1, v2
                t1 = estado_dic[v1[0]]
                t2 = estado_dic[v1[1]]
                t3 = estado_dic[v2[0]]
                t4 = estado_dic[v2[1]]
                """
                print estado_dic
                print t1
                print t2
                print t3
                print t4

                """
                ox = None
                oy = None
                cx1 = None
                cy1 = None
                cx2 = None
                cy2 = None

                if t1 == t3:
                    #print 'c1'
                    ox = t1[0]
                    oy = t1[1]
                    cx1 = t2[0]
                    cy1 = t2[1]
                    cx2 = t4[0]
                    cy2 = t4[1]

                if t1 == t4:
                    #print 'c2'
                    ox = t1[0]
                    oy = t1[1]
                    cx1 = t2[0]
                    cy1 = t2[1]
                    cx2 = t3[0]
                    cy2 = t3[1]

                if t2 == t3:
                    #print 'c3'
                    ox = t2[0]
                    oy = t2[1]
                    cx1 = t1[0]
                    cy1 = t1[1]
                    cx2 = t4[0]
                    cy2 = t4[1]

                if t2 == t4:
                    #print 'c4'
                    ox = t2[0]
                    oy = t2[1]
                    cx1 = t1[0]
                    cy1 = t1[1]
                    cx2 = t3[0]
                    cy2 = t3[1]
                """
                print ox
                print oy
                print cx1
                print cy1
                print cx2
                print cy2

                """
                vx1 = cx1 - ox
                vy1 = cy1 - oy
                vx2 = cx2 - ox
                vy2 = cy2 - oy
                """
                print 'Coordenadas vectores'
                print vx1
                print vy1
                print vx2
                print vy2

                """
                producto_punto = ((vx1 * vx2) + (vy1 * vy2))
                r1 = math.sqrt((vx1 * vx1) + (vy1 * vy1)) + 0.01
                r2 = math.sqrt((vx2 * vx2) + (vy2 * vy2)) + 0.01
                """
                print 'Producto punto ', producto_punto
                print 'r1 ', r1
                print 'r2 ', r2

                """
                resultado = abs(producto_punto/(r1*r2))
                #print 'Resultado ', resultado
                angulo = math.acos(resultado)
                #print 'Angulo ', angulo
                condicion = math.pi/6
                if angulo < condicion:
                    costo += 1
        return costo
        #return 0

    def criterio_propio(self, estado_dic):
        """
        Implementa y comenta correctamente un criterio de costo que sea conveniente para que un grafo
        luzca bien.

        @param estado_dic: Diccionario cuyas llaves son los vértices del grafo y cuyos valores es una
                           tupla con la posición (x, y) de ese vértice en el dibujo.

        @return: Un número.

        """
        #######################################################################
        #                          20 PUNTOS
        #######################################################################
        # ¿Crees que hubiera sido bueno incluir otro criterio? ¿Cual?
        #
        # Si, pues en algunos grafos se cargan mucho los vertices a cierto cuadrante de la imagen
        # dejando mucho espacio en blanco si dividieramos la cantidad de vertices entre cuatro y los
        # acomodaramos en cada cuadrante pienso que se podria ver mejor la imagen.
        #
        # Desarrolla un criterio propio y ajusta su importancia en el costo total con K4 ¿Mejora el resultado? ¿En
        # que mejora el resultado final?
        #
        # Si, se cargan mas equitativamente los vertices en la imagen igual adjunto dos imagenes.
        # NOTA: La imagen CP1 es el grafo sin mi criterio.
        #
        # ------ IMPLEMENTA AQUI TU CÓDIGO ------------------------------------
        #

        #print estado_dic
        c1 = 0
        c2 = 0
        c3 = 0
        c4 = 0
        dim = self.dim

        for v in self.vertices:

            #print v
            a,b = estado_dic[v]
            #print a,b

            if a <= dim/2 and b <= dim/2:
                c1 += 1

            if a <= dim and b <= dim/2:
                c2 += 1

            if a <= dim/2 and b <= dim:
                c3 += 1

            if a <= dim and b <= dim:
                c4 += 1

        total = 0
        nvertices = round(len(self.vertices) / 4)
        #print nvertices

        if c1 > nvertices:
            total += abs(nvertices - c1)

        if c2 > nvertices:
            total += abs(nvertices - c1)

        if c3 > nvertices:
            total += abs(nvertices - c1)

        if c4 > nvertices:
            total += abs(nvertices - c1)

        #print total

        return total
        #return 0

    def estado2dic(self, estado):
        """
        Convierte el estado en forma de tupla a un estado en forma de diccionario

        @param: Una tupla con las posiciones (x1, y1, x2, y2, ...)

        @return: Un diccionario cuyas llaves son el nombre de cada arista y su valor es una tupla (x, y)

        """
        return {self.vertices[i]: (estado[2 * i], estado[2 * i + 1]) for i in range(len(self.vertices))}

    def dibuja_grafo(self, estado=None):
        """
        Dibuja el grafo utilizando PIL, donde estado es una
        lista de dimensión 2*len(vertices), donde cada valor es
        la posición en x y y respectivamente de cada vertice. dim es
        la dimensión de la figura en pixeles.

        Si no existe una posición, entonces se obtiene una en forma
        aleatoria.

        """
        if not estado:
            estado = self.estado_aleatorio()

        # Diccionario donde lugar[vertice] = (posX, posY)
        lugar = self.estado2dic(estado)

        # Abre una imagen y para dibujar en la imagen
        # Imagen en blanco
        imagen = Image.new('RGB', (self.dim, self.dim), (255, 255, 255))
        dibujar = ImageDraw.ImageDraw(imagen)

        for (v1, v2) in self.aristas:
            dibujar.line((lugar[v1], lugar[v2]), fill=(255, 0, 0))

        for v in self.vertices:
            dibujar.text(lugar[v], v, (0, 0, 0))

        imagen.show()


def main():
    """
    La función principal

    """

    # Vamos a definir un grafo sencillo
    vertices_sencillo = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    aristas_sencillo = [('B', 'G'),
                        ('E', 'F'),
                        ('H', 'E'),
                        ('D', 'B'),
                        ('H', 'G'),
                        ('A', 'E'),
                        ('C', 'F'),
                        ('H', 'B'),
                        ('F', 'A'),
                        ('C', 'B'),
                        ('H', 'F')]
    dimension = 400

    # Y vamos a hacer un dibujo del grafo sin decirle como hacer para
    # ajustarlo.
    grafo_sencillo = problema_grafica_grafo(
        vertices_sencillo, aristas_sencillo, dimension)

    estado_aleatorio = grafo_sencillo.estado_aleatorio()
    grafo_sencillo.dibuja_grafo(estado_aleatorio)
    print "Costo del estado aleatorio: ", grafo_sencillo.costo(estado_aleatorio)

    # Ahora vamos a encontrar donde deben de estar los puntos
    """
    tiempo_inicial = time.time()
    solucion = blocales.temple_simulado(
        grafo_sencillo, lambda i: 1000 * math.exp(-0.0010 * i))
    tiempo_final = time.time()
    grafo_sencillo.dibuja_grafo(solucion)
    print "\nUtilizando una calendarización exponencial con K = 1000 y delta = 0.0001"
    print "Costo de la solución encontrada: ", grafo_sencillo.costo(solucion)
    print "Tiempo de ejecución en segundos: ", tiempo_final - tiempo_inicial

    """
    ##########################################################################
    #                          20 PUNTOS
    ##########################################################################
    # ¿Que valores para ajustar el temple simulado (T0 y K) son los que mejor resultado dan?
    #
    # Pues en cuanto a resultados las variaciones que hice me arrojan buenos grafos la diferencia importante
    # se noto en el tiempo. Aumente el T0 y tardaba demasiado tiempo. al delta lo reduje y me arrojaba grafos
    # con costo mayor a cero pero "bonitos". El ajuste que me gusto fue el original con una variacion en el delta
    # al cual le puse el valor de 0.0010. El ajuste inicial tardaba mas de un minuto y en todas las corridas que hice
    # me dio un costo de cero. Pero en el nuevo ajuste se hacen los grafos con costo cero y en un tiempo menor a diez segundos.
    #
    # ¿Que encuentras en los resultados?, ¿Cual es el criterio mas importante?
    #
    # Me gustan los resultados, el criterio mas importante a mi parecer es el angulo entre aristas se me hace que se ven
    # muy mal los grafos sin este criterio.

    ##########################################################################
    #                          20 PUNTOS
    ##########################################################################
    # En general para obtener mejores resultados del temple simulado, es necesario utilizar una
    # función de calendarización acorde con el metodo en que se genera el vecino aleatorio.
    # Existen en la literatura varias combinaciones. Busca en la literatura diferentes métodos de
    # calendarización (al menos uno más diferente al exponencial) y ajusta los parámetros
    # para que obtenga la mejor solución posible en el menor tiempo posible.
    #
    # Escribe aqui tus comentarios y prueba otro metodo de claendarización para compararlo con el
    # exponencial.
    #
    # Pues no me gustaron los resultados con el calendarizador de boltzmann me arroja
    # grafos con costo cero pero no tan "bonitos" que con el temple simulado se nota bastante la forma
    # en como se forman los vecinos. Estuve probando varios ajustes
    # para reducir el tiempo. Probe aumentar el delta pero al aumentarlo me daba grafos con costos mayor a cero.
    # el mejor delta que pude encontrar es con valor de 0.15 en el cual me da grafos con costo cero pero con tiempo
    # entre treinta y cuarenta segundos. igual adjunto dos imagenes de los grafos obtenidos. El de boltzmann
    # con costo cero tardo 37 segundos y el exponencial con costo cero tardo 8 segundos.
    #
    # ------ IMPLEMENTA AQUI TU CÓDIGO ---------------------------------------
    #
    #"""

    #"""
    tiempo_inicial = time.time()
    solucion = blocales.temple_simulado(
        grafo_sencillo, lambda i: cal_boltzmann(i, 1000, 0.15))
    tiempo_final = time.time()
    grafo_sencillo.dibuja_grafo(solucion)
    print "\nUtilizando una calendarización boltzmann con K = 1000 y delta = 0.15"
    print "Costo de la solución encontrada: ", grafo_sencillo.costo(solucion)
    print "Tiempo de ejecución en segundos: ", tiempo_final - tiempo_inicial

    #"""

def cal_boltzmann(iteracion, K=100, delta=0.01):
    """
    Calendarizador boltzman

    Aplica la formula temperatura = exp(-delta / k * iteracion)

    @param iteracion: Un entero con la iteración (empezando por 0)
    @param K: Valor de temperatura en la primer iteración
    @param delta: Variación exponencial (4 veces delta es .1 el valor de K)

    @return: Un flotante con la temperatura a esa iteración

    """
    return exp(-delta / K * iteracion)

if __name__ == '__main__':
    main()