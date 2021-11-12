from abstract.Instruccion import Instruccion
from abstract.Retorno import Retornar
from excepciones.Excepciones import Excepciones
from tablaSimbolos.Tipo import tipos
from tablaSimbolos.C3D import C3D
from abstract.Retorno import Retornar

class Variable(Instruccion):
    def __init__(self, id, line, column):
        super().__init__(tipos.VARIABLE, line, column)
        self.line = line
        self.column = column
        self.id = id
    
    def interpretar(self, tree, table):
        genAux = C3D()
        gen = genAux.getInstance()
        
        variable = table.getVariable(self.id)
        if(variable == None):
            print("No existe la variable")
            tree.addError(Excepciones("Semántico", "No existe la variable", self.line, self.column))
            return Excepciones("Semántico", "No existe la variable", self.line, self.column)
        gen.addComment("Guardando variable")
        temp = gen.addTemp()
        tempPos = variable.pos
        if(not variable.isGlobal):
            tempPos = gen.addTemp()
            gen.addExp(tempPos, "P",'+', variable.pos)
        gen.getStack(temp, tempPos)
        if variable.tipo != tipos.BOOLEAN:
            return Retornar(temp, variable.tipo, True, variable.vector, variable.struct)
        if self.ev == '':
            self.ev = gen.newLabel()
        if self.ef == '':
            self.ef = gen.newLabel()
        gen.newIF(temp, '==', '1', self.ev)
        gen.addGoto(self.ef)
        retorno = Retornar(None, tipos.BOOLEAN, False, variable.vector, variable.struct)
        retorno.ev = self.ev
        retorno.ef = self.ef
        gen.addComment("Fin variable")
        return retorno
    
    def getNodo(self):
        pass