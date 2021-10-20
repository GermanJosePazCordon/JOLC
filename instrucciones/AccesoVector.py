from expression.Primitiva import Primitiva
from abstract.Instruccion import Instruccion
from tablaSimbolos.Tipo import tipos
from tablaSimbolos.C3D import C3D
from abstract.Retorno import Retornar
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
        if self.type == 'pos':
            return self.porPos(tree, table)
        
    def porPos(self, tree, table):
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
        
        return Retornar(tmpP, tipos.ENTERO, True)
        
    
    def getNodo(self):
        pass
