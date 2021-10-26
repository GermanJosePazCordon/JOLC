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
        parametrosFun = funcion.listaParametros
        instruccionesFun = funcion.listaInstrucciones
        if len(self.listaParametros) != len(parametrosFun):
            #Error
            print("Numero de parametros incorrecto")
            return
        #-----------------------------------------------------------------
        parametrosLlamada = []
        size = table.size
        for i in self.listaParametros:
            parametrosLlamada.append(i.id.interpretar(tree, table))
        #---------------------------------------------------------------
        genAux = C3D()
        gen = genAux.getInstance()
        
        
        if funcion.Bfuncion is False:
            #DECLARANDO LA FUNCION CON SUS PARAMETROS
            tabla = Entorno(table)
            returnn = gen.newLabel()
            tabla.returnn = returnn
            tabla.size = 1
            cont = 0
            
            for i in parametrosFun:
                if i.tipo is None:
                    i.tipo = funcion.retorno
                tabla.setVariable(i.id.id, i.tipo, (i.tipo == tipos.CADENA or i.tipo == tipos.STRUCT), parametrosLlamada[cont].vector)
                cont += 1
    
            gen.initFun(self.id)
            for i in instruccionesFun:
                i.interpretar(tree, tabla)
            gen.addLabel(returnn)
            gen.endFun()
            funcion.Bfuncion = True
        
        #EMPEZANDO LA LLAMADA
        '''parametrosLlamada = []
        size = table.size
        for i in self.listaParametros:
            parametrosLlamada.append(i.id.interpretar(tree, table))'''
            
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