from abstract.Instruccion import Instruccion
from abstract.Retorno import Retornar
from tablaSimbolos.Tipo import tipos
from tablaSimbolos.C3D import C3D


class Relacional(Instruccion):
    def __init__(self, operador, operando1, operando2, line, column):
        super().__init__(tipos.BOOLEAN, line, column)
        self.column = column
        self.line = line
        self.operador = operador
        self.op1 = operando1
        self.op2 = operando2

    def interpretar(self, tree, table):
        aux = C3D()
        gen = aux.getInstance()
        p1 = None
        p2 = None
        p1 = self.op1.interpretar(tree, table)
        
        retorno = Retornar(None, tipos.BOOLEAN, False)
        
        if p1.tipo != tipos.BOOLEAN:
            p2 = self.op2.interpretar(tree, table)
            if (p1.tipo == tipos.ENTERO or p1.tipo == tipos.DECIMAL) and (p2.tipo == tipos.ENTERO or p2.tipo == tipos.DECIMAL):
                self.verifyLabel()
                gen.newIF(p1.value, self.operador, p2.value, self.ev)
                gen.addGoto(self.ef)
            elif p1.tipo == tipos.CADENA and p2.tipo == tipos.CADENA:
                gen.compararString()
                tmp = gen.addTemp()

                gen.addExp(tmp, 'P', '+', table.size)
                    
                gen.addExp(tmp, tmp, "+", '1')
                gen.setStack(tmp, p1.value)

                gen.addExp(tmp, tmp, '+', '1')
                gen.setStack(tmp, p2.value)

                gen.newTable(table.size)
                gen.callFun('compararString')
                temp = gen.addTemp()
                gen.getStack(temp, 'P')
                gen.getTable(table.size)   
                
                ev = gen.newLabel()
                ef = gen.newLabel()
                self.ev = ev
                self.ef = ef
                if self.operador == "==":
                    gen.newIF(temp, "==", "0", self.ef)
                    gen.addGoto(self.ev) 
                else:
                    gen.newIF(temp, "==", "1", self.ef)
                    gen.addGoto(self.ev)   
        else:
            goto = gen.newLabel()
            tmp = gen.addTemp()

            gen.addLabel(p1.ev)
            gen.addExp(tmp, '1', '', '')
            gen.addGoto(goto)

            gen.addLabel(p1.ef)
            gen.addExp(tmp, '0', '', '')

            gen.addLabel(goto)

            p2 = self.op2.interpretar(tree, table)
            if p2.tipo != tipos.BOOLEAN:
                print("Error, no se pueden comparar")
                return
            salida = gen.newLabel()
            temp2 = gen.addTemp()

            gen.addLabel(p2.ev)
            
            gen.addExp(temp2, '1', '', '')
            gen.addGoto(salida)

            gen.addLabel(p2.ef)
            gen.addExp(temp2, '0', '', '')

            gen.addLabel(salida)

            self.verifyLabel()
            gen.newIF(tmp, self.operador, temp2, self.ev)
            gen.addGoto(self.ef)
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
