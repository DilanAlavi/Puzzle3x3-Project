#################################################################
# Nombre      : Agente PSR                                      #
# Version     : 0.06.10.2024                                    #
# Autor       : Victor              
# Descripcion : Clase especificacion de Agente, implementa      #
#               algoritmos Backtrack para PSR con mejoras       #
#################################################################

from AgenteIA.Agente import Agente


class AgentePSR(Agente):

    def __init__(self):
        Agente.__init__(self)
        self.variables = None
        self.dominio = None
        self.vecinos = None
        self.asignaciones = 0  

    def setVariables(self, variables):
        self.variables = variables

    def setDominio(self, dominio):
        self.dominio = dominio

    def setVecinos(self, vecinos):
        self.vecinos = vecinos

    def asignar(self, variable, val, asignacion):

        asignacion[variable] = val
        self.asignaciones += 1 
    def programa(self):
        def backtrack(asignacion):
            if self.esCompleto(asignacion):
                return asignacion
            vari = self.seleccionarVariableNoAsignada(asignacion)

            for valor in self.getDominio():
                if self.getConflictos(vari, valor, asignacion) == 0:
                    self.asignar(vari, valor, asignacion)
                    resultado = backtrack(asignacion)
                    if resultado is not None:
                        return resultado

            self.desasignar(vari, asignacion)
            return None

        self.acciones = backtrack({})
        self.vive = False

    def desasignar(self, variable, asignacion):
        if variable in asignacion:
            del asignacion[variable]

    def seleccionarVariableNoAsignada(self, asignacion):
        return ([var for var in self.variables if var not in asignacion])[0]

    def getConflictos(self, var, val, asignacion):
        conflictos = 0
        for vecino in self.vecinos[var]:
            if vecino in asignacion and asignacion[vecino] == val:
                conflictos += 1
        return conflictos

    def getDominio(self):
        return self.dominio

    def esCompleto(self, asignacion):
        return len(asignacion) == len(self.variables)

    def reiniciar(self):
        self.asignaciones = 0
        self.acciones = None
        self.vive = True

    def contarSoluciones(self):
        soluciones = []

        def backtrack(asignacion):
            if self.esCompleto(asignacion):
                soluciones.append(asignacion.copy())
                return
            vari = self.seleccionarVariableNoAsignada(asignacion)

            for valor in self.getDominio():
                if self.getConflictos(vari, valor, asignacion) == 0:
                    self.asignar(vari, valor, asignacion)
                    backtrack(asignacion)
                    self.desasignar(vari, asignacion)

        backtrack({})
        return soluciones


