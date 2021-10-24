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
        if self.funcion == 'float':
            genAux = C3D()
            gen = genAux.getInstance()
            if value.tipo == tipos.ENTERO:
                self.tipo = tipos.DECIMAL
                return Retornar(value.value, tipos.DECIMAL, True)
            else:
                #Error
                return
        elif self.funcion == 'string':
            self.tipo = tipos.CADENA
            if value.tipo == tipos.VECTOR:
                return self.retorno(self.getArreglo(tree, table, value.value))
            return self.retorno(str(value.value))
        elif self.funcion == 'typeof':
            self.tipo = tipos.CADENA
            tmp = self.getType(value)
            if tmp == "Tipo no definido":
                #Error
                return
            return self.retorno(tmp)
        elif self.funcion == 'parse':
            if self.tipo == tipos.ENTERO: #and value.tipo == tipos.CADENA:
                self.tipo = tipos.ENTERO
                return self.parseInt(tree, table, value)
            elif self.tipo == tipos.DECIMAL: #and value.tipo == tipos.CADENA:
                self.tipo = tipos.DECIMAL
                return self.parseFloat(tree, table, value)
            else:
                #Error
                return
        elif self.funcion == 'trunc':
            if self.tipo is None:
                self.tipo = tipos.ENTERO
                return self.retorno(int(value.value)) 
            elif self.tipo == tipos.ENTERO and value.tipo == tipos.DECIMAL:
                self.tipo = tipos.ENTERO
                return self.retorno(int(value.value))
            else:
                #Error
                return  
        elif self.funcion == 'length':
            genAux = C3D()
            gen = genAux.getInstance()
            if value.tipo == tipos.VECTOR:
                self.tipo = tipos.ENTERO
                tmp =  gen.addTemp()
                gen.getHeap(tmp, value.value)
                return Retornar(tmp, tipos.ENTERO, True)
            else:
                #Error
                return
        else:
            #Error
                return
            
    
    def retorno(self, result):
        return Primitiva(self.tipo, str(result), self.line, self.column)
    
    def parseInt(self, tree, table, value):
        genAux = C3D()
        gen = genAux.getInstance()
        
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
        gen.addExp(multi, num, '*', unidad)
        gen.addExp(suma, suma, '+', multi)
        
        gen.addExp(entero, entero, '-', '1')
        gen.addExp(tmpH, tmpH, "+", "1")
        gen.addGoto(continuando)
        gen.addLabel(salida)
        
        salida = gen.newLabel()
        continuando = gen.newLabel()
        gen.addExp(decimal, "0", '', '')
        gen.addLabel(cambio)
        
        gen.getHeap(num, tmpH)
        gen.newIF(num, "==", "-1", salida) 
        
        gen.addExp(tmpH, tmpH, "+", "1")
        gen.addLabel(continuando)
        gen.getHeap(num, tmpH)
        gen.newIF(num, "==", "-1", salida) 
        #----------------------------------- OBTENIENDO LA UNIDAD: UNIDAD DECENA CENTENA MILLAR ...
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
        gen.addExp(unidad, 1, '/', unidad)
        gen.addExp(multi, num, '*', unidad)
        gen.addExp(suma, suma, '+', multi)
        
        gen.addExp(decimal, decimal, '+', '1')
        gen.addExp(tmpH, tmpH, "+", "1")
        gen.addGoto(continuando)
        gen.addLabel(salida)
        
        return Retornar(suma, tipos.DECIMAL, True)
    
    def getType(self, value):
        if value.tipo == tipos.ENTERO:
            return "Int64"
        elif value.tipo == tipos.DECIMAL:
            return "Float64"
        elif value.tipo == tipos.CADENA:
            return "String"
        elif value.tipo == tipos.BOOLEAN:
            return "Bool"
        elif value.tipo == tipos.CARACTER:
            return "Char"
        elif value.tipo == tipos.VECTOR:
            return "Arreglo"
        elif value.tipo == tipos.STRUCT:
            return "Struct"
        elif value.tipo == tipos.FUNCION:
            return "Funcion"
        elif value.tipo == tipos.NULO:
            return "Nothing"
        else:
            return "Tipo no definido"
        
    def getArreglo(self, tree, table, vector):
        res = "["
        for i in vector:
            if(i == "[" or i == "]"):
                res += i
                continue
            tmp = i.interpretar(tree, table)
            if isinstance(tmp, Excepciones):
                tree.updateConsola(tmp.show())
                return
            if tmp.tipo == tipos.VECTOR:
                res += self.getArreglo(tree, table, tmp.value) + ","
            else:
                res += str(tmp.value) + ","
        res = res[:-1]
        res += "]"
        return str(res)
    
    def getNodo(self):
        pass