from abstract.Instruccion import Instruccion
from tablaSimbolos.Tipo import tipos
from tablaSimbolos.C3D import C3D
from tablaSimbolos.Entorno import Entorno
from excepciones.Excepciones import Excepciones

class While(Instruccion):
    def __init__(self, express, listaInstrucciones, line, column):
        super().__init__(tipos.CADENA, line, column)
        self.line = line
        self.column = column
        self.express = express
        self.listaInstrucciones = listaInstrucciones
    
    def interpretar(self, tree, table):
        if self.express.tipo != tipos.BOOLEAN:
            #Error
            tree.addError(Excepciones("Semántico", "Tipo invalido de condicion", self.line, self.column))
            return Excepciones("Semántico", "Tipo invalido de condicion", self.line, self.column)
        genAux = C3D()
        gen = genAux.getInstance()
        gen.addComment("Empezando While")
        continueando = gen.newLabel()
        gen.addGoto(continueando)
        gen.addLabel(continueando)
        condicion = self.express.interpretar(tree, table)
        if isinstance(condicion, Excepciones): return condicion
        tabla = Entorno(table) #Nueva tabla
        tabla.entorno = "While"
        table.addTabla(tabla)
        tabla.breakk = condicion.ef
        tabla.continuee = continueando
        gen.addLabel(condicion.ev)
        for i in self.listaInstrucciones:
            val = i.interpretar(tree, tabla) #Ejecuatamos en la nueva tabla
            if isinstance(val, Excepciones): return val
        gen.addGoto(continueando) 
        gen.addLabel(condicion.ef)
        gen.addComment("Fin While")
        
        
    def getNodo(self):
        pass