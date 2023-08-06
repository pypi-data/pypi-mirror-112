from motus.Experimento import Experimento
import motus.Funciones_Auxiliares as fa
import numpy as np
from scipy.stats import entropy
import matplotlib.pyplot as plt
from matplotlib.figure import Figure


class MultiplesExperimentos:

    def __init__(self,
                 lista_archivos,
                 dimension_caja=None,
                 cantidad_filas=10,
                 cantidad_columnas=10,
                 procesar_tiempo_archivo_irregular=False,
                 puntos_importantes=None,
                 objeto_a_promediar=1,
                 tamanio_intervalo_para_promedio=100,
                 genera_matriz_recurrencia=False):
        self.lista_archivos = lista_archivos
        self.lista_experimentos = []
        self.resultados_entropia_regiones = None
        self.resultados_entropia_velocidad = None
        self.resultados_entropia_obj_1 = None
        self.resultados_entropia_obj_2 = None
        self.resultados_entropia_obj_3 = None
        self.resultados_entropia_obj_4 = None
        self.resultados_divergencia_regiones = None
        self.genera_matriz_recurrencia = genera_matriz_recurrencia

        if dimension_caja is None:
            self.dimension_caja = [100, 100]

        self.dimension_caja = dimension_caja
        self.cantidad_filas = cantidad_filas
        self.cantidad_columnas = cantidad_columnas
        self.procesar_tiempo_archivo_irregular = procesar_tiempo_archivo_irregular
        self.puntos_importantes = puntos_importantes
        self.objeto_a_promediar = objeto_a_promediar
        self.tamanio_intervalo_para_promedio = tamanio_intervalo_para_promedio

    def inicializa_experimentos(self):

        print("Procesar tiempo irregular: ", self.procesar_tiempo_archivo_irregular)
        if isinstance(self.lista_archivos, dict):

            count = 0

            print("Diccionario de archivos: ", self.lista_archivos)

            for (nombre, valor) in self.lista_archivos.items():
                if valor.get() is True:
                    count =+ 1
                    print("conteo de experimentos: ", count)
                    self.lista_experimentos.append(Experimento(str(nombre),
                                                   dimension_caja=self.dimension_caja,
                                                   cantidad_filas=self.cantidad_filas,
                                                   cantidad_columnas=self.cantidad_columnas,
                                                   procesar_tiempo_archivo_irregular=
                                                               self.procesar_tiempo_archivo_irregular,
                                                   puntos_importantes=self.puntos_importantes,
                                                   objeto_a_promediar=self.objeto_a_promediar,
                                                   tamanio_intervalo_para_promedio=self.tamanio_intervalo_para_promedio,
                                                   genera_matriz_recurrencia=self.genera_matriz_recurrencia))

        else:
            for archivo in self.lista_archivos:
                self.lista_experimentos.append(Experimento(archivo,
                                                           dimension_caja=self.dimension_caja,
                                                           cantidad_filas=self.cantidad_filas,
                                                           cantidad_columnas=self.cantidad_columnas,
                                                           procesar_tiempo_archivo_irregular=
                                                           self.procesar_tiempo_archivo_irregular,
                                                           puntos_importantes=self.puntos_importantes,
                                                           objeto_a_promediar=self.objeto_a_promediar,
                                                           tamanio_intervalo_para_promedio=self.tamanio_intervalo_para_promedio,
                                                           genera_matriz_recurrencia=self.genera_matriz_recurrencia))

    def calcula_entropia_regiones(self):

        if self.resultados_entropia_regiones is None:
            self.resultados_entropia_regiones = []

            for experimento in self.lista_experimentos:

                matriz_tiempo_plana = np.copy(experimento.matriz_cuadriculada.flatten())

                entropia_experimento = entropy(matriz_tiempo_plana)

                self.resultados_entropia_regiones.append(round(entropia_experimento, 6))

    def calcula_entropia_velocidad(self):
        if self.resultados_entropia_velocidad is None:
            self.resultados_entropia_velocidad = []

            for experimento in self.lista_experimentos:
                experimento.calcula_histograma_velocidades()
                histograma_velocidad = experimento.valores_histograma_velocidad
                entropia_velocidad = entropy(histograma_velocidad)
                self.resultados_entropia_velocidad.append(round(entropia_velocidad, 6))

    def calcula_entropia_obj_1(self):
        if self.resultados_entropia_obj_1 is None:
            self.resultados_entropia_obj_1 = []

            for experimento in self.lista_experimentos:
                experimento.calcula_histograma_objeto_1()
                histograma_obj_1 = experimento.valores_histograma_objeto_1
                entropia_obj_1 = entropy(histograma_obj_1)
                self.resultados_entropia_obj_1.append(round(entropia_obj_1, 6))

    def calcula_entropia_obj_2(self):
        if self.resultados_entropia_obj_2 is None:
            self.resultados_entropia_obj_2 = []

            for experimento in self.lista_experimentos:
                experimento.calcula_histograma_objeto_2()
                histograma_obj_2 = experimento.valores_histograma_objeto_2
                entropia_obj_2 = entropy(histograma_obj_2)
                self.resultados_entropia_obj_2.append(round(entropia_obj_2, 6))

    def calcula_entropia_obj_3(self):
        if self.resultados_entropia_obj_3 is None:
            self.resultados_entropia_obj_3 = []

            for experimento in self.lista_experimentos:
                experimento.calcula_histograma_objeto_3()
                histograma_obj_3 = experimento.valores_histograma_objeto_3
                entropia_obj_3 = entropy(histograma_obj_3)
                self.resultados_entropia_obj_3.append(round(entropia_obj_3, 6))

    def calcula_entropia_obj_4(self):
        if self.resultados_entropia_obj_4 is None:
            self.resultados_entropia_obj_4 = []

            for experimento in self.lista_experimentos:
                experimento.calcula_histograma_objeto_4()
                histograma_obj_4 = experimento.valores_histograma_objeto_4
                entropia_obj_4 = entropy(histograma_obj_4)
                self.resultados_entropia_obj_4.append(round(entropia_obj_4, 6))

    def calcula_divergencia_regiones(self):

        if self.resultados_divergencia_regiones is None:
            self.resultados_divergencia_regiones = []

            for i in range(0, len(self.lista_experimentos)-1):

                p0 = self.lista_experimentos[i]
                p1 = self.lista_experimentos[i+1]

                nuevo_p1, nuevo_p2 = fa.arreglos_a_modificar(p0.matriz_cuadriculada, p1.matriz_cuadriculada)

                matriz_tiempo_p0_plana = np.copy(nuevo_p1.flatten())
                matriz_tiempo_p1_plana = np.copy(nuevo_p2.flatten())

                entropia_experimento = entropy(matriz_tiempo_p0_plana, matriz_tiempo_p1_plana)

                self.resultados_divergencia_regiones.append(round(entropia_experimento, 6))

    def graficar(self, grafica):
        print("-----------------------------------------------")
        print("Gráfica deseada", grafica)

        if grafica is 'entropia_regiones':
            plt.plot(range(1, len(self.resultados_entropia_regiones)+1),
                     self.resultados_entropia_velocidad)
            plt.show()

        elif grafica is 'entropia_velocidad':
            plt.plot(range(1, len(self.resultados_entropia_regiones)+1),
                     self.resultados_entropia_velocidad)
            plt.show()

        elif grafica is 'divergencia_regiones':
            plt.plot(range(1, len(self.resultados_divergencia_regiones)+1),
                     self.resultados_divergencia_regiones, 'o')
            plt.plot(range(1, len(self.resultados_divergencia_regiones)+1),
                     self.resultados_divergencia_regiones)
            plt.show()

    def regresa_imagen_grafica(self, grafica):
        print("-----------------------------------------------")
        print("Gráfica deseada:", grafica)

        fig = Figure(figsize=(6, 6))
        fig_plot = fig.add_subplot(111)
        fig_plot.grid(True)

        if grafica is 'entropia_regiones':
            fig_plot.plot(range(1, len(self.resultados_entropia_regiones)+1),
                          self.resultados_entropia_regiones, 'o')
            fig_plot.plot(range(1, len(self.resultados_entropia_regiones)+1),
                          self.resultados_entropia_regiones)

        elif grafica is 'entropia_velocidad':
            fig_plot.plot(range(1, len(self.resultados_entropia_velocidad)+1),
                          self.resultados_entropia_velocidad, 'o')
            fig_plot.plot(range(1, len(self.resultados_entropia_velocidad)+1),
                          self.resultados_entropia_velocidad)

        elif grafica is 'entropia_obj_1':
            fig_plot.plot(range(1, len(self.resultados_entropia_obj_1)+1),
                          self.resultados_entropia_obj_1, 'o')
            fig_plot.plot(range(1, len(self.resultados_entropia_obj_1)+1),
                          self.resultados_entropia_obj_1)

        elif grafica is 'entropia_obj_2':
            fig_plot.plot(range(1, len(self.resultados_entropia_obj_2)+1),
                          self.resultados_entropia_obj_2, 'o')
            fig_plot.plot(range(1, len(self.resultados_entropia_obj_2)+1),
                          self.resultados_entropia_obj_2)

        elif grafica is 'entropia_obj_3':
            fig_plot.plot(range(1, len(self.resultados_entropia_obj_3)+1),
                          self.resultados_entropia_obj_3, 'o')
            fig_plot.plot(range(1, len(self.resultados_entropia_obj_3)+1),
                          self.resultados_entropia_obj_3)

        elif grafica is 'entropia_obj_4':
            fig_plot.plot(range(1, len(self.resultados_entropia_obj_4)+1),
                          self.resultados_entropia_obj_4, 'o')
            fig_plot.plot(range(1, len(self.resultados_entropia_obj_4)+1),
                          self.resultados_entropia_obj_4)


        elif grafica is 'divergencia':
            fig_plot.plot(range(1, len(self.resultados_divergencia_regiones)+1),
                          self.resultados_divergencia_regiones, 'o')
            fig_plot.plot(range(1, len(self.resultados_divergencia_regiones)+1),
                          self.resultados_divergencia_regiones)

        return fig
