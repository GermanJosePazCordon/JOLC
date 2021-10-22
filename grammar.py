# --------------------
# German Paz
# --------------------

from platform import node
import re
from abstract.NodoAST import NodoAST

from excepciones.Excepciones import Excepciones

from tablaSimbolos.Tipo import tipos
from tablaSimbolos.Arbol import Arbol
from tablaSimbolos.TablaSimbolos import tablaSimbolos

from expression.Primitiva import Primitiva
from expression.Aritmetica import Aritmetica
from expression.Nativa import Nativa
from expression.Relacional import Relacional
from expression.Logica import Logica
from expression.Variable import Variable

from instrucciones.Print import Print
from instrucciones.Println import Println
from instrucciones.DeclararVariable import DeclararVariable
from instrucciones.FuncionNativa import FuncionNativa
from instrucciones.EvaluarIF import EvaluarIF
from instrucciones.ListaIF import ListaIF
from instrucciones.While import While
from instrucciones.Break import Break
from instrucciones.Return import Return
from instrucciones.Continue import Continue
from instrucciones.For import For
from instrucciones.AccesoVector import AccesoVector
from instrucciones.ModificarVector import ModificarVector
from instrucciones.Funciones import Funciones
from instrucciones.Llamada import Llamada
from instrucciones.Structs import Structs
from instrucciones.Atributo import Atributo
from instrucciones.AccesoAtributo import AccesoAtributo
from instrucciones.AsignarAtributo import AsignarAtributo
from instrucciones.Push import Push

import sys

sys.setrecursionlimit(3000)

errores = []
reservadas = {
    'println'   : 'PRINTLN',
    'print'     : 'PRINT',
    
    'if'        : 'IF',
    'else'      : 'ELSE',
    'elseif'    : 'ELSEIF',
    'while'     : 'WHILE',
    'for'       : 'FOR',
    
    'in'        : 'IN',
    'end'       : 'END',
    
    'return'    : 'RETURN',
    'continue'  : 'CONTINUE',
    'break'     : 'BREAK',
     
    'true'      : 'TRUE',
    'false'     : 'FALSE',
    
    'log'       : 'LOG',
    'log10'     : 'LOG10',
    'sin'       : 'SENO',
    'cos'       : 'COSENO',
    'tan'       : 'TANGENTE',
    'sqrt'      : 'RAIZ',
    
    'Int64'     : 'RINT',
    'Float64'   : 'RFLOAT',
    'Bool'      : 'RBOOL',
    'Char'      : 'RCHAR',
    'String'    : 'RSTRING',
    'nothing'   : 'RNULO',
    
    'uppercase' : 'UPPER',
    'lowercase' : 'LOWER',
    'parse'     : 'PARSE',
    'trunc'     : 'TRUNC',
    'float'     : 'FLOAT',
    'string'    : 'STR',
    'typeof'    : 'TYPEOF',
    
    'push'      : 'PUSH',
    'pop'       : 'POP',
    'length'    : 'LENGTH',
    
    'function'  : 'FUNCTION',
    'struct'    : 'STRUCT',
    'mutable'    : 'MUTABLE',
    
    
    'global'    : 'GLOBAL',
    'local'     : 'LOCAL',
}

tokens  = [
    # Simbolos
    'PTCOMA',
    'DBPUNTO',
    'DOSPUNTO',
    'PARIZQ',
    'PARDER',    
    'CORIZQ',    
    'CORDER',    
    'COMA',
    'PUNTO',
   
    # Mate
    'MAS',
    'MENOS',
    'POR',
    'DIVIDIDO',
    'POTENCIA',
    'MODULO',
    
    # Relacional
    'MAYORIGUAL',
    'MENORIGUAL',
    'MAYORQUE',
    'MENORQUE',
    'IGUALACION',
    'DIFERENCIACION',
    'IGUAL',

    # Logico
    'AND',
    'OR',
    'NOT',

    # Tipos
    'DECIMAL',
    'ENTERO',
    'CADENA',
    'CARACTER',
    'ID'
] + list(reservadas.values())
# Tokens

