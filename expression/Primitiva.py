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
        elif self.tipo == tipos.CARACTER:
            return Retornar(ord(str(self.value)), self.tipo, False)
        elif self.tipo == tipos.BOOLEAN:
            if self.ev == '':
                self.ev = gen.newLabel()
            if self.ef == '':
                self.ef = gen.newLabel()
            
            if(self.value == "true"):
                gen.addGoto(self.ev)
                gen.addGoto(self.ef)
            else:
                gen.addGoto(self.ef)
                gen.addGoto(self.ev)
            
            retorno = Retornar(self.value, self.tipo, False)
            retorno.ev = self.ev
            retorno.ef = self.ef

            return retorno
        elif self.tipo == tipos.CADENA:
            temp = gen.addTemp()
            gen.addExp(temp, 'H', '', '')

            for char in str(self.value):
                gen.setHeap('H', ord(char))   # heap[H] = NUM;
                gen.nextHeap()                # H = H + 1;

            gen.setHeap('H', '-1')            # FIN DE CADENA
            gen.nextHeap()

            return Retornar(temp, tipos.CADENA, True)
        elif self.tipo == tipos.VECTOR:
            tmpH = gen.addTemp()
            gen.addExp(tmpH, 'H', '', '')
            
            tmp = gen.addTemp()
            gen.addExp(tmp, tmpH, "+", 1)
            
            gen.setHeap('H', len(self.value))
            size = len(self.value) + 1
            gen.addExp('H', 'H', '+', size)
            
            for i in self.value: 
                gen.setHeap(tmp, i.interpretar(tree, table).value)
                gen.addExp(tmp, tmp, '+', '1')

            vec = self.getTipo(self.value)
            return Retornar(tmpH, tipos.VECTOR, True, vec)            
            
    def getTipo(self, vector):
        vec = []
        for i in vector:
            if i.tipo == tipos.VECTOR:
                tmp = self.getTipo(i.value)
                vec.append(tmp)
                return vec
            else:
                vec.append(i.tipo)
                return vec
    
    def getNodo(self):
        pass