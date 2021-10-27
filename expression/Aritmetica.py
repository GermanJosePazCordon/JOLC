from abstract.Instruccion import Instruccion
from instrucciones.Llamada import Llamada
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
        gen.addComment("Empezando aritmetica")
        left = None
        right = None
        unario = None
        if self.opU is None:
            gen.addComment("Interpretando op1")
            p1 = self.op1.interpretar(tree, table)
            if isinstance(p1, Excepciones):
                return p1
            left = p1.value

            #--------------------------------------------------
            if isinstance(self.op2, Llamada) and table.inFun:
                genAux = C3D()
                gen = genAux.getInstance()
                gen.saveTemp(table, left) 
            #--------------------------------------------------
            gen.addComment("Interpretando op2")
            p2 = self.op2.interpretar(tree, table)
            if isinstance(p2, Excepciones):
                return p2
            right = p2.value
            
            #--------------------------------------------------
            if isinstance(self.op2, Llamada) and table.inFun:
                genAux = C3D()
                gen = genAux.getInstance()
                gen.getTemp(table, left)
            #--------------------------------------------------

            if self.op1.tipo == tipos.BOOLEAN:
                left = str(left).lower()
            elif self.op2.tipo == tipos.BOOLEAN:
                right = str(right).lower()
        else:
            gen.addComment("Interpretando opU")
            unario = self.opU.interpretar(tree, table)
            if isinstance(unario, Excepciones):
                return unario
            pu = unario
            unario = unario.value
        gen.addComment("Realizando operacion")
        if self.operador == '+':
            if p1.tipo == tipos.ENTERO:  # Entero + algo
                if p2.tipo == tipos.ENTERO:
                    # Entero + Entero
                    self.tipo = tipos.ENTERO
                    temp = gen.addTemp()
                    gen.addExp(temp, left, self.operador, right)
                    #gen.deleteTemp(temp)
                    return self.retorno(temp, True)
                elif p2.tipo == tipos.DECIMAL:
                    # Entero + Decimal
                    self.tipo = tipos.DECIMAL
                    temp = gen.addTemp()
                    gen.addExp(temp, left, self.operador, right)
                    #gen.deleteTemp(temp)
                    return self.retorno(temp, True)
                else:
                    #Error
                    print("Operandos erroneos para +")
                    return
            elif p1.tipo == tipos.DECIMAL:  # Decimal + algo
                if p2.tipo == tipos.ENTERO:
                    # Decimal + Entero
                    self.tipo = tipos.DECIMAL
                    temp = gen.addTemp()
                    gen.addExp(temp, left, self.operador, right)
                    #gen.deleteTemp(temp)
                    return self.retorno(temp, True)
                elif p2.tipo == tipos.DECIMAL:
                    # Decimal + Decimal
                    self.tipo = tipos.DECIMAL
                    # Decimal + Decimal
                    temp = gen.addTemp()
                    gen.addExp(temp, left, self.operador, right)
                    #gen.deleteTemp(temp)
                    return self.retorno(temp, True)
                else:
                    #Error
                    print("Operandos erroneos para +")
                    return
            else:
                #Error
                print("Operandos erroneos para +")
                return
        elif self.operador == '-':
            if p1.tipo == tipos.ENTERO:  # Entero - algo
                if p2.tipo == tipos.ENTERO:
                    self.tipo = tipos.ENTERO
                    # Entero - Entero
                    temp = gen.addTemp()
                    gen.addExp(temp, left, self.operador, right)
                    #gen.deleteTemp(temp)
                    return self.retorno(temp, True)
                elif p2.tipo == tipos.DECIMAL:
                    self.tipo = tipos.DECIMAL
                    # Entero - Decimal
                    temp = gen.addTemp()
                    gen.addExp(temp, left, self.operador, right)
                    #gen.deleteTemp(temp)
                    return self.retorno(temp, True)
                else:
                    #Error
                    print("Operandos erroneos para -")
                    return
            elif p1.tipo == tipos.DECIMAL:  # Decimal - algo
                if p2.tipo == tipos.ENTERO:
                    self.tipo = tipos.DECIMAL
                    # Decimal - Entero
                    temp = gen.addTemp()
                    gen.addExp(temp, left, self.operador, right)
                    #gen.deleteTemp(temp)
                    return self.retorno(temp, True)
                elif p2.tipo == tipos.DECIMAL:
                    self.tipo = tipos.DECIMAL
                    # Decimal - Decimal
                    temp = gen.addTemp()
                    gen.addExp(temp, left, self.operador, right)
                    #gen.deleteTemp(temp)
                    return self.retorno(temp, True)
                else:
                    #Error
                    print("Operandos erroneos para -")
                    return
            else:
                #Error
                    print("Operandos erroneos para -")
                    return
        elif self.operador == '*':
            if p1.tipo == tipos.ENTERO:  # Entero * algo
                if p2.tipo == tipos.ENTERO:
                    self.tipo = tipos.ENTERO
                    # Entero * Entero
                    temp = gen.addTemp()
                    gen.addExp(temp, left, self.operador, right)
                    #gen.deleteTemp(temp)
                    return self.retorno(temp, True)
                elif p2.tipo == tipos.DECIMAL:
                    self.tipo = tipos.DECIMAL
                    # Entero * Decimal
                    temp = gen.addTemp()
                    gen.addExp(temp, left, self.operador, right)
                    #gen.deleteTemp(temp)
                    return self.retorno(temp, True)
                else:
                    #Error
                    print("Operandos erroneos para *")
                    return
            elif p1.tipo == tipos.DECIMAL:  # Decimal * algo
                if p2.tipo == tipos.ENTERO:
                    self.tipo = tipos.DECIMAL
                    # Decimal * Entero
                    temp = gen.addTemp()
                    gen.addExp(temp, left, self.operador, right)
                    #gen.deleteTemp(temp)
                    return self.retorno(temp, True)
                elif p2.tipo == tipos.DECIMAL:
                    self.tipo = tipos.DECIMAL
                    # Decimal * Decimal
                    temp = gen.addTemp()
                    gen.addExp(temp, left, self.operador, right)
                    #gen.deleteTemp(temp)
                    return self.retorno(temp, True)
                else:
                    #Error
                    print("Operandos erroneos para *")
                    return
            elif p1.tipo == tipos.CADENA:  # Cadena * algo
                if p2.tipo == tipos.CADENA:
                    self.tipo = tipos.CADENA
                    gen.concatString()
                    tmp = gen.addTemp()

                    gen.addExp(tmp, 'P', '+', table.size)

                    gen.addExp(tmp, tmp, "+", '1')
                    gen.setStack(tmp, left)

                    gen.addExp(tmp, tmp, '+', '1')
                    gen.setStack(tmp, right)

                    gen.newTable(table.size)
                    gen.callFun('concatString')
                    temp = gen.addTemp()
                    gen.getStack(temp, 'P')
                    gen.getTable(table.size)
                    #gen.deleteTemp(temp)
                    return Retornar(temp, tipos.CADENA, True)
                else:
                    #Error
                    print("Operandos erroneos para *")
                    return
            else:
                #Error
                    print("Operandos erroneos para *")
                    return
        elif self.operador == '/':
            if p1.tipo == tipos.ENTERO or p1.tipo == tipos.DECIMAL:  # Entero / algo
                if p2.tipo == tipos.ENTERO or p2.tipo == tipos.DECIMAL:
                    self.tipo = tipos.DECIMAL
                    # Entero / Entero
                    izq = gen.addTemp()
                    der = gen.addTemp()
                    temp = gen.addTemp()
                    gen.addExp(izq, left, '', '')
                    gen.addExp(der, right, '', '')
                    
                    condicional = gen.newLabel()
                    salida = gen.newLabel()
                    salida2 = gen.newLabel()
                    
                    gen.newIF(der, "==", "0", condicional)
                    gen.addGoto(salida)
                    gen.addLabel(condicional)
                    
                    gen.addPrint("c", 77)
                    gen.addPrint("c", 97)
                    gen.addPrint("c", 116)
                    gen.addPrint("c", 104)
                    gen.addPrint("c", 69)
                    gen.addPrint("c", 114)
                    gen.addPrint("c", 114)
                    gen.addPrint("c", 111)
                    gen.addPrint("c", 114)
                    gen.addPrint("c", 10)
                    
                    gen.addExp(temp, 0, '', '')
                    gen.addGoto(salida2)
                    
                    gen.addLabel(salida) 
                    gen.addExp(temp, izq, self.operador, der)
                    gen.addLabel(salida2)
                    return self.retorno(temp, True)
                else:
                    #Error
                    print("Operandos erroneos para /")
                    return
            else:
                #Error
                print("Operandos erroneos para /")
                return
        elif self.operador == '^':
            if p1.tipo == tipos.ENTERO or p1.tipo == tipos.DECIMAL:
                if p2.tipo == tipos.ENTERO:
                    self.tipo = p1.tipo
                    '''tmp = gen.addTemp()
                    gen.addExp(tmp, "math.Pow(" + left + "," + right + ")", '', '')
                    if gen.imath == False:
                        gen.imports += ';\n\t"math"'
                        gen.imath = True
                    return Retornar(tmp, p1.tipo, True)'''
                    gen.potencia()
                    tmp = gen.addTemp()

                    gen.addExp(tmp, 'P', '+', table.size)

                    gen.addExp(tmp, tmp, "+", '1')
                    gen.setStack(tmp, left)

                    gen.addExp(tmp, tmp, '+', '1')
                    gen.setStack(tmp, right)

                    gen.newTable(table.size)
                    gen.callFun('potencia')
                    temp = gen.addTemp()
                    gen.getStack(temp, 'P')
                    gen.getTable(table.size)
                    #gen.deleteTemp(temp)
                    return Retornar(temp, p1.tipo, True)
                else:
                    #Error
                    print("Operandos erroneos para ^")
                    return
            elif p1.tipo == tipos.CADENA:
                if p2.tipo == tipos.ENTERO:
                    self.tipo = tipos.CADENA
                    gen.potenciaString()
                    tmp = gen.addTemp()

                    gen.addExp(tmp, 'P', '+', table.size)

                    gen.addExp(tmp, tmp, "+", '1')
                    gen.setStack(tmp, left)

                    gen.addExp(tmp, tmp, '+', '1')
                    gen.setStack(tmp, right)

                    gen.newTable(table.size)
                    gen.callFun('potenciaString')
                    temp = gen.addTemp()
                    gen.getStack(temp, 'P')
                    gen.getTable(table.size)
                    return Retornar(temp, tipos.CADENA, True)
                else:
                    #Error
                    print("Operandos erroneos para ^")
                    return
            else:
                #Error
                print("Operandos erroneos para ^")
                return
        elif self.operador == '%':
            if p1.tipo == tipos.ENTERO or p1.tipo == tipos.DECIMAL:
                if p2.tipo == tipos.ENTERO or p2.tipo == tipos.DECIMAL:
                    if p1.tipo == tipos.ENTERO and p2.tipo == tipos.ENTERO:
                        self.tipo = tipos.ENTERO
                    else: 
                        self.tipo = tipos.DECIMAL
                    if gen.imath == False:
                        gen.imports += ';\n\t"math"'
                        gen.imath = True
                    izq = gen.addTemp()
                    der = gen.addTemp()
                    temp = gen.addTemp()
                    gen.addExp(izq, left, '', '')
                    gen.addExp(der, right, '', '')

                    condicional = gen.newLabel()
                    salida = gen.newLabel()
                    salida2 = gen.newLabel()

                    gen.newIF(der, "==", "0", condicional)
                    gen.addGoto(salida)
                    gen.addLabel(condicional)

                    gen.addPrint("c", 77)
                    gen.addPrint("c", 97)
                    gen.addPrint("c", 116)
                    gen.addPrint("c", 104)
                    gen.addPrint("c", 69)
                    gen.addPrint("c", 114)
                    gen.addPrint("c", 114)
                    gen.addPrint("c", 111)
                    gen.addPrint("c", 114)
                    gen.addPrint("c", 10)

                    gen.addExp(temp, 0, '', '')
                    gen.addGoto(salida2)

                    gen.addLabel(salida) 
                    gen.addExp(temp, "math.Mod(" + izq + "," + der + ")", '', '')
                    gen.addLabel(salida2)
                    #gen.deleteTemp(temp)
                    return self.retorno(temp, True)
                else:
                    #Error
                    print("Operandos erroneos para %")
                    return
            else:
                #Error
                print("Operandos erroneos para %")
                return
            '''gen.modulo()
            tmp = gen.addTemp()
            gen.addExp(tmp, 'P', '+', table.size)
            gen.addExp(tmp, tmp, "+", '1')
            gen.setStack(tmp, left)
            gen.addExp(tmp, tmp, '+', '1')
            gen.setStack(tmp, right)

            gen.addExp(tmp, tmp, '+', '1')
            gen.setStack(tmp, int(float(left)/float(right)))

            gen.newTable(table.size)
            gen.callFun('modulo')
            temp = gen.addTemp()
            gen.getStack(temp, 'P')
            gen.getTable(table.size)
            return Retornar(temp, tipos.DECIMAL, True)'''
        elif self.operador == '-u':
            if pu.tipo == tipos.ENTERO:
                self.tipo = tipos.ENTERO
                temp = gen.addTemp()
                gen.addExp(temp, unario, "*", "-1")
                #gen.deleteTemp(temp)
                return self.retorno(temp, True)
            elif pu.tipo == tipos.DECIMAL:
                self.tipo = tipos.DECIMAL
                temp = gen.addTemp()
                gen.addExp(temp, unario, "*", "-1")
                #gen.deleteTemp(temp)
                return self.retorno(temp, True)
            else:
                #Error
                print("Operandos erroneos para el operador unario")
                return

    def retorno(self, result, temp):
        return Retornar(result, self.tipo, temp)

    def getNodo(self):
        pass
