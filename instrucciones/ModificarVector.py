from abstract.Instruccion import Instruccion
from expression.Variable import Variable
from tablaSimbolos.Tipo import tipos
from tablaSimbolos.C3D import C3D
from abstract.Retorno import Retornar
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
        pos = []
        for i in self.listaPos:
            result = i.interpretar(tree, table)
            if isinstance(result, Excepciones): return result
            if result.tipo != tipos.ENTERO:
                #Error
                tree.addError(Excepciones("Semántico", "Tipo de posicion de acceso invalido", self.line, self.column))
                return Excepciones("Semántico", "Tipo de poscion de acceso invalido", self.line, self.column)
            pos.append(result.value)
            
        declara = Variable(self.id, self.line, self.column)
        variable = declara.interpretar(tree, table)
        if isinstance(variable, Excepciones): return variable
        
        value = self.express.interpretar(tree, table)
        if isinstance(value, Excepciones): return value
        
        types = self.verifyTipo(variable.vector, len(pos))
        if value.tipo != types[0]:
            #Error
            tree.addError(Excepciones("Semántico", "Tipo de valor incorrecto al modificar vector", self.line, self.column))
            return Excepciones("Semántico", "Tipo de valor incorrecto al modificar vector", self.line, self.column)
        
        genAux = C3D()
        gen = genAux.getInstance()
        gen.addComment("Empezando modificacion a vector")
        tmp = gen.addTemp()
        tmpP = gen.addTemp()
        size = gen.addTemp()
        posHeap = gen.addTemp()
        tmpH = gen.addTemp()
        
        
        gen.addExp(tmpP, variable.value,'','')

        
        correcto = gen.newLabel()
        error = gen.newLabel()
        salida2 = gen.newLabel()
        
        for i in pos:
            condicional = gen.newLabel()
            gen.getHeap(size, tmpP)
            gen.addExp(posHeap, i, '', '')
            
            
            gen.newIF(posHeap, '>', size, error)
            gen.newIF(posHeap, '<', '1', error)
            gen.addGoto(condicional)
            
            gen.addLabel(condicional)
            gen.addExp(tmpH, tmpP, '+', posHeap)
            gen.getHeap(tmpP, tmpH)
        gen.addGoto(correcto)
        
        gen.addLabel(error)
        gen.addComment("Print BoundsError")
        gen.addPrint("c", 66)
        gen.addPrint("c", 111)
        gen.addPrint("c", 117)
        gen.addPrint("c", 110)
        gen.addPrint("c", 100)
        gen.addPrint("c", 115)
        gen.addPrint("c", 69)
        gen.addPrint("c", 114)
        gen.addPrint("c", 114)
        gen.addPrint("c", 111)
        gen.addPrint("c", 114)
        gen.addPrint("c", 10)
        gen.addGoto(salida2)
        
        gen.addLabel(correcto)
        gen.setHeap(tmpH, value.value)
        gen.addLabel(salida2)
        gen.addComment("Fin modificacion a vector")
    
    def verifyTipo(self, vector, lvl):
        if lvl == 0:
            if type(vector) is list:
                tipo = tipos.VECTOR
                tmp = [tipo, vector]
            else:
                tipo = vector
                tmp = [tipo, vector]
        else:
            tmp = self.verifyTipo(vector[0], (lvl - 1))
        return tmp
    
    def getNodo(self):
        pass
