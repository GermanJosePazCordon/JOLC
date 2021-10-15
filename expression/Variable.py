from abstract.NodoAST import NodoAST
from abstract.Instruccion import Instruccion
from tablaSimbolos.Tipo import tipos
from expression.Primitiva import Primitiva
from excepciones.Excepciones import Excepciones

class Variable(Instruccion):
    def __init__(self, id, line, column):
        super().__init__(tipos.VARIABLE, line, column)
        self.line = line
        self.column = column
        self.id = id
    
    def interpretar(self, tree, table):
        variable = table.getVariable(self.id)
        if variable is None:
            tree.addError(Excepciones("Semántico", "No existe la variable", self.line, self.column))
            return Excepciones("Semántico", "No existe la variable", self.line, self.column)
        else:
            self.tipo = variable.getTipo()
            return Primitiva(self.tipo, variable.getValue(), self.line, self.column)
    
    def getNodo(self):
        nodo = NodoAST("VARIABLE")
        nodo.agregarHijo(self.id)
        return nodo