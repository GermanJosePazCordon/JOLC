
from abstract.NodoAST import NodoAST
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
        self.vector = ''
        self.listaParametros = listaParametros
        self.listaInstrucciones = listaInstrucciones
        if isinstance(types, tipos):
            self.retorno = types
        else:
            self.retorno = tipos.VECTOR
            self.vector = types
    
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
        returnn = gen.newLabel()
        tabla.inFun = True
        tabla.returnn = returnn
        tabla.size = 1 
        for i in self.listaParametros:
            tipo = i.tipo
            vec = ''
            if tipo is None:
                tipo = self.retorno
            elif isinstance(i.tipo, tipos):
                tipo = i.tipo
            else:
                tipo = tipos.VECTOR
                vec = i.tipo
            tabla.setVariable(i.express.id, tipo, (i.tipo == tipos.CADENA or i.tipo == tipos.STRUCT), vec)

        gen.initFun(self.id)
        gen.addComment("Interpretando instrucciones funcion")
        for i in self.listaInstrucciones:
            i.interpretar(tree, tabla)
        gen.addLabel(returnn)
        gen.endFun()
        gen.addComment("Fin declaracion de funciones")
        
    
    def getNodo(self):
        pass