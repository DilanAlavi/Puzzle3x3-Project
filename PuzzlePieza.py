import pygame

class PuzzlePieza:
    def __init__(self, x, y, imagen, numero, superficie):
        self.x = x
        self.y = y
        self.imagen = imagen
        self.numero = numero
        self.superficie = superficie
        self.ancho = 100
        self.altura = 100

    def mostrar(self):
        self.superficie.blit(self.imagen, (self.x, self.y))

    def mover(self, nuevo_x, nuevo_y):
        self.x = nuevo_x
        self.y = nuevo_y