from sys import addaudithook
from expression.Primitiva import Primitiva
from abstract.Instruccion import Instruccion
from tablaSimbolos.Tipo import tipos
from tablaSimbolos.C3D import C3D
from tablaSimbolos.Entorno import Entorno
from excepciones.Excepciones import Excepciones
from instrucciones.Break import Break
from instrucciones.Return import Return
from instrucciones.Continue import Continue
from instrucciones.DeclararVariable import DeclararVariable
from expression.Variable import Variable

class For(Instruccion):
    def __init__(self, variable, types, rangoinf, rangosup, cadena, listaInstrucciones, line, column):
        super().__init__(tipos.CADENA, line, column)
        self.line = line
        self.column = column
        self.listaInstrucciones = listaInstrucciones
        self.variable = variable
        self.types = types
        self.rangoinf = rangoinf
        self.rangosup = rangosup
        self.cadena = cadena
    
    def interpretar(self, tree, table):
        if self.types == "rango":
            self.rango(tree, table)
        elif self.types == "cadena":
            self.cadenas(tree, table)
        else:
            self.vector(tree, table)
        return
        
    
    def rango(self, tree, table):
        genAux = C3D()
        gen = genAux.getInstance()
        
        ri = self.rangoinf.interpretar(tree, table)
        ru = self.rangosup.interpretar(tree, table)
        if ri.tipo != tipos.ENTERO and ri.tipo != tipos.DECIMAL:
            #Error
            print("Tipo incorrecto rango inferior")
            return
        if ru.tipo != tipos.ENTERO and ru.tipo != tipos.DECIMAL:
            #Error
            print("Tipo incorrecto rango superior")
            return
        
        tabla = Entorno(table) #Nueva tabla
        
        variable = tabla.getVariable(self.variable)
        if variable is None:
            declara = DeclararVariable(ri.tipo, self.variable, self.rangoinf, None, self.line, self.column)
            declara.interpretar(tree, tabla)
            
        tmpP = gen.addTemp()
        declara = gen.addTemp()
        gen.addExp(tmpP, 'P', '+', '1')
        gen.setStack(tmpP, ri.value)
        
        condicional = gen.newLabel()
        salida = gen.newLabel()
        continuando = gen.newLabel()
        iterador = gen.newLabel()
        
        gen.addLabel(continuando)
        gen.getStack(declara, tmpP)
        
        tabla.breakk = salida
        tabla.continuee = iterador
        
        gen.newIF(declara, "<=", ru.value, condicional)
        gen.addGoto(salida)
        gen.addLabel(condicional)
        
        variable = tabla.getVariable(self.variable)
        gen.setStack(variable.pos, declara)
        for i in self.listaInstrucciones:
            i.interpretar(tree, tabla) #Ejecuatamos en la nueva tabla
        
        gen.addLabel(iterador)
        gen.addExp(declara, declara, "+", "1")
        gen.setStack(tmpP, declara)
        
        gen.addGoto(continuando) 
        gen.addLabel(salida)
    
    def cadenas(self, tree, table):
        genAux = C3D()
        gen = genAux.getInstance()
        
        cadena = self.cadena.interpretar(tree, table)
        
        if cadena.tipo != tipos.CADENA:
            #Error
            print("Tipo incorrecto cadena invalido")
            return
        
        tabla = Entorno(table) #Nueva tabla
        
        variable = tabla.getVariable(self.variable)
        if variable is None:
            value = Primitiva(tipos.CADENA, "X", self.line, self.column)
            declara = DeclararVariable(tipos.CARACTER, self.variable, value, None, self.line, self.column)
            declara.interpretar(tree, tabla)
        
        tmpP = gen.addTemp()
        tmpH = gen.addTemp()
        gen.addExp('H', '0', '', '')
        gen.addExp(tmpH, 'H', '', '')
        gen.addExp(tmpP, 'P', '', '')
        
        
        condicional = gen.newLabel()
        salida = gen.newLabel()
        continuando = gen.newLabel()
        iterador = gen.newLabel()
        
        tmp = gen.addTemp()
        gen.addLabel(continuando)
        gen.getHeap(tmp, tmpH)
        
        tabla.breakk = salida
        tabla.continuee = iterador
        
        gen.newIF(tmp, "!=", "-1", condicional)
        gen.addGoto(salida)
        gen.addLabel(condicional)
        #------------------------------------
        variable = tabla.getVariable(self.variable)
        var = gen.addTemp() 
        gen.getStack(var, variable.pos)
        gen.setHeap(var, tmp)
        for i in self.listaInstrucciones:
            i.interpretar(tree, tabla) #Ejecuatamos en la nueva tabla
        gen.addGoto(iterador)
        gen.addLabel(iterador)
        gen.addExp(tmpH, tmpH, "+", "1")
        #------------------------------------
        gen.addGoto(continuando)
        gen.addLabel(salida)
        
        
        
    
    def vector(self, tree, table):
        pass
    
    def getNodo(self):
        pass
    