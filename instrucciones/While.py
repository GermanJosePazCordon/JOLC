from abstract.NodoAST import NodoAST
from expression.Primitiva import Primitiva
from abstract.Instruccion import Instruccion
from tablaSimbolos.Tipo import tipos
from tablaSimbolos.TablaSimbolos import tablaSimbolos
from excepciones.Excepciones import Excepciones
from instrucciones.Break import Break
from instrucciones.Return import Return
from instrucciones.Continue import Continue

class While(Instruccion):
    def __init__(self, express, listaInstrucciones, line, column):
        super().__init__(tipos.CADENA, line, column)
        self.line = line
        self.column = column
        self.express = express
        self.listaInstrucciones = listaInstrucciones
    
    def interpretar(self, tree, table):
        if self.express.tipo != tipos.BOOLEAN:
            tree.addError(Excepciones("Semántico", "Tipo de condicional invalido", self.line, self.column))
            return Excepciones("Semantico", "Tipo de condicional invalido", self.line, self.column)
        breakk = False
        while(self.express.interpretar(tree, table).value == "true"):
            tabla = tablaSimbolos(table)
            tabla.setEntorno("while")
            tree.addTabla(tabla)
            for i in self.listaInstrucciones:
                if isinstance(i, Excepciones):
                    tree.updateConsola(str(i))
                    tree.addError(i.toString())
                    continue
                result = i.interpretar(tree, tabla)
                if isinstance(result, Excepciones):
                    tree.updateConsola(result.toString())
                if isinstance(result, Primitiva): return result
                if isinstance(result, Continue): break
                if isinstance(result, Return): return result
                if isinstance(result, Break): 
                    breakk = True 
                    break
            if breakk:
                break
        
    def getNodo(self):
        nodo = NodoAST("CICLO_WHILE")
        nodo.agregarHijo("WHILE")
        nuevo = NodoAST("EXPRESION")
        nuevo.agregarHijoNodo(self.express.getNodo())
        nodo.agregarHijoNodo(nuevo)
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