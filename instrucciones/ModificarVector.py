from abstract.NodoAST import NodoAST
from abstract.Instruccion import Instruccion
from tablaSimbolos.Tipo import tipos
from excepciones.Excepciones import Excepciones

class ModificarVector(Instruccion):
    def __init__(self, ids, listaPos, express, line, column):
        super().__init__(tipos.VECTOR, line, column)
        self.line = line
        self.column = column
        self.listaPos = listaPos
        self.express = express
        self.id = ids
    
    def interpretar(self, tree, table):
        variable = None
        variable = table.getVariable(self.id)
        if variable is None:
            tree.addError(Excepciones("Semántico", "No existe la variable", self.line, self.column))
            return Excepciones("Semantico", "No existe la variable", self.line, self.column)
        pos = []
        for i in self.listaPos:
            result = i.interpretar(tree, table)
            if isinstance(result, Excepciones): return result
            if result.tipo != tipos.ENTERO:
                tree.addError(Excepciones("Semántico", "Tipo de posicion incorrecta", self.line, self.column))
                return Excepciones("Semantico", "Tipo de posicion incorrecta", self.line, self.column)
            pos.append(int(result.value) - 1) #EL MENOS UNO PORQUE JULIA EMPIZA DESDE 1 Y PYTHON DESDE 0
        self.searchPos(tree, table, pos, variable, self.express)   
        
    def searchPos(self, tree, table, pos, vector, expresion):
        valor = None
        indice = None
        if len(pos) > 0:
            if vector.tipo != tipos.VECTOR:
                tree.addError(Excepciones("Semántico", "El acceso no es a un vector", self.line, self.column))
                return Excepciones("Semantico", "El acceso no es a un vector", self.line, self.column)
            if (pos[0] - 1) > len(vector.value):
                tree.addError(Excepciones("Semántico", "Indice mayor al tamaño", self.line, self.column))
                return Excepciones("Semantico", "Indice mayor al tamaño", self.line, self.column)
            valor = vector.value[pos[0]]
            indice = pos.pop(0)
            #SI AUN QUEDAN POSICONES EN LA LISTA DE POSICIONES HACEMOS QUE EL METODO SE LLAME A SI MISMO
            if len(pos) > 0:
                self.searchPos(tree, table, pos, valor.interpretar(tree, table), expresion)
            else:
               vector.value[indice] = expresion.interpretar(tree, table)
            
            
    
    def getNodo(self):
        nodo = NodoAST("MOD_VECTOR")
        nodo.agregarHijo(self.id)
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
        nodo.agregarHijo("=")
        nuevo = NodoAST("EXPRESION")
        nuevo.agregarHijoNodo(self.express.getNodo())
        nodo.agregarHijoNodo(nuevo)
        nodo.agregarHijo(";")
        return nodo