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
            value = self.cadena.interpretar(tree, table)
            if isinstance(value, Excepciones): return value
            if value.tipo == tipos.CADENA:
                self.cadenas(tree, table, value)
            else:
                self.vector(tree, table, value)
        return
        
    
    def rango(self, tree, table):
        genAux = C3D()
        gen = genAux.getInstance()
        gen.addComment("Empezando FOR por rango")
        ri = self.rangoinf.interpretar(tree, table)
        if isinstance(ri, Excepciones): return ri
        ru = self.rangosup.interpretar(tree, table)
        if isinstance(ru, Excepciones): return ru
        if ri.tipo != tipos.ENTERO and ri.tipo != tipos.DECIMAL:
            #Error
            tree.addError(Excepciones("Semántico", "Tipo de rango inferior incorrecto", self.line, self.column))
            return Excepciones("Semántico", "Tipo de rango inferior incorrecto", self.line, self.column)
        if ru.tipo != tipos.ENTERO and ru.tipo != tipos.DECIMAL:
            #Error
            tree.addError(Excepciones("Semántico", "Tipo de rango superior incorrecto", self.line, self.column))
            return Excepciones("Semántico", "Tipo de rango superior incorrecto", self.line, self.column)
        
        tabla = Entorno(table) #Nueva tabla
        tabla.entorno = "For"
        table.addTabla(tabla)
        
        variable = tabla.getVariable(self.variable)
        if variable is None:
            gen.addComment("Declarando iterador")
            declara = DeclararVariable(ri.tipo, self.variable, self.rangoinf, None, self.line, self.column)
            val  = declara.interpretar(tree, tabla)
            if isinstance(val, Excepciones): return val
        variable = tabla.getVariable(self.variable)    
        tmpP = gen.addTemp()
        declara = gen.addTemp()
        gen.addExp(tmpP, 'P', '+', variable.pos)
        
        condicional = gen.newLabel()
        salida = gen.newLabel()
        continuando = gen.newLabel()
        iterador = gen.newLabel()
        
        gen.setStack(tmpP, ri.value)
        
        gen.addLabel(continuando)
        gen.getStack(declara, tmpP)
        
        tabla.breakk = salida
        tabla.continuee = iterador
        
        gen.newIF(declara, "<=", ru.value, condicional)
        gen.addGoto(salida)
        gen.addLabel(condicional)
        
        #gen.setStack(tmpP, declara)
        for i in self.listaInstrucciones:
            if i != '':
                val = i.interpretar(tree, tabla) #Ejecuatamos en la nueva tabla
                if isinstance(val, Excepciones): return val
        
        gen.addGoto(iterador)
        gen.addLabel(iterador)
        gen.addExp(declara, declara, "+", "1")
        gen.setStack(tmpP, declara)
        
        gen.addGoto(continuando) 
        gen.addLabel(salida)
        gen.addComment("Fin FOR por rango")
        
    def cadenas(self, tree, table, cadena):
        genAux = C3D()
        gen = genAux.getInstance()
        gen.addComment("Empezando FOR por cadena")
        if cadena.tipo != tipos.CADENA:
            #Error
            tree.addError(Excepciones("Semántico", "La expresion de es de tipo cadena", self.line, self.column))
            return Excepciones("Semántico", "La expresion de es de tipo cadena", self.line, self.column)
        
        tabla = Entorno(table) #Nueva tabla
        tabla.entorno = "For"
        table.addTabla(tabla)
        
        variable = tabla.getVariable(self.variable)
        if variable is None:
            gen.addComment("Declarando variable iteradora")
            value = Primitiva(tipos.CARACTER, 'A', self.line, self.column)
            declara = DeclararVariable(None, self.variable, value, None, self.line, self.column)
            val = declara.interpretar(tree, tabla)
            if isinstance(val, Excepciones): return val
        variable = tabla.getVariable(self.variable)
        tmpP = gen.addTemp()
        tmpH = gen.addTemp()
        gen.addExp(tmpH, cadena.value, '', '')
        gen.addExp(tmpP, 'P', '+', variable.pos)
        
        salida = gen.newLabel()
        continuando = gen.newLabel()
        iterador = gen.newLabel()
        
        tmp = gen.addTemp()
        gen.addLabel(continuando)
        gen.getHeap(tmp, tmpH)
        
        tabla.breakk = salida
        tabla.continuee = iterador
        
        gen.newIF(tmp, "==", "-1", salida)
        #------------------------------------
        
        gen.setStack(tmpP, tmp)
        for i in self.listaInstrucciones:
            val = i.interpretar(tree, tabla) #Ejecuatamos en la nueva tabla
            if isinstance(val, Excepciones): return val
            
        gen.addGoto(iterador)
        gen.addLabel(iterador)
        gen.addExp(tmpH, tmpH, "+", "1")
        #------------------------------------
        gen.addGoto(continuando)
        gen.addLabel(salida)
        gen.addComment("Fin FOR por cadena")
           
    def vector(self, tree, table, vector):
        genAux = C3D()
        gen = genAux.getInstance()
        gen.addComment("Empezando FOR por vector")
        if vector.tipo != tipos.VECTOR:
            #Error
            tree.addError(Excepciones("Semántico", "La expresion de es de tipo vector", self.line, self.column))
            return Excepciones("Semántico", "La expresion de es de tipo vector", self.line, self.column)

        tabla = Entorno(table) #Nueva tabla
        tabla.entorno = "For"
        table.addTabla(tabla)
        
        variable = tabla.getVariable(self.variable)
        if variable is None:
            if type(vector.vector[0]) is list:
                tipo = tipos.VECTOR
            else:
                tipo = vector.vector[0]
            gen.addComment("Declarando variable iteradora")
            value = Primitiva(tipos.ENTERO, 0, self.line, self.column)
            declara = DeclararVariable(tipos.CARACTER, self.variable, value, None, self.line, self.column)
            val = declara.interpretar(tree, tabla)
            if isinstance(val, Excepciones): return val
            variable = tabla.getVariable(self.variable)
            variable.tipo = tipo
            variable.vector = vector.vector[0]
        variable = tabla.getVariable(self.variable)

        tmpP = gen.addTemp()
        gen.addExp(tmpP, 'P', '+', variable.pos)
        #gen.addExp(vector.value, vector.value, '+', tmpP)
        size = gen.addTemp()
        gen.getHeap(size, vector.value)
        inicio = gen.addTemp()
        gen.addExp(inicio, vector.value, "+", "1")
        
        tmp = gen.addTemp()
        gen.getHeap(tmp, inicio)
        gen.setStack(tmpP, tmp)
        
        gen.addExp(inicio, inicio, "+", "1")
        
        continuando = gen.newLabel()
        salida = gen.newLabel()
        iterador = gen.newLabel()

        gen.addLabel(continuando)
        
        tabla.breakk = salida
        tabla.continuee = iterador
        
        gen.newIF(size, "==", "0", salida)
        
        tmp = gen.addTemp()
        gen.getHeap(tmp, inicio)
        
        #gen.setStack(tmpP, tmp)
        
        for i in self.listaInstrucciones:
            val = i.interpretar(tree, tabla) #Ejecuatamos en la nueva tabla
            if isinstance(val, Excepciones): return val
        
        gen.addGoto(iterador)
        gen.addLabel(iterador)
        gen.addExp(inicio, inicio, "+", "1")
        gen.addExp(size, size, "-", "1")
        
        gen.setStack(tmpP, tmp)
        
        gen.addGoto(continuando)
        gen.addLabel(salida)
        gen.addComment("Fin FOR por vector")
        
    def getNodo(self):
        pass
    