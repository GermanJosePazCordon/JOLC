from abstract.Instruccion import Instruccion
from tablaSimbolos.C3D import C3D
from tablaSimbolos.Tipo import tipos

class Return(Instruccion):
    def __init__(self, express, line, column):
        super().__init__(tipos.RETURN, line, column);
        self.line = line
        self.column  = column
        self.express = express
        
    def interpretar(self, tree, table):
        genAux = C3D()
        gen = genAux.getInstance()
        value = self.express.interpretar(tree, table)
        if value.tipo == tipos.BOOLEAN:
            tmp = gen.newLabel()
            gen.addLabel(value.ev)
            gen.setStack('P', '1')
            gen.addGoto(tmp)
            gen.addLabel(value.ef)
            gen.setStack('P', '0')
            gen.addLabel(tmp)
        else:
            gen.setStack('P', value.value)
        gen.addGoto(table.returnn)
    
    def getNodo(self):
        pass