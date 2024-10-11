#################################################################
# Nombre      : Agente Buscador                                 #
# Version     : 0.06.10.2024                                    #
# Autor       : Victor             #
# Descripcion : Clase especificacion de Agente, implementa      #
#               algoritmos de busqueda                          #
#################################################################

from AgenteIA.Agente import Agente
from copy import deepcopy


class AgenteBuscador(Agente):

    def __init__(self):
        super().__init__()
        self.funcion_sucesor = []
        self.tecnica = None
        self.estado_inicial = None
        self.estado_meta = None
        self.acciones = None

    def set_tecnica(self, tecnica):
        self.tecnica = tecnica

    def set_estado_inicial(self, estado_inicial):
        self.estado_inicial = estado_inicial

    def set_estado_meta(self, estado_meta):
        self.estado_meta = estado_meta

    def add_funcion_sucesor(self, funcion):
        self.funcion_sucesor.append(funcion)


    def test_objetivo(self, nodo):
        return nodo == self.estado_meta

    def genera_hijos(self, nodo):
        raise NotImplementedError('Se debe implementar la generación de hijos.')

    def get_costo(self, camino):
        raise NotImplementedError('Se debe implementar la función de costo.')

    def get_heuristica(self, camino):
        raise NotImplementedError('Se debe implementar la función heurística.')

    def get_funcion_a(self, camino):
        raise NotImplementedError('Se debe implementar la función A*.')

    def programa(self):
        frontera = [[self.estado_inicial]]
        visitados = []
        pasos = 0

        while frontera:
            pasos += 1
            camino = self.seleccionar_camino(frontera)

            nodo = camino[-1]
            if self.test_objetivo(nodo):
                self.acciones = camino
                break

            visitados.append(nodo)
            self.expandir_frontera(nodo, camino, frontera, visitados)

            self.ordenar_frontera(frontera)

        return self.acciones

    def seleccionar_camino(self, frontera):
        if self.tecnica == "profundidad":
            return frontera.pop()
        else:
            return frontera.pop(0)

    def expandir_frontera(self, nodo, camino, frontera, visitados):
        for hijo in self.genera_hijos(nodo):
            if hijo and hijo not in visitados:
                nuevo_camino = deepcopy(camino)
                nuevo_camino.append(hijo)
                frontera.append(nuevo_camino)

    def ordenar_frontera(self, frontera):
        if self.tecnica == "costouniforme":
            frontera.sort(key=lambda camino: self.get_costo(camino))
        elif self.tecnica == "codicioso":
            frontera.sort(key=lambda camino: self.get_heuristica(camino))
        elif self.tecnica == "A*":
            frontera.sort(key=lambda camino: self.get_funcion_a(camino))

