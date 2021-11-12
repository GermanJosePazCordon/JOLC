from abstract.Instruccion import Instruccion
from abstract.Retorno import Retornar
from excepciones.Excepciones import Excepciones
from tablaSimbolos.C3D import C3D
from tablaSimbolos.Tipo import tipos

class Llamada(Instruccion):
    def __init__(self, ids, listaParametros, line, column):
        super().__init__(tipos.VECTOR, line, column)
        self.line = line
        self.column = column
        self.id = ids
        self.listaParametros = listaParametros
    
    def interpretar(self, tree, table):
        if self.listaParametros is None:
            self.listaParametros = []
        funcion = table.getFuncion(self.id)
        if funcion is None:
            funcion = table.getStruct(self.id)
            if funcion is None:
                #Error
                tree.addError(Excepciones("Semántico", "No existe la funcion", self.line, self.column))
                return Excepciones("Semántico", "No existe la funcion", self.line, self.column)
            return self.isStruct(tree, table, funcion)
        if funcion.tipo == tipos.FUNCION:
            return self.isFuncion(tree, table, funcion)
        else:
            #Error
            tree.addError(Excepciones("Semántico", "El id no es de una funcion o un struct", self.line, self.column))
            return Excepciones("Semántico", "El id no es de una funcion o un struct", self.line, self.column)
        
    def isFuncion(self, tree, table, funcion):
        size = table.size
        parametrosFun = funcion.listaParametros
        if len(self.listaParametros) != len(parametrosFun):
            #Error
            tree.addError(Excepciones("Semántico", "Numero incorrecto de parametros", self.line, self.column))
            return Excepciones("Semántico", "Numero incorrecto de parametros", self.line, self.column)
        genAux = C3D()
        gen = genAux.getInstance()
        gen.addComment("Empezando llamada funcion")
        parametrosLlamada = []
        for i in self.listaParametros:
            tmp = gen.temps[len(gen.temps) - 1]
            if isinstance(i.express, Llamada) and table.inFun:
                gen.saveTemp(table, tmp)
            val = i.express.interpretar(tree, table)
            if isinstance(val, Excepciones): return val
            parametrosLlamada.append(val)
            if isinstance(i.express, Llamada) and table.inFun:
                gen.getTemp(table, tmp)
        
        #EMPEZANDO LA LLAMADA
        tmp = gen.addTemp()
        gen.addExp(tmp, 'P', '+', (size + 1))
        cont = 0;
        for i in parametrosLlamada:
            cont += 1
            gen.setStack(tmp, i.value)
            if len(parametrosLlamada) != cont:
                gen.addExp(tmp, tmp, '+', 1)
        
        gen.newTable(size)
        gen.callFun(self.id)
        gen.getStack(tmp, 'P')
        gen.getTable(size)
        
        if funcion.retorno2 == tipos.BOOLEAN:
            gen.addComment("Asiganando ev ef llamada funcion")
            ev = gen.newLabel()
            ef = gen.newLabel()
            gen.newIF(tmp, "==", "0", ef)
            gen.addGoto(ev)
            retorno = Retornar(tmp, tipos.BOOLEAN, False)
            retorno.ev = ev
            retorno.ef = ef
            gen.addComment("Fin llamada funcion")
            return retorno
        elif funcion.retorno2 == tipos.VECTOR:
            gen.addComment("Fin llamada funcion")
            return Retornar(tmp, tipos.VECTOR, True, funcion.vector)
        elif isinstance(funcion.retorno2, tipos):
            gen.addComment("Fin llamada funcion")
            return Retornar(tmp, funcion.retorno2, True)
        else:
            gen.addComment("Fin llamada funcion")
            return Retornar(tmp, tipos.STRUCT, True, '', funcion.retorno)
    
    def isStruct(self, tree, table, struct):
        atributos = struct[1]
        if len(self.listaParametros) != len(atributos):
            #Error
            tree.addError(Excepciones("Semántico", "Numero incorrecto de parametros", self.line, self.column))
            return Excepciones("Semántico", "Numero incorrecto de parametros", self.line, self.column)
        
        genAux = C3D()
        gen = genAux.getInstance()
        gen.addComment("Empezando llamada struct")
        
        tmpH = gen.addTemp()
        gen.addExp(tmpH, 'H', '', '')
        gen.addExp('H', 'H', '+', len(atributos))
        pos = gen.addTemp()
        gen.addExp(pos, tmpH, '', '')
        cont = 0
        for i in self.listaParametros:
            value = i.express.interpretar(tree, table)
            if isinstance(value, Excepciones): return value
            gen.addComment("Guardando atributo")
            gen.setHeap(pos, value.value)
            #struct[1][cont].inicio = cont
            gen.addExp(pos, pos, '+', 1)
            cont += 1
        gen.addComment("Fin llamada struct")   
        return Retornar(tmpH, tipos.STRUCT, True, '', self.id)
    
    def getNodo(self):
        pass
    