import pygame
import time
import threading
from AgenteIA.Entorno import Entorno
from PuzzlePieza import PuzzlePieza
from AgenteBot import AgenteBot
import random
import sys


class TableroP(Entorno):
    def __init__(self):
        Entorno.__init__(self)
        pygame.init()
        self.ancho = 300
        self.altura = 300
        self.ventana = pygame.display.set_mode((self.ancho, self.altura + 140))
        pygame.display.set_caption('Puzzle 8 con Imagen')
        self.cargar_imagen()
        self.estado_inicial()
        self.modo_usuario = True
        self.modo_bot = False
        self.font = pygame.font.Font(None, 30)
        self.movimientos_bot = []
        self.agente_bot = AgenteBot()
        self.ultimo_movimiento = 0
        self.pensando = False
        self.mensaje = ""

    def cargar_imagen(self):
        imagen_completa = pygame.image.load('imagen_puzzle.jpg')
        imagen_completa = pygame.transform.scale(imagen_completa, (300, 300))
        self.piezas = []
        for i in range(3):
            for j in range(3):
                pieza = imagen_completa.subsurface((j * 100, i * 100, 100, 100))
                self.piezas.append(pieza)

    def es_solucionable(self, estado):
        inversiones = 0
        for i in range(len(estado)):
            for j in range(i + 1, len(estado)):
                if estado[i] != 0 and estado[j] != 0 and estado[i] > estado[j]:
                    inversiones += 1
        return inversiones % 2 == 0

    def estado_inicial(self):
        while True:
            numeros = list(range(9))
            random.shuffle(numeros)
            if self.es_solucionable(numeros):
                break

        self.tablero = []
        for i in range(3):
            for j in range(3):
                if numeros[i * 3 + j] == 0:
                    self.espacio_vacio = (i, j)
                    self.tablero.append(None)
                else:
                    pieza = PuzzlePieza(j * 100, i * 100, self.piezas[numeros[i * 3 + j] - 1], numeros[i * 3 + j],
                                        self.ventana)
                    self.tablero.append(pieza)

    def obtener_estado_actual(self):
        return [pieza.numero if pieza else 0 for pieza in self.tablero]

    def resolver_bot(self):
        self.pensando = True
        self.mensaje = "Pensando..."
        estado_actual = self.obtener_estado_actual()

        def calcular_solucion():
            start_time = time.time()
            self.movimientos_bot = self.agente_bot.resolver(estado_actual)
            end_time = time.time()
            self.mensaje = f"Solución encontrada en {end_time - start_time:.2f} segundos"
            self.pensando = False

        threading.Thread(target=calcular_solucion).start()

    def ejecutar_movimiento_bot(self):
        tiempo_actual = time.time()
        if self.movimientos_bot and tiempo_actual - self.ultimo_movimiento > 0.5:
            accion = self.movimientos_bot.pop(0)
            self.mover_pieza(accion)
            self.ultimo_movimiento = tiempo_actual
            return True
        return False

    def mover_pieza(self, direccion):
        i, j = self.espacio_vacio
        if direccion == 'arriba' and i > 0:
            self.tablero[i * 3 + j], self.tablero[(i - 1) * 3 + j] = self.tablero[(i - 1) * 3 + j], None
            self.tablero[i * 3 + j].mover(j * 100, i * 100)
            self.espacio_vacio = (i - 1, j)
        elif direccion == 'abajo' and i < 2:
            self.tablero[i * 3 + j], self.tablero[(i + 1) * 3 + j] = self.tablero[(i + 1) * 3 + j], None
            self.tablero[i * 3 + j].mover(j * 100, i * 100)
            self.espacio_vacio = (i + 1, j)
        elif direccion == 'izquierda' and j > 0:
            self.tablero[i * 3 + j], self.tablero[i * 3 + j - 1] = self.tablero[i * 3 + j - 1], None
            self.tablero[i * 3 + j].mover(j * 100, i * 100)
            self.espacio_vacio = (i, j - 1)
        elif direccion == 'derecha' and j < 2:
            self.tablero[i * 3 + j], self.tablero[i * 3 + j + 1] = self.tablero[i * 3 + j + 1], None
            self.tablero[i * 3 + j].mover(j * 100, i * 100)
            self.espacio_vacio = (i, j + 1)

    def mover_pieza_usuario(self, pos_mouse):
        x, y = pos_mouse
        j, i = x // 100, y // 100
        if (i, j) != self.espacio_vacio:
            if abs(i - self.espacio_vacio[0]) + abs(j - self.espacio_vacio[1]) == 1:
                if i == self.espacio_vacio[0]:
                    direccion = 'izquierda' if j < self.espacio_vacio[1] else 'derecha'
                else:
                    direccion = 'arriba' if i < self.espacio_vacio[0] else 'abajo'
                self.mover_pieza(direccion)

    def nuevo_juego(self):
        self.estado_inicial()
        self.modo_usuario = True
        self.modo_bot = False
        self.movimientos_bot = []
        self.pensando = False
        self.mensaje = "Nuevo juego iniciado"

    def dibujar(self):
        self.ventana.fill((255, 255, 255))
        for pieza in self.tablero:
            if pieza:
                pieza.mostrar()

        # Dibujar botones
        pygame.draw.rect(self.ventana, (200, 200, 200) if self.modo_usuario else (150, 150, 150), (10, 310, 135, 40))
        pygame.draw.rect(self.ventana, (200, 200, 200) if self.modo_bot else (150, 150, 150), (155, 310, 135, 40))
        pygame.draw.rect(self.ventana, (200, 200, 200), (10, 360, 135, 40))  # Nuevo Juego button
        pygame.draw.rect(self.ventana, (200, 200, 200), (155, 360, 135, 40))  # Salir button
        pygame.draw.rect(self.ventana, (200, 200, 200), (10, 410, 280, 40))  # Experimento button

        texto_usuario = self.font.render("Modo Usuario", True, (0, 0, 0))
        texto_bot = self.font.render("Modo Bot", True, (0, 0, 0))
        texto_nuevo = self.font.render("Nuevo Juego", True, (0, 0, 0))
        texto_salir = self.font.render("Salir", True, (0, 0, 0))
        texto_experimento = self.font.render("Ejecutar Experimento", True, (0, 0, 0))

        self.ventana.blit(texto_usuario, (15, 320))
        self.ventana.blit(texto_bot, (170, 320))
        self.ventana.blit(texto_nuevo, (20, 370))
        self.ventana.blit(texto_salir, (195, 370))
        self.ventana.blit(texto_experimento, (50, 420))

        if self.mensaje:
            texto_mensaje = self.font.render(self.mensaje, True, (255, 0, 0))
            self.ventana.blit(texto_mensaje, (10, 280))

    def ejecutar_experimento(self):
        self.mensaje = "Ejecutando experimento..."
        threading.Thread(target=self._ejecutar_experimento).start()

    def _ejecutar_experimento(self):
        num_estados = 10  # Ajusta según tus necesidades
        heuristicas = [
            self.agente_bot.heuristica_piezas_fuera_lugar,
            self.agente_bot.heuristica_distancia_manhattan,
            self.agente_bot.heuristica_secuencia_lineal_conflictos
        ]

        resultados = {
            'codiciosa_h1': {'optimas': 0, 'tiempo': 0, 'max_frontera': 0, 'soluciones': 0, 'timeout': 0},
            'codiciosa_h2': {'optimas': 0, 'tiempo': 0, 'max_frontera': 0, 'soluciones': 0, 'timeout': 0},
            'codiciosa_h3': {'optimas': 0, 'tiempo': 0, 'max_frontera': 0, 'soluciones': 0, 'timeout': 0},
            'a_estrella_h1': {'optimas': 0, 'tiempo': 0, 'max_frontera': 0, 'soluciones': 0, 'timeout': 0},
            'a_estrella_h2': {'optimas': 0, 'tiempo': 0, 'max_frontera': 0, 'soluciones': 0, 'timeout': 0},
            'a_estrella_h3': {'optimas': 0, 'tiempo': 0, 'max_frontera': 0, 'soluciones': 0, 'timeout': 0},
        }

        for i in range(num_estados):
            estado = self.agente_bot.generar_estado_valido()
            print(f"\nEstado inicial {i + 1}: {estado}")

            for j, heuristica in enumerate(heuristicas, 1):
                # Búsqueda Codiciosa
                inicio = time.time()
                camino, nodos_expandidos, max_frontera = self.agente_bot.busqueda_codiciosa(estado, heuristica)
                fin = time.time()
                clave_codiciosa = f'codiciosa_h{j}'
                resultados[clave_codiciosa]['soluciones'] += 1 if camino else 0
                resultados[clave_codiciosa]['optimas'] += 1 if camino and len(
                    camino) <= 20 else 0  # Ajusta criterio de óptima
                resultados[clave_codiciosa]['max_frontera'] = max(resultados[clave_codiciosa]['max_frontera'],
                                                                  max_frontera)
                resultados[clave_codiciosa]['tiempo'] += (fin - inicio)
                print(
                    f"\n{clave_codiciosa.upper()} -> Solución: {camino}, Nodos expandidos: {nodos_expandidos}, Max frontera: {max_frontera}, Tiempo: {fin - inicio:.4f} segundos")

                # A*
                inicio = time.time()
                camino, nodos_expandidos, max_frontera = self.agente_bot.a_estrella(estado, heuristica)
                fin = time.time()
                clave_a_estrella = f'a_estrella_h{j}'
                resultados[clave_a_estrella]['soluciones'] += 1 if camino else 0
                resultados[clave_a_estrella]['optimas'] += 1 if camino and len(
                    camino) <= 20 else 0  # Ajusta criterio de óptima
                resultados[clave_a_estrella]['max_frontera'] = max(resultados[clave_a_estrella]['max_frontera'],
                                                                   max_frontera)
                resultados[clave_a_estrella]['tiempo'] += (fin - inicio)
                print(
                    f"\n{clave_a_estrella.upper()} -> Solución: {camino}, Nodos expandidos: {nodos_expandidos}, Max frontera: {max_frontera}, Tiempo: {fin - inicio:.4f} segundos")

        # Promediar tiempos al final
        for clave in resultados:
            resultados[clave]['tiempo'] /= num_estados

        print("\n--- Resumen del Experimento ---")
        for clave, datos in resultados.items():
            print(f"\n{clave.upper()}:")
            print(f"  Soluciones encontradas: {datos['soluciones']}/{num_estados}")
            print(f"  Soluciones óptimas: {datos['optimas']}")
            print(f"  Tiempo promedio por estado: {datos['tiempo']:.4f} segundos")
            print(f"  Tamaño máximo de la frontera: {datos['max_frontera']}")
            print(f"  Timeouts: {datos['timeout']}")
            prob_optima = datos['optimas'] / num_estados if datos['soluciones'] > 0 else 0
            print(f"  Probabilidad de solución óptima: {prob_optima:.2%}")

        self.mensaje = "Experimento completado. Ver consola para resultados."

    def run(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Click izquierdo
                        if event.pos[1] > 300:  # Click en los botones
                            if event.pos[1] < 350:  # Botones de modo
                                if event.pos[0] < 145:  # Botón Modo Usuario
                                    self.modo_usuario = True
                                    self.modo_bot = False
                                    self.mensaje = ""
                                elif event.pos[0] > 155:  # Botón Modo Bot
                                    self.modo_usuario = False
                                    self.modo_bot = True
                                    self.resolver_bot()
                            elif event.pos[1] < 400:  # Botones Nuevo Juego y Salir
                                if event.pos[0] < 145:  # Botón Nuevo Juego
                                    self.nuevo_juego()
                                elif event.pos[0] > 155:  # Botón Salir
                                    running = False
                            else:  # Botón Experimento
                                self.ejecutar_experimento()
                        elif self.modo_usuario and event.pos[1] < 300:
                            self.mover_pieza_usuario(event.pos)

            if self.modo_bot and not self.pensando and self.movimientos_bot:
                self.ejecutar_movimiento_bot()

            self.dibujar()
            pygame.display.update()
            clock.tick(60)

        pygame.quit()
        sys.exit()