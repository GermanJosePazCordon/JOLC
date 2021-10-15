from abstract.Instruccion import Instruccion
from tablaSimbolos.C3D import C3D
from tablaSimbolos.Tipo import tipos
from expression.Primitiva import Primitiva
from excepciones.Excepciones import Excepciones
from abstract.Retorno import Retornar


class Aritmetica(Instruccion):
    def __init__(self, operador, operando1, operando2, line, column):
        super().__init__(tipos.ENTERO, line, column)
        self.line = line
        self.column = column
        self.operador = operador
        if operando2 is None:
            self.opU = operando1
        else:
            self.op1 = operando1
            self.op2 = operando2
            self.opU = None

    def interpretar(self, tree, table):
        aux = C3D()
        gen = aux.getInstance()
        left = None
        right = None
        unario = None
        p1 = None
        p2 = None
        pu = None
        if self.opU is None:
            p1 = self.op1.interpretar(tree, table)
            if isinstance(p1, Excepciones):
                return p1
            left = p1.value

            p2 = self.op2.interpretar(tree, table)
            if isinstance(p2, Excepciones):
                return p2
            right = p2.value

            if self.op1.tipo == tipos.BOOLEAN:
                left = str(left).lower()
            elif self.op2.tipo == tipos.BOOLEAN:
                right = str(right).lower()
        else:
            unario = self.opU.interpretar(tree, table)
            if isinstance(unario, Excepciones):
                return unario
            pu = unario
            unario = unario.value

        if self.operador == '+':
            if p1.tipo == tipos.ENTERO:  # Entero + algo
                if p2.tipo == tipos.ENTERO:
                     # Entero + Entero
                    self.tipo = tipos.ENTERO
                    temp = gen.addTemp()
                    gen.addExp(temp, left, self.operador, right)
                    return self.retorno(temp, True)
                elif p2.tipo == tipos.DECIMAL:
                     # Entero + Decimal
                    self.tipo = tipos.DECIMAL
                    temp = gen.addTemp()
                    gen.addExp(temp, left, self.operador, right)
                    return self.retorno(temp, True)
                else:
                    # ERRORES
                    pass
            elif p1.tipo == tipos.DECIMAL:  # Decimal + algo
                if p2.tipo == tipos.ENTERO:
                    # Decimal + Entero
                    self.tipo = tipos.DECIMAL
                    temp = gen.addTemp()
                    gen.addExp(temp, left, self.operador, right)
                    return self.retorno(temp, True)
                elif p2.tipo == tipos.DECIMAL:
                    # Decimal + Decimal
                    self.tipo = tipos.DECIMAL
                    # Decimal + Decimal
                    temp = gen.addTemp()
                    gen.addExp(temp, left, self.operador, right)
                    return self.retorno(temp, True)
                else:
                    # ERRORES
                    pass
            else:
                # ERRORES
                pass
        elif self.operador == '-':
            if p1.tipo == tipos.ENTERO:  # Entero - algo
                if p2.tipo == tipos.ENTERO:
                    self.tipo = tipos.ENTERO
                    # Entero - Entero
                    temp = gen.addTemp()
                    gen.addExp(temp, left, self.operador, right)
                    return self.retorno(temp, True)
                elif p2.tipo == tipos.DECIMAL:
                    self.tipo = tipos.DECIMAL
                    # Entero - Decimal
                    temp = gen.addTemp()
                    gen.addExp(temp, left, self.operador, right)
                    return self.retorno(temp, True)
                else:
                    # ERRORES
                    pass
            elif p1.tipo == tipos.DECIMAL:  # Decimal - algo
                if p2.tipo == tipos.ENTERO:
                    self.tipo = tipos.DECIMAL
                    # Decimal - Entero
                    temp = gen.addTemp()
                    gen.addExp(temp, left, self.operador, right)
                    return self.retorno(temp, True)
                elif p2.tipo == tipos.DECIMAL:
                    self.tipo = tipos.DECIMAL
                    # Decimal - Decimal
                    temp = gen.addTemp()
                    gen.addExp(temp, left, self.operador, right)
                    return self.retorno(temp, True)
                else:
                    # ERRORES
                    pass
            else:
                # ERRORES
                pass
        elif self.operador == '*':
            if p1.tipo == tipos.ENTERO:  # Entero * algo
                if p2.tipo == tipos.ENTERO:
                    self.tipo = tipos.ENTERO
                    # Entero * Entero
                    temp = gen.addTemp()
                    gen.addExp(temp, left, self.operador, right)
                    return self.retorno(temp, True)
                elif p2.tipo == tipos.DECIMAL:
                    self.tipo = tipos.DECIMAL
                    # Entero * Decimal
                    temp = gen.addTemp()
                    gen.addExp(temp, left, self.operador, right)
                    return self.retorno(temp, True)
                else:
                    # ERRORES
                    pass
            elif p1.tipo == tipos.DECIMAL:  # Decimal * algo
                if p2.tipo == tipos.ENTERO:
                    self.tipo = tipos.DECIMAL
                    # Decimal * Entero
                    temp = gen.addTemp()
                    gen.addExp(temp, left, self.operador, right)
                    return self.retorno(temp, True)
                elif p2.tipo == tipos.DECIMAL:
                    self.tipo = tipos.DECIMAL
                    # Decimal * Decimal
                    temp = gen.addTemp()
                    gen.addExp(temp, left, self.operador, right)
                    return self.retorno(temp, True)
                else:
                    # ERRORES
                    pass
            elif p1.tipo == tipos.CADENA:  # Cadena * algo
                if p2.tipo == tipos.CADENA:
                    # ERRORES
                    pass
                else:
                    # ERRORES
                    pass
            else:
                # ERRORES
                pass
        elif self.operador == '/':
            if int(right) != 0 or float(right) != 0:
               if p1.tipo == tipos.ENTERO:  # Entero / algo
                   if p2.tipo == tipos.ENTERO:
                        self.tipo = tipos.DECIMAL
                        # Entero / Entero
                        temp = gen.addTemp()
                        gen.addExp(temp, left, self.operador, right)
                        return self.retorno(temp, True)
                   elif p2.tipo == tipos.DECIMAL:
                        self.tipo = tipos.DECIMAL
                        # Entero / Decimal
                        temp = gen.addTemp()
                        gen.addExp(temp, left, self.operador, right)
                        return self.retorno(temp, True)
                   else:
                        #Error
                        pass
               elif p1.tipo == tipos.DECIMAL:  # Decimal / algo
                    if p2.tipo == tipos.ENTERO:
                        self.tipo = tipos.DECIMAL
                        # Decimal / Entero
                        temp = gen.addTemp()
                        gen.addExp(temp, left, self.operador, right)
                        return self.retorno(temp, True)
                    elif p2.tipo == tipos.DECIMAL:
                        self.tipo = tipos.DECIMAL
                        # Decimal / Decimal
                        temp = gen.addTemp()
                        gen.addExp(temp, left, self.operador, right)
                        return self.retorno(temp, True)
                    else:
                        #Error
                        pass
               else:
                    #Error
                    pass
            else:
               #Error
               pass
        
    def retorno(self, result, temp):
        return Retornar(result, self.tipo, temp)

    def getNodo(self):
        pass
