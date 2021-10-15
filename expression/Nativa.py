
from abstract.NodoAST import NodoAST
from abstract.Instruccion import Instruccion
from tablaSimbolos.Tipo import tipos
from expression.Primitiva import Primitiva
from excepciones.Excepciones import Excepciones
import math

class Nativa(Instruccion):
    def __init__(self, operacion, expresion, expresion2, line, column):
        super().__init__(tipos.ENTERO, line, column)
        self.line = line
        self.column = column
        self.operacion = operacion
        self.expresion = expresion
        self.expresion2 = expresion2
    
    def interpretar(self, tree, table):
        valor = None
        valor2 = None
        valor = self.expresion.interpretar(tree, table)
        if isinstance(valor, Excepciones):
            return valor
        if self.operacion == "upper":
            if valor.tipo == tipos.CADENA:
                self.tipo = tipos.CADENA
                return self.retorno(valor.value.upper())
            elif valor.tipo == tipos.CARACTER:
                self.tipo = tipos.CARACTER
                return self.retorno(valor.value.upper())
            else:
                tree.addError(Excepciones("Semántico", "Operando erroneo para uppercase", self.line, self.column))
                return Excepciones("Semántico", "Operando erroneo para uppercase", self.line, self.column)
        elif self.operacion == "lower":
            if valor.tipo == tipos.CADENA:
                self.tipo = tipos.CADENA
                return self.retorno(valor.value.lower())
            elif valor.tipo == tipos.CARACTER:
                self.tipo = tipos.CARACTER
                return self.retorno(valor.value.lower())
            else:
                tree.addError(Excepciones("Semántico", "Operando erroneo para uppercase", self.line, self.column))
                return Excepciones("Semántico", "Operando erroneo para uppercase", self.line, self.column)
        elif self.operacion == "seno":
            if valor.tipo == tipos.ENTERO:
                self.tipo = tipos.DECIMAL
                return self.retorno(math.sin(int(valor.value)))
            elif valor.tipo == tipos.DECIMAL:
                self.tipo = tipos.DECIMAL
                return self.retorno(math.sin(float(valor.value)))
            else:
                tree.addError(Excepciones("Semántico", "Operando erroneo para seno", self.line, self.column))
                return Excepciones("Semántico", "Operando erroneo para seno", self.line, self.column)
        elif self.operacion == "coseno":
            if valor.tipo == tipos.ENTERO:
                self.tipo = tipos.DECIMAL
                return self.retorno(math.cos(int(valor.value)))
            elif valor.tipo == tipos.DECIMAL:
                self.tipo = tipos.DECIMAL
                return self.retorno(math.cos(float(valor.value)))
            else:
                tree.addError(Excepciones("Semántico", "Operando erroneo para coseno", self.line, self.column))
                return Excepciones("Semántico", "Operando erroneo para coseno", self.line, self.column)
        elif self.operacion == "tangente":
            if valor.tipo == tipos.ENTERO:
                self.tipo = tipos.DECIMAL
                return self.retorno(math.tan(int(valor.value)))
            elif valor.tipo == tipos.DECIMAL:
                self.tipo = tipos.DECIMAL
                return self.retorno(math.tan(float(valor.value)))
            else:
                tree.addError(Excepciones("Semántico", "Operando erroneo para tangente", self.line, self.column))
                return Excepciones("Semántico", "Operando erroneo para tangente", self.line, self.column)
        elif self.operacion == "raiz":
            if int(valor.value) >= 0:
                if valor.tipo == tipos.ENTERO:
                    self.tipo = tipos.DECIMAL
                    return self.retorno(math.sqrt(int(valor.value)))
                elif valor.tipo == tipos.DECIMAL:
                    self.tipo = tipos.DECIMAL
                    return self.retorno(math.sqrt(float(valor.value)))
                else:
                    tree.addError(Excepciones("Semántico", "Operando erroneo para raiz cuadrada", self.line, self.column))
                    return Excepciones("Semántico", "Operando erroneo para raiz cuadrada", self.line, self.column)
            else:
                    tree.addError(Excepciones("Semántico", "Operando erroneo para raiz cuadrada", self.line, self.column))
                    return Excepciones("Semántico", "Operando erroneo para raiz cuadrada", self.line, self.column)
        elif self.operacion == "log10":
            if int(valor.value) > 0:
                if valor.tipo == tipos.ENTERO:
                    self.tipo = tipos.DECIMAL
                    return self.retorno(math.log10(int(valor.value)))
                elif valor.tipo == tipos.DECIMAL:
                    self.tipo = tipos.DECIMAL
                    return self.retorno(math.log10(float(valor.value)))
                else:
                    tree.addError(Excepciones("Semántico", "Operando erroneo para logaritmo de base 10", self.line, self.column))
                    return Excepciones("Semántico", "Operando erroneo para logaritmo de base 10", self.line, self.column)
            else:
                    tree.addError(Excepciones("Semántico", "Operando erroneo para logaritmo de base 10", self.line, self.column))
                    return Excepciones("Semántico", "Operando erroneo para logaritmo de base 10", self.line, self.column)
        elif self.operacion == "log":
            valor2 = self.expresion2.interpretar(tree, table)
            if isinstance(valor2, Excepciones):
                return valor2
            if valor.tipo == tipos.ENTERO:
                if int(valor.value) > 0 and int(valor2.value) > 0:
                    if valor2.tipo == tipos.ENTERO:
                        self.tipo = tipos.DECIMAL
                        return self.retorno(math.log(int(valor2.value), int(valor.value)))
                    elif valor2.tipo == tipos.DECIMAL:
                        self.tipo = tipos.DECIMAL
                        return self.retorno(math.log(int(valor2.value), float(valor.value)))
                else:
                    tree.addError(Excepciones("Semántico", "Base y/o valor erroneos para el logaritmo", self.line, self.column))
                    return Excepciones("Semántico", "Base y/o valor erroneos para el logaritmo", self.line, self.column)
            elif valor.tipo == tipos.DECIMAL:
                if int(valor.value) > 0 and int(valor2.value) > 0:
                    if valor2.tipo == tipos.ENTERO:
                        self.tipo = tipos.DECIMAL
                        return self.retorno(math.log(float(valor2.value), int(valor.value)))
                    elif valor2.tipo == tipos.DECIMAL:
                        self.tipo = tipos.DECIMAL
                        return self.retorno(math.log(float(valor2.value), float(valor.value)))
                else:
                    tree.addError(Excepciones("Semántico", "Base y/o valor erroneos para el logaritmo", self.line, self.column))
                    return Excepciones("Semántico", "Base y/o valor erroneos para el logaritmo", self.line, self.column)
            else:
                tree.addError(Excepciones("Semántico", "Operando erroneo para logaritmo de base", self.line, self.column))
                return Excepciones("Semántico", "Operando erroneo para logaritmo de base", self.line, self.column)
        else:
            tree.addError(Excepciones("Semántico", "Tipo de operacion erroneo", self.line, self.column))
            return Excepciones("Semántico", "Tipo de operacion erroneo", self.line, self.column)
                
    def retorno(self, result):
        return Primitiva(self.tipo, str(result), self.line, self.column)

    def getNodo(self):
        nodo = NodoAST("FUNCION NATIVA")
        nodo.agregarHijo(self.operacion)
        nodo.agregarHijo("(")
        nodo2 = NodoAST("EXPRESION")
        nodo2.agregarHijoNodo(self.expresion.getNodo())
        nodo.agregarHijoNodo(nodo2)
        if self.operacion == "log":
            nodo.agregarHijo(",")
            nodo2 = NodoAST("EXPRESION")
            nodo2.agregarHijoNodo(self.expresion2.getNodo())
            nodo.agregarHijoNodo(nodo2)
        nodo.agregarHijo(")")
        return nodo