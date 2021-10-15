
from abstract.NodoAST import NodoAST
from abstract.Instruccion import Instruccion
from tablaSimbolos.Tipo import tipos
from expression.Primitiva import Primitiva
from excepciones.Excepciones import Excepciones

class Relacional(Instruccion):
    def __init__(self, operador, operando1, operando2, line, column):
        super().__init__(tipos.BOOLEAN, line, column)
        self.column = column;
        self.line = line;
        self.operador = operador;
        self.op1 = operando1;
        self.op2 = operando2;
    
    def interpretar(self, tree, table):
        left = None
        right = None
        p1 = None
        p2 = None
        p1 = self.op1.interpretar(tree, table)
        if isinstance(p1, Excepciones):
            return p1
        left = p1.value

        p2 = self.op2.interpretar(tree, table)
        if isinstance(p2, Excepciones):
            return p2
        right = p2.value
        
        self.tipo = tipos.BOOLEAN
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
        if self.operador == '>':
            if p1.tipo == tipos.ENTERO and p2.tipo == tipos.ENTERO:
                return self.retorno(int(left) > int(right))
            elif p1.tipo == tipos.ENTERO and p2.tipo == tipos.DECIMAL:
                return self.retorno(int(left) > float(right))
            elif p1.tipo == tipos.DECIMAL and p2.tipo == tipos.ENTERO:
                return self.retorno(float(left) > int(right))
            elif p1.tipo == tipos.DECIMAL and p2.tipo == tipos.DECIMAL:
                return self.retorno(float(left) > float(right))
            elif p1.tipo == tipos.CADENA and p2.tipo == tipos.CADENA:
                return self.retorno(left > right)
            elif p1.tipo == tipos.BOOLEAN and p2.tipo == tipos.BOOLEAN:
                return self.retorno(left > right)
            else:
                tree.addError(Excepciones("Semántico", "Operandos erroneos para >", self.line, self.column))
                return Excepciones("Semántico", "Operandos erroneos para >", self.line, self.column)
        elif self.operador == '>=':
            if p1.tipo == tipos.ENTERO and p2.tipo == tipos.ENTERO:
                return self.retorno(int(left) >= int(right))
            elif p1.tipo == tipos.ENTERO and p2.tipo == tipos.DECIMAL:
                return self.retorno(int(left) >= float(right))
            elif p1.tipo == tipos.DECIMAL and p2.tipo == tipos.ENTERO:
                return self.retorno(float(left) >= int(right))
            elif p1.tipo == tipos.DECIMAL and p2.tipo == tipos.DECIMAL:
                return self.retorno(float(left) >= float(right))
            elif p1.tipo == tipos.CADENA and p2.tipo == tipos.CADENA:
                return self.retorno(left >= right)
            elif p1.tipo == tipos.BOOLEAN and p2.tipo == tipos.BOOLEAN:
                return self.retorno(left >= right)
            else:
                tree.addError(Excepciones("Semántico", "Operandos erroneos para >=", self.line, self.column))
                return Excepciones("Semántico", "Operandos erroneos para >=", self.line, self.column)
        elif self.operador == '<':
            if p1.tipo == tipos.ENTERO and p2.tipo == tipos.ENTERO:
                return self.retorno(int(left) < int(right))
            elif p1.tipo == tipos.ENTERO and p2.tipo == tipos.DECIMAL:
                return self.retorno(int(left) < float(right))
            elif p1.tipo == tipos.DECIMAL and p2.tipo == tipos.ENTERO:
                return self.retorno(float(left) < int(right))
            elif p1.tipo == tipos.DECIMAL and p2.tipo == tipos.DECIMAL:
                return self.retorno(float(left) < float(right))
            elif p1.tipo == tipos.CADENA and p2.tipo == tipos.CADENA:
                return self.retorno(left < right)
            elif p1.tipo == tipos.BOOLEAN and p2.tipo == tipos.BOOLEAN:
                return self.retorno(left < right)
            else:
                tree.addError(Excepciones("Semántico", "Operandos erroneos para <", self.line, self.column))
                return Excepciones("Semántico", "Operandos erroneos para <", self.line, self.column)
        elif self.operador == '<=':
            if p1.tipo == tipos.ENTERO and p2.tipo == tipos.ENTERO:
                return self.retorno(int(left) <= int(right))
            elif p1.tipo == tipos.ENTERO and p2.tipo == tipos.DECIMAL:
                return self.retorno(int(left) <= float(right))
            elif p1.tipo == tipos.DECIMAL and p2.tipo == tipos.ENTERO:
                return self.retorno(float(left) <= int(right))
            elif p1.tipo == tipos.DECIMAL and p2.tipo == tipos.DECIMAL:
                return self.retorno(float(left) <= float(right))
            elif p1.tipo == tipos.CADENA and p2.tipo == tipos.CADENA:
                return self.retorno(left <= right)
            elif p1.tipo == tipos.BOOLEAN and p2.tipo == tipos.BOOLEAN:
                return self.retorno(left <= right)
            else:
                tree.addError(Excepciones("Semántico", "Operandos erroneos para <=", self.line, self.column))
                return Excepciones("Semántico", "Operandos erroneos para <=", self.line, self.column)
        elif self.operador == '==':
            if p1.tipo == tipos.ENTERO and p2.tipo == tipos.ENTERO:
                return self.retorno(int(left) == int(right))
            elif p1.tipo == tipos.ENTERO and p2.tipo == tipos.DECIMAL:
                return self.retorno(int(left) == float(right))
            elif p1.tipo == tipos.DECIMAL and p2.tipo == tipos.ENTERO:
                return self.retorno(float(left) == int(right))
            elif p1.tipo == tipos.DECIMAL and p2.tipo == tipos.DECIMAL:
                return self.retorno(float(left) == float(right))
            elif p1.tipo == tipos.CADENA and p2.tipo == tipos.CADENA:
                return self.retorno(left == right)
            elif p1.tipo == tipos.BOOLEAN and p2.tipo == tipos.BOOLEAN:
                return self.retorno(left == right)
            elif p1.tipo == tipos.NULO or p2.tipo == tipos.NULO:
                return self.retorno(left == right)
            else:
                tree.addError(Excepciones("Semántico", "Operandos erroneos para ==", self.line, self.column))
                return Excepciones("Semántico", "Operandos erroneos para ==", self.line, self.column)
        elif self.operador == '!=':
            if p1.tipo == tipos.ENTERO and p2.tipo == tipos.ENTERO:
                return self.retorno(int(left) != int(right))
            elif p1.tipo == tipos.ENTERO and p2.tipo == tipos.DECIMAL:
                return self.retorno(int(left) != float(right))
            elif p1.tipo == tipos.DECIMAL and p2.tipo == tipos.ENTERO:
                return self.retorno(float(left) != int(right))
            elif p1.tipo == tipos.DECIMAL and p2.tipo == tipos.DECIMAL:
                return self.retorno(float(left) != float(right))
            elif p1.tipo == tipos.CADENA and p2.tipo == tipos.CADENA:
                return self.retorno(left != right)
            elif p1.tipo == tipos.BOOLEAN and p2.tipo == tipos.BOOLEAN:
                return self.retorno(left != right)
            elif p1.tipo == tipos.NULO or p2.tipo == tipos.NULO:
                return self.retorno(left != right)
            else:
                tree.addError(Excepciones("Semántico", "Operandos erroneos para !=", self.line, self.column))
                return Excepciones("Semántico", "Operandos erroneos para !=", self.line, self.column)
        else:
            tree.addError(Excepciones("Semántico", "Tipo de operacion erroneo", self.line, self.column))
            return Excepciones("Semántico", "Tipo de operacion erroneo", self.line, self.column)
    
    def retorno(self, result):
        return Primitiva(self.tipo, str(result).lower(), self.line, self.column)

    def getNodo(self):
        nodo = NodoAST("RELACIONAL")
        nodo2 = NodoAST("EXPRESION")
        nodo2.agregarHijoNodo(self.op1.getNodo())
        nodo.agregarHijoNodo(nodo2)
        nodo.agregarHijo(self.operador)
        nodo3 = NodoAST("EXPRESION")
        nodo3.agregarHijoNodo(self.op2.getNodo())
        nodo.agregarHijoNodo(nodo3)

        return nodo
        