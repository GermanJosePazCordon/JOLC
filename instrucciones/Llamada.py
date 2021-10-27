from abstract.Instruccion import Instruccion
from instrucciones.Return import Return
from abstract.Retorno import Retornar
from tablaSimbolos.C3D import C3D
from tablaSimbolos.Entorno import Entorno
from tablaSimbolos.Simbolo import Simbolo
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
            #Error
            print("No existe la funcion")
            return
        if funcion.tipo == tipos.FUNCION:
            return self.isFuncion(tree, table, funcion)
        elif funcion.tipo == tipos.STRUCT:
            return self.isStruct(tree, table, funcion)
        else:
            #Error
            print("El id no es de una funcion o un struct")
            return
        
    def isFuncion(self, tree, table, funcion):
        size = table.size
        parametrosFun = funcion.listaParametros
        if len(self.listaParametros) != len(parametrosFun):
            #Error
            print("Numero de parametros incorrecto")
            return
        genAux = C3D()
        gen = genAux.getInstance()
        gen.addComment("Empezando llamada")
        parametrosLlamada = []
        for i in self.listaParametros:
            tmp = gen.temps[len(gen.temps) - 1]
            if isinstance(i.express, Llamada) and table.inFun:
                gen.saveTemp(table, tmp)
            parametrosLlamada.append(i.express.interpretar(tree, table))
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
        
        return Retornar(tmp, funcion.retorno, True)
    
    def isStruct(self, tree, table, struct):
        pass
    
    def getNodo(self):
        pass