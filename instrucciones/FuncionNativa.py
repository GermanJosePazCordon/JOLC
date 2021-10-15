
from abstract.NodoAST import NodoAST
from abstract.Instruccion import Instruccion
from tablaSimbolos.Tipo import tipos
from expression.Primitiva import Primitiva
from excepciones.Excepciones import Excepciones

class FuncionNativa(Instruccion):
    def __init__(self, funcion, expresion, tipo, line, column):
        super().__init__(tipos.CADENA, line, column)
        self.line = line
        self.column = column
        self.funcion = funcion
        self.expresion = expresion
        self.tipo = tipo
        self.funcion = funcion
    
    def interpretar(self, tree, table):
        valor = self.expresion.interpretar(tree, table)
        if isinstance(valor, Excepciones): return valor
        if self.funcion == 'float':
            if valor.tipo == tipos.ENTERO:
                self.tipo = tipos.DECIMAL
                return self.retorno(float(valor.value))
            else:
                tree.addError(Excepciones("Semántico", "Tipo incorrecto para la funcion float", self.line, self.column))
                return Excepciones("Semantico", "Tipo incorrecto para la funcion float", self.line, self.column)
        elif self.funcion == 'string':
            self.tipo = tipos.CADENA
            if valor.tipo == tipos.VECTOR:
                return self.retorno(self.getArreglo(tree, table, valor.value))
            return self.retorno(str(valor.value))
        elif self.funcion == 'typeof':
            self.tipo = tipos.CADENA
            tmp = self.getType(valor)
            if tmp == "Tipo no definido":
                tree.addError(Excepciones("Semántico", "Tipo no definido", self.line, self.column))
                return Excepciones("Semantico", "Tipo no definido", self.line, self.column)
            return self.retorno(tmp)
        elif self.funcion == 'parse':
            if self.tipo == tipos.ENTERO: #and valor.tipo == tipos.CADENA:
                self.tipo = tipos.ENTERO
                return self.retorno(int(float(valor.value)))
            elif self.tipo == tipos.DECIMAL: #and valor.tipo == tipos.CADENA:
                self.tipo = tipos.DECIMAL
                return self.retorno(float(valor.value))
            else:
                tree.addError(Excepciones("Semántico", "Tipo incorrecto para la funcion parse", self.line, self.column))
                return Excepciones("Semantico", "Tipo incorrecto para la funcion parse", self.line, self.column)
        elif self.funcion == 'trunc':
            if self.tipo is None:
                self.tipo = tipos.ENTERO
                return self.retorno(int(valor.value)) 
            elif self.tipo == tipos.ENTERO and valor.tipo == tipos.DECIMAL:
                self.tipo = tipos.ENTERO
                return self.retorno(int(valor.value))
            else:
                tree.addError(Excepciones("Semántico", "Tipo incorrecto para la funcion trunc", self.line, self.column))
                return Excepciones("Semantico", "Tipo incorrecto para la funcion trunc", self.line, self.column)    
        elif self.funcion == 'length':
            if valor.tipo == tipos.VECTOR:
                self.tipo = tipos.ENTERO
                return self.retorno(len(valor.value))
            else:
                tree.addError(Excepciones("Semántico", "Tipo incorrecto para la funcion length", self.line, self.column))
                return Excepciones("Semantico", "Tipo incorrecto para la funcion length", self.line, self.column) 
        elif self.funcion == 'pop':
            if valor.tipo == tipos.VECTOR:
                tmp = valor.value.pop()
                self.tipo = tmp.tipo
                if tmp.tipo == tipos.VECTOR:
                    self.tipo = tipos.CADENA
                    return self.retorno(self.getArreglo(tree, table, tmp.value))
                return self.retorno((tmp.value))
            else:
                tree.addError(Excepciones("Semántico", "Tipo incorrecto para la funcion pop", self.line, self.column))
                return Excepciones("Semantico", "Tipo incorrecto para la funcion pop", self.line, self.column)  
        else:
            tree.addError(Excepciones("Semántico", "Tipo de funcion nativa incorrecto", self.line, self.column))
            return Excepciones("Semantico", "Tipo de funcion nativa incorrecto", self.line, self.column)
            
    
    def retorno(self, result):
        return Primitiva(self.tipo, str(result), self.line, self.column)
    
    def getType(self, valor):
        if valor.tipo == tipos.ENTERO:
            return "Int64"
        elif valor.tipo == tipos.DECIMAL:
            return "Float64"
        elif valor.tipo == tipos.CADENA:
            return "String"
        elif valor.tipo == tipos.BOOLEAN:
            return "Bool"
        elif valor.tipo == tipos.CARACTER:
            return "Char"
        elif valor.tipo == tipos.VECTOR:
            return "Arreglo"
        elif valor.tipo == tipos.STRUCT:
            return "Struct"
        elif valor.tipo == tipos.FUNCION:
            return "Funcion"
        elif valor.tipo == tipos.NULO:
            return "Nothing"
        else:
            return "Tipo no definido"
        
    def getArreglo(self, tree, table, vector):
        res = "["
        for i in vector:
            if(i == "[" or i == "]"):
                res += i
                continue
            tmp = i.interpretar(tree, table)
            if isinstance(tmp, Excepciones):
                tree.updateConsola(tmp.show())
                return
            if tmp.tipo == tipos.VECTOR:
                res += self.getArreglo(tree, table, tmp.value) + ","
            else:
                res += str(tmp.value) + ","
        res = res[:-1]
        res += "]"
        return str(res)
    
    def getNodo(self):
        nodo = NodoAST("FUNCION NATIVA")
        nodo.agregarHijo(self.funcion)
        if self.funcion == 'pop':
            nodo.agregarHijo("!")
        nodo.agregarHijo("(")
        if self.funcion == "parse" or self.funcion == "trunc":
            if self.tipo is not None:
                nodo.agregarHijo(self.tipo.name)
                nodo.agregarHijo(",")
        
        nodo2 = NodoAST("EXPRESION")
        nodo2.agregarHijoNodo(self.expresion.getNodo())
        nodo.agregarHijoNodo(nodo2)
        nodo.agregarHijo(")")
        return nodo