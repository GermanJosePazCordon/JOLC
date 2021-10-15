
from abstract.NodoAST import NodoAST
from tablaSimbolos.Simbolo import Simbolo
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
        if self.listaAtributos is None:
            self.listaAtributos = []
        datos = {'struct': self.id,'mutable' : self.mutable, 'atributos' : self.listaAtributos}
        table.setVariable(Simbolo(self.line, self.column, tipos.STRUCT, self.id, datos))
        
    
    def getNodo(self):
        nodo = NodoAST("DECLARAR_STRUCT")
        if self.mutable:
            nodo.agregarHijo("MUTABLE")
        nodo.agregarHijo("STRUCT")
        nodo.agregarHijo("ID")
        nuevo = NodoAST("LISTAATRIBUTO")
        one = True
        for i in self.listaAtributos:
            if one:
                nuevo.agregarHijoNodo(i.getNodo())
                one = False
            else:
                tmp = nuevo
                nuevo2 = NodoAST("ID")
                nuevo = NodoAST("LISTAATRIBUTO")
                nuevo.agregarHijoNodo(tmp)
                nuevo2.agregarHijoNodo(i.getNodo())
                nuevo.agregarHijoNodo(nuevo2)
        nodo.agregarHijoNodo(nuevo)
        nodo.agregarHijo("END")
        nodo.agregarHijo(";")
        return nodo