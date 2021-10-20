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
            if value.tipo == tipos.ENTERO:
                gen.addPrint("d", value.value)
            elif value.tipo == tipos.DECIMAL:
                gen.printFloat("g", value.value)
            elif value.tipo == tipos.CARACTER:
                gen.addPrint("c", ord(value.value))
            elif value.tipo == tipos.BOOLEAN:
                tempLbl = gen.newLabel()
                gen.addLabel(value.ev)
                gen.printTrue()
                gen.addGoto(tempLbl)
                gen.addLabel(value.ef)
                gen.printFalse()
                gen.addLabel(tempLbl)
            elif value.tipo == tipos.CADENA:
                gen.fPrintString()
                tmp = gen.addTemp()
                gen.addExp(tmp, "P", "+", table.size)
                gen.addExp(tmp, tmp, "+", "1")
                gen.setStack(tmp, value.value)
                gen.newTable(table.size)
                gen.callFun("printString")
                gen.getStack(gen.addTemp(), "P")
                gen.getTable(table.size)
            elif value.tipo == tipos.VECTOR:
                gen.printVector()
                tmp = gen.addTemp()
                gen.addExp(tmp, "P", "+", table.size)
                gen.addExp(tmp, tmp, "+", "1")
                gen.setStack(tmp, value.value)
                gen.newTable(table.size)
                gen.callFun("printVector")
                gen.getStack(gen.addTemp(), "P")
                gen.getTable(table.size)
                pass
            else:
                print("POR HACER")
        gen.addPrint("c", 10)
 
    def getNodo(self):
        pass