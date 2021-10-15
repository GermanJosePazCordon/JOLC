from abstract.NodoAST import NodoAST
from abstract.Instruccion import Instruccion
from tablaSimbolos.Tipo import tipos

class Atributo(Instruccion):
    def __init__(self, types, ids, tipoID, line, column):
        super().__init__(tipos.CADENA, line, column)
        self.line = line
        self.column = column
        self.type = types
        self.id = ids
        self.tipoID = tipoID
    
    def interpretar(self, tree, table):
        return self
    
    def getTipo(self):
        return self.type
    
    def getID(self):
        return self.id
    
    def getNodo(self):
        nodo = NodoAST("ATRIBUTO")
        nodo.agregarHijo(self.id)
        if self.type is None and self.tipoID is None:
            nodo.agregarHijo(";")
        else:
            nodo.agregarHijo("::")
            if self.type is not None:
                nodo.agregarHijo(self.type.name)
            else:
                nodo.agregarHijo(self.tipoID)
            nodo.agregarHijo(";")
        return nodo