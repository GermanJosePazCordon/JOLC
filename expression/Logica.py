
from abstract.NodoAST import NodoAST
from abstract.Instruccion import Instruccion
from tablaSimbolos.Tipo import tipos
from expression.Primitiva import Primitiva
from excepciones.Excepciones import Excepciones


class Logica(Instruccion):
    def __init__(self, operador, operando1, operando2, line, column):
        super().__init__(tipos.BOOLEAN, line, column)
        self.line = line
        self.column = column
        self.operador = operador
        if operando2 is None:
            self.opU = operando1
        else:
            self.op1 = operando1
            self.op2 = operando2
            self.opU = None
    
    def interpretar(self, tree, table):
        left = None
        right = None
        unario = None
        p1 = None
        p2 = None
        pu = None
        self.tipo = tipos.BOOLEAN
        if self.opU is None:
            p1 = self.op1.interpretar(tree, table)
            if isinstance(p1, Excepciones):
                return p1
            left = p1.value

            p2 = self.op2.interpretar(tree, table)
            if isinstance(p2, Excepciones):
                return p2
            right = p2.value
            
            if p1.tipo == tipos.BOOLEAN:
                if str(left).lower() == "true":
                    left = True
                else:
                    left = False
            if p2.tipo == tipos.BOOLEAN:
                if str(right).lower() == "true":
                    right = True
                else:
                    right = False
        else:
            pu = self.opU.interpretar(tree, table)
            if isinstance(pu, Excepciones):
                return pu
            unario = pu.value
            if pu.tipo == tipos.BOOLEAN:
                if str(unario).lower() == "true":
                    unario = True
                else:
                    unario = False
        if self.operador == '&&':
            if self.op1.tipo == tipos.BOOLEAN and self.op2.tipo == tipos.BOOLEAN:
                if left and right:
                    return self.retorno("true")
                else:
                    return self.retorno("false")
            else:
                tree.addError(Excepciones("Semántico", "Error de tipos en operacion &&", self.line, self.column))
                return Excepciones("Semántico", "Error de tipos en operacion &&", self.line, self.column)
        elif self.operador == '||':
            if self.op1.tipo == tipos.BOOLEAN and self.op2.tipo == tipos.BOOLEAN:
                if left or right:
                    return self.retorno("true")
                else:
                    return self.retorno("false")
            else:
                tree.addError(Excepciones("Semántico", "Error de tipos en operacion ||", self.line, self.column))
                return Excepciones("Semántico", "Error de tipos en operacion ||", self.line, self.column)
        elif self.operador == '!':
            if self.opU.tipo == tipos.BOOLEAN:
                if unario:
                    return self.retorno("false")
                else:
                    return self.retorno("true")
            else:
                tree.addError(Excepciones("Semántico", "Error de tipos en operacion !", self.line, self.column))
                return Excepciones("Semántico", "Error de tipos en operacion !", self.line, self.column)
        else:
            tree.addError(Excepciones("Semántico", "Tipo de operacion erroneo", self.line, self.column))
            return Excepciones("Semántico", "Tipo de operacion erroneo", self.line, self.column)
                
            
    def retorno(self, result):
        return Primitiva(tipos.BOOLEAN, str(result).lower(), self.line, self.column)

    def getNodo(self):
        nodo = NodoAST("LOGICA")
        if self.opU is None:
            nodo2 = NodoAST("EXPRESION")
            nodo2.agregarHijoNodo(self.op1.getNodo())
            nodo.agregarHijoNodo(nodo2)
            nodo.agregarHijo(self.operador)
            nodo3 = NodoAST("EXPRESION")
            nodo3.agregarHijoNodo(self.op2.getNodo())
            nodo.agregarHijoNodo(nodo3)
        else: 
            nodo.agregarHijo(self.operador)
            nodo2 = NodoAST("EXPRESION")
            nodo2.agregarHijoNodo(self.opU.getNodo())
            nodo.agregarHijoNodo(nodo2)
        return nodo
        