from abstract.Instruccion import Instruccion
from abstract.Retorno import Retornar
from tablaSimbolos.Tipo import tipos
from tablaSimbolos.C3D import C3D


class Logica(Instruccion):
    def __init__(self, operador, operando1, operando2, line, column):
        super().__init__(tipos.BOOLEAN, line, column)
        self.line = line
        self.column = column
        self.operador = operador
        if operando2 is None:
            self.opU = operando1
        else:
            self.op1 = operando1
            self.op2 = operando2
            self.opU = None
    
    def interpretar(self, tree, table):
        left = None
        right = None
        unario = None
        p1 = None
        p2 = None
        pu = None
        genAux = C3D()
        gen = genAux.getInstance()

        self.verifyLabel()
        lbl = ''

        if self.operador == '&&':
            lbl = self.op1.ev = gen.newLabel()
            self.op2.ev = self.ev
            self.op1.ef = self.op2.ef = self.ef
        elif self.operador == '||':
            self.op1.ev = self.op2.ev = self.ev
            lbl = self.op1.ef = gen.newLabel()
            self.op2.ef = self.ef
        else:
            lbl = self.opU.ef = gen.newLabel()
            self.opU.ev = self.ef
            self.opU.ef = self.ev
            pu = self.opU.interpretar(tree, table)
            if pu.tipo != tipos.BOOLEAN:
                # ERRORES
                return
            retorno = Retornar(None, tipos.BOOLEAN, False)
            retorno.ev = self.ev
            retorno.ef = self.ef
            return retorno
        left = self.op1.interpretar(tree, table)
        if left.tipo != tipos.BOOLEAN:
            # ERRORES
            return
        gen.addLabel(lbl)
        right = self.op2.interpretar(tree, table)
        if right.tipo != tipos.BOOLEAN:
            # ERRORES
            return
        retorno = Retornar(None, tipos.BOOLEAN, False)
        retorno.ev = self.ev
        retorno.ef = self.ef
        return retorno
    
    def verifyLabel(self):
        genAux = C3D()
        gen = genAux.getInstance()
        if self.ev == '':
            self.ev = gen.newLabel()
        if self.ef == '':
            self.ef = gen.newLabel()

    def getNodo(self):
        pass
        