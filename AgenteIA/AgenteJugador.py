#################################################################
# Nombre      : Entorno                                         #
# Version     : 0.06.10.2024                                    #
# Autor       : Victor                                          #
# Descripcion : Clase Agentes con Adversarios                   #
#################################################################

from AgenteIA.Agente import Agente
from collections import namedtuple

ElEstado = namedtuple('ElEstado', 'jugador, get_utilidad, tablero, movidas')


class AgenteJugador(Agente):

    def __init__(self):
        super().__init__()
        self.estado = None
        self.juego = None
        self.utilidad = None

    def jugadas(self, estado):
        raise Exception("Error: No se implemento")

    def get_utilidad(self, estado, jugador):
        raise Exception("Error: No se implemento")

    def testTerminal(self, estado):
        return not self.jugadas(estado)

    def getResultado(self, estado, m):
        raise Exception("Error: No se implemento")

    def programa(self):
        # Puedes escoger una de estas estrategias:
        self.acciones = self.minimax()
       # self.acciones = self.podaAlphaBeta()
        # self.acciones = self.podaalphaBetaFunEval(self.estado, self.estado.jugador)



    def minimax(self):
        return max(self.jugadas(self.estado), key=lambda a: self.valorMin(self.getResultado(self.estado, a)))

    def valorMax(self, estado):
        """Función de valor máximo de Minimax."""
        if self.testTerminal(estado):
            return self.get_utilidad(estado, self.estado.jugador)
        return self.max_valor(estado)

    def valorMin(self, estado):

        if self.testTerminal(estado):
            return self.get_utilidad(estado, self.estado.jugador)
        return self.min_valor(estado)

    def max_valor(self, estado):

        valor = -float('inf')
        for accion in self.jugadas(estado):
            valor = max(valor, self.valorMin(self.getResultado(estado, accion)))
        return valor

    def min_valor(self, estado):

        valor = float('inf')
        for accion in self.jugadas(estado):
            valor = min(valor, self.valorMax(self.getResultado(estado, accion)))
        return valor



    def podaAlphaBeta(self):
        alpha = -float('inf')
        beta = float('inf')
        return max(self.jugadas(self.estado), key=lambda a: self.valorMinAlphaBeta(self.getResultado(self.estado, a), alpha, beta))

    def valorMaxAlphaBeta(self, estado, alpha, beta):
        if self.testTerminal(estado):
            return self.get_utilidad(estado, self.estado.jugador)
        return self.max_valor_alpha_beta(estado, alpha, beta)

    def valorMinAlphaBeta(self, estado, alpha, beta):
        if self.testTerminal(estado):
            return self.get_utilidad(estado, self.estado.jugador)
        return self.min_valor_alpha_beta(estado, alpha, beta)

    def max_valor_alpha_beta(self, estado, alpha, beta):
        valor = -float('inf')
        for accion in self.jugadas(estado):
            valor = max(valor, self.valorMinAlphaBeta(self.getResultado(estado, accion), alpha, beta))
            if valor >= beta:
                return valor
            alpha = max(alpha, valor)
        return valor

    def min_valor_alpha_beta(self, estado, alpha, beta):
        valor = float('inf')
        for accion in self.jugadas(estado):
            valor = min(valor, self.valorMaxAlphaBeta(self.getResultado(estado, accion), alpha, beta))
            if valor <= alpha:
                return valor
            beta = min(beta, valor)
        return valor


    def podaalphaBetaFunEval(self, estado, jugador):
        alpha = -float('inf')
        beta = float('inf')
        profundidad_max = 3  # Profundidad máxima de la búsqueda
        return max(self.jugadas(estado), key=lambda a: self.valorMinAlphaBetaFunEval(self.getResultado(estado, a), alpha, beta, profundidad_max, jugador))

    def valorMaxAlphaBetaFunEval(self, estado, alpha, beta, profundidad, jugador):
        if self.testTerminal(estado) or profundidad == 0:
            return self.evaluarEstado(estado, jugador)
        return self.max_valor_alpha_beta_fun_eval(estado, alpha, beta, profundidad, jugador)

    def valorMinAlphaBetaFunEval(self, estado, alpha, beta, profundidad, jugador):
        if self.testTerminal(estado) or profundidad == 0:
            return self.evaluarEstado(estado, jugador)
        return self.min_valor_alpha_beta_fun_eval(estado, alpha, beta, profundidad, jugador)

    def max_valor_alpha_beta_fun_eval(self, estado, alpha, beta, profundidad, jugador):
        valor = -float('inf')
        for accion in self.jugadas(estado):
            valor = max(valor, self.valorMinAlphaBetaFunEval(self.getResultado(estado, accion), alpha, beta, profundidad - 1, jugador))
            if valor >= beta:
                return valor
            alpha = max(alpha, valor)
        return valor

    def min_valor_alpha_beta_fun_eval(self, estado, alpha, beta, profundidad, jugador):
        valor = float('inf')
        for accion in self.jugadas(estado):
            valor = min(valor, self.valorMaxAlphaBetaFunEval(self.getResultado(estado, accion), alpha, beta, profundidad - 1, jugador))
            if valor <= alpha:
                return valor
            beta = min(beta, valor)
        return valor

