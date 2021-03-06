from tablaSimbolos.Entorno import Entorno
from tablaSimbolos.Tipo import tipos

class C3D:
    gen = None
    def __init__(self):
        # Contadores
        self.countTemp = 0
        self.countLabel = 0
        self.code = ''
        self.funcs = ''
        self.natives = ''
        self.inFunc = False
        self.inNatives = False
        self.temps = []
        self.free = []
        self.used = []
        #-----------------------
        self.imports = '\n\t"fmt"'
        self.imath = False
        #-----------------------
        self.BprintString = False
        self.BconcatString = False
        self.Bpotencia = False
        self.BpotenciaString = False
        self.Bmodulo = False
        self.BcompararString = False
        self.BtoString = False
        
    def cleanAll(self):
        # Contadores
        self.countTemp = 0
        self.countLabel = 0
        # Code
        self.code = ''
        self.funcs = ''
        self.natives = ''
        self.inFunc = False
        self.inNatives = False
        # Lista de Temporales
        self.temps = []
        # Lista de Nativas
        self.printString = False
        C3D.gen = C3D()
    
    def getHeader(self):
        ret = 'package main;\n\nimport ('
        ret += self.imports 
        ret += '\n);\n\n'
        if len(self.temps) > 0:
            ret += 'var '
            for temp in range(len(self.temps)):
                ret += self.temps[temp]
                if temp != (len(self.temps) - 1):
                    ret += ", "
            ret += " float64;\n"
        ret += "var P, H float64;\nvar stack [100000]float64;\nvar heap [100000]float64;\n\n"
        return ret

    def getCode(self):
        return f'{self.getHeader()}{self.natives}\n{self.funcs}\nfunc main(){{\n{self.code}\n}}'

    def codeIn(self, code, tab="\t"):
        if(self.inNatives):
            if(self.natives == ''):
                self.natives = self.natives + '\n'
            self.natives = self.natives + tab + code
        elif(self.inFunc):
            if(self.funcs == ''):
                self.funcs = self.funcs + '\n'
            self.funcs = self.funcs + tab +  code
        else:
            self.code = self.code + '\t' +  code

    def getInstance(self):
        if C3D.gen == None:
            C3D.gen = C3D()
        return C3D.gen
    
    def addComment(self, comment):
        self.codeIn(f'/*============== {comment} ==============*/\n')
    
    def addTemp(self):
        if len(self.free) > 0:
            temp = self.free.pop()
            self.used.append(temp)
            return temp
        temp = f't{self.countTemp}'
        self.countTemp += 1
        self.temps.append(temp)
        self.used.append(temp)
        return temp

    def deleteTemp(self, tmp):
        self.used.remove(tmp)
        self.free.append(tmp)

    def newLabel(self):
        label = f'L{self.countLabel}'
        self.countLabel += 1
        return label

    def addLabel(self, label):
        self.codeIn(f'{label}:\n')

    def addGoto(self, label):
        self.codeIn(f'goto {label};\n')
    
    def newIF(self, left, op, right, label):
        self.codeIn(f'if {left} {op} {right} {{goto {label};}}\n')

    def addExp(self, izq, op1, op, op2):
        self.codeIn(f'{izq}={op1}{op}{op2};\n')
    
    def initFun(self, id):
        if(not self.inNatives):
            self.inFunc = True
        self.codeIn(f'func {id}(){{\n', '')
    
    def endFun(self):
        self.codeIn('return;\n}\n');
        if(not self.inNatives):
            self.inFunc = False

    def setStack(self, pos, value):
        self.codeIn(f'stack[int({pos})]={value};\n')
    
    def getStack(self, izq, pos):
        self.codeIn(f'{izq}=stack[int({pos})];\n')

    def newTable(self, size):
        self.codeIn(f'P=P+{size};\n')

    def callFun(self, id):
        self.codeIn(f'{id}();\n')

    def getTable(self, size):
        self.codeIn(f'P=P-{size};\n')

    def setHeap(self, pos, value):
        self.codeIn(f'heap[int({pos})]={value};\n')

    def getHeap(self, izq, pos):
        self.codeIn(f'{izq}=heap[int({pos})];\n')

    def nextHeap(self):
        self.codeIn('H=H+1;\n')
      
    def saveTemp(self, table, temp):
        self.addComment("Guardando temporales")
        tmp = self.addTemp()
        self.addExp(tmp, 'P', '+', table.size)
        self.setStack(tmp, temp)
        table.size = table.size + 1
        self.addComment("Temporales guardados")
    
    def getTemp(self, table, temp):
        self.addComment("Recuperando temporales") 
        table.size = table.size - 1
        tmp = self.addTemp()
        self.addExp(tmp, 'P', '+', table.size)
        self.getStack(temp, tmp)
        self.addComment("Temporales recuperados") 
        
    # INSTRUCCIONES
    def addPrint(self, type, value):
        self.codeIn(f'fmt.Printf("%{type}", int({value}));\n')
        
    def printFloat(self, type, value):
        self.codeIn(f'fmt.Printf("%f", {value});\n')
    
    def printTrue(self):
        self.addComment("Imprimiendo true")
        self.addPrint("c", 116) #t
        self.addPrint("c", 114) #r
        self.addPrint("c", 117) #u
        self.addPrint("c", 101) #e

    def printFalse(self):
        self.addComment("Imprimiendo false")
        self.addPrint("c", 102) #f
        self.addPrint("c", 97)  #a
        self.addPrint("c", 108) #l
        self.addPrint("c", 115) #s
        self.addPrint("c", 101) #e
    
    def printNothing(self):
        self.addComment("Imprimiendo nothing")
        self.addPrint("c", 110) #n
        self.addPrint("c", 111) #o
        self.addPrint("c", 116) #t
        self.addPrint("c", 104) #h
        self.addPrint("c", 105) #i
        self.addPrint("c", 110) #n
        self.addPrint("c", 103) #g
    
    def printString(self):
        if self.BprintString:
            return
        self.BprintString = True
        self.inNatives = True

        self.initFun("printString")
        salida = self.newLabel()
        comprobar = self.newLabel()

        tmpP = self.addTemp()
        tmpH = self.addTemp()

        self.addExp(tmpP, "P", "+", "1")

        self.getStack(tmpH, tmpP)

        tmp = self.addTemp()
        self.addLabel(comprobar)
        self.getHeap(tmp, tmpH)

        self.newIF(tmp, "==", "-1", salida)
        self.addPrint("c", tmp)
        self.addExp(tmpH, tmpH, "+", "1")
        self.addGoto(comprobar)
        self.addLabel(salida)
        self.endFun()
        self.inNatives = False
        
    def concatString(self):
        if self.BconcatString:
            return
        self.BconcatString = True
        self.inNatives = True
        self.initFun("concatString")
        
        tmpH = self.addTemp()
        tmpP = self.addTemp()
        self.addExp(tmpH, 'H', '', '')
        self.addExp(tmpP, "P", "+", "1")
        
        tmp = self.addTemp()
        self.getStack(tmp, tmpP)
        tmpP = self.addTemp()
        self.addExp(tmpP, "P", "+", "2")
        
        salida = self.newLabel()
        condicional = self.newLabel()
        
        self.addLabel(condicional)
        tmp2 = self.addTemp()
        self.getHeap(tmp2, tmp)
        self.newIF(tmp2, "==", "-1", salida)
        self.setHeap("H", tmp2)
        self.nextHeap()
        
        self.addExp(tmp, tmp, "+", "1")
        self.addGoto(condicional)
        
        self.addLabel(salida)
        
        tmpAux = tmp;
        tmp2 = tmp;
        tmp = self.addTemp()
        self.getStack(tmp, tmpP)
        
        salida = self.newLabel()
        condicional = self.newLabel()
        self.addLabel(condicional)
        tmpAux = tmp;
        tmp = self.addTemp()
        self.getHeap(tmp, tmpAux)
        self.newIF(tmp, "==", "-1", salida)
        self.setHeap("H", tmp)
        self.nextHeap()

        tmp = tmpAux
        self.addExp(tmp, tmpAux, "+", "1")
        self.addGoto(condicional)
        
        self.addLabel(salida)
        self.setHeap("H", -1)
        self.nextHeap()
        self.setStack("P", tmpH)
        
        self.endFun()
        self.inNatives = False
    
    def potencia(self):
        if self.Bpotencia:
            return
        self.Bpotencia = True
        self.inNatives = True
        self.initFun("potencia")
        
        tmpH = self.addTemp()
        tmpP = self.addTemp()
        self.addExp(tmpH, 'H', '', '')
        self.addExp(tmpP, "P", "+", "1")
        
        tmp = self.addTemp()
        self.getStack(tmp, tmpP)
        base = tmp
        
        tmpP = self.addTemp()
        self.addExp(tmpP, "P", "+", "2")
        tmp = self.addTemp()
        self.getStack(tmp, tmpP)
        exponente = tmp
        
        exp0 = self.newLabel()
        exp1 = self.newLabel()
        retornando = self.newLabel()
        condicional = self.newLabel()
        salida = self.newLabel()
        continuando = self.newLabel()
        
        self.newIF(exponente, "==", "0", exp0)
        self.addGoto(exp1)
        self.addLabel(exp0)
        self.setStack("P", "1")
        self.addGoto(retornando)
        self.addLabel(exp1)
        
        contador = self.addTemp();
        self.addExp(contador, '1', '', '')
        elevado = self.addTemp();
        self.addExp(elevado, '1', '', '')
        
        self.addLabel(continuando)
        self.newIF(contador, "<=", exponente, condicional)
        self.addGoto(salida)
        self.addLabel(condicional)
        
        tmp2 = self.addTemp()
        self.addExp(tmp2, elevado, "*", base)
        self.addExp(elevado, tmp2, '', '')
        self.setStack(tmpP, tmp2)
        
        self.addExp(contador, contador, "+", 1) #contador = contador + 1
        
        self.addGoto(continuando)
        self.addLabel(salida)
        
        tmp = self.addTemp()
        self.getStack(tmp, tmpP)
        self.setStack("P", tmp)
        
        self.addGoto(retornando)
        self.addLabel(retornando)
        
        self.endFun()
        self.inNatives = False
    
    def potenciaString(self):
        if self.BpotenciaString:
            return
        self.BpotenciaString = True
        self.inNatives = True
        self.initFun("potenciaString")
        
        tmpH = self.addTemp()
        tmpP = self.addTemp()
        self.addExp(tmpH, 'H', '', '')
        self.addExp(tmpP, "P", "+", "1")
        
        busca = self.addTemp()
        self.addExp(busca, tmpP, '', '')
        buscador = self.addTemp()
        self.getStack(buscador, busca)
        
        tmpP = self.addTemp()
        self.addExp(tmpP, "P", "+", "2")
        tmp = self.addTemp()
        self.getStack(tmp, tmpP)
        exponente = tmp
        
        exp1 = self.newLabel()
        condicional = self.newLabel()
        salida = self.newLabel()
        continuando = self.newLabel()
        
        self.newIF(exponente, "==", "1", exp1)
        self.addGoto(continuando)
        #-------------------------------
        self.addLabel(exp1)
        salida2 = self.newLabel()
        tmp2 = self.addTemp()
        self.getHeap(tmp2, buscador)
        self.newIF(tmp2, "==", "-1", salida)
        self.setHeap("H", tmp2)
        self.nextHeap()
        
        self.addExp(buscador, buscador, "+", "1")
        self.addGoto(exp1)
        #-------------------------------
        
        self.addLabel(continuando)
        self.newIF(exponente, ">", "1", condicional)
        self.addGoto(salida)
        self.addLabel(condicional)
        #-------------------------------
        salida2 = self.newLabel()
        tmp2 = self.addTemp()
        self.getHeap(tmp2, buscador)
        self.newIF(tmp2, "==", "-1", salida2)
        self.setHeap("H", tmp2)
        self.nextHeap()
        
        self.addExp(buscador, buscador, "+", "1")
        self.addGoto(condicional)
        
        self.addLabel(salida2)
        self.getStack(buscador, busca)
        
        salida2 = self.newLabel()
        condicional2 = self.newLabel()
        self.addLabel(condicional2)

        tmp2 = self.addTemp()
        self.getHeap(tmp2, buscador)
        self.newIF(tmp2, "==", "-1", salida2)
        self.setHeap("H", tmp2)
        self.nextHeap()

        self.addExp(buscador, buscador, "+", "1")
        self.addGoto(condicional2)
        
        self.addLabel(salida2)
        #-------------------------------
        self.addExp(exponente, exponente, "-", 1)
        self.addGoto(continuando)
        self.addLabel(salida)

        self.setHeap("H", -1)
        self.nextHeap()
        self.setStack("P", tmpH)
        
        self.endFun()
        self.inNatives = False 
    
    def modulo(self):
        if self.Bmodulo:
            return
        self.Bmodulo = True
        self.inNatives = True
        self.initFun("modulo")
        
        tmpH = self.addTemp()
        tmpP = self.addTemp()
        self.addExp(tmpH, 'H', '', '')
        self.addExp(tmpP, "P", "+", "1")
        
        tmp = self.addTemp()
        self.getStack(tmp, tmpP)
        numerador = tmp
        
        tmpP = self.addTemp()
        self.addExp(tmpP, "P", "+", "2")
        tmp = self.addTemp()
        self.getStack(tmp, tmpP)
        denominador = tmp
        
        tmpP = self.addTemp()
        self.addExp(tmpP, "P", "+", "3")
        tmp = self.addTemp()
        self.getStack(tmp, tmpP)
        entero = tmp
        
        div = self.addTemp()
        self.addExp(div, numerador, '/', denominador) 
        
        mul = self.addTemp()
        self.addExp(mul, div, "-", entero)
        
        mul2 = self.addTemp()
        self.addExp(mul2, mul, "*", denominador)
        
        self.setStack("P", mul2)
        
        self.endFun()
        self.inNatives = False 
        
    def compararString(self):
        if self.Bmodulo:
            return
        self.Bmodulo = True
        self.inNatives = True
        self.initFun("compararString")
        
        #tmpH = self.addTemp()
        tmpP = self.addTemp()
        #self.addExp(tmpH, 'H', '', '')
        self.addExp(tmpP, "P", "+", "1")
        
        tmp = self.addTemp()
        self.getStack(tmp, tmpP)
        string1 = tmp
        self.addExp(tmpP, tmpP, "+", "1")
        
        tmp = self.addTemp()
        self.getStack(tmp, tmpP)
        string2 = tmp
        
        condicional = self.newLabel()
        salida = self.newLabel()
        continuando = self.newLabel()
        
        self.addLabel(continuando)
        
        tmp = self.addTemp()
        self.getHeap(tmp, string1)
        tmpAux = tmp # temporal con la primera posicion del heap para el primer string
        tmp = self.addTemp()
        self.getHeap(tmp, string2)
        
        self.newIF(tmpAux, "!=", tmp, condicional)
        self.newIF(tmpAux, "==", -1, salida)
        self.addExp(string1, string1, "+", "1")
        self.addExp(string2, string2, "+", "1")
        self.addGoto(continuando)
        
        self.addLabel(salida)
        self.setStack("P", 1) #CASO DONDE SON IGUALES
        salida = self.newLabel()
        self.addGoto(salida)
        
        self.addLabel(condicional)
        self.setStack("P", 0) #CADO DONDE SON DIFERENTES
        self.addLabel(salida)
        
        self.endFun()
        self.inNatives = False 
    
    def toString(self):
        if self.BtoString:
            return
        self.BtoString = True
        self.inNatives = True
        self.initFun("toString")
        
        if self.imath == False:
            self.imports += ';\n\t"math"'
            self.imath = True
            
        t0 = self.addTemp()
        t1 = self.addTemp()
        t2 = self.addTemp()
        exit = self.newLabel()
        
        self.addExp(t0, 'H', '', '')
        self.addExp(t1, 'P', '+', '1')
        self.getStack(t2, t1)
        
        l0 = self.newLabel()
        
        self.newIF(t2, '>', 0, l0)
        self.setHeap('H', 45)
        self.nextHeap()
        self.addExp(t2, 0, '-', t2)
        self.addLabel(l0)
        
        l1 = self.newLabel()
        self.newIF(t2, '<', 1, l1)
        self.newIF(t2, '<', 10, l1)
        t3 = self.addTemp()
        self.addExp(t3, 1, '', '')

        self.codeIn(f'{t1} = math.Mod({t2},{1});\n')
        self.addExp(t1, t2, '-', t1)
        l3 = self.newLabel()
        l4 = self.newLabel()
        self.addLabel(l3)
        
        self.newIF(t1, '<', 10, l4)
        self.addExp(t1, t1, '/', 10)
        t4 = self.addTemp()
        
        self.codeIn(f'{t4} = math.Mod({t1},{1});\n')
        self.addExp(t1, t1, '-', t4)
        self.addExp(t3, t3, '*', 10)
        self.addGoto(l3)
        self.addLabel(l4)
        
        self.addExp(t4, t1, '+', 48)
        self.setHeap('H', t4)
        self.nextHeap()
        
        self.addExp(t1, t1, '*', t3)
        self.addExp(t2, t2, '-', t1)
        self.addGoto(l0)
        self.addLabel(l1)
        
        self.codeIn(f'{t3} = math.Mod({t2},{1});\n')
        self.addExp(t4, t2, '-', t3)
        self.addExp(t3, t4, '+', 48)
        self.addExp(t2, t2, '-', t4)
        self.setHeap('H', t3)
        self.nextHeap()
        
        self.newIF(t2, '==', 0, exit)
        self.setHeap('H', 46)
        self.nextHeap()
        l6 = self.newLabel()
        t5 = self.addTemp()
        self.addExp(t5, 0, '', '')
        self.addLabel(l6)
        self.newIF(t2, '==', 0, exit)
        self.newIF(t5, '==', 6, exit)
        self.addExp(t2, t2, '*', 10)
        
        self.codeIn(f'{t3} = math.Mod({t2},{1});\n')
        self.addExp(t3, t2, '-', t3)
        self.addExp(t4, t3, '+', 48)
        self.setHeap('H', t4)
        self.nextHeap()
        self.addExp(t2, t2, '-', t3)
        self.addExp(t5, t5, '+', 1)
        self.addGoto(l6)

        self.addLabel(exit)
        self.setHeap('H',-1)
        self.nextHeap()
        self.setStack('P', t0)
        
        self.endFun()
        self.inNatives = False 