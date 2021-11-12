from abstract.Instruccion import Instruccion
from abstract.Retorno import Retornar
from excepciones.Excepciones import Excepciones
from expression.Variable import Variable
from tablaSimbolos.C3D import C3D
from tablaSimbolos.Tipo import tipos

class AsignarAtributo(Instruccion):
    def __init__(self, idVar, listaID, express, line, column):
        super().__init__(tipos.CADENA, line, column)
        self.line = line
        self.column = column
        self.id = idVar
        self.listaID = listaID
        self.express = express
    
    def interpretar(self, tree, table):
        struct = table.getVariable(self.id)
        value = self.express.interpretar(tree, table)
        if isinstance(value, Excepciones): return value
        if struct is None:
            #Error
            tree.addError(Excepciones("Semántico", "No existe el struct", self.line, self.column))
            return Excepciones("Semántico", "No existe el struct", self.line, self.column)
        declara = Variable(self.id, self.line, self.column)
        variable = declara.interpretar(tree, table)
        if isinstance(variable, Excepciones): return variable
        
        genAux = C3D()
        gen = genAux.getInstance()
        gen.addComment("Empezando acceso atributo")
        
        inicio = gen.addTemp() 
        gen.addExp(inicio, variable.value, '', '')        
        
        #VALIDANDO LISTA DE ATRIBUTOS
        dic = table.getStruct(struct.struct)
        for att in range(len(self.listaID)):
            if dic[0] == False:
                #Error
                tree.addError(Excepciones("Semántico", "El struct no es mutable", self.line, self.column))
                return Excepciones("Semántico", "El struct no es mutable", self.line, self.column)
            existe = False
            cont = 0;
            for i in dic[1]:
                if i.id == self.listaID[att]:
                    existe = True
                    break;
                cont += 1
            if existe == False:
                #Error
                tree.addError(Excepciones("Semántico", "No existe el atributo", self.line, self.column))
                return Excepciones("Semántico", "No existe el atributo", self.line, self.column)
            if att == len(self.listaID) - 1:
                #FINAL DE LA LISTA ID
                gen.addComment("Struct obtenido, buscando posicion del elemento")
                gen.addExp(inicio, inicio, '+', cont)
                gen.setHeap(inicio, value.value)
            else:
                if isinstance(dic[1][cont].tipo, tipos):
                    #Error
                    tree.addError(Excepciones("Semántico", "No existe el struct", self.line, self.column))
                    return Excepciones("Semántico", "No existe el struct", self.line, self.column)
                else:
                    tmp = table.getStruct(dic[1][cont].tipo)
                    if tmp is not None:
                        dic = tmp
                        gen.addComment("Cambiando inicio de struct")
                        tmpH = gen.addTemp()
                        gen.addExp(tmpH, inicio, '+', cont)
                        gen.getHeap(inicio, tmpH)
                        gen.addComment("Ejecutando siguiente atributo")
                        continue
                    else:
                        #Error
                        tree.addError(Excepciones("Semántico", "No existe el struct", self.line, self.column))
                        return Excepciones("Semántico", "No existe el struct", self.line, self.column)
           
    def getNodo(self):
        pass