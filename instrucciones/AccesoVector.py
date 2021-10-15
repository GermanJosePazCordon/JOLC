
from abstract.NodoAST import NodoAST
from expression.Primitiva import Primitiva
from abstract.Instruccion import Instruccion
from tablaSimbolos.Tipo import tipos
from excepciones.Excepciones import Excepciones

class AccesoVector(Instruccion):
    def __init__(self, types, ids, listaPos, rangoinf, rangosup, line, column):
        super().__init__(tipos.VECTOR, line, column)
        self.line = line
        self.column = column
        self.type = types
        self.listaPos = listaPos
        self.rangoinf = rangoinf
        self.rangosup = rangosup
        self.id = ids
    
    def interpretar(self, tree, table):
        variable = None
        variable = table.getVariable(self.id)
        if variable is None:
            tree.addError(Excepciones("Semántico", "No existe la variable", self.line, self.column))
            return Excepciones("Semantico", "No existe la variable", self.line, self.column)
        pos = []
        if self.type == 'rango':
            #COSAS DE RANGO
            if self.rangoinf.tipo != tipos.ENTERO or self.rangosup.tipo != tipos.ENTERO:
                tree.addError(Excepciones("Semántico", "Tipo de rangos incorrecto", self.line, self.column))
                return Excepciones("Semantico", "Tipo de rango incorrecto", self.line, self.column)
            for i in range((self.rangoinf.value - 1), (self.rangosup.value), 1):
                if i >= len(variable.value):
                    tree.addError(Excepciones("Semántico", "Indice mayor al tamaño", self.line, self.column))
                    return Excepciones("Semantico", "Indice mayor al tamaño", self.line, self.column)
                if i < 0:
                    tree.addError(Excepciones("Semántico", "Indice menor a cero", self.line, self.column))
                    return Excepciones("Semantico", "Indice menor a cero", self.line, self.column)
                pos.append(variable.value[i])
            return Primitiva(tipos.VECTOR, pos, self.line, self.column)
        else:
            for i in self.listaPos:
                result = i.interpretar(tree, table)
                if isinstance(result, Excepciones): return result
                if result.tipo != tipos.ENTERO:
                    tree.addError(Excepciones("Semántico", "Tipo de posicion incorrecta", self.line, self.column))
                    return Excepciones("Semantico", "Tipo de posicion incorrecta", self.line, self.column)
                pos.append(int(result.value) - 1) #EL MENOS UNO PORQUE JULIA EMPIZA DESDE 1 Y PYTHON DESDE 0
            return self.searchValue(tree, table, pos, variable)
        
    def searchValue(self, tree, table, pos, vector):
        valor = None
        if len(pos) > 0:
            if vector.tipo != tipos.VECTOR:
                tree.addError(Excepciones("Semántico", "El acceso no es a un vector", self.line, self.column))
                return Excepciones("Semantico", "El acceso no es a un vector", self.line, self.column)
            if (pos[0] - 1) > len(vector.value):
                tree.addError(Excepciones("Semántico", "Indice mayor al tamaño", self.line, self.column))
                return Excepciones("Semantico", "Indice mayor al tamaño", self.line, self.column)
            valor = vector.value[pos[0]]
            pos.pop(0)
            #SI AUN QUEDAN POSICONES EN LA LISTA DE POSICIONES HACEMOS QUE EL METODO SE LLAME A SI MISMO
            if len(pos) > 0:
                return self.searchValue(tree, table, pos, valor.interpretar(tree, table))
            tmp = valor.interpretar(tree, table)
            return tmp
    
    def getNodo(self):
        nodo = NodoAST("ACCESOVECTOR")
        nodo.agregarHijo(self.id)
        if self.type == 'rango':
            nodo.agregarHijo("[")
            nodo2 = NodoAST("EXPRESION")
            nodo2.agregarHijoNodo(self.rangoinf.getNodo())
            nodo.agregarHijoNodo(nodo2)
            nodo.agregarHijo(":")
            nodo2 = NodoAST("EXPRESION")
            nodo2.agregarHijoNodo(self.rangosup.getNodo())
            nodo.agregarHijoNodo(nodo2)
            nodo.agregarHijo("]")
        else:
            nuevo = NodoAST("LISTAPOS")
            one = True
            for i in self.listaPos:
                if one:
                    nuevo2 = NodoAST("EXPRESION")
                    nuevo2.agregarHijoNodo(i.getNodo())
                    nuevo.agregarHijo("[")
                    nuevo.agregarHijoNodo(nuevo2)
                    nuevo.agregarHijo("]")
                    one = False
                else:
                    tmp = nuevo
                    nuevo3 = NodoAST("EXPRESION")
                    nuevo3.agregarHijoNodo(i.getNodo())
                    nuevo2 = NodoAST("POS")
                    nuevo2.agregarHijo("[")
                    nuevo2.agregarHijoNodo(nuevo3)
                    nuevo2.agregarHijo("]")
                    nuevo = NodoAST("LISTAPOS")
                    nuevo.agregarHijoNodo(tmp)
                    nuevo.agregarHijoNodo(nuevo2)
            nodo.agregarHijoNodo(nuevo)
        return nodo