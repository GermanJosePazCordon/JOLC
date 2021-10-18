from abstract.NodoAST import NodoAST
from instrucciones.Break import Break
from instrucciones.Return import Return
from instrucciones.Continue import Continue
from abstract.Instruccion import Instruccion
from tablaSimbolos.Tipo import tipos
from tablaSimbolos.C3D import C3D
from excepciones.Excepciones import Excepciones

class EvaluarIF(Instruccion):
    def __init__(self, instruccionesIF, instruccionElse, line, column):
        super().__init__(tipos.CADENA, line, column)
        self.line = line
        self.column = column
        self.instruccionesIF = instruccionesIF
        self.instruccionElse = instruccionElse
    
    def interpretar(self, tree, table):
        genAux = C3D()
        gen = genAux.getInstance()
        one = False
        salida = gen.newLabel()
        for i in self.instruccionesIF:
            if one:
                gen.addLabel(condicion.ef)
            one = True
            express = i.getExpresion()
            if express.tipo != tipos.BOOLEAN:
                print('Tipo invalido de condicion')
                return
            condicion = express.interpretar(tree, table)
        
            gen.addLabel(condicion.ev)
            instrucciones = i.getInstrucciones()
            for j in instrucciones:
                j.interpretar(tree, table)
            gen.addGoto(salida)
        gen.addLabel(condicion.ef)
        if self.instruccionElse != None:
            instrucciones = self.instruccionElse.getInstrucciones()
            for j in instrucciones:
                j.interpretar(tree, table)
                gen.addLabel(salida)

    def getNodo(self):
        pass