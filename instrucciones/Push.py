from abstract.NodoAST import NodoAST
from abstract.Instruccion import Instruccion
from tablaSimbolos.Tipo import tipos
from expression.Primitiva import Primitiva
from excepciones.Excepciones import Excepciones

class Push(Instruccion):
    def __init__(self, ids, expresion, line, column):
        super().__init__(tipos.CADENA, line, column)
        self.line = line
        self.column = column
        self.expresion = expresion
        self.id = ids
    
    def interpretar(self, tree, table):
        self.tipo = tipos.VECTOR
        vector = self.id.interpretar(tree, table)
        valor = self.expresion.interpretar(tree, table)
        if vector.tipo == tipos.VECTOR:
            vector.value.append(valor)
            return None
        else:
            tree.addError(Excepciones("Semántico", "Tipo incorrecto para la funcion push", self.line, self.column))
            return Excepciones("Semantico", "Tipo incorrecto para la funcion push", self.line, self.column)
       
    def getNodo(self):
        nodo = NodoAST("INSTRUCCION_PUSH")
        nodo.agregarHijo("PUSH")
        nodo.agregarHijo("!")
        nodo.agregarHijo("(")
        nuevo = NodoAST("EXPRESION")
        nuevo.agregarHijoNodo(self.id.getNodo())
        nodo.agregarHijoNodo(nuevo)
        nodo.agregarHijo(",")
        nuevo = NodoAST("EXPRESION")
        nuevo.agregarHijoNodo(self.expresion.getNodo())
        nodo.agregarHijoNodo(nuevo)
        nodo.agregarHijo(")")
        nodo.agregarHijo(";")
        return nodo