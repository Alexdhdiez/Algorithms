"""Alejandro del Hierro"""
"""Algoritmos y Computación, Universidad de Valladolid"""
"""Curso 2018-2019"""
import numpy
import random
from scipy.stats import binom
from time import time
import itertools
import os
random.seed()

def leer(ruta):
    datos = numpy.genfromtxt(ruta, delimiter=" ",missing_values=".",filling_values=0,dtype=int)
    return numpy.array(datos)

def guardar(ruta, solucion):
    numpy.savetxt("ruta", solucion, delimiter=" ",fmt='%d')
    return

def valido(individuo, numero, fil, col):
    """Comprueba si un digito introducido no se ha introducido ya antes en el mismo bloque"""
    for i in range(fil,fil+3):
        for j in range (col,col+3):
            if (individuo[i][j] == numero):
                return False
    return True

def crear_indiv(objetivo):
    """Crea un individuo introducienddo una permutacion de los 9 posibles digitos en cada bloque, sin cambiar los ya fijados"""
    indiv = numpy.copy(objetivo)

    for i in range (0,9,3):
        for j in range (0,9,3):
            posibles = [1,2,3,4,5,6,7,8,9]
            #En cada bloque se genera una permutacion
            if(indiv[i][j]==0):
                num = posibles[random.randint(0,len(posibles)-1)]
                #Escoge un numero de los posibles
                while(not valido(indiv,num,i,j)):
                    num = posibles[random.randint(0,len(posibles)-1)]
                indiv[i][j] = num
                posibles.pop(posibles.index(num))#Eliminamos el numero que ya hemos metido

            else:
                posibles.pop(posibles.index(indiv[i][j]))

            if(indiv[i][j+1]==0):
                num = posibles[random.randint(0,len(posibles)-1)]
                while(not valido(indiv,num,i,j)):
                    num = posibles[random.randint(0,len(posibles)-1)]
                indiv[i][j+1] = num
                posibles.pop(posibles.index(num))
            else:
                posibles.pop(posibles.index(indiv[i][j+1]))

            if(indiv[i][j+2]==0):
                num = posibles[random.randint(0,len(posibles)-1)]
                while(not valido(indiv,num,i,j)):
                    num = posibles[random.randint(0,len(posibles)-1)]
                indiv[i][j+2] = num
                posibles.pop(posibles.index(num))
            else:
                posibles.pop(posibles.index(indiv[i][j+2]))

            if(indiv[i+1][j]==0):
                num = posibles[random.randint(0,len(posibles)-1)]
                while(not valido(indiv,num,i,j)):
                    num = posibles[random.randint(0,len(posibles)-1)]
                indiv[i+1][j] = num
                posibles.pop(posibles.index(num))
            else:
                posibles.pop(posibles.index(indiv[i+1][j]))

            if(indiv[i+1][j+1]==0):
                num = posibles[random.randint(0,len(posibles)-1)]
                while(not valido(indiv,num,i,j)):
                    num = posibles[random.randint(0,len(posibles)-1)]
                indiv[i+1][j+1] = num
                posibles.pop(posibles.index(num))
            else:
                posibles.pop(posibles.index(indiv[i+1][j+1]))

            if(indiv[i+1][j+2]==0):
                num = posibles[random.randint(0,len(posibles)-1)]
                while(not valido(indiv,num,i,j)):
                    num = posibles[random.randint(0,len(posibles)-1)]
                indiv[i+1][j+2] = num
                posibles.pop(posibles.index(num))
            else:
                posibles.pop(posibles.index(indiv[i+1][j+2]))

            if(indiv[i+2][j]==0):
                num = posibles[random.randint(0,len(posibles)-1)]
                while(not valido(indiv,num,i,j)):
                    num = posibles[random.randint(0,len(posibles)-1)]
                indiv[i+2][j] = num
                posibles.pop(posibles.index(num))
            else:
                posibles.pop(posibles.index(indiv[i+2][j]))

            if(indiv[i+2][j+1]==0):
                num = posibles[random.randint(0,len(posibles)-1)]
                while(not valido(indiv,num,i,j)):
                    num = posibles[random.randint(0,len(posibles)-1)]
                indiv[i+2][j+1] = num
                posibles.pop(posibles.index(num))
            else:
                posibles.pop(posibles.index(indiv[i+2][j+1]))

            if(indiv[i+2][j+2]==0):
                num = posibles[random.randint(0,len(posibles)-1)]
                while(not valido(indiv,num,i,j)):
                    num = posibles[random.randint(0,len(posibles)-1)]
                indiv[i+2][j+2] = num
                posibles.pop(posibles.index(num))
            else:
                posibles.pop(posibles.index(indiv[i+2][j+2]))

    return indiv


