from abstract.NodoAST import NodoAST
from excepciones.Excepciones import Excepciones

from abstract.Instruccion import Instruccion
from tablaSimbolos.Tipo import tipos

class AccesoAtributo(Instruccion):
    def __init__(self, idVar, listaID, line, column):
        super().__init__(tipos.CADENA, line, column)
        self.line = line
        self.column = column
        self.idVar = idVar
        self.listaID = listaID
    
    def interpretar(self, tree, table):
        variable = table.getVariable(self.idVar)
        if variable is None:
            tree.addError(Excepciones("Semántico", "No existe la variable", self.line, self.column))
            return Excepciones("Semantico", "No existe la variable", self.line, self.column)
        if variable.tipo != tipos.STRUCT:
            tree.addError(Excepciones("Semántico", "El id no es de una variable tipo struct", self.line, self.column))
            return Excepciones("Semantico", "El id no es de una variable tipo struct", self.line, self.column)
        valor = None
        dic = variable.value
        for i in range(len(self.listaID)):
            lavaes = dic.keys()
            if self.listaID[i] in dic.keys():
                if i == len(self.listaID) - 1:
                    valor = dic[self.listaID[i]]
                    #valor = valor.interpretar(tree, table)
                    return valor
                else:
                    if dic[self.listaID[i]].tipo == tipos.STRUCT:
                        valor = dic[self.listaID[i]]
                        dic = valor.value
                        continue
                    else:
                        #No existe el dic
                        tree.addError(Excepciones("Semántico", "El valor del atriuto no es de tipo struct", self.line, self.column))
                        return Excepciones("Semantico", "El valor del atriuto no es de tipo struct", self.line, self.column)
            else:
                #la llave no existe
                tree.addError(Excepciones("Semántico", "No existe el atributo", self.line, self.column))
                return Excepciones("Semantico", "No existe el atributo", self.line, self.column)
            
    def getNodo(self):
        nodo = NodoAST("ACCESOATRIBUTO")
        nodo.agregarHijo(self.idVar)
        nodo.agregarHijo(".")
        nuevo = NodoAST("LISTAID")
        one = True;
        for i in self.listaID:
            if one:
                nuevo.agregarHijo(i)
                one = False
            else:
                tmp = nuevo
                nuevo2 = NodoAST("ID")
                nuevo2.agregarHijo(".")
                nuevo2.agregarHijo(i)
                nuevo = NodoAST("LISTAID")
                nuevo.agregarHijoNodo(tmp)
                nuevo.agregarHijoNodo(nuevo2)
        nodo.agregarHijoNodo(nuevo)
        return nodo