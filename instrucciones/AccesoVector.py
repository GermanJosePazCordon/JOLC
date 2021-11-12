from expression.Primitiva import Primitiva
from abstract.Instruccion import Instruccion
from expression.Variable import Variable
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
        else:
            return self.porRango(tree, table)
        
    def porPos(self, tree, table):
        pos = []
        for i in self.listaPos:
            result = i.interpretar(tree, table)
            if isinstance(result, Excepciones): return result
            if isinstance(result, Excepciones):
                return result
            if result.tipo != tipos.ENTERO:
                #Error
                tree.addError(Excepciones("Semántico", "Tipo de posicion de acceso incorrecta", self.line, self.column))
                return Excepciones("Semántico", "Tipo de posicion de acceso incorrecta", self.line, self.column)
            pos.append(result.value)
        genAux = C3D()
        gen = genAux.getInstance()
        gen.addComment("Empezando acceso a vector")
        tmp = gen.addTemp()
        tmpP = gen.addTemp() 
        size = gen.addTemp()
        posHeap = gen.addTemp()
        tmpH = gen.addTemp()
        
        declara = Variable(self.id, self.line, self.column)
        variable = declara.interpretar(tree, table)
        if isinstance(variable, Excepciones): return variable
        
        types = self.verifyTipo(variable.vector, len(pos))
        
        #gen.addExp(tmp, 'P', '+', variable.pos)
        gen.addExp(tmpP, variable.value,'','')

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
        gen.addGoto(salida2)
        gen.addComment("Print BoundsError")
        gen.addLabel(error)
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
        gen.addExp(tmpP, 0, '', '')
        gen.addGoto(salida2)
        
        gen.addLabel(salida2)
        gen.addComment("Fin acceso a vector")
        return Retornar(tmpP, types[0], True, types[1])
      
    def porRango(self, tree, table):
        genAux = C3D()
        gen = genAux.getInstance()
        
        ri = self.rangoinf.interpretar(tree, table)
        ru = self.rangosup.interpretar(tree, table)
        if ri.tipo != tipos.ENTERO and ri.tipo != tipos.DECIMAL:
            #Error
            tree.addError(Excepciones("Semántico", "Tipo incorrecto de rango inferior", self.line, self.column))
            return Excepciones("Semántico", "Tipo incorrecto de rango inferior", self.line, self.column)
        if ru.tipo != tipos.ENTERO and ru.tipo != tipos.DECIMAL:
            #Error
            tree.addError(Excepciones("Semántico", "Tipo incorrecto de rango superior", self.line, self.column))
            return Excepciones("Semántico", "Tipo incorrecto de rango superior", self.line, self.column)
        
        variable = table.getVariable(self.id)
        if variable is None:
            #Error
            tree.addError(Excepciones("Semántico", "No existe la variable", self.line, self.column))
            return Excepciones("Semántico", "No existe la variable", self.line, self.column)
        
        tmpP = gen.addTemp() 
        size = gen.addTemp()
        posHeap = gen.addTemp()
        tmpH = gen.addTemp()
        
        salida = gen.newLabel()
        continuando = gen.newLabel()
        
        gen.addExp(size, ru.value, "-", ri.value)
        gen.addExp(size, size, "+", "1")
        
        gen.addExp(posHeap, ri.value, '', '')
        gen.getStack(tmpP, variable.pos)
        gen.addExp(tmpH, tmpP, '+', posHeap)
        

        
        tmpH2 = gen.addTemp()
        gen.addExp(tmpH2, 'H', '', '')
        tmp = gen.addTemp()
        gen.addExp(tmp, tmpH2, "+", 1)
        
        gen.setHeap('H', len(self.value))
        size = len(self.value) + 1
        gen.addExp('H', 'H', '+', size)
        
        
        
        gen.addLabel(continuando)
        gen.newIF(size, "==", "0", salida)
        #----------------------------------
        
        #----------------------------------
        
        gen.addExp(size, size, "-", "1")
        gen.addExp(tmpH, tmpH, '+', "1")
        gen.addGoto(continuando)
        gen.addLabel(salida)
        
        value = Primitiva(tipos.VECTOR, 's', self.line, self.column)
        return Retornar(value, tipos.VECTOR, True, [variable.vector])
      
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
