from abstract.NodoAST import NodoAST
from abstract.Instruccion import Instruccion
from tablaSimbolos.Tipo import tipos

class Break(Instruccion):
    def __init__(self, line, column):
        super().__init__(tipos.BREAK, line, column);
        self.line = line
        self.column  = column
        
    def interpretar(self, tree, table):
        return self
    
    def getNodo(self):
        nodo = NodoAST("TRANSFERENCIA")
        nodo.agregarHijo("BREAK")
        nodo.agregarHijo(";")
        return nodo