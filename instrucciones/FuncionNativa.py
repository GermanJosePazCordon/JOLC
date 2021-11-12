from abstract.Instruccion import Instruccion
from tablaSimbolos.Tipo import tipos
from tablaSimbolos.C3D import C3D
from abstract.Retorno import Retornar
from expression.Primitiva import Primitiva
from excepciones.Excepciones import Excepciones

class FuncionNativa(Instruccion):
    def __init__(self, funcion, expresion, tipo, line, column):
        super().__init__(tipos.CADENA, line, column)
        self.line = line
        self.column = column
        self.funcion = funcion
        self.expresion = expresion
        self.tipo = tipo
        self.funcion = funcion
    
    def interpretar(self, tree, table):
        value = self.expresion.interpretar(tree, table)
        if isinstance(value, Excepciones): return value
        if self.funcion == 'float':
            genAux = C3D()
            gen = genAux.getInstance()
            gen.addComment("Empezando float")
            if value.tipo == tipos.ENTERO:
                self.tipo = tipos.DECIMAL
                gen.addComment("Fin float")
                return Retornar(value.value, tipos.DECIMAL, True)
            else:
                #Error
                tree.addError(Excepciones("Semántico", "Tipo de expresion invalido para float", self.line, self.column))
                return Excepciones("Semántico", "Tipo de expresion invalido para float", self.line, self.column)
        elif self.funcion == 'string':
            genAux = C3D()
            gen = genAux.getInstance()
            gen.addComment("Empezando toString")
            gen.toString()
            tmp = gen.addTemp()

            gen.addExp(tmp, 'P', '+', table.size)

            gen.addExp(tmp, tmp, "+", '1')
            gen.setStack(tmp, value.value)

            gen.newTable(table.size)
            gen.callFun('toString')
            temp = gen.addTemp()
            gen.getStack(temp, 'P')
            gen.getTable(table.size)
            
            gen.addComment("finalizando toString")
            return Retornar(temp, tipos.CADENA, True)
        
            #tree.addError(Excepciones("Semántico", "Funcion nativa string no implementada", self.line, self.column))
            #return Excepciones("Semántico", "Funcion nativa string no implementada", self.line, self.column)
        elif self.funcion == 'parse':
            if self.tipo == tipos.ENTERO: #and value.tipo == tipos.CADENA:
                self.tipo = tipos.ENTERO
                return self.parseInt(tree, table, value)
            elif self.tipo == tipos.DECIMAL: #and value.tipo == tipos.CADENA:
                self.tipo = tipos.DECIMAL
                return self.parseFloat(tree, table, value)
            else:
                #Error
                tree.addError(Excepciones("Semántico", "Tipo de expresion invalido para parse", self.line, self.column))
                return Excepciones("Semántico", "Tipo de expresion invalido para parse", self.line, self.column)
        elif self.funcion == 'trunc':
            if value.tipo == tipos.DECIMAL:
                self.tipo = tipos.ENTERO
                genAux = C3D()
                gen = genAux.getInstance()
                gen.addComment("Empezando trunc")
                if gen.imath == False:
                        gen.imports += ';\n\t"math"'
                        gen.imath = True        
                tmp = gen.addTemp()
                gen.addExp(tmp, "math.Mod(" + value.value + "," + "1" + ")", '', '')
                res = gen.addTemp()
                gen.addExp(res, value.value, '-', tmp)
                salida = gen.newLabel()
                gen.newIF(value.value, ">=", 0, salida)
                gen.addExp(res, res, '+', 1)
                gen.addLabel(salida)
                gen.addComment("Fin trunc")
                return Retornar(res, tipos.ENTERO, True)
            else:
                #Error
                tree.addError(Excepciones("Semántico", "Tipo de expresion invalido para trunc", self.line, self.column))
                return Excepciones("Semántico", "Tipo de expresion invalido para trunc", self.line, self.column)
        elif self.funcion == 'length':
            genAux = C3D()
            gen = genAux.getInstance()
            gen.addComment("Empezando length")
            if value.tipo == tipos.VECTOR:
                self.tipo = tipos.ENTERO
                tmp =  gen.addTemp()
                gen.getHeap(tmp, value.value)
                gen.addComment("Fin length")
                return Retornar(tmp, tipos.ENTERO, True)
            else:
                #Error
                tree.addError(Excepciones("Semántico", "Tipo de expresion invalido para length", self.line, self.column))
                return Excepciones("Semántico", "Tipo de expresion invalido para length", self.line, self.column)
        else:
            #Error
            tree.addError(Excepciones("Semántico", "Tipo de funcion nativa no declarado", self.line, self.column))
            return Excepciones("Semántico", "Tipo de funcion nativa no decladaro", self.line, self.column)
              
    def parseInt(self, tree, table, value):
        genAux = C3D()
        gen = genAux.getInstance()
        gen.addComment("Empezando parseInt")
    
        tmpH = gen.addTemp()
        gen.addExp(tmpH, value.value, '', '')
        
        salida = gen.newLabel()
        continuando = gen.newLabel()
        
        entero = gen.addTemp()
        gen.addExp(entero, "0", '-', '1')
        
        num = gen.addTemp()
        suma = gen.addTemp()
        multi = gen.addTemp()
        unidad = gen.addTemp()
        
        #-------------------------------------CONTANDO CANTIDAD DE ENTEROS
        gen.addComment("Contantdo cantidad de enteros")
        gen.addLabel(continuando)
        gen.getHeap(num, tmpH)
        gen.newIF(num, "==", "-1", salida)
        gen.newIF(num, "==", "46", salida)   
        gen.addExp(entero, entero, '+', '1')
        gen.addExp(tmpH, tmpH, "+", "1")
        gen.addGoto(continuando)
        gen.addLabel(salida)
        #--------------------------------
        
        salida = gen.newLabel()
        continuando = gen.newLabel()
        gen.addExp(tmpH, value.value, '', '')
        
        gen.addLabel(continuando)
        gen.getHeap(num, tmpH)
        gen.newIF(num, "==", "-1", salida)
        gen.newIF(num, "==", "46", salida)   
        
        #----------------------------------- OBTENIENDO LA UNIDAD: UNIDAD DECENA CENTENA MILLAR ...
        gen.addComment("Obteniendo unidad: unidad, decena centena ....")
        gen.potencia()
        tmp = gen.addTemp()
        gen.addExp(tmp, 'P', '+', table.size)
        gen.addExp(tmp, tmp, "+", '1')
        gen.setStack(tmp, 10)
        gen.addExp(tmp, tmp, '+', '1')
        gen.setStack(tmp, entero)
        gen.newTable(table.size)
        gen.callFun('potencia')
        gen.getStack(unidad, 'P')
        gen.getTable(table.size)
        #-----------------------------------
        gen.addExp(num, num, '-', 48)
        gen.addComment("Multiplicando unidad por numero para obtener el numero a sumar")
        gen.addExp(multi, num, '*', unidad)
        gen.addExp(suma, suma, '+', multi)
        
        gen.addExp(entero, entero, '-', '1')
        gen.addExp(tmpH, tmpH, "+", "1")
        gen.addGoto(continuando)
        gen.addLabel(salida)

        
        return Retornar(suma, tipos.ENTERO, True)
    
    def parseFloat(self, tree, table, value):
        genAux = C3D()
        gen = genAux.getInstance()
        gen.addComment("Empezando parseFloat")
        tmpH = gen.addTemp()
        gen.addExp(tmpH, value.value, '', '')
        
        salida = gen.newLabel()
        continuando = gen.newLabel()
        
        entero = gen.addTemp()
        gen.addExp(entero, "0", '-', '1')
        
        decimal = gen.addTemp()
        gen.addExp(decimal, "1", '', '')
        
        num = gen.addTemp()
        suma = gen.addTemp()
        multi = gen.addTemp()
        unidad = gen.addTemp()
        
        #-------------------------------------CONTANDO CANTIDAD DE ENTEROS
        gen.addComment("Contantdo cantidad de enteros")
        gen.addLabel(continuando)
        gen.getHeap(num, tmpH)
        gen.newIF(num, "==", "-1", salida)
        gen.newIF(num, "==", "46", salida)   
        gen.addExp(entero, entero, '+', '1')
        gen.addExp(tmpH, tmpH, "+", "1")
        gen.addGoto(continuando)
        gen.addLabel(salida)
        #--------------------------------
    
        salida = gen.newLabel()
        continuando = gen.newLabel()
        cambio = gen.newLabel()
        gen.addExp(tmpH, value.value, '', '')
        
        gen.addLabel(continuando)
        gen.getHeap(num, tmpH)
        gen.newIF(num, "==", "-1", salida)
        gen.newIF(num, "==", "46", cambio)   
        
        #----------------------------------- OBTENIENDO LA UNIDAD: UNIDAD DECENA CENTENA MILLAR ...
        gen.addComment("Obteniendo unidad: unidad, decena centena ....")
        gen.potencia()
        tmp = gen.addTemp()
        gen.addExp(tmp, 'P', '+', table.size)
        gen.addExp(tmp, tmp, "+", '1')
        gen.setStack(tmp, 10)
        gen.addExp(tmp, tmp, '+', '1')
        gen.setStack(tmp, entero)
        gen.newTable(table.size)
        gen.callFun('potencia')
        gen.getStack(unidad, 'P')
        gen.getTable(table.size)
        #-----------------------------------
        
        gen.addExp(num, num, '-', 48)
        gen.addComment("Multiplicando unidad por numero para obtener el numero a sumar")
        gen.addExp(multi, num, '*', unidad)
        gen.addExp(suma, suma, '+', multi)
        
        gen.addExp(entero, entero, '-', '1')
        gen.addExp(tmpH, tmpH, "+", "1")
        gen.addGoto(continuando)
        gen.addLabel(salida)
        
        salida = gen.newLabel()
        continuando = gen.newLabel()
        gen.addExp(decimal, "0", '', '')
        gen.addComment("Empezando a sumar los decimales")
        gen.addLabel(cambio)
        
        gen.getHeap(num, tmpH)
        gen.newIF(num, "==", "-1", salida) 
        
        gen.addExp(tmpH, tmpH, "+", "1")
        gen.addLabel(continuando)
        gen.getHeap(num, tmpH)
        gen.newIF(num, "==", "-1", salida) 
        #----------------------------------- OBTENIENDO LA UNIDAD: UNIDAD DECENA CENTENA MILLAR ...
        gen.addComment("Obteniendo unidad: unidad, decena centena ....")
        gen.potencia()
        tmp = gen.addTemp()
        gen.addExp(tmp, 'P', '+', table.size)
        gen.addExp(tmp, tmp, "+", '1')
        gen.setStack(tmp, 10)
        gen.addExp(tmp, tmp, '+', '1')
        gen.setStack(tmp, decimal)
        gen.newTable(table.size)
        gen.callFun('potencia')
        gen.getStack(unidad, 'P')
        gen.getTable(table.size)
        #-----------------------------------
        
        gen.addExp(num, num, '-', 48)
        gen.addComment("Para los decimales la unidad debe ser el reciproco")
        gen.addExp(unidad, 1, '/', unidad)
        gen.addExp(multi, num, '*', unidad)
        gen.addExp(suma, suma, '+', multi)
        
        gen.addExp(decimal, decimal, '+', '1')
        gen.addExp(tmpH, tmpH, "+", "1")
        gen.addGoto(continuando)
        gen.addLabel(salida)
        
        return Retornar(suma, tipos.DECIMAL, True)

    def getNodo(self):
        pass