from abstract.NodoAST import NodoAST
from abstract.Instruccion import Instruccion
from tablaSimbolos.Tipo import tipos

class Continue(Instruccion):
    def __init__(self, line, column):
        super().__init__(tipos.CONTINUE, line, column);
        self.line = line
        self.column  = column
        
    def interpretar(self, tree, table):
        return self
    
    def getNodo(self):
        nodo = NodoAST("TRANSFERENCIA")
        nodo.agregarHijo("CONTINUE")
        nodo.agregarHijo(";")
        return nodo