from abstract.NodoAST import NodoAST
from abstract.Instruccion import Instruccion
from tablaSimbolos.C3D import C3D
from tablaSimbolos.Tipo import tipos

class Break(Instruccion):
    def __init__(self, line, column):
        super().__init__(tipos.BREAK, line, column);
        self.line = line
        self.column  = column
        
    def interpretar(self, tree, table):
        if table.breakk == '':
            #Error
            print("Break fuera de ciclo")
            return
        genAux = C3D()
        gen = genAux.getInstance()
        gen.addGoto(table.breakk)
    
    def getNodo(self):
        pass