def f_fitness(individuo):
    """Mide el fitness de un individuo sumando los unicos de filas y de columnas. Maximo valor 162"""
    unicos_col = 0
    unicos_fil = 0

    #CUENTA UNICOS POR COLUMNA
    for i in range(0, 9):  #Para cada columna
        unicos_c = len(set(individuo[:,i]))
        unicos_col += unicos_c

    for i in range(0, 9):  #Para cada fila
        unicos_f = len(set(individuo[i,:]))
        unicos_fil += unicos_f

    fitness = unicos_col + unicos_fil
    return fitness


def ordenar(poblacion):
    poblacion.sort(key = lambda indiv: f_fitness(indiv), reverse = True)
    return poblacion


def cruce(padre, madre, p):
    """Intercambia unn numero de bloques entre dos progenitores para crear dos descendientes. Ocurre con probabilidad p"""
    copia_1 = numpy.copy(padre)
    copia_2 = numpy.copy(madre)
    nc = random.randint(0,4)
    if (binom.rvs(1, p) == 1):
        for n_blq_intercambiados in range(0,nc):
            #Aumentamos el numero de bloques que se intercambian
            p1_blq = 3*random.randint(0,2)
            p2_blq = 3*random.randint(0,2)

            while p1_blq == p2_blq:
                p2_blq = 3*random.randint(0,2)

            #Intercambio de bloques
            temp3 = copia_1[p1_blq:p1_blq+3,p2_blq:p2_blq+3]
            copia_1[p1_blq:p1_blq+3,p2_blq:p2_blq+3] = copia_2[p1_blq:p1_blq+3,p2_blq:p2_blq+3]
            copia_2[p1_blq:p1_blq+3,p2_blq:p2_blq+3] = temp3

    hijo_1 = copia_1
    hijo_2 = copia_2

    return hijo_1,hijo_2


def mutacion(indiv, p, objetivo):
    """Muta algunos de los digitos de un bloque aleatorio intercambiando dos digitos entre si. Ocurre con probabilidad p."""
    nm = random.randint(0,9)
    if (binom.rvs(1, p)==1): #Muta
        for i in range (0,nm):
            p1_blq = 3*random.randint(0,2)
            p2_blq = 3*random.randint(0,2)

            bloque = indiv[p1_blq:p1_blq+3,p2_blq:p2_blq+3]
            n1_i = random.randint(0,2)
            n1_j = random.randint(0,2)

            n2_i = random.randint(0,2)
            n2_j = random.randint(0,2)

            if(objetivo[p1_blq+n1_i][p2_blq+n1_j] == 0 and objetivo[p1_blq+n2_i][p2_blq+n2_j] == 0):
                temp = indiv[p1_blq+n1_i][p2_blq+n1_j]
                indiv[p1_blq+n1_i][p2_blq+n1_j] = indiv[p1_blq+n2_i][p2_blq+n2_j]
                indiv[p1_blq+n2_i][p2_blq+n2_j] = temp

    return indiv

def perturbar_bloque(poblacion,objetivo):
    """Cambia un bloque de todos los individuos de una poblacion por otro nuevo"""
    pob_pertur = []
    for indiv in poblacion:

        posibles = [1,2,3,4,5,6,7,8,9]
        i=random.choice([0,3,6])
        j=random.choice([0,3,6])

        indiv[i:i+3, j:j+3] = numpy.copy(objetivo[i:i+3, j:j+3])

        if(indiv[i][j]==0):
            num = posibles[random.randint(0,len(posibles)-1)]
            #Escoge un numero de los posibles
            while(not valido(indiv,num,i,j)):
                num = posibles[random.randint(0,len(posibles)-1)]
            indiv[i][j] = num
            posibles.pop(posibles.index(num))#Eliminamos el numero que ya hemos metido

        else:
            posibles.pop(posibles.index(indiv[i][j]))

        if(indiv[i][j+1]==0):
            num = posibles[random.randint(0,len(posibles)-1)]
            while(not valido(indiv,num,i,j)):
                num = posibles[random.randint(0,len(posibles)-1)]
            indiv[i][j+1] = num
            posibles.pop(posibles.index(num))
        else:
            posibles.pop(posibles.index(indiv[i][j+1]))

        if(indiv[i][j+2]==0):
            num = posibles[random.randint(0,len(posibles)-1)]
            while(not valido(indiv,num,i,j)):
                num = posibles[random.randint(0,len(posibles)-1)]
            indiv[i][j+2] = num
            posibles.pop(posibles.index(num))
        else:
            posibles.pop(posibles.index(indiv[i][j+2]))

        if(indiv[i+1][j]==0):
            num = posibles[random.randint(0,len(posibles)-1)]
            while(not valido(indiv,num,i,j)):
                num = posibles[random.randint(0,len(posibles)-1)]
            indiv[i+1][j] = num
            posibles.pop(posibles.index(num))
        else:
            posibles.pop(posibles.index(indiv[i+1][j]))

        if(indiv[i+1][j+1]==0):
            num = posibles[random.randint(0,len(posibles)-1)]
            while(not valido(indiv,num,i,j)):
                num = posibles[random.randint(0,len(posibles)-1)]
            indiv[i+1][j+1] = num
            posibles.pop(posibles.index(num))
        else:
            posibles.pop(posibles.index(indiv[i+1][j+1]))

        if(indiv[i+1][j+2]==0):
            num = posibles[random.randint(0,len(posibles)-1)]
            while(not valido(indiv,num,i,j)):
                num = posibles[random.randint(0,len(posibles)-1)]
            indiv[i+1][j+2] = num
            posibles.pop(posibles.index(num))
        else:
            posibles.pop(posibles.index(indiv[i+1][j+2]))

        if(indiv[i+2][j]==0):
            num = posibles[random.randint(0,len(posibles)-1)]
            while(not valido(indiv,num,i,j)):
                num = posibles[random.randint(0,len(posibles)-1)]
            indiv[i+2][j] = num
            posibles.pop(posibles.index(num))
        else:
            posibles.pop(posibles.index(indiv[i+2][j]))

        if(indiv[i+2][j+1]==0):
            num = posibles[random.randint(0,len(posibles)-1)]
            while(not valido(indiv,num,i,j)):
                num = posibles[random.randint(0,len(posibles)-1)]
            indiv[i+2][j+1] = num
            posibles.pop(posibles.index(num))
        else:
            posibles.pop(posibles.index(indiv[i+2][j+1]))

        if(indiv[i+2][j+2]==0):
            num = posibles[random.randint(0,len(posibles)-1)]
            while(not valido(indiv,num,i,j)):
                num = posibles[random.randint(0,len(posibles)-1)]
            indiv[i+2][j+2] = num
            posibles.pop(posibles.index(num))
        else:
            posibles.pop(posibles.index(indiv[i+2][j+2]))

        pob_pertur.append(indiv)

    return pob_pertur


