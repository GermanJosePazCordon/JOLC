from abstract.Instruccion import Instruccion
from tablaSimbolos.C3D import C3D
from tablaSimbolos.Tipo import tipos

class Continue(Instruccion):
    def __init__(self, line, column):
        super().__init__(tipos.CONTINUE, line, column);
        self.line = line
        self.column  = column
        
    def interpretar(self, tree, table):
        if table.continuee == '':
            #Error
            print("Continue fuera de ciclo")
            return
        genAux = C3D()
        gen = genAux.getInstance()
        gen.addGoto(table.continuee)
    
    def getNodo(self):
        pass