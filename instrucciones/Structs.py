from abstract.Instruccion import Instruccion
from tablaSimbolos.Tipo import tipos

class Structs(Instruccion):
    def __init__(self, mutable, ids, listaAtributos, line, column):
        super().__init__(tipos.STRUCT, line, column)
        self.line = line
        self.column = column
        self.mutable = mutable
        self.id = ids
        self.listaAtributos = listaAtributos
    
    def interpretar(self, tree, table):
        lista = []
        for i in self.listaAtributos:
            lista.append(i.interpretar(tree, table))
        table.setStruct(self.id, lista, self.mutable, self.line, self.column)
    
    def getNodo(self):
        pass