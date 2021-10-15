from abstract.Instruccion import Instruccion
from tablaSimbolos.Tipo import tipos
from tablaSimbolos.C3D import C3D

class Println(Instruccion):
    def __init__(self, expresion, line, column):
        super().__init__(tipos.CADENA, line, column)
        self.expresion = expresion  
    
    def interpretar(self, tree, table):
        for i in self.expresion:
            value = i.interpretar(tree, table)
            genAux = C3D()
            gen = genAux.getInstance()
            if(value.tipo == tipos.ENTERO):
                gen.addPrint("d", value.value)
            elif(value.tipo == tipos.DECIMAL):
                gen.printFloat("g", value.value)
            elif value.tipo == tipos.BOOLEAN:
                tempLbl = gen.newLabel()
                gen.putLabel(value.ev)
                gen.printTrue()
                gen.addGoto(tempLbl)
                gen.putLabel(value.ef)
                gen.printFalse()
                gen.putLabel(tempLbl)
            elif value.tipo == tipos.CADENA:
                gen.fPrintString()
                tmp = gen.addTemp()
                gen.addExp(tmp, "P", "+", table.size)
                gen.addExp(tmp, tmp, "+", "1")
                gen.setStack(tmp, value.value)
                gen.newEnv(table.size)
                gen.callFun("printString")
                gen.getStack(gen.addTemp(), "P")
                gen.retEnv(table.size)
            else:
                print("POR HACER")
        gen.addPrint("c", 10)
 
    def getNodo(self):
        pass