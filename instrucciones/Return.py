from abstract.NodoAST import NodoAST
from excepciones.Excepciones import Excepciones
from abstract.Instruccion import Instruccion
from tablaSimbolos.Tipo import tipos

class Return(Instruccion):
    def __init__(self, express, line, column):
        super().__init__(tipos.RETURN, line, column);
        self.line = line
        self.column  = column
        self.express = express
        
    def interpretar(self, tree, table):
        result = None
        if self.express != None:
            result = self.express.interpretar(tree, table)
        if isinstance(result, Excepciones): return result
        self.result = result
        return self
    
    def getNodo(self):
        nodo = NodoAST("TRANSFERENCIA")
        nodo.agregarHijo("RETURN")
        if self.express is not None:
            nodo.agregarHijoNodo(self.express.getNodo())
        nodo.agregarHijo(";")
        return nodo