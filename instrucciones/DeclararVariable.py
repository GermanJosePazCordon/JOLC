from abstract.Instruccion import Instruccion
from tablaSimbolos.Tipo import tipos
from tablaSimbolos.C3D import C3D

class DeclararVariable(Instruccion):
    def __init__(self, operador, id, value, globall, line, column):
        super().__init__(tipos.CADENA, line, column)
        
        self.tipo = operador
        self.id = id
        self.value = value
        self.line = line
        self.column= column
        self.globall = globall
    
    def interpretar(self, tree, table):
        '''if self.tipo is not None and self.tipo != self.value.tipo:
            #Error
            print("Tipos incorrectos al declarar variable")
            return'''
        genAux = C3D()
        gen = genAux.getInstance()
        gen.addComment("Empezando declaracion varible")
        value = self.value.interpretar(tree, table)
        vairable = table.getVariable(self.id)
        if vairable == None:
            vairable = table.setVariable(self.id, value.tipo, (value.tipo == tipos.CADENA or value.tipo == tipos.STRUCT), value.vector)
        vairable.tipo = value.tipo
        pos = vairable.pos
        if not vairable.isGlobal:
            pos = gen.addTemp()
            gen.addExp(pos, 'P',  "+", vairable.pos)
        if(value.tipo == tipos.BOOLEAN):
            ev = gen.newLabel()
            gen.addLabel(value.ev)
            gen.setStack(pos, "1")
            gen.addGoto(ev)
            gen.addLabel(value.ef)
            gen.setStack(pos, "0")
            gen.addLabel(ev)
        else:
            gen.setStack(pos, value.value)
        gen.addComment("Fin declaracion varible")
            
    def getNodo(self):
        pass