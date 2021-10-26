
from abstract.NodoAST import NodoAST
from tablaSimbolos.Simbolo import Simbolo
from abstract.Instruccion import Instruccion
from tablaSimbolos.Tipo import tipos

class Funciones(Instruccion):
    def __init__(self, ids, types, listaParametros, listaInstrucciones, line, column):
        super().__init__(tipos.FUNCION, line, column)
        self.line = line
        self.column = column
        self.id = ids
        self.tipo = tipos.FUNCION
        self.retorno = types
        self.listaParametros = listaParametros
        self.listaInstrucciones = listaInstrucciones
        self.Bfuncion = False
    
    def interpretar(self, tree, table):
        if self.listaParametros is None:
            self.listaParametros = []
        if self.listaInstrucciones is None:
            self.listaInstrucciones = []
        table.setFuncion(self.id, self)
    
    def getNodo(self):
        pass