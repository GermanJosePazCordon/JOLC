
from abstract.NodoAST import NodoAST
from excepciones.Excepciones import Excepciones
from abstract.Instruccion import Instruccion
from tablaSimbolos.Tipo import tipos
from expression.Primitiva import Primitiva

class ConstruccionStruct(Instruccion):
    def __init__(self, struct, listaParametros, line, column):
        super().__init__(tipos.STRUCT, line, column)
        self.line = line
        self.column = column
        self.struct = struct
        self.listaParametros= listaParametros
    
    def interpretar(self, tree, table):
        
        atributosStruct = self.struct.value["atributos"]
        if len(self.listaParametros) != len(atributosStruct):
            tree.addError(Excepciones("Semántico", "Numero de parametros incorrecto", self.line, self.column))
            return Excepciones("Semantico", "Numero de parametros incorrecto", self.line, self.column)
        
        dic = {}
        dic["struct"] = self.struct.value["struct"]
        dic["mutable"] = self.struct.value["mutable"]
        for i in range(len(self.listaParametros)):
            express = self.listaParametros[i].interpretar(tree, table)
            if atributosStruct[i].type is None:
                dic[atributosStruct[i].id] = express
            elif atributosStruct[i].type == express.tipo:
                dic[atributosStruct[i].id] = express
            else:
                tree.addError(Excepciones("Semántico", "Tipo de atributo y parametro no coinciden", self.line, self.column))
                return Excepciones("Semantico", "Tipo de atributo y parametro no coinciden", self.line, self.column)
        tmp = Primitiva(tipos.STRUCT, dic, self.line, self.column) 
        return tmp      
        
    def getNodo(self):
        nodo = NodoAST("LLAMADA")
        nodo.agregarHijo(self.struct.id)
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
        return nodo