from typing import List, Tuple, Callable
import heapq
import random
import time

class AgenteBot:
    def __init__(self):
        self.estado_meta = (1, 2, 3, 4, 5, 6, 7, 8, 0)

    def generar_estado_valido(self) -> Tuple[int, ...]:
        while True:
            estado = list(range(9))
            random.shuffle(estado)
            if self.es_solucionable(estado):
                return tuple(estado)

    def es_solucionable(self, estado: List[int]) -> bool:
        inversiones = 0
        for i in range(len(estado)):
            for j in range(i + 1, len(estado)):
                if estado[i] != 0 and estado[j] != 0 and estado[i] > estado[j]:
                    inversiones += 1
        return inversiones % 2 == 0

    def generar_sucesores(self, estado: Tuple[int, ...]) -> List[Tuple[str, Tuple[int, ...]]]:
        indice_vacio = self.encontrar_vacio(estado)
        movimientos_validos = self.obtener_movimientos_validos(indice_vacio)
        sucesores = self.aplicar_movimientos(estado, indice_vacio, movimientos_validos)
        return sucesores

    def encontrar_vacio(self, estado: Tuple[int, ...]) -> int:
        return estado.index(0)

    def obtener_movimientos_validos(self, indice_vacio: int) -> List[Tuple[str, int]]:
        i, j = divmod(indice_vacio, 3)
        movimientos = [
            ('arriba', -3, i > 0),
            ('abajo', 3, i < 2),
            ('izquierda', -1, j > 0),
            ('derecha', 1, j < 2)
        ]
        return [(movimiento, offset) for movimiento, offset, condicion in movimientos if condicion]

    def intercambiar(self, estado: List[int], indice_vacio: int, offset: int) -> Tuple[int, ...]:
        nuevo_estado = list(estado)
        nuevo_estado[indice_vacio], nuevo_estado[indice_vacio + offset] = nuevo_estado[indice_vacio + offset], nuevo_estado[indice_vacio]
        return tuple(nuevo_estado)

    def aplicar_movimientos(self, estado: Tuple[int, ...], indice_vacio: int, movimientos: List[Tuple[str, int]]) -> List[Tuple[str, Tuple[int, ...]]]:
        sucesores = [(movimiento, self.intercambiar(estado, indice_vacio, offset)) for movimiento, offset in movimientos]
        return sucesores


    def heuristica_piezas_fuera_lugar(self, estado: Tuple[int, ...]) -> int:
        return sum(1 for i, v in enumerate(estado) if v != 0 and v != i + 1)

    def heuristica_distancia_manhattan(self, estado: Tuple[int, ...]) -> int:
        return sum(abs(i // 3 - estado.index(i) // 3) + abs(i % 3 - estado.index(i) % 3)
                   for i in range(1, 9))

    def heuristica_secuencia_lineal_conflictos(self, estado: Tuple[int, ...]) -> int:
        h = self.heuristica_distancia_manhattan(estado)
        h += self.contar_conflictos_filas(estado)
        h += self.contar_conflictos_columnas(estado)
        return h

    def contar_conflictos_filas(self, estado: Tuple[int, ...]) -> int:
        conflictos = 0
        for fila in range(3):
            for i in range(3):
                for j in range(i + 1, 3):
                    if estado[fila * 3 + i] != 0 and estado[fila * 3 + j] != 0:
                        if (estado[fila * 3 + i] - 1) // 3 == fila and (estado[fila * 3 + j] - 1) // 3 == fila:
                            if estado[fila * 3 + i] > estado[fila * 3 + j]:
                                conflictos += 2
        return conflictos

    def contar_conflictos_columnas(self, estado: Tuple[int, ...]) -> int:
        conflictos = 0
        for columna in range(3):
            for i in range(3):
                for j in range(i + 1, 3):
                    if estado[i * 3 + columna] != 0 and estado[j * 3 + columna] != 0:
                        if (estado[i * 3 + columna] - 1) % 3 == columna and (estado[j * 3 + columna] - 1) % 3 == columna:
                            if estado[i * 3 + columna] > estado[j * 3 + columna]:
                                conflictos += 2
        return conflictos


    def busqueda_codiciosa(self, estado_inicial: Tuple[int, ...], heuristica: Callable) -> Tuple[List[str], int, int]:
        frontera = self.inicializar_frontera(estado_inicial, heuristica)
        visitados = set()
        nodos_expandidos = 0
        max_frontera = 0

        while frontera:
            max_frontera = self.actualizar_max_frontera(frontera, max_frontera)
            estado, camino = self.extraer_mejor_nodo(frontera)

            if self.es_estado_meta(estado):
                return camino, nodos_expandidos, max_frontera

            if estado in visitados:
                continue

            visitados.add(estado)
            nodos_expandidos += 1

            self.expandir_nodo(estado, camino, frontera, visitados, heuristica)

        return [], nodos_expandidos, max_frontera

    def inicializar_frontera(self, estado_inicial: Tuple[int, ...], heuristica: Callable) -> List[Tuple[int, Tuple[int, ...], List[str]]]:
        return [(heuristica(estado_inicial), estado_inicial, [])]

    def actualizar_max_frontera(self, frontera: List[Tuple[int, Tuple[int, ...], List[str]]], max_frontera: int) -> int:
        return max(max_frontera, len(frontera))

    def extraer_mejor_nodo(self, frontera: List[Tuple[int, Tuple[int, ...], List[str]]]) -> Tuple[Tuple[int, ...], List[str]]:
        _, estado, camino = heapq.heappop(frontera)
        return estado, camino

    def es_estado_meta(self, estado: Tuple[int, ...]) -> bool:
        return estado == self.estado_meta

    def expandir_nodo(self, estado: Tuple[int, ...], camino: List[str], frontera: List[Tuple[int, Tuple[int, ...], List[str]]], visitados: set, heuristica: Callable):
        for accion, nuevo_estado in self.generar_sucesores(estado):
            if nuevo_estado not in visitados:
                heapq.heappush(frontera, (heuristica(nuevo_estado), nuevo_estado, camino + [accion]))


    def a_estrella(self, estado_inicial: Tuple[int, ...], heuristica: Callable) -> Tuple[List[str], int, int]:
        frontera = self.inicializar_frontera_a_estrella(estado_inicial)
        visitados = set()
        nodos_expandidos = 0
        max_frontera = 0

        while frontera:
            max_frontera = self.actualizar_max_frontera(frontera, max_frontera)
            g, estado, camino = self.extraer_mejor_nodo_a_estrella(frontera)

            if self.es_estado_meta(estado):
                return camino, nodos_expandidos, max_frontera

            if estado in visitados:
                continue

            visitados.add(estado)
            nodos_expandidos += 1

            self.expandir_nodo_a_estrella(estado, camino, frontera, visitados, heuristica, g)

        return [], nodos_expandidos, max_frontera

    def inicializar_frontera_a_estrella(self, estado_inicial: Tuple[int, ...]) -> List[Tuple[int, int, Tuple[int, ...], List[str]]]:
        return [(0, 0, estado_inicial, [])]

    def actualizar_max_frontera(self, frontera: List[Tuple[int, int, Tuple[int, ...], List[str]]], max_frontera: int) -> int:
        return max(max_frontera, len(frontera))

    def extraer_mejor_nodo_a_estrella(self, frontera: List[Tuple[int, int, Tuple[int, ...], List[str]]]) -> Tuple[int, Tuple[int, ...], List[str]]:
        _, g, estado, camino = heapq.heappop(frontera)
        return g, estado, camino

    def es_estado_meta(self, estado: Tuple[int, ...]) -> bool:
        return estado == self.estado_meta

    def expandir_nodo_a_estrella(self, estado: Tuple[int, ...], camino: List[str], frontera: List[Tuple[int, int, Tuple[int, ...], List[str]]], visitados: set, heuristica: Callable, g: int):
        """Expande el nodo actual en la búsqueda A*, generando sucesores."""
        for accion, nuevo_estado in self.generar_sucesores(estado):
            if nuevo_estado not in visitados:
                nuevo_g = g + 1
                f = nuevo_g + heuristica(nuevo_estado)
                heapq.heappush(frontera, (f, nuevo_g, nuevo_estado, camino + [accion]))



    def experimento_rapido(self, num_estados: int = 1000, max_profundidad: int = 20, tiempo_limite: float = 0.1) -> dict:
        resultados = self.inicializar_resultados()
        heuristicas = self.obtener_heuristicas()
        estados = self.generar_estados_validos(num_estados)

        for algoritmo in ['codiciosa', 'a_estrella']:
            for h_index, heuristica in enumerate(heuristicas, 1):
                clave = f"{algoritmo}_h{h_index}"
                for estado in estados:
                    self.ejecutar_experimento(resultados, clave, algoritmo, estado, heuristica, max_profundidad, tiempo_limite)

        self.promediar_tiempos(resultados, num_estados)
        return resultados

    def inicializar_resultados(self) -> dict:
        return {
            'codiciosa_h1': {'optimas': 0, 'tiempo': 0, 'max_frontera': 0, 'soluciones': 0, 'timeout': 0},
            'codiciosa_h2': {'optimas': 0, 'tiempo': 0, 'max_frontera': 0, 'soluciones': 0, 'timeout': 0},
            'codiciosa_h3': {'optimas': 0, 'tiempo': 0, 'max_frontera': 0, 'soluciones': 0, 'timeout': 0},
            'a_estrella_h1': {'optimas': 0, 'tiempo': 0, 'max_frontera': 0, 'soluciones': 0, 'timeout': 0},
            'a_estrella_h2': {'optimas': 0, 'tiempo': 0, 'max_frontera': 0, 'soluciones': 0, 'timeout': 0},
            'a_estrella_h3': {'optimas': 0, 'tiempo': 0, 'max_frontera': 0, 'soluciones': 0, 'timeout': 0},
        }

    def obtener_heuristicas(self) -> List[Callable]:
        return [
            self.heuristica_piezas_fuera_lugar,
            self.heuristica_distancia_manhattan,
            self.heuristica_secuencia_lineal_conflictos
        ]

    def generar_estados_validos(self, num_estados: int) -> List[Tuple[int, ...]]:
        return [self.generar_estado_valido() for _ in range(num_estados)]

    def ejecutar_experimento(self, resultados: dict, clave: str, algoritmo: str, estado: Tuple[int, ...], heuristica: Callable, max_profundidad: int, tiempo_limite: float):
        inicio = time.time()

        if algoritmo == 'codiciosa':
            solucion, max_frontera = self.busqueda_codiciosa_limitada(estado, heuristica, max_profundidad, tiempo_limite)
        else:
            solucion, max_frontera = self.a_estrella_limitada(estado, heuristica, max_profundidad, tiempo_limite)

        fin = time.time()
        self.actualizar_resultados(resultados, clave, solucion, max_frontera, fin - inicio)

    def actualizar_resultados(self, resultados: dict, clave: str, solucion: List[str], max_frontera: int, tiempo: float):
        resultados[clave]['tiempo'] += tiempo
        resultados[clave]['max_frontera'] = max(resultados[clave]['max_frontera'], max_frontera)

        if solucion is not None:
            resultados[clave]['soluciones'] += 1
            if solucion:
                resultados[clave]['optimas'] += 1
        else:
            resultados[clave]['timeout'] += 1

    def promediar_tiempos(self, resultados: dict, num_estados: int):
        for clave in resultados:
            resultados[clave]['tiempo'] /= num_estados


    def busqueda_codiciosa_limitada(self, estado_inicial: Tuple[int, ...], heuristica: Callable, max_profundidad: int,
                                    tiempo_limite: float) -> Tuple[List[str], int]:
        inicio = time.time()
        frontera = self.inicializar_frontera_codiciosa(estado_inicial, heuristica)
        max_frontera = 0

        while self.condicion_continua(frontera, inicio, tiempo_limite):
            max_frontera = self.actualizar_max_frontera(frontera, max_frontera)
            estado, camino = self.extraer_mejor_nodo_codiciosa(frontera)

            if self.es_estado_meta(estado):
                return camino, max_frontera

            if self.alcanzado_max_profundidad(camino, max_profundidad):
                continue

            self.expandir_nodo_codiciosa(estado, camino, frontera, heuristica)

        return None, max_frontera

    def a_estrella_limitada(self, estado_inicial: Tuple[int, ...], heuristica: Callable, max_profundidad: int,
                            tiempo_limite: float) -> Tuple[List[str], int]:
        inicio = time.time()
        frontera = self.inicializar_frontera_a_estrella(estado_inicial)
        max_frontera = 0
        visitados = set()

        while self.condicion_continua(frontera, inicio, tiempo_limite):
            max_frontera = self.actualizar_max_frontera(frontera, max_frontera)
            g, estado, camino = self.extraer_mejor_nodo_a_estrella(frontera)

            if self.es_estado_meta(estado):
                return camino, max_frontera

            if self.alcanzado_max_profundidad(camino, max_profundidad):
                continue

            # Aquí llamamos a la función con el nombre correcto
            self.expandir_nodo_a_estrella_limitada(estado, camino, frontera, visitados, heuristica, g)

        return None, max_frontera

    def expandir_nodo_a_estrella_limitada(self, estado: Tuple[int, ...], camino: List[str], frontera: List[Tuple[int, int, Tuple[int, ...], List[str]]],
                                        visitados: set, heuristica: Callable, g: int):
        """Expande el nodo actual en A*, generando sucesores y actualizando la frontera."""
        visitados.add(estado)  # Añadir el estado actual a los visitados
        for accion, nuevo_estado in self.generar_sucesores(estado):
            if nuevo_estado not in visitados:
                nuevo_g = g + 1
                f = nuevo_g + heuristica(nuevo_estado)
                heapq.heappush(frontera, (f, nuevo_g, nuevo_estado, camino + [accion]))
                
    def resolver(self, estado_inicial: List[int]) -> List[str]:
        solucion, _, _ = self.a_estrella(tuple(estado_inicial), self.heuristica_distancia_manhattan)
        return solucion