from abstract.Instruccion import Instruccion
from tablaSimbolos.Tipo import tipos

class ListaIF(Instruccion):
    def __init__(self, express, listaInstruccion, line, column):
        super().__init__(tipos.CADENA, line, column)
        self.line = line
        self.column = column
        self.express = express
        self.listaInstruccion = listaInstruccion
    
    def interpretar(self, tree, table):
        return self
    
    def getExpresion(self):
        return self.express
    
    def getInstrucciones(self):
        return self.listaInstruccion
    
    def getNodo(self):
        return None