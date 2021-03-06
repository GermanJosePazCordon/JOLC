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
        gen.addComment("Empezando IF")
        one = False
        salida = gen.newLabel()
        for i in self.instruccionesIF:
            if one:
                gen.addComment("Agregando etiqueta para elseif")
                gen.addLabel(condicion.ef)
            one = True 
            express = i.getExpresion()
            if express.tipo != tipos.BOOLEAN:
                #Error
                tree.addError(Excepciones("Semántico", "Tipo invalido de condicion", self.line, self.column))
                return Excepciones("Semántico", "Tipo invalido de condicion", self.line, self.column)
            gen.addComment("Interpretando condicion")
            condicion = express.interpretar(tree, table)
            if isinstance(condicion, Excepciones): return condicion
            gen.addLabel(condicion.ev)
            instrucciones = i.getInstrucciones()
            gen.addComment("Interpretando instrucciones IF/ELSEIF")
            for j in instrucciones:
                val = j.interpretar(tree, table)
                if isinstance(val, Excepciones): return val
            gen.addGoto(salida)
        gen.addLabel(condicion.ef)
        if self.instruccionElse != None:
            gen.addComment("Interpretando instrucciones ELSE")
            instrucciones = self.instruccionElse.getInstrucciones()
            for j in instrucciones:
                val = j.interpretar(tree, table)
                if isinstance(val, Excepciones): return val
        gen.addLabel(salida)
        gen.addComment("Fin IF")

    def getNodo(self):
        pass