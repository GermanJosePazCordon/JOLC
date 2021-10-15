from abstract.NodoAST import NodoAST
from expression.Primitiva import Primitiva
from instrucciones.Atributo import Atributo
from abstract.Instruccion import Instruccion
from tablaSimbolos.Tipo import tipos
from tablaSimbolos.Simbolo import Simbolo
from excepciones.Excepciones import Excepciones

class DeclararVariable(Instruccion):
    def __init__(self, operador, id, value, globall, line, column):
        super().__init__(tipos.CADENA, line, column)
        
        self.operador = operador
        self.id = id
        self.value = value
        self.line = line
        self.column= column
        self.globall = globall
    
    def interpretar(self, tree, table):
        if isinstance(self.value, Atributo):
            self.id = self.value.id
            self.operador = self.value.tipo
            self.line = self.value.line
            self.column = self.value.column
            self.value = Primitiva(self.value.tipo, 0, self.line, self.column)
        valor = self.value.interpretar(tree, table)
        if isinstance(valor, Excepciones):
            return valor
        
        self.sinTipo = False
        if self.operador is None:
            self.sinTipo = True
            self.operador = valor.tipo
            self.type = self.operador
        
        variable = table.getVariable(self.id)
        
        if variable is None:
            if self.operador == valor.tipo:
                table.setVariable(Simbolo(self.line, self.column, self.operador, self.id, valor.value))
            else:
                tree.addError(Excepciones("Semántico", "Tipo y valor incorrectos", self.line, self.column))
                return Excepciones("Semantico", "Tipo y valor incorrectos", self.line, self.column)
        else:
            # CUANDO TENGA VARIABLES
            if self.globall == None:
                variable.setValue(valor.value)
                variable.setTipo(valor.tipo)
            
    def getNodo(self):
        nodo = NodoAST("DECLARARVARIABLE")
        if self.globall is not None:
            nodo.agregarHijo("global")
        nodo.agregarHijo(self.id)
        nodo.agregarHijo("=")
        if self.value.getNodo() is None:
            pass
        nodo2 = NodoAST("EXPRESION")
        nodo2.agregarHijoNodo(self.value.getNodo())
        nodo.agregarHijoNodo(nodo2)
        if self.sinTipo == False:
            nodo.agregarHijo("::")
            if self.tipo is not None:
                nodo.agregarHijo(self.tipo.name)
        nodo.agregarHijo(";")
        return nodo