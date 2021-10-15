from abstract.Instruccion import Instruccion
from tablaSimbolos.Tipo import tipos
from tablaSimbolos.C3D import C3D

class Print(Instruccion):
    def __init__(self, expresion, line, column):
        super().__init__(tipos.CADENA, line, column)
        self.expresion = expresion  
    
    def interpretar(self, tree, table):
        for i in self.expresion:
            value = i.interpretar(tree, table)
            genAux = C3D()
            gen = genAux.getInstance()
            if value.tipo == tipos.ENTERO:
                gen.Print("d", value.value)
            elif value.tipo == tipos.DECIMAL:
                gen.Print("f", value.value)
            elif value.tipo == tipos.BOOLEAN:
                etiqueta = gen.newLabel()
                gen.addLabel(value.ev)
                gen.printTrue()
                gen.addGoto(etiqueta)
                gen.addLabel(value.ef)
                gen.printFalse()
                gen.addLabel(etiqueta)
            elif value.tipo == tipos.CADENA:
                gen.printString()
                tmp = gen.addTemp()
                gen.addExp(tmp, 'P', table.size, '+')
                gen.addExp(tmp, tmp, '1', '+')
                gen.setStack(tmp, value.value)
                gen.newTable(table.size)
                gen.callFun('printString')
                temp = gen.addTemp()
                gen.getStack(temp, 'P')
                gen.getTable(table.size)
            else:
                print("POR HACER")
        
    def getNodo(self):
        pass