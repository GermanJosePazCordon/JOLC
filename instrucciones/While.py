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
            print("Tipo de condicional invalido")
            return
        genAux = C3D()
        gen = genAux.getInstance()
        gen.addComment("Empezando While")
        continueando = gen.newLabel()
        gen.addGoto(continueando)
        gen.addLabel(continueando)
        condicion = self.express.interpretar(tree, table)
        tabla = Entorno(table) #Nueva tabla
        tabla.breakk = condicion.ef
        tabla.continuee = continueando
        gen.addLabel(condicion.ev)
        for i in self.listaInstrucciones:
            i.interpretar(tree, tabla) #Ejecuatamos en la nueva tabla
        gen.addGoto(continueando) 
        gen.addLabel(condicion.ef)
        gen.addComment("Fin While")
        
        
    def getNodo(self):
        pass