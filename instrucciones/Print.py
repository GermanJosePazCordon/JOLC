from abstract.Instruccion import Instruccion
from excepciones.Excepciones import Excepciones
from tablaSimbolos.Tipo import tipos
from tablaSimbolos.C3D import C3D

class Print(Instruccion):
    def __init__(self, expresion, line, column):
        super().__init__(tipos.CADENA, line, column)
        self.expresion = expresion  
    
    def interpretar(self, tree, table):
        for i in self.expresion:
            value = i.interpretar(tree, table)
            if isinstance(value, Excepciones): return value
            genAux = C3D()
            gen = genAux.getInstance()
            if value.tipo == tipos.ENTERO:
                gen.addPrint("d", value.value)
            elif value.tipo == tipos.DECIMAL:
                gen.printFloat("f", value.value)
            elif value.tipo == tipos.CARACTER:
                gen.addPrint("c", value.value)
            elif value.tipo == tipos.BOOLEAN:
                tempLbl = gen.newLabel()
                gen.addLabel(value.ev)
                gen.printTrue()
                gen.addGoto(tempLbl)
                gen.addLabel(value.ef)
                gen.printFalse()
                gen.addLabel(tempLbl)
            elif value.tipo == tipos.NULO:
                gen.printNothing()
            elif value.tipo == tipos.CADENA:
                gen.printString()
                tmp = gen.addTemp()
                gen.addExp(tmp, "P", "+", table.size)
                gen.addExp(tmp, tmp, "+", "1")
                gen.setStack(tmp, value.value)
                gen.newTable(table.size)
                gen.callFun("printString")
                gen.getStack(gen.addTemp(), "P")
                gen.getTable(table.size)
            elif value.tipo == tipos.VECTOR:
                gen.addComment("Empezando print vector")
                size = gen.addTemp()
                gen.getHeap(size, value.value)
                inicio = gen.addTemp()
                gen.addExp(inicio, value.value, "+", "1")
                gen.addPrint("c", 91)
                self.printVector(tree, table, inicio, size, value.vector[0])
                gen.addPrint("c", 93)
                gen.addComment("Fin print vector")
 
    def printVector(self, tree, table, inicio, size, vector):
        genAux = C3D()
        gen = genAux.getInstance()
        
        tmp = gen.addTemp()
        continuando = gen.newLabel()
        elemento = gen.newLabel()
        salida = gen.newLabel()
             
        gen.addGoto(elemento)
        gen.addLabel(continuando)
        gen.newIF(size, "==", "0", salida)
          
        gen.addPrint("c", 44)
        gen.addLabel(elemento)
        
        
        gen.getHeap(tmp, inicio)
        if type(vector) is list:   
            gen.addPrint("c", 91)
            
            tmpS = gen.addTemp()
            tmpI = gen.addTemp()
            gen.addComment("Guardando temporales")
            gen.addExp(tmpS, size, '', '')
            gen.addExp(tmpI, inicio, '', '')
            gen.getHeap(size, tmp)
            gen.addExp(inicio, tmp, "+", "1")
            self.printVector(tree, table, inicio, size, vector[0])  
            gen.addComment("Recuperando temporales")
            gen.addExp(size, tmpS, '', '')
            gen.addExp(inicio, tmpI, '', '')
            gen.addPrint("c", 93)
        else:
            if vector == tipos.ENTERO:
                gen.addPrint("d", tmp)
            elif vector == tipos.DECIMAL:
                gen.printFloat("g", tmp)
            elif vector == tipos.CARACTER: 
                gen.addPrint("c", tmp) 
            elif vector == tipos.CADENA:
                gen.printString()
                tmp2 = gen.addTemp()
                gen.addExp(tmp2, "P", "+", table.size)
                gen.addExp(tmp2, tmp2, "+", "1")
                gen.setStack(tmp2, tmp)
                gen.newTable(table.size)
                gen.callFun("printString")
                gen.getStack(gen.addTemp(), "P")
                gen.getTable(table.size)
            
        gen.addExp(inicio, inicio, "+", "1")
        gen.addExp(size, size, "-", "1")
        
        gen.addGoto(continuando)
        gen.addLabel(salida)
        
        
    def getNodo(self):
        pass