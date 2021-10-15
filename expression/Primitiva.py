from abstract.Instruccion import Instruccion
from abstract.Retorno import Retornar
from tablaSimbolos.C3D import C3D
from tablaSimbolos.Tipo import tipos

class Primitiva(Instruccion):

    def __init__(self, tipo, value, line, column):
        super().__init__(self, line, column)
        self.value = value
        self.tipo = tipo
    
    def interpretar(self, tree, table):
        genAux = C3D()
        gen = genAux.getInstance()
        if(self.tipo == tipos.ENTERO or self.tipo == tipos.DECIMAL):
            return Retornar(str(self.value), self.tipo, False)
        elif self.tipo == tipos.BOOLEAN:
            if self.ev == '':
                self.ev = gen.newLabel()
            if self.ef == '':
                self.ef = gen.newLabel()
            
            if(self.value):
                gen.addGoto(self.ev)
                gen.addGoto(self.ef)
            else:
                gen.addGoto(self.ev)
                gen.addGoto(self.ef)
            
            ret = Retornar(self.value, self.tipo, False)
            ret.ev = self.ev
            ret.ef = self.ef

            return ret
        elif self.tipo == tipos.CADENA:
            retTemp = gen.addTemp()
            gen.addExp(retTemp, 'H', '', '')

            for char in str(self.value):
                gen.setHeap('H', ord(char))   # heap[H] = NUM;
                gen.nextHeap()                # H = H + 1;

            gen.setHeap('H', '-1')            # FIN DE CADENA
            gen.nextHeap()

            return Retornar(retTemp, tipos.CADENA, True)
        else:
            print('Por hacer')
    
    def getNodo(self):
        pass