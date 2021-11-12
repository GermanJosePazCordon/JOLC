
from abstract.NodoAST import NodoAST
from excepciones.Excepciones import Excepciones
from tablaSimbolos.C3D import C3D
from tablaSimbolos.Entorno import Entorno
from tablaSimbolos.Simbolo import Simbolo
from abstract.Instruccion import Instruccion
from tablaSimbolos.Tipo import tipos

class Funciones(Instruccion):
    def __init__(self, ids, types, listaParametros, listaInstrucciones, line, column):
        super().__init__(tipos.FUNCION, line, column)
        self.line = line
        self.column = column
        self.id = ids
        self.tipo = tipos.FUNCION
        self.retorno = ''
        self.retorno2 = ''
        self.vector = ''
        self.listaParametros = listaParametros
        self.listaInstrucciones = listaInstrucciones
        if types is None:
            self.retorno = tipos.ENTERO
        elif isinstance(types, tipos):
            self.retorno = types
            self.retorno2 = types
        elif type(types) is list:
            self.retorno = tipos.VECTOR
            self.retorno2 = tipos.VECTOR
            self.vector = types
        else:
            self.retorno = types
            self.retorno2 = types
            
    def interpretar(self, tree, table):
        
        if self.listaParametros is None:
            self.listaParametros = []
        if self.listaInstrucciones is None:
            self.listaInstrucciones = []
        table.setFuncion(self.id, self)
        genAux = C3D()
        gen = genAux.getInstance()
        gen.addComment("Empezando declaracion de funciones")
        #DECLARANDO LA FUNCION CON SUS PARAMETROS
        tabla = Entorno(table)
        tabla.entorno = self.id
        table.addTabla(tabla)
        returnn = gen.newLabel()
        tabla.inFun = True
        tabla.returnn = returnn
        tabla.size = 1 
        for i in self.listaParametros:
            tipo = i.tipo
            vec = ''
            struct = ''
            if tipo is None:
                tipo = self.retorno
            elif isinstance(i.tipo, tipos):
                tipo = i.tipo
            elif type(i.tipo) is list:
                tipo = tipos.VECTOR
                vec = i.tipo
                self.retorno = tipos.VECTOR
            else:
                self.retorno = tipos.STRUCT
                tipo = tipos.STRUCT
                struct = i.tipo
            tabla.setVariable(i.express.id, tipo, (i.tipo == tipos.CADENA or i.tipo == tipos.STRUCT), vec, struct, self.line, self.column)

        gen.initFun(self.id)
        gen.addComment("Interpretando instrucciones funcion")
        for i in self.listaInstrucciones:
            val = i.interpretar(tree, tabla)
            if isinstance(val, Excepciones): return val
        gen.addGoto(returnn)
        gen.addLabel(returnn)
        gen.endFun()
        gen.addComment("Fin declaracion de funciones")
        
    
    def getNodo(self):
        pass