# Simbolos
t_PTCOMA    = r';'
t_DBPUNTO   = r'::'
t_DOSPUNTO  = r':'
t_PARIZQ    = r'\('
t_PARDER    = r'\)'
t_CORIZQ    = r'\['
t_CORDER    = r'\]'
t_COMA      = r','
t_PUNTO     = r'\.'

# Mate
t_MAS       = r'\+'
t_MENOS     = r'-'
t_POR       = r'\*'
t_DIVIDIDO  = r'/'
t_POTENCIA  = r'\^'
t_MODULO    = r'%'

# Relacional
t_MENORIGUAL     = r'<='
t_MAYORIGUAL     = r'>='
t_MENORQUE       = r'<'
t_MAYORQUE       = r'>'
t_IGUALACION     = r'=='
t_DIFERENCIACION = r'!='
t_IGUAL          = r'='

# Logico
t_AND   = r'&&'
t_OR    = r'\|\|'
t_NOT   = r'!'

def t_DECIMAL(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Float value too large %d", t.value)
        t.value = 0
    return t

def t_ENTERO(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

def t_ID(t):
     r'[a-zA-Z][a-zA-Z_0-9]*'
     t.type = reservadas.get(t.value,'ID')
     return t

def t_CARACTER(t):
    r'(\'.*?\')'
    t.value = t.value[1:-1] # remuevo las comillas simples
    return t

def t_CADENA(t):
    r'(\".*?\")'
    t.value = t.value[1:-1] # remuevo las comillas
    return t

def t_COMENTARIO_MULTILINEA(t):
    r'\#\=(.|\n)*?\=\#'
    t.lexer.lineno += t.value.count('\n')

# Comentario simple // ...
def t_COMENTARIO_SIMPLE(t):
    r'\#.*\n'
    t.lexer.lineno += 1
     
# Caracteres ignorados
t_ignore = " \t\r"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    errores.append(Excepciones("Lexico","Error léxico: " + t.value[0] , t.lexer.lineno, find_column(input, t)))
    t.lexer.skip(1)
    
# Compute column.
#     input is the input text string
#     token is a token instance
def find_column(inp, token):
    line_start = inp.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1

import ply.lex as lex
lexer = lex.lex()

#lex.lex(reflags=re.IGNORECASE)
# Asociación de operadores y precedencia
precedence = (
    ('left','OR'),
    ('left','AND'),
    ('right','NOT'),
    ('left','IGUALACION', 'DIFERENCIACION', 'MENORQUE', 'MENORIGUAL', 'MAYORQUE', 'MAYORIGUAL'),
    ('left','MAS','MENOS'),
    ('left','POR','DIVIDIDO', "MODULO"),
    ('left','POTENCIA'), 
    ('right','UMENOS'),
    )
     
# Definición de la gramática
def p_instrucciones_lista(t):
    'instrucciones : instrucciones instruccion'
    t[1].append(t[2])
    t[0] = t[1]

def p_instrucciones_lista1(t):
    'instrucciones : instruccion'
    t[0] = []
    t[0].append(t[1])
    
def p_instrucciones_evaluar(t):
    '''
    instruccion : IMPRIMIR
                | IMPRIMIRLN
                | DECLARARVARIABLE PTCOMA
                | NOMBRAR
                | CONDICIONAL 
                | CICLO_WHILE
                | TRANSFERENCIA
                | CICLO_FOR
                | INSTRUCCION_PUSH
                | MOD_VECTOR
                | FUNCIONES
                | LLAMADA
                | DECLARAR_STRUCT
                | ASIGNAR_STRUCT
    '''
    t[0] = t[1]

def p_instruccion_error(t):
    'instruccion : error PTCOMA'
    errores.append(Excepciones("Sintactico :",  "Error Sintáctico:" + str(t[1].value), t.lineno(1), find_column(input, t.slice[1])))
    t[0] = ""
   
def p_imprimir(t):
    'IMPRIMIR : PRINT PARIZQ LISTAEXPRESION PARDER PTCOMA'
    t[0] = Print(t[3], t.lineno(1), find_column(input, t.slice[1])) 
    
def p_print_vacio(t):
    'IMPRIMIR : PRINT PARIZQ PARDER PTCOMA'
    t[0] = Print(None, t.lineno(1), find_column(input, t.slice[1])) 

def p_println_vaico(t):
    'IMPRIMIRLN : PRINTLN PARIZQ PARDER PTCOMA'
    t[0] = Println(None, t.lineno(1), find_column(input, t.slice[1])) 

def p_imprimirln(t):
    'IMPRIMIRLN : PRINTLN PARIZQ LISTAEXPRESION PARDER PTCOMA'
    t[0] = Println(t[3], t.lineno(1), find_column(input, t.slice[1]))

def p_expresiones_lista(t):
    'LISTAEXPRESION : LISTAEXPRESION COMA EXPRESION'
    t[1].append(t[3])
    t[0] = t[1]

def p_expresiones_lista1(t):
    'LISTAEXPRESION : EXPRESION'
    t[0] = []
    t[0].append(t[1])

def p_declarar_variable_tipo(t):
    'DECLARARVARIABLE : ID IGUAL EXPRESION DBPUNTO tipo'
    t[0] = DeclararVariable(t[5], t[1], t[3], None, t.lineno(1), find_column(input, t.slice[1]))
    
def p_declarar_variable_tipo2(t):
    'DECLARARVARIABLE : ID IGUAL EXPRESION DBPUNTO ID'
    t[0] = DeclararVariable(None, t[1], t[3], None, t.lineno(1), find_column(input, t.slice[1]))

def p_declarar_variable(t):
    'DECLARARVARIABLE : ID IGUAL EXPRESION'
    t[0] = DeclararVariable(None, t[1], t[3], None, t.lineno(1), find_column(input, t.slice[1]))

def p_declarar_variable_id(t):
    'NOMBRAR : ATRIBUTO'
    t[0] = DeclararVariable(None, None, t[1], None, 0, 0)

def p_declarar_variable_id_global(t):
    'NOMBRAR : GLOBAL ATRIBUTO'
    t[0] = DeclararVariable(None, None, t[2], t[1], t.lineno(1), find_column(input, t.slice[1]))
    
def p_declarar_variable_tipo_global(t):
    'DECLARARVARIABLE : GLOBAL ID IGUAL EXPRESION DBPUNTO tipo'
    t[0] = DeclararVariable(t[6], t[2], t[4], t[1], t.lineno(1), find_column(input, t.slice[1]))

def p_declarar_variable_global(t):
    'DECLARARVARIABLE : GLOBAL ID IGUAL EXPRESION'
    t[0] = DeclararVariable(None, t[2], t[4], None, t.lineno(1), find_column(input, t.slice[1]))
    
def p_declarar_variable_tipo_local(t):
    'DECLARARVARIABLE : LOCAL ID IGUAL EXPRESION DBPUNTO tipo'
    t[0] = DeclararVariable(t[6], t[2], t[4], None, t.lineno(1), find_column(input, t.slice[1]))

def p_declarar_variable_local(t):
    'DECLARARVARIABLE : LOCAL ID IGUAL EXPRESION'
    t[0] = DeclararVariable(None, t[2], t[4], None, t.lineno(1), find_column(input, t.slice[1]))

def p_tranferencia(t):
    '''
    TRANSFERENCIA : BREAK PTCOMA
                  | CONTINUE PTCOMA
                  | RETURN EXPRESION PTCOMA
                  | RETURN PTCOMA
    '''
    if t[1] == 'break'      : t[0] = Break(t.lineno(2), find_column(input, t.slice[2]))
    elif t[1] == 'continue' : t[0] = Continue(t.lineno(2), find_column(input, t.slice[2]))
    elif t[1] == 'return':
        if t[2] == ';':
            t[0] = Return(None, t.lineno(2), find_column(input, t.slice[2]))
        else:
            t[0] = Return(t[2], t.lineno(3), find_column(input, t.slice[3]))

def p_condicional_if(t):
    'CONDICIONAL : INSTRUCCIONES_IF END PTCOMA'
    t[0] = EvaluarIF(t[1], None, 0, 0)

def p_condicional_if_else(t):
    'CONDICIONAL : INSTRUCCIONES_IF INSTRUCCION_ELSE END PTCOMA'
    t[0] = EvaluarIF(t[1], t[2], 0, 0)

def p_instrucciones_if(t):
    'INSTRUCCIONES_IF :  INSTRUCCION_IF'
    if t[1] == None:
        t[0] = []
    else:
        t[0] = [t[1]]
    
def p_instrucciones_eelse_if(t):
    'INSTRUCCIONES_IF :  INSTRUCCIONES_IF INSTRUCCION_ELSE_IF'
    if t[2] != None:
        t[1].append(t[2])
    t[0] = t[1]
        
def p_instruccion_if(t):
    'INSTRUCCION_IF : IF EXPRESION instrucciones'
    t[0] = ListaIF(t[2], t[3], t.lineno(1), find_column(input, t.slice[1]))
    
def p_instruccion_else(t):
    'INSTRUCCION_ELSE : ELSE instrucciones'
    t[0] = ListaIF(None, t[2], t.lineno(1), find_column(input, t.slice[1]))
    
def p_instruccion_else_if(t):
    'INSTRUCCION_ELSE_IF : ELSEIF EXPRESION instrucciones'
    t[0] = ListaIF(t[2], t[3], t.lineno(1), find_column(input, t.slice[1]))
    
def p_instruccion_while(t):
    'CICLO_WHILE : WHILE EXPRESION instrucciones END PTCOMA'
    t[0] = While(t[2], t[3], t.lineno(1), find_column(input, t.slice[1]))

def p_instruccion_for_rango(t):
    'CICLO_FOR : FOR ID IN EXPRESION DOSPUNTO EXPRESION instrucciones END PTCOMA'
    t[0] = For(t[2], 'rango', t[4], t[6], None, t[7], t.lineno(1), find_column(input, t.slice[1]))
    
def p_instruccion_for_cadena(t):
    'CICLO_FOR : FOR ID IN EXPRESION instrucciones END PTCOMA'
    t[0] = For(t[2], 'cadena', None, None, t[4], t[5], t.lineno(1), find_column(input, t.slice[1]))
    
def p_modificar_vector(t):
    'MOD_VECTOR : ID LISTAPOS IGUAL EXPRESION PTCOMA'
    t[0] = ModificarVector(t[1], t[2], t[4], t.lineno(1), find_column(input, t.slice[1]))
    
def p_funciones(t):
    '''
    FUNCIONES : FUNCTION ID PARIZQ LISTAPARAMETROS PARDER instrucciones END PTCOMA
              | FUNCTION ID PARIZQ PARDER instrucciones END PTCOMA
    '''
    if t[4] == ')' :  t[0] = Funciones(t[2], None, t[5], t.lineno(1), find_column(input, t.slice[1]))
    else           :  t[0] = Funciones(t[2], t[4], t[6], t.lineno(1), find_column(input, t.slice[1]))

def p_lista_parametros1(t):
    '''
    LISTAPARAMETROS : LISTAPARAMETROS COMA EXPRESION
                    | LISTAPARAMETROS COMA EXPRESION DBPUNTO ID
                    | LISTAPARAMETROS COMA EXPRESION DBPUNTO tipo
    '''
    t[1].append(t[3])
    t[0] = t[1]
    
def p_lista_parametros2(t):
    '''
    LISTAPARAMETROS : EXPRESION
                    | EXPRESION DBPUNTO ID
                    | EXPRESION DBPUNTO tipo
    '''
    t[0] = []
    t[0].append(t[1])
    
def p_llamda_funciones(t):
    '''
    LLAMADA : ID PARIZQ LISTAPARAMETROS PARDER PTCOMA
            | ID PARIZQ PARDER PTCOMA
    '''
    if t[3] == ')' : t[0] = Llamada(t[1], None, t.lineno(1), find_column(input, t.slice[1]))
    else           : t[0] = Llamada(t[1], t[3], t.lineno(1), find_column(input, t.slice[1]))

def p_expresion_llamada_funciones(t):
    '''
    EXPRESION : ID PARIZQ LISTAPARAMETROS PARDER
              | ID PARIZQ PARDER
    '''
    if t[3] == ')' : t[0] = Llamada(t[1], None, t.lineno(1), find_column(input, t.slice[1]))
    else           : t[0] = Llamada(t[1], t[3], t.lineno(1), find_column(input, t.slice[1]))
    
def p_structs(t):
    '''
    DECLARAR_STRUCT : STRUCT ID LISTAATRIBUTO END PTCOMA
                    | MUTABLE STRUCT ID LISTAATRIBUTO END PTCOMA
    '''
    if t[1] == 'struct': t[0] = Structs(False, t[2], t[3], t.lineno(1), find_column(input, t.slice[1]))
    else: t[0] = Structs(True, t[3], t[4], t.lineno(1), find_column(input, t.slice[1]))

def p_struct_lista_atributo1(t):
    'LISTAATRIBUTO : LISTAATRIBUTO ATRIBUTO'
    t[1].append(t[2])
    t[0] = t[1]

def p_struct_lista_atributo2(t):
    'LISTAATRIBUTO : ATRIBUTO'
    t[0] = []
    t[0].append(t[1])
    
def p_struct_atributo(t):
    '''
    ATRIBUTO : ID DBPUNTO tipo PTCOMA
             | ID PTCOMA
    '''
    if t[2] == ';' : t[0] = Atributo(None, t[1], None, t.lineno(1), find_column(input, t.slice[1]))
    else:  t[0] = Atributo(t[3], t[1], None, t.lineno(1), find_column(input, t.slice[1]))

def p_struct_atributo2(t):
    '''
    ATRIBUTO : ID DBPUNTO ID PTCOMA
    '''
    t[0] = Atributo(None, t[1], t[3], t.lineno(1), find_column(input, t.slice[1]))

def p_asignar_struct(t):
    'ASIGNAR_STRUCT : ID PUNTO LISTAID IGUAL EXPRESION PTCOMA'
    t[0] = AsignarAtributo(t[1], t[3], t[5], t.lineno(1), find_column(input, t.slice[1]))

# Expresiones
def p_expresion_primitiva_entero(t):
    'EXPRESION : ENTERO'
    t[0] = Primitiva(tipos.ENTERO, t[1], t.lineno(1), find_column(input, t.slice[1]))

def p_expresion_primitiva_decimal(t):
    'EXPRESION : DECIMAL'
    t[0] = Primitiva(tipos.DECIMAL, t[1], t.lineno(1), find_column(input, t.slice[1]))

def p_expresion_primitiva_cadena(t):
    'EXPRESION : CADENA'
    t[0] = Primitiva(tipos.CADENA, t[1], t.lineno(1), find_column(input, t.slice[1]))

def p_expresion_primitiva_caracter(t):
    'EXPRESION : CARACTER'
    t[0] = Primitiva(tipos.CARACTER, t[1], t.lineno(1), find_column(input, t.slice[1]))

def p_expresion_primitiva_booleana_true(t):
    'EXPRESION : TRUE'
    t[0] = Primitiva(tipos.BOOLEAN, t[1], t.lineno(1), find_column(input, t.slice[1]))

def p_expresion_primitiva_booleana_false(t):
    'EXPRESION : FALSE'
    t[0] = Primitiva(tipos.BOOLEAN, t[1], t.lineno(1), find_column(input, t.slice[1]))

def p_expresion_nula(t):
    'EXPRESION : RNULO'
    t[0] = Primitiva(tipos.NULO, None, t.lineno(1), find_column(input, t.slice[1]))

def p_expresion_variable(t):
    'EXPRESION : ID'
    t[0] = Variable(t[1], t.lineno(1), find_column(input, t.slice[1]))

def p_expresion_binaria(t):
    '''
    EXPRESION : EXPRESION MAS EXPRESION
              | EXPRESION MENOS EXPRESION
              | EXPRESION POR EXPRESION
              | EXPRESION DIVIDIDO EXPRESION
              | EXPRESION MODULO EXPRESION
              | EXPRESION POTENCIA EXPRESION
    '''
    if   t[2] == '+': t[0] = Aritmetica('+', t[1], t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '-': t[0] = Aritmetica('-', t[1], t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '*': t[0] = Aritmetica('*', t[1], t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '/': t[0] = Aritmetica('/', t[1], t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '%': t[0] = Aritmetica('%', t[1], t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '^': t[0] = Aritmetica('^', t[1], t[3], t.lineno(2), find_column(input, t.slice[2]))

def p_expresion_unaria(t):
    'EXPRESION : MENOS EXPRESION %prec UMENOS'
    t[0] = Aritmetica('-u', t[2], None, t.lineno(1), find_column(input, t.slice[1]))

def p_expresion_agrupacion(t):
    'EXPRESION : PARIZQ EXPRESION PARDER'
    t[0] = t[2]

def p_expresion_nativa(t):
    '''
    EXPRESION : UPPER PARIZQ EXPRESION PARDER
              | LOWER PARIZQ EXPRESION PARDER
              | SENO PARIZQ EXPRESION PARDER
              | COSENO PARIZQ EXPRESION PARDER
              | TANGENTE PARIZQ EXPRESION PARDER
              | RAIZ PARIZQ EXPRESION PARDER
              | LOG10 PARIZQ EXPRESION PARDER
              | LOG PARIZQ EXPRESION COMA EXPRESION PARDER
    '''
    if   t[1] == 'uppercase': t[0] = Nativa("upper", t[3], None, t.lineno(2), find_column(input, t.slice[2]))
    elif t[1] == 'lowercase': t[0] = Nativa("lower", t[3], None, t.lineno(2), find_column(input, t.slice[2]))
    elif t[1] == 'sin': t[0] = Nativa("seno", t[3], None, t.lineno(2), find_column(input, t.slice[2]))
    elif t[1] == 'cos': t[0] = Nativa("coseno", t[3], None, t.lineno(2), find_column(input, t.slice[2]))
    elif t[1] == 'tan': t[0] = Nativa("tangente", t[3], None, t.lineno(2), find_column(input, t.slice[2]))
    elif t[1] == 'sqrt': t[0] = Nativa("raiz", t[3], None, t.lineno(2), find_column(input, t.slice[2]))
    elif t[1] == 'log10': t[0] = Nativa("log10", t[3], None, t.lineno(2), find_column(input, t.slice[2]))
    elif t[1] == 'log': t[0] = Nativa("log", t[3], t[5], t.lineno(2), find_column(input, t.slice[2]))

def p_funciones_nativas(t):
    '''
    EXPRESION : FLOAT PARIZQ EXPRESION PARDER
              | STR PARIZQ EXPRESION PARDER
              | TYPEOF PARIZQ EXPRESION PARDER
              | PARSE PARIZQ tipo COMA EXPRESION PARDER
              | TRUNC PARIZQ tipo COMA EXPRESION PARDER
              | TRUNC PARIZQ EXPRESION PARDER
              | LENGTH PARIZQ EXPRESION PARDER
              | POP NOT PARIZQ EXPRESION PARDER
    '''
    if   t[1] == 'float'  : t[0] = FuncionNativa('float', t[3], None,  t.lineno(1), find_column(input, t.slice[1]))
    elif t[1] == 'string' : t[0] = FuncionNativa('string', t[3], None,  t.lineno(1), find_column(input, t.slice[1]))
    elif t[1] == 'typeof' : t[0] = FuncionNativa('typeof', t[3], None,  t.lineno(1), find_column(input, t.slice[1]))
    elif t[1] == 'parse'  : t[0] = FuncionNativa('parse', t[5], t[3],  t.lineno(1), find_column(input, t.slice[1]))
    elif t[1] == 'length' : t[0] = FuncionNativa('length', t[3], None,  t.lineno(1), find_column(input, t.slice[1]))
    elif t[1] == 'pop'    : t[0] = FuncionNativa('pop', t[4], None,  t.lineno(1), find_column(input, t.slice[1]))
    elif t[1] == 'trunc' :  
        if t[4] == ',' : 
            t[0] = FuncionNativa('trunc', t[5], t[3],  t.lineno(1), find_column(input, t.slice[1]))
        else:
            t[0] = FuncionNativa('trunc', t[3], None,  t.lineno(1), find_column(input, t.slice[1]))

def p_funcion_nativa_push(t):
    'INSTRUCCION_PUSH : PUSH NOT PARIZQ EXPRESION COMA EXPRESION PARDER PTCOMA' 
    t[0] = Push(t[4], t[6], t.lineno(1), find_column(input, t.slice[1]))
    
def p_expresion_relacional(t):
    '''
    EXPRESION : EXPRESION IGUALACION EXPRESION
              | EXPRESION DIFERENCIACION EXPRESION
              | EXPRESION MENORQUE EXPRESION
              | EXPRESION MENORIGUAL EXPRESION
              | EXPRESION MAYORQUE EXPRESION
              | EXPRESION MAYORIGUAL EXPRESION
    '''
    if   t[2] == '==': t[0] = Relacional('==', t[1], t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '!=': t[0] = Relacional('!=', t[1], t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '<': t[0] = Relacional('<', t[1], t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '<=': t[0] = Relacional('<=', t[1], t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '>': t[0] = Relacional('>', t[1], t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '>=': t[0] = Relacional('>=', t[1], t[3], t.lineno(2), find_column(input, t.slice[2]))

def p_expresion_logica(t):
    '''
    EXPRESION : EXPRESION OR EXPRESION
              | EXPRESION AND EXPRESION
              | NOT EXPRESION
    '''
    if   t[2] == '||': t[0] = Logica('||', t[1], t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '&&': t[0] = Logica('&&', t[1], t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[1] == '!': t[0] = Logica('!', t[2], None, t.lineno(1), find_column(input, t.slice[1]))
 
def p_expresion_vector(t):
    'EXPRESION : CORIZQ LISTAVECTOR CORDER'
    t[0] = Primitiva(tipos.VECTOR, t[2], t.lineno(1), find_column(input, t.slice[1]))
    
def p_lista_vector1(t):
    'LISTAVECTOR : LISTAVECTOR COMA EXPRESION'
    t[1].append(t[3])
    t[0] = t[1]

def p_lista_vector2(t):
    'LISTAVECTOR : EXPRESION'
    t[0] = []
    t[0].append(t[1])

def p_acceso_vector_rango(t):
    'EXPRESION : ID CORIZQ EXPRESION DOSPUNTO EXPRESION CORDER'
    t[0] = AccesoVector('rango', t[1], None, t[3], t[5], t.lineno(2), find_column(input, t.slice[2]))
    
def p_acceso_vector_pos(t):
    'EXPRESION : ID LISTAPOS'
    t[0] = AccesoVector('pos', t[1], t[2], None, None, 0, 0)
    
def p_lista_pos1(t):
    'LISTAPOS : LISTAPOS CORIZQ EXPRESION CORDER'
    t[1].append(t[3])
    t[0] = t[1]
    
def p_lista_pos2(t):
    'LISTAPOS : CORIZQ EXPRESION CORDER'
    t[0] = []
    t[0].append(t[2])

def p_expresion_acceso_struct(t):
    'EXPRESION : ID PUNTO LISTAID'
    t[0] = AccesoAtributo(t[1], t[3], t.lineno(1), find_column(input, t.slice[1]))

def p_lista_id1(t):
    'LISTAID : LISTAID PUNTO ID'
    t[1].append(t[3])
    t[0] = t[1]

def p_lista_id2(t):
    'LISTAID : ID'
    t[0] = []
    t[0].append(t[1])

def p_tipo(t):
    '''
    tipo : RINT
         | RFLOAT
         | RBOOL
         | RCHAR
         | RSTRING
    '''
    if t[1] == 'Int64':     t[0] = tipos.ENTERO
    elif t[1] == 'Float64': t[0] = tipos.DECIMAL
    elif t[1] == 'Bool':    t[0] = tipos.BOOLEAN
    elif t[1] == 'Char':    t[0] = tipos.CARACTER
    elif t[1] == 'String':  t[0] = tipos.CADENA
    elif t[1] == 'nothing': t[0] = tipos.NULO
 
import ply.yacc as yacc
parser = yacc.yacc()

def getErrores():
    return errores

from tablaSimbolos.Entorno import Entorno

def parse(inputs):
    global errores
    global lexer 
    global input 
    errores = []
    lexer = lex.lex(reflags=re.IGNORECASE)
    input = inputs
    ast = Arbol(parser.parse(input))
    tabla = Entorno(None)
    #tabla = tablaSimbolos(None)
    #ast.addTabla(tabla)
    #ast.setGlobal(tabla)
    #print(str(ast.getInstrucciones()))

    
    for i in ast.getInstruccion():
        if i == '':
            ast.updateConsola(str(i) + "\n")
            continue
        tmp = i.interpretar(ast, tabla)
        
        if isinstance(tmp, Excepciones):
            print(str(tmp.show()))
            
    return ast
    #print(str(ast.getConsola()))