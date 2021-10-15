
from abstract.NodoAST import NodoAST
from tablaSimbolos.TablaSimbolos import tablaSimbolos
from expression.Primitiva import Primitiva
from abstract.Instruccion import Instruccion
from tablaSimbolos.Tipo import tipos
from tablaSimbolos.Simbolo import Simbolo
from excepciones.Excepciones import Excepciones
from instrucciones.Break import Break
from instrucciones.Return import Return
from instrucciones.Continue import Continue
from instrucciones.DeclararVariable import DeclararVariable

class For(Instruccion):
    def __init__(self, variable, types, rangoinf, rangosup, cadena, listaInstrucciones, line, column):
        super().__init__(tipos.CADENA, line, column)
        self.line = line
        self.column = column
        self.listaInstrucciones = listaInstrucciones
        self.variable = variable
        self.types = types
        self.rangoinf = rangoinf
        self.rangosup = rangosup
        self.pos = cadena
    
    def interpretar(self, tree, table):
        if self.rangoinf is not None:
            inferior = self.rangoinf.interpretar(tree, table)
        if self.rangosup is not None:
            superior = self.rangosup.interpretar(tree, table)
        if self.pos is not None:
            tmp = self.pos.interpretar(tree, table)
            if tmp.tipo == tipos.CADENA:
                self.types = 'cadena'
                cadena = tmp
            else:
                self.types = 'vector'
                vector = tmp
                
        if self.types == 'rango':
            if  inferior.tipo != tipos.ENTERO and inferior.tipo != tipos.DECIMAL:
                tree.addError(Excepciones("Semántico", "Tipo de rango inferior invalido", self.line, self.column))
                return Excepciones("Semantico", "Tipo de rango inferior invalido", self.line, self.column)
            if  superior.tipo != tipos.ENTERO and superior.tipo != tipos.DECIMAL:
                tree.addError(Excepciones("Semántico", "Tipo de rango superior invalido", self.line, self.column))
                return Excepciones("Semantico", "Tipo de rango superior invalido", self.line, self.column)
            return self.rangos(tree, table, inferior, superior)
        elif self.types == 'cadena':
            return self.cadenas(tree, table, cadena.value)
        elif self.types == 'vector':
            return self.vectores(tree, table, vector.value)
            
    def rangos(self, tree, table, rangoinf, rangosup):
        if rangoinf.tipo == tipos.ENTERO:
            ri = int(rangoinf.value)
        else:
            ri = float(rangoinf.value)
        if rangosup.tipo == tipos.ENTERO:
            ru = int(rangosup.value)
        else:
            ru = float(rangosup.value)
        if ru < ri:
            tree.addError(Excepciones("Semántico", "Rango inferior mayor a rango superior", self.line, self.column))
            exp =  Excepciones("Semantico", "Rango inferior mayor a rango superior", self.line, self.column)
            tree.updateConsola(str(exp.show()))
            return exp
        rango = int(float(ru - ri)) + 1
        tabla = tablaSimbolos(table)
        tabla.setEntorno("for")
        tree.addTabla(tabla)
        iterador = tabla.getVariable(self.variable)
        if iterador is None:
            tabla.setVariable(Simbolo(self.line, self.column, tipos.ENTERO, self.variable, 0))
            iterador = tabla.getVariable(self.variable)
        for i in range(rango):
            iterador.setValue(i + ri)
            iterador.setTipo(rangoinf.tipo)
            tabla2 = tablaSimbolos(tabla)
            tabla2.setEntorno("for")
            tree.addTabla(tabla2)
            for m in self.listaInstrucciones:
                if isinstance(m, Excepciones):
                    tree.updateConsola(str(m))
                    tree.addError(m.toString())
                    continue
                result = m.interpretar(tree, tabla2)
                if isinstance(result, Excepciones):
                    tree.updateConsola(result.toString())
                if isinstance(result, Primitiva): return result
                if isinstance(result, Break): return None
                if isinstance(result, Continue): break
                if isinstance(result, Return): return result
                
    def cadenas(self, tree, table, cadena):
        tabla = tablaSimbolos(table)
        tabla.setEntorno("for")
        tree.addTabla(tabla)
        
        for i in cadena:
            
            declara = Simbolo(self.line, self.column, tipos.CADENA, self.variable, i)
            tabla.updateVariable(declara)
            
            tabla2 = tablaSimbolos(tabla)
            tabla2.setEntorno("for")
            tree.addTabla(tabla2)
            
            for m in self.listaInstrucciones:
                if isinstance(m, Excepciones):
                    tree.updateConsola(str(m))
                    tree.addError(m.toString())
                    continue
                result = m.interpretar(tree, tabla2)
                if isinstance(result, Excepciones):
                    tree.updateConsola(result.toString())
                if isinstance(result, Break): return None
                if isinstance(result, Continue): break
                if isinstance(result, Return): return result
        
    def vectores(self, tree, table, arreglo):
        
        tabla = tablaSimbolos(table)
        tabla.setEntorno("for")
        tree.addTabla(tabla)
        
        for i in arreglo:
            tmp = i.interpretar(tree, table)
            
            declara = Simbolo(self.line, self.column, tmp.tipo, self.variable, tmp.value)
            tabla.updateVariable(declara)
            
            tabla2 = tablaSimbolos(tabla)
            tabla2.setEntorno("for")
            tree.addTabla(tabla2)
            
            for m in self.listaInstrucciones:
                if isinstance(m, Excepciones):
                    tree.updateConsola(str(m))
                    tree.addError(m.toString())
                    continue
                result = m.interpretar(tree, tabla2)
                if isinstance(result, Excepciones):
                    tree.updateConsola(result.toString())
                if isinstance(result, Break): return None
                if isinstance(result, Continue): break
                if isinstance(result, Return): return result
    
    def getNodo(self):
        nodo = NodoAST("CICLO_FOR")
        nodo.agregarHijo("FOR")
        nodo.agregarHijo(self.variable)
        nodo.agregarHijo("IN")
        if self.types == 'rango':
            nuevo = NodoAST("EXPRESION")
            nuevo.agregarHijoNodo(self.rangoinf.getNodo())
            nodo.agregarHijoNodo(nuevo)
            nodo.agregarHijo(":")
            nuevo = NodoAST("EXPRESION")
            nuevo.agregarHijoNodo(self.rangosup.getNodo())
            nodo.agregarHijoNodo(nuevo)
        else:
            nuevo = NodoAST("EXPRESION")
            nuevo.agregarHijoNodo(self.pos.getNodo())
            nodo.agregarHijoNodo(nuevo) 
        nuevo = NodoAST("INSTRUCCIONES")
        one = True
        for i in self.listaInstrucciones:
            if one:
                nuevo2 = NodoAST("INSTRUCCION")
                nuevo2.agregarHijoNodo(i.getNodo())
                nuevo.agregarHijoNodo(nuevo2)
                one = False
            else:
                tmp = nuevo
                nuevo2 = NodoAST("INSTRUCCION")
                nuevo = NodoAST("INSTRUCCIONES")
                nuevo.agregarHijoNodo(tmp)
                nuevo2.agregarHijoNodo(i.getNodo())
                nuevo.agregarHijoNodo(nuevo2)
        nodo.agregarHijoNodo(nuevo)
        nodo.agregarHijo("END")
        nodo.agregarHijo(";")
        return nodo
    