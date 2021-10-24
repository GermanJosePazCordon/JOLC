from abstract.Instruccion import Instruccion
from tablaSimbolos.Tipo import tipos
from tablaSimbolos.C3D import C3D
from abstract.Retorno import Retornar

class Nativa(Instruccion):
    def __init__(self, operacion, expresion, expresion2, line, column):
        super().__init__(tipos.ENTERO, line, column)
        self.line = line
        self.column = column
        self.operacion = operacion
        self.expresion = expresion
        self.expresion2 = expresion2
    
    def interpretar(self, tree, table):
        value = self.expresion.interpretar(tree, table)
        genAux = C3D()
        gen = genAux.getInstance()
        if value.tipo != tipos.CADENA:
            #Error
            print("Tipo de operacion erroneo")
            return
                
        tmpH = gen.addTemp()
        gen.addExp(tmpH, value.value, '', '')
        
        salida = gen.newLabel()
        continuando = gen.newLabel()
        
        nada = gen.newLabel()
        
        letra = gen.addTemp()
        gen.addLabel(continuando)
        
        gen.getHeap(letra, tmpH)
        
        gen.newIF(letra, "==", "-1", salida)
        
        if self.operacion == "upper":
            gen.newIF(letra, "<", "97", nada)
            gen.newIF(letra, ">", "122", nada)
            gen.addExp(letra, letra, "-", "32")
            gen.setHeap(tmpH, letra)
        else:
            gen.newIF(letra, "<", "65", nada)
            gen.newIF(letra, ">", "90", nada)
            gen.addExp(letra, letra, "+", "32")
            gen.setHeap(tmpH, letra)
        
        gen.addGoto(nada)
        gen.addLabel(nada)
        gen.addExp(tmpH, tmpH, "+", "1")
        gen.addGoto(continuando)
        gen.addLabel(salida)
        
        return Retornar(value.value, value.tipo, True)

    def getNodo(self):
        pass