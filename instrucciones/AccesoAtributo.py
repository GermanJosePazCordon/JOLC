from abstract.Instruccion import Instruccion
from abstract.Retorno import Retornar
from expression.Variable import Variable
from instrucciones.AccesoVector import AccesoVector
from tablaSimbolos.C3D import C3D
from tablaSimbolos.Tipo import tipos

class AccesoAtributo(Instruccion):
    def __init__(self, idVar, listaID, line, column, isVec):
        super().__init__(tipos.CADENA, line, column)
        self.line = line
        self.column = column
        self.id = idVar
        self.listaID = listaID
        self.isVec = isVec
    
    def interpretar(self, tree, table):
        struct = table.getVariable(self.id)
        if struct is None:
            #Error
            print("No existe el struct")
            return
        '''elif struct.tipo != tipos.STRUCT:
            #Error
            print("La variable no es tipo struct")
            return'''
        declara = Variable(self.id, self.line, self.column)
        variable = declara.interpretar(tree, table)
        
        genAux = C3D()
        gen = genAux.getInstance()
        gen.addComment("Empezando acceso atributo")
        
        inicio = gen.addTemp() 
        gen.addExp(inicio, variable.value, '', '')        
        
        #VALIDANDO LISTA DE ATRIBUTOS
        dic = table.getStruct(struct.struct)
        for att in range(len(self.listaID)):
            existe = False
            cont = 0;
            for i in dic[1]:
                if i.id == self.listaID[att]:
                    existe = True
                    break;
                cont += 1
            if existe == False:
                #Error
                print("No existe el atributo")
                return
            if att == len(self.listaID) - 1:
                #FINAL DE LA LISTA ID
                gen.addExp(inicio, inicio, '+', cont)
                tmp = gen.addTemp()
                gen.getHeap(tmp, inicio)
                tipo = dic[1][cont].tipo
                if tipo == tipos.BOOLEAN:
                    gen.addComment("Acceso devolviendo boolean")
                    gen.addComment("Finalizando acceso atributo")
                    pass
                elif tipo == tipos.VECTOR or type(tipo) is list:
                    gen.addComment("Acceso devolviendo vector")
                    gen.addComment("Finalizando acceso atributo")
                    return Retornar(tmp, tipos.VECTOR, True, tipo)
                else:
                    gen.addComment("Finalizando acceso atributo")
                    return Retornar(tmp, tipo, True)
            else:
                if isinstance(dic[1][cont].tipo, tipos):
                    #Error
                    print("No existe el struct")
                    return
                else:
                    tmp = table.getStruct(dic[1][cont].tipo)
                    if tmp is not None:
                        dic = tmp
                        gen.addComment("Cambiando inicio de struct")
                        tmpH = gen.addTemp()
                        gen.addExp(tmpH, inicio, '+', cont)
                        gen.getHeap(inicio, tmpH)
                        #gen.addExp(inicio, inicio, '+', cont)
                        gen.addComment("Ejecutando siguiente atributo")
                        continue
                    else:
                        #Error
                        print("No existe el struct")
                        return
                        
            
    def getNodo(self):
        pass