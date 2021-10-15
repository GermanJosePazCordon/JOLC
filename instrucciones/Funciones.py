
from abstract.NodoAST import NodoAST
from tablaSimbolos.Simbolo import Simbolo
from abstract.Instruccion import Instruccion
from tablaSimbolos.Tipo import tipos

class Funciones(Instruccion):
    def __init__(self, ids, listaParametros, listaInstrucciones, line, column):
        super().__init__(tipos.FUNCION, line, column)
        self.line = line
        self.column = column
        self.id = ids
        self.listaParametros = listaParametros
        self.listaInstrucciones = listaInstrucciones
    
    def interpretar(self, tree, table):
        if self.listaParametros is None:
            self.listaParametros = []
        if self.listaInstrucciones is None:
            self.listaInstrucciones = []
        datos = {'parametros' : self.listaParametros, 'instrucciones' : self.listaInstrucciones}
        table.setVariable(Simbolo(self.line, self.column, tipos.FUNCION, self.id, datos))
    
    def getNodo(self):
        nodo = NodoAST("FUNCIONES")
        nodo.agregarHijo("FUNCTION")
        nodo.agregarHijo(self.id)
        nodo.agregarHijo("(")
        if self.listaParametros is not None:
            nuevo = NodoAST("LISTAPARAMETROS")
            one = True
            for i in self.listaParametros:
                if one:
                    nodo2 = NodoAST("EXPRESION")
                    nodo2.agregarHijoNodo(i.getNodo())
                    nuevo.agregarHijoNodo(nodo2)
                    one = False
                else:
                    tmp = nuevo
                    nuevo2 = NodoAST("EXPRESION")
                    nuevo = NodoAST("LISTAPARAMETROS")
                    nuevo.agregarHijoNodo(tmp)
                    nuevo.agregarHijo(",")
                    nuevo2.agregarHijoNodo(i.getNodo())
                    nuevo.agregarHijoNodo(nuevo2)
            nodo.agregarHijoNodo(nuevo)
        nodo.agregarHijo(")")
        nuevo = NodoAST("INSTRUCCIONES")
        one = True
        for i in self.listaInstrucciones:
            if one:
                nuevo2 = NodoAST("INSTRUCCION")
                nuevo2.agregarHijoNodo(i.getNodo())
                nuevo.agregarHijoNodo(nuevo2)
                one = False
            else:
                tmp = nuevo
                nuevo2 = NodoAST("INSTRUCCION")
                nuevo = NodoAST("INSTRUCCIONES")
                nuevo.agregarHijoNodo(tmp)
                nuevo2.agregarHijoNodo(i.getNodo())
                nuevo.agregarHijoNodo(nuevo2)
        nodo.agregarHijoNodo(nuevo)  
        nodo.agregarHijo("END")
        nodo.agregarHijo(";")
        return nodo