
from abstract.NodoAST import NodoAST
from instrucciones.Return import Return
from expression.Primitiva import Primitiva
from tablaSimbolos.TablaSimbolos import tablaSimbolos
from tablaSimbolos.Simbolo import Simbolo
from abstract.Instruccion import Instruccion
from tablaSimbolos.Tipo import tipos
from excepciones.Excepciones import Excepciones
from instrucciones.ConstruccionStruct import ConstruccionStruct

class Llamada(Instruccion):
    def __init__(self, ids, listaParametros, line, column):
        super().__init__(tipos.VECTOR, line, column)
        self.line = line
        self.column = column
        self.id = ids
        self.listaParametros = listaParametros
    
    def interpretar(self, tree, table):
        isFunction = True
        if self.listaParametros is None:
            self.listaParametros = []
        funcion = table.getVariable(self.id)
        if funcion is None:
            tree.addError(Excepciones("Semántico", "Funcion no declarada", self.line, self.column))
            return Excepciones("Semantico", "Funcion no decladara", self.line, self.column)
        if funcion.tipo == tipos.FUNCION:
            isFunction = True
        elif funcion.tipo == tipos.STRUCT:
            isFunction = False
        else:
            tree.addError(Excepciones("Semántico", "El id no es de una funcion", self.line, self.column))
            return Excepciones("Semantico", "El id no es de una funcion", self.line, self.column)
        self.isFun = isFunction
        self.Func = funcion
        if isFunction:
            #METODO PARA FUNCIONES
            parametrosFun = funcion.value['parametros']
            instruccionesFun = funcion.value['instrucciones']
            if len(self.listaParametros) != len(parametrosFun):
                tree.addError(Excepciones("Semántico", "Numero de parametros incorrecto", self.line, self.column))
                return Excepciones("Semantico", "Numero de parametros incorrecto", self.line, self.column)
            
            #CRENADO EL ENTORNO DE LA FUNCION
            tabla = tablaSimbolos(table)
            tabla.setEntorno(self.id)
            tree.addTabla(tabla)
            
            for i in range(len(self.listaParametros)):
                valor = self.listaParametros[i].interpretar(tree, table)
                if isinstance(valor, Excepciones): return valor
                tabla.setVariable(Simbolo(self.line, self.column, valor.tipo, parametrosFun[i].id, valor.value))
            
            for m in instruccionesFun:
                if isinstance(m, Excepciones):
                    tree.updateConsola(str(m))
                    tree.addError(m.show())
                    continue
                result = m.interpretar(tree, tabla)
                if isinstance(result, Excepciones): return result
                if isinstance(result, Return):
                    if result is None:
                        return
                    tmp = result.result.interpretar(tree, tabla)
                    return tmp
                if isinstance(result, Primitiva): return result
        else:
            #METODOS PARA STRUCTS
            tmp = ConstruccionStruct(funcion, self.listaParametros, self.line, self.column)
            self.nodoStruct = tmp.getNodo()
            tmp = tmp.interpretar(tree, table)
            
            return tmp
    
    def getNodo(self):
        try:
            if self.isFun is False:
                return self.nodoStruct
            nodo = NodoAST("LLAMADA")
            nodo.agregarHijo(self.Func.id)
            nodo.agregarHijo("(")
            if self.listaParametros is not None:
                nuevo = NodoAST("LISTAPARAMETROS")
                one = True
                for i in self.listaParametros:
                    if one:
                        nodo2 = NodoAST("EXPRESION")
                        nodo2.agregarHijoNodo(i.getNodo())
                        nuevo.agregarHijoNodo(nodo2)
                        one = False
                    else:
                        tmp = nuevo
                        nuevo2 = NodoAST("EXPRESION")
                        nuevo = NodoAST("LISTAPARAMETROS")
                        nuevo.agregarHijoNodo(tmp)
                        nuevo.agregarHijo(",")
                        nuevo2.agregarHijoNodo(i.getNodo())
                        nuevo.agregarHijoNodo(nuevo2)
                nodo.agregarHijoNodo(nuevo)
            nodo.agregarHijo(")")
            return nodo
        except:
            pass