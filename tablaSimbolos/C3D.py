from tablaSimbolos.Entorno import Entorno

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
        #-----------------------
        self.imports = '\n\t"fmt";'
        self.imath = False
        #-----------------------
        self.printString = False
        self.BconcatString = False
        self.Bpotencia = False
        self.BpotenciaString = False
        self.Bmodulo = False
        self.BcompararString = False
        
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
        ret += '\n)\n\n'
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
    
    def addTemp(self):
        temp = f't{self.countTemp}'
        self.countTemp += 1
        self.temps.append(temp)
        return temp

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

    # INSTRUCCIONES
    def addPrint(self, type, value):
        self.codeIn(f'fmt.Printf("%{type}", int({value}));\n')
        
    def printFloat(self, type, value):
        self.codeIn(f'fmt.Printf("%{type}", float64({value}));\n')
    
    def printTrue(self):
        self.addPrint("c", 116)
        self.addPrint("c", 114)
        self.addPrint("c", 117)
        self.addPrint("c", 101)

    def printFalse(self):
        self.addPrint("c", 102)
        self.addPrint("c", 97)
        self.addPrint("c", 108)
        self.addPrint("c", 115)
        self.addPrint("c", 101)
    
    def fPrintString(self):
        if self.printString:
            return
        self.printString = True
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