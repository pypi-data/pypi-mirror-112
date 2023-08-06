import numpy as np
import pandas as pd


def obtener_valor_promediado_para_distancia_a_objeto(arreglo, indice, tamanio_intervalo):
    if indice - tamanio_intervalo < 0:
        left = arreglo[0:indice]
    else:
        left = arreglo[(indice - tamanio_intervalo):indice]
    if indice + tamanio_intervalo > len(arreglo):
        right = arreglo[(indice + 1):len(arreglo)]
    else:
        right = arreglo[indice + 1:(indice + tamanio_intervalo) + 1]
    arreglo_final = left + [arreglo[indice]] + right
    promedio = sum(arreglo_final) / len(arreglo_final)
    return promedio


def obtener_arreglo_con_valores_promediados_para_distancia_a_objeto(arreglo, tamanio_intervalo):
    arreglo_con_promedio = []
    for i in range(len(arreglo)):
        valor_promediado = obtener_valor_promediado_para_distancia_a_objeto(arreglo, i, tamanio_intervalo)
        arreglo_con_promedio.append(valor_promediado)
    return arreglo_con_promedio


def obtener_vectores_posicion_flechas(vector_x, vector_y):
    x_direct = []
    y_direct = []

    for i in range(0, len(vector_x) - 1):
        x1 = vector_x[i]
        x2 = vector_x[i + 1]
        y1 = vector_y[i]
        y2 = vector_y[i + 1]
        x_punta, y_punta = obtener_punta_vector(x1, x2, y1, y2)
        x_direct.append(x_punta)
        y_direct.append(y_punta)

    return x_direct, y_direct


def calcula_distancia_entre_puntos(x_1, x_2, y_1, y_2):
    return np.sqrt((x_2 - x_1) ** 2 + (y_2 - y_1) ** 2)


def obtener_punta_vector(x_1, x_2, y_1, y_2):
    return x_2 - x_1, y_2 - y_1


def modificar_lista_para_cilindros(lista_a_modificar, lista_radios_cilindros, distancia):
    for i in range(0, len(lista_radios_cilindros)):
        if distancia < lista_radios_cilindros[i]:
            lista_a_modificar[i] += 1
    return lista_a_modificar


def pintar_cilindro(x_centro, y_centro, radio, altura, ax):
    angulos = np.linspace(0, 2 * np.pi, 1000)

    x = x_centro + radio * np.cos(angulos)
    y = y_centro + radio * np.sin(angulos)

    x[x < 0] = np.nan
    y[y < 0] = np.nan

    x[x > 100] = np.nan
    y[y > 100] = np.nan

    z = np.linspace(0, altura, 1000)

    x_cilindro, z_cilindro = np.meshgrid(x, z)

    ax.plot_surface(x_cilindro, y, z_cilindro)


def arreglos_a_modificar(m1, m2):
    nuevo_m1 = np.copy(m1)
    nuevo_m2 = np.copy(m2)

    indices_con_valores_0 = np.argwhere(nuevo_m2 == 0)

    for indices in indices_con_valores_0:
        nuevo_m1[indices[0], indices[1]] = 0
        nuevo_m2[indices[0], indices[1]] = 1

    return nuevo_m1, nuevo_m2


def genera_serie_de_datos(datos):
    return pd.Series(datos)


def genera_dataframes_de_datos(datos):
    diccionario_csv = {
        'valores': datos
    }
    tabla_csv = pd.DataFrame(diccionario_csv)
    return tabla_csv


def exporta_archivo(archivo, nombre_a_guardar, tipo):
    if tipo is "csv":
        archivo.to_csv(nombre_a_guardar)