Tam_pob = 100 #Individuos por poblacion
N_gen = 1000
Ratio_sel = 0.05
N_elite = int(Ratio_sel*Tam_pob)
prob_recomb = 0.99
prob_selecc = numpy.linspace(1, 0, Tam_pob)/sum(numpy.linspace(1, 0, Tam_pob))
#Mayor probabilidad para los mejor adaptados

Regenerar = 10

def resolver(objetivo):
    antiguedad = 0
    prob_mut = 0.1

    """Creacion de una poblacion inicial"""
    poblacion = []
    for i in range(0, Tam_pob):
        poblacion.append(crear_indiv(objetivo))

    for generacion in range(0, N_gen):
        tiempo_inic = time()

        mayor_adap = 0

        """Recorrer poblacion en busca del individuo con mayor adaptacion para
        comprobar si es o no una solucion"""
        for c in range(0, Tam_pob):
            fitness = f_fitness(poblacion[c])
            if(fitness == 162): #Maximo valor de fitness posible
                print("Solucion encontrada en la generacion %d" % generacion)
                print(poblacion[c])
                return poblacion[c]

            if fitness > mayor_adap:
                mayor_adap = fitness

        print("Mejor adaptacion: %d" % mayor_adap)


        """Ordenacion de la poblacion en funcion de su funcion de adaptacion"""
        poblacion = ordenar(poblacion)

        nueva_pob = []
        if (antiguedad != Regenerar):

            """Seleccion de los mejor adaptados"""
            for elite in range(0, N_elite):
                nueva_pob.append(poblacion[elite])

        if (antiguedad == Regenerar):
            antiguedad = 0
            #Tasa variable de mutacion
            if prob_mut + 0.1 <=1:
                prob_mut += 0.1
            print("Catastrofe genetica, perturbaciones")
            #nueva_pob[random.randint(0, N_elite-1)] = crear_indiv(objetivo)
            nueva_pob = perturbar_bloque(poblacion,objetivo)

        else:

            for i in range(N_elite, Tam_pob, 2):
                """Seleccion de los individuos que se reproduciran"""
                selec = numpy.random.choice(numpy.linspace(0,Tam_pob-1, Tam_pob), size = 2, p = prob_selecc)

                padre = poblacion[int(selec[0])]
                madre = poblacion[int(selec[1])]

                hijo_1, hijo_2 = cruce(padre, madre, prob_recomb)

                hijo_1 = mutacion(hijo_1, prob_mut, objetivo)
                hijo_2 = mutacion(hijo_2, prob_mut, objetivo)

                nueva_pob.append(hijo_1)
                nueva_pob.append(hijo_2)

        poblacion = ordenar(nueva_pob)

        if(f_fitness(poblacion[0]) == mayor_adap):
            antiguedad += 1
        else:
            antiguedad = 0

        os.system("cls")
        print("Generacion %d" % generacion)
        print("Tiempo de cambio de generacion: ", time()-tiempo_inic," segundos")
        print(poblacion[0])

    return poblacion[0]

objetivo = leer("sudoku_facil.txt")

solucion = resolver(objetivo)
print("Mejor solucion obtenida:")
print(solucion)
print("fitness de la solución = ", f_fitness(solucion))
numpy.savetxt("sol_sudoku_facil.txt", solucion, delimiter=" ",fmt='%d')
