from tablaSimbolos.Entorno import Entorno

class C3D:
    generator = None
    def __init__(self):
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
        C3D.generator = C3D()
    
    #############
    # CODE
    #############
    def getHeader(self):
        ret = 'package main;\n\nimport (\n\t"fmt"\n)\n\n'
        if len(self.temps) > 0:
            ret += 'var '
            for temp in range(len(self.temps)):
                ret += self.temps[temp]
                if temp != (len(self.temps) - 1):
                    ret += ", "
            ret += " float64\n"
        ret += "var P, H float64;\nvar stack [100000]float64;\nvar heap [100000]float64;\n\n"
        return ret

    def getCode(self):
        return f'{self.getHeader()}{self.natives}\n{self.funcs}\nfunc main(){{\n{self.code}\n}}'

    def codeIn(self, code, tab="\t"):
        if(self.inNatives):
            if(self.natives == ''):
                self.natives = self.natives + '/*-----NATIVES-----*/\n'
            self.natives = self.natives + tab + code
        elif(self.inFunc):
            if(self.funcs == ''):
                self.funcs = self.funcs + '/*-----FUNCS-----*/\n'
            self.funcs = self.funcs + tab +  code
        else:
            self.code = self.code + '\t' +  code

    def addComment(self, comment):
        self.codeIn(f'/* {comment} */\n')
    
    def getInstance(self):
        if C3D.generator == None:
            C3D.generator = C3D()
        return C3D.generator

    def addSpace(self):
        self.codeIn("\n")

    ########################
    # Manejo de Temporales
    ########################
    def addTemp(self):
        temp = f't{self.countTemp}'
        self.countTemp += 1
        self.temps.append(temp)
        return temp

    #####################
    # Manejo de Labels
    #####################
    def newLabel(self):
        label = f'L{self.countLabel}'
        self.countLabel += 1
        return label

    def putLabel(self, label):
        self.codeIn(f'{label}:\n')

    ###################
    # GOTO
    ###################
    def addGoto(self, label):
        self.codeIn(f'goto {label};\n')
    
    ###################
    # IF
    ###################
    def addIf(self, left, op, right, label):
        self.codeIn(f'if {left} {op} {right} {{goto {label};}}\n')

    ###################
    # EXPRESIONES
    ###################
    def addExp(self, result, left, op, right):
        self.codeIn(f'{result}={left}{op}{right};\n')
    
    ###################
    # FUNCS
    ###################
    def addBeginFunc(self, id):
        if(not self.inNatives):
            self.inFunc = True
        self.codeIn(f'func {id}(){{\n', '')
    
    def addEndFunc(self):
        self.codeIn('return;\n}\n');
        if(not self.inNatives):
            self.inFunc = False

    ###############
    # STACK
    ###############
    def setStack(self, pos, value):
        self.codeIn(f'stack[int({pos})]={value};\n')
    
    def getStack(self, place, pos):
        self.codeIn(f'{place}=stack[int({pos})];\n')

    #############
    # ENVS
    #############
    def newEnv(self, size):
        self.codeIn(f'P=P+{size};\n')

    def callFun(self, id):
        self.codeIn(f'{id}();\n')

    def retEnv(self, size):
        self.codeIn(f'P=P-{size};\n')

    ###############
    # HEAP
    ###############
    def setHeap(self, pos, value):
        self.codeIn(f'heap[int({pos})]={value};\n')

    def getHeap(self, place, pos):
        self.codeIn(f'{place}=heap[int({pos})];\n')

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
    
    ##############
    # NATIVES
    ##############
    def fPrintString(self):
        if self.printString:
            return
        self.printString = True
        self.inNatives = True

        self.addBeginFunc("printString")
        salida = self.newLabel()
        comprobar = self.newLabel()

        tmpP = self.addTemp()
        tmpH = self.addTemp()

        self.addExp(tmpP, "P", "+", "1")

        self.getStack(tmpH, tmpP)

        tmp = self.addTemp()
        self.putLabel(comprobar)
        self.getHeap(tmp, tmpH)

        self.addIf(tmp, "==", "-1", salida)
        self.addPrint("c", tmp)
        self.addExp(tmpH, tmpH, "+", "1")
        self.addGoto(comprobar)
        self.putLabel(salida)
        self.addEndFunc()
        self.inNatives = False