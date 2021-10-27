from abstract.Instruccion import Instruccion

class Parametro(Instruccion):

    def __init__(self, ids, types, line, column):
        super().__init__(self, line, column)
        self.express= ids
        self.tipo = types
    
    def interpretar(self, tree, table):
        return self           
            
    def getNodo(self):
        pass