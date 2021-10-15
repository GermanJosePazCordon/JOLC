from enum import Enum

class Tipo:
    def __init__(self, tipos):
        self.tipos = tipos
        
    def equals(self, obj):
        self.tipos = obj 
        return  self.tipos
    
    def getTipo(self):
        return self.tipos
    
    def setTipo(self, tipo):
        self.tipos = tipo
    
class tipos(Enum):
    ENTERO = 1
    DECIMAL = 2
    CARACTER = 3
    BOOLEAN = 4
    CADENA = 5
    BREAK = 6
    RETURN = 7
    CONTINUE = 8
    VARIABLE = 9
    FUNCION = 10
    STRUCT = 11
    VECTOR = 12
    NULO = 13