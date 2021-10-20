from abstract.Instruccion import Instruccion
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
            
            if isinstance(result, Excepciones):
                return result
            if result.tipo != tipos.ENTERO:
                #Error
                print("Tipo de posicion incorrecta")
                return
            pos.append(result.value)
        
        genAux = C3D()
        gen = genAux.getInstance()
        tmpP = gen.addTemp()
        size = gen.addTemp()
        posHeap = gen.addTemp()
        tmpH = gen.addTemp()
        
        variable = table.getVariable(self.id)
        if variable is None:
            #Error
            print("No existe la variable")
            return
        gen.addExp(tmpP, variable.pos, '', '')
        
        for i in pos:
            gen.getHeap(size, tmpP)
            gen.addExp(posHeap, i, '', '')
            gen.addExp(tmpH, tmpP, '+', posHeap)
            gen.getHeap(tmpP, tmpH)
        
        gen.setHeap(tmpH, self.express.interpretar(tree, table).value)
        
    
    def getNodo(self):
        pass
