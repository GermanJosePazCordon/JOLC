
from abstract.NodoAST import NodoAST
from instrucciones.Break import Break
from instrucciones.Return import Return
from instrucciones.Continue import Continue
from abstract.Instruccion import Instruccion
from tablaSimbolos.Tipo import tipos
from excepciones.Excepciones import Excepciones

class EvaluarIF(Instruccion):
    def __init__(self, instruccionesIF, instruccionElse, line, column):
        super().__init__(tipos.CADENA, line, column)
        self.line = line
        self.column = column
        self.instruccionesIF = instruccionesIF
        self.instruccionElse = instruccionElse
    
    def interpretar(self, tree, table):
        for i in self.instruccionesIF:
            express = i.getExpresion()
            if(express.tipo != tipos.BOOLEAN):
                tree.addError(Excepciones("Semántico", "Tipo de condicional invalido", self.line, self.column))
                return Excepciones("Semantico", "Tipo de condicional invalido", self.line, self.column)
            condicion = express.interpretar(tree, table)
            if isinstance(condicion, Excepciones): return condicion
            if(condicion.value == 'true'):
                #CREANDO EL NUEVO ENTORNO
                instrucciones = i.getInstrucciones()
                for j in instrucciones:
                    valor = j.interpretar(tree, table)
                    if isinstance(valor, Break): return valor
                    if isinstance(valor, Continue): return valor
                    if isinstance(valor, Return): return valor
                return 
        if(self.instruccionElse != None):
            instrucciones = self.instruccionElse.getInstrucciones()
            for j in instrucciones:
                    valor = j.interpretar(tree, table)
                    if isinstance(valor, Excepciones): return valor
                    if isinstance(valor, Break): return valor
                    if isinstance(valor, Continue): return valor
                    if isinstance(j, Return): return valor
            

    def getNodo(self):
        nodo = NodoAST("CONDICIONAL")
        nuevo = NodoAST("INSTRUCCIONES_IF")
        one = True
        for i in self.instruccionesIF:
            if one:
                nuevo2 = NodoAST("INSTRUCCION_IF")
                nuevo2.agregarHijo("IF")
                nuevo3 = NodoAST("EXPRESION")
                nuevo3.agregarHijoNodo(i.getExpresion().getNodo())
                nuevo2.agregarHijoNodo(nuevo3)
                nuevo3 = NodoAST("INSTRUCCIONES")
                dos = True
                instrucciones = i.getInstrucciones()
                for j in instrucciones:
                    if dos:
                        nuevo4 = NodoAST("INSTRUCCION")
                        nuevo4.agregarHijoNodo(j.getNodo())
                        nuevo3.agregarHijoNodo(nuevo4)
                        dos = False
                    else:
                        tmp = nuevo3
                        nuevo4 = NodoAST("INSTRUCCION")
                        nuevo3 = NodoAST("INSTRUCCIONES")
                        nuevo3.agregarHijoNodo(tmp)
                        nuevo4.agregarHijoNodo(j.getNodo())
                        nuevo3.agregarHijoNodo(nuevo4)
                nuevo2.agregarHijoNodo(nuevo3)
                nuevo.agregarHijoNodo(nuevo2)
                one = False
                continue
            else:
                tmp = nuevo
                nuevo2 = NodoAST("INSTRUCCION_ELSE_IF")
                nuevo = NodoAST("INSTRUCCIONES_IF")
                nuevo.agregarHijoNodo(tmp)
                nuevo2.agregarHijo("ELSEIF")
                nuevo3 = NodoAST("EXPRESION")
                nuevo3.agregarHijoNodo(i.getExpresion().getNodo())
                nuevo2.agregarHijoNodo(nuevo3)
                nuevo3 = NodoAST("INSTRUCCIONES")
                dos = True
                instrucciones = i.getInstrucciones()
                for j in instrucciones:
                    if dos:
                        nuevo4 = NodoAST("INSTRUCCION")
                        nuevo4.agregarHijoNodo(j.getNodo())
                        nuevo3.agregarHijoNodo(nuevo4)
                        dos = False
                    else:
                        tmp = nuevo3
                        nuevo4 = NodoAST("INSTRUCCION")
                        nuevo3 = NodoAST("INSTRUCCIONES")
                        nuevo3.agregarHijoNodo(tmp)
                        nuevo4.agregarHijoNodo(j.getNodo())
                        nuevo3.agregarHijoNodo(nuevo4)
                nuevo2.agregarHijoNodo(nuevo3)
                nuevo.agregarHijoNodo(nuevo2)
        nodo.agregarHijoNodo(nuevo)
        if self.instruccionElse is not None:
            nuevo = NodoAST("INSTRUCCIONES_IF")
            nuevo2 = NodoAST("INSTRUCCION_ELSE")
            nuevo2.agregarHijo("ELSE")
            dos = True
            for j in self.instruccionElse.getInstrucciones():
                if dos:
                    nuevo4 = NodoAST("INSTRUCCION")
                    nuevo4.agregarHijoNodo(j.getNodo())
                    nuevo3.agregarHijoNodo(nuevo4)
                    dos = False
                else:
                    tmp = nuevo3
                    nuevo4 = NodoAST("INSTRUCCION")
                    nuevo3 = NodoAST("INSTRUCCIONES")
                    nuevo3.agregarHijoNodo(tmp)
                    nuevo4.agregarHijoNodo(j.getNodo())
                    nuevo3.agregarHijoNodo(nuevo4)
            nuevo2.agregarHijoNodo(nuevo3)
            nuevo.agregarHijoNodo(nuevo2)
            nodo.agregarHijoNodo(nuevo)
        nodo.agregarHijo("END")
        nodo.agregarHijo(";")
        return nodo