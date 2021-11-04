from abstract.NodoAST import NodoAST
from abstract.Instruccion import Instruccion
from tablaSimbolos.Tipo import tipos

class Atributo(Instruccion):
    def __init__(self, types, ids, tipoID, line, column):
        super().__init__(tipos.CADENA, line, column)
        self.line = line
        self.column = column
        self.tipo = types
        self.id = ids
        self.tipoID = tipoID #Parametro cuando el tipo del atributo no es de tipos, sino un ID
        self.vector = ''
        self.inicio = ''
    
    def interpretar(self, tree, table):
        return self
    
    def getTipo(self):
        return self.tipo
    
    def getID(self):
        return self.id
    
    def getNodo(self):
        pass