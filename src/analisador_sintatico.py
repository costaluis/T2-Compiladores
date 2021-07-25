from os import linesep
from sys import exec_prefix
from analisador_lexico import *
import re

#Verificação da entrada
if(len(sys.argv) > 2):
    print("Numero de argumentos invalido!")
    sys.exit(1)

#Verificação da abertura do arquivo
try:
    f = open(sys.argv[1], "r")
except:
    print("Nao foi possivel abrir o arquivo!")
    sys.exit(2)


token = ''
linha = f.readline()
cont_linha = 1

def error_func(S):
    while(token not in S):
        get_token()


erro_regex = 'erro\\(\\"(.*)\\"\\)'
def get_token():
    global linha
    global cont_linha
    global token
    
    fim = False
    while(True):
        cadeia = analisador_lexico(linha)
        if(cadeia != ''):
            break
        linha = f.readline()
        cont_linha += 1
        if(len(linha) == 0):
            return

    cadeia = cadeia.split(', ')

    token = cadeia[1].replace('\n', '')
    var = re.match(erro_regex, cadeia[1])
    if(var):
        print('Erro léxico na linha {}: '.format(cont_linha), var.groups()[0])
    linha = linha.replace(cadeia[0],'', 1)
    linha = linha.strip()
'''    if(linha):
        if(linha[0]=='{' and linha[len(linha)-1]=='}'):
            linha=''
    if(not linha):
        linha = f.readline()
        cont_linha += 1
        if(not linha):
            fim = True'''


def programa(S):
    if(token == 'simb_program'):
        get_token()
    else:
        print("Erro sintático na linha {}: 'program' esperado".format(cont_linha))
        error_func(['id'] + S)
    if(token == 'id'):
        get_token()
    else:
        print("Erro sintático na linha {}: identificador esperado".format(cont_linha))
        error_func(['simb_pv'] + S)
    if(token == 'simb_pv'):
        get_token()
    else:
        print("Erro sintático na linha {}: ';' esperado".format(cont_linha))
        error_func(P['corpo'] + ['simb_p'] + S)
    corpo(['simb_p'] + S)
    
    if(token == 'simb_p'):
        get_token()
    else:
        print("Erro sintático na linha {}: '.' esperado".format(cont_linha))
        error_func(S)
    

def corpo(S):
    dc(['simb_begin'] + S)
    if(token == 'simb_begin'):
        get_token()
    else:
        print("Erro sintático na linha {}: 'begin' esperado".format(cont_linha))
        error_func(P['comandos'] + ['simb_end'] + S)
    comandos(['simb_end'] + S)
    
    if(token == 'simb_end'):
        get_token()
    else:
        print("Erro sintático na linha {}: 'end' esperado".format(cont_linha))
        error_func(S)
    

def dc(S):
    dc_c(P['dc_v'] + P['dc_p'] + S)
    dc_v(P['dc_p'] + S)
    dc_p(S)


def dc_c(S):
    if(token == 'simb_const'):
        get_token()
        if(token == 'id'):
            get_token()
        else:
            print("Erro sintático na linha {}: identificador esperado".format(cont_linha))
            error_func(['simb_igual'] + S)
        if(token == 'simb_igual'):
            get_token()
        else:
            print("Erro sintático na linha {}: '=' esperado".format(cont_linha))
            error_func(P['numero'] + S)
        numero(['simb_pv'] + S)
        
        if(token == 'simb_pv'):
            get_token()
        else:
            print("Erro sintático na linha {}: ';' esperado".format(cont_linha))
            error_func(P['dc_c'] + S)
        dc_c(S)
        
    else:
        return

def dc_v(S):
    if(token == 'simb_var'):
        get_token()
        variaveis(['simb_dp'] + S)
        if(token == 'simb_dp'):
            get_token()
        else:
            print("Erro sintático na linha {}: ':' esperado".format(cont_linha))
            error_func(P['tipo_var'] + S)
        tipo_var(['simb_pv'] + S)
        
        if(token == 'simb_pv'):
            get_token()
        else:
            print("Erro sintático na linha {}: ';' esperado".format(cont_linha))
            error_func(P['dc_v'] + S)
        dc_v(S)
    else:
        return


def tipo_var(S):
    if(token == 'simb_tipo'):
        get_token()
    else:
        print("Erro sintático na linha {}: tipo da variável esperado".format(cont_linha))
        error_func(S)


def variaveis(S):
    if(token == 'id'):
        get_token()
    else:
        print("Erro sintático na linha {}: identificador esperado".format(cont_linha))
        error_func(P['mais_var'] + S)
    mais_var(S)


def mais_var(S):
    if(token == 'simb_virg'):
        get_token()
    else:
        return
    variaveis(S)


def dc_p(S):
    if(token == 'simb_procedure'):
        get_token()
        if(token == 'id'):
            get_token()
        else:
            print("Erro sintático na linha {}: identificador esperado".format(cont_linha))
            error_func(P['parametros'] + ['simb_pv'] + S)
        parametros(['simb_pv'] + S)
        
        if(token == 'simb_pv'):
            get_token()
        else:
            print("Erro sintático na linha {}: ';' esperado".format(cont_linha))
            error_func(P['corpo_p'] + P['dc_p'] + S)
        corpo_p(P['dc_p'] + S)
        dc_p(S)

    else:
        return


def parametros(S):
    if(token == 'simb_apar'):
        get_token()
        lista_par(['simb_fpar'] + S)
        if(token == 'simb_fpar'):
            get_token()
        else:
            print("Erro sintático na linha {}: ')' esperado".format(cont_linha))
            error_func(S)
        
    else:
        return

def lista_par(S):
    variaveis(['simb_dp'] + S)
    if(token == 'simb_dp'):
        get_token()
    else:
        print("Erro sintático na linha {}: ':' esperado".format(cont_linha))
        error_func(P['tipo_var'] + S)
    tipo_var(P['mais_par'] + S)
    mais_par(S)


def mais_par(S):
    if(token == 'simb_pv'):
        get_token()
        lista_par(S)
    else:
        return


def corpo_p(S):
    dc_loc(['simb_begin'] + S)
    if(token == 'simb_begin'):
        get_token()
    else:
        print("Erro sintático na linha {}: 'begin' esperado".format(cont_linha))
        error_func(P['comandos'] + ['simb_end'] + S)
    comandos(['simb_end'] + S)
    
    if(token == 'simb_end'):
        get_token()
    else:
        print("Erro sintático na linha {}: 'end' esperado".format(cont_linha))
        error_func(['simb_pv'] + S)
    if(token == 'simb_pv'):
        get_token()
    else:
        print("Erro sintático na linha {}: ';' esperado".format(cont_linha))
        error_func(S)
        

def dc_loc(S):
    dc_v(S)


def lista_arg(S):
    if(token == 'simb_apar'):
        get_token()
        argumentos(['simb_fpar'] + S)
        if(token == 'simb_fpar'):
            get_token()
        else:
            print("Erro sintático na linha {}: ')' esperado".format(cont_linha))
            error_func(S)
    else:
        return

def argumentos(S):
    if(token == 'id'):
        get_token()
    else:
        print("Erro sintático na linha {}: identificador esperado".format(cont_linha))
        error_func(P['mais_ident'] + S)
    mais_ident(S)


def mais_ident(S):
    if(token == 'simb_pv'):
        get_token()
        argumentos(S)
    else:
        return

def pfalsa(S):
    if(token == 'simb_else'):
        get_token()
        cmd(S)
    else:
        return

def comandos(S):
    if(token in P['cmd']):
        cmd(['simb_pv'] + S)
        if(token == 'simb_pv'):
            get_token()
        else:
            print("Erro sintático na linha {}: ';' esperado".format(cont_linha))
            error_func(P['comandos'] + S)
        comandos(S)
    else:
        return

def cmd(S):
    if(token == 'simb_read'):
        get_token()
        if(token == 'simb_apar'):
            get_token()
        else:
            print("Erro sintático na linha {}: '(' esperado".format(cont_linha))
            error_func(P['variaveis'] + S)
        variaveis(['simb_fpar'] + S)

        if(token == 'simb_fpar'):
            get_token()
        else:
            print("Erro sintático na linha {}: ')' esperado".format(cont_linha))
            error_func(S)

    elif(token == 'simb_write'):
        get_token()
        if(token == 'simb_apar'):
            get_token()
        else:
            print("Erro sintático na linha {}: '(' esperado".format(cont_linha))
            error_func(P['variaveis'] + S)
        variaveis(['simb_fpar'] + S)
        
        if(token == 'simb_fpar'):
            get_token()
        else:
            print("Erro sintático na linha {}: ')' esperado".format(cont_linha))
            error_func(S)

    elif(token == 'simb_while'):
        get_token()
        if(token == 'simb_apar'):
            get_token()
        else:
            print("Erro sintático na linha {}: '(' esperado".format(cont_linha))
            error_func(P['condicao'] + S)
        condicao(['simb_fpar'] + S)

        if(token == 'simb_fpar'):
            get_token()
        else:
            print("Erro sintático na linha {}: ')' esperado".format(cont_linha))
            error_func(['simb_do'] + S)
        if(token == 'simb_do'):
            get_token()
        else:
            print("Erro sintático na linha {}: 'do' esperado".format(cont_linha))
            error_func(P['cmd'] + S)
        cmd(S)
        
    elif(token == 'simb_if'):
        get_token()
        condicao(['simb_then'] + S)
        if(token == 'simb_then'):
            get_token()
        else:
            print("Erro sintático na linha {}: 'then' esperado".format(cont_linha))
            error_func(P['cmd'] + S)
        cmd(P['pfalsa'] + S)
        pfalsa(S)

    elif(token == 'id'):
        get_token()
        ident(S)

    elif(token == 'simb_begin'):
        get_token()
        comandos(['simb_end'] + S)
        if(token == 'simb_end'):
            get_token()
        else:
            print("Erro sintático na linha {}: 'end' esperado".format(cont_linha))
            error_func(S)

    elif(token == 'simb_for'):
        get_token()
        if(token == 'id'):
            get_token()
        else:
            print("Erro sintático na linha {}: identificador esperado".format(cont_linha))
            error_func(['simb_atrib'] + S)
        if(token == 'simb_atrib'):
            get_token()
        else:
            print("Erro sintático na linha {}: ':=' esperado".format(cont_linha))
            error_func(P['expressao'] + S)
        expressao(['simb_to'] + S)
        
        if(token == 'simb_to'):
            get_token()
        else:
            print("Erro sintático na linha {}: 'to' esperado".format(cont_linha))
            error_func(P['expressao'] + S)
        expressao(['simb_do'] + S)

        if(token == 'simb_do'):
            get_token()
        else:
            print("Erro sintático na linha {}: 'do' esperado".format(cont_linha))
            error_func(P['cmd'] + S)
        cmd(S)

    else:
        print("Erro sintático na linha {}: comando esperado".format(cont_linha))
        error_func(S)

def ident(S):
    if(token == 'simb_atrib'):
        get_token()
        expressao(S)
    else:
        lista_arg(S)


def condicao(S):
    expressao(P['relacao'] + S) 
    relacao(P['expressao'] + S)
    expressao(S)

def relacao(S):
    if(token == 'simb_igual'):
        get_token()
    elif(token == 'simb_dif'):
        get_token()
    elif(token == 'simb_maior_igual'):
        get_token()
    elif(token == 'simb_menor_igual'):
        get_token()
    elif(token == 'simb_maior'):
        get_token()
    elif(token == 'simb_menor'):
        get_token()
    else:
        print("Erro sintático na linha {}: comparação esperada".format(cont_linha))
        error_func(S)

def expressao(S):
    termo(P['outros_termos'] + S)
    outros_termos(S)
    return

def op_un(S):
    if(token == 'simb_mais'):
        get_token()
    elif(token == 'simb_menos'):
        get_token()
    else:
        return

def outros_termos(S):
    if(token in P['op_ad']):
        op_ad(P['termo'] + S)
        termo(P['outros_termos'] + S)
        outros_termos(S)
    else:
        return

def op_ad(S):
    if(token == 'simb_mais'):
        get_token()
    elif(token == 'simb_menos'):
        get_token()
    else:
        print("Erro sintático na linha {}: operador '+' ou '-' esperado".format(cont_linha))
        error_func(S)

def termo(S):
    op_un(P['fator'] + S)
    fator(P['mais_fatores'] + S)
    mais_fatores(S)

def mais_fatores(S):
    if(token in P['op_mul']):
        op_mul(P['fator'] + S)
        fator(P['mais_fatores'] + S)
        mais_fatores(S)
    else:
        return


def op_mul(S):
    if(token == 'simb_mult'):
        get_token()
    elif(token == 'simb_div'):
        get_token()
    else:
        print("Erro sintático na linha {}: operador '*' ou '/' esperado".format(cont_linha))
        error_func(S)


def fator(S):
    if(token == 'id'):
        get_token()
    elif(token == 'simb_apar'):
        get_token()
        expressao(['simb_fpar'] + S)
        if(token == 'simb_fpar'):
            get_token()
        else:
            error_func(S)
    elif(token in P['numero']):
        numero(S)
    else:
        print("Erro sintático na linha {}: fator esperado".format(cont_linha))
        error_func(S)

def numero(S):
    if(token == 'num_int'):
        get_token()
    elif(token == 'num_real'):
        get_token()
    else:
        print("Erro sintático na linha {}: valor numérico esperado".format(cont_linha))
        error_func(S)

P = {
    'programa': ['simb_program'],
    'corpo': ['simb_const', 'simb_var', 'simb_procedure'],
    'dc': ['simb_const', 'simb_var', 'simb_procedure'],
    'dc_c': ['simb_const'],
    'dc_v': ['simb_var'],
    'tipo_var': ['num_int', 'num_real'],
    'variaveis': ['id'],
    'mais_var': ['simb_virg'],
    'dc_p': ['simb_procedure'],
    'parametros': ['simb_apar'],
    'lista_par': ['id'],
    'mais_par': ['simb_pv'],
    'corpo_p': ['simb_var'],
    'dc_loc': ['simb_var'],
    'lista_arg': ['simb_apar'],
    'argumentos': ['id'],
    'mais_ident': ['simb_pv'],
    'pfalsa': ['simb_else'],
    'comandos': ['simb_read', 'simb_write', 'simb_while', 'simb_if', 'id', 'simb_begin', 'simb_for'],
    'cmd': ['simb_read', 'simb_write', 'simb_while', 'simb_if', 'id', 'simb_begin', 'simb_for'],
    'ident': ['simb_atrib', 'simb_apar'],
    'relacao': ['simb_igual', 'simb_dif', 'simb_maior_igual', 'simb_menor_igual', 'simb_maior', 'simb_menor'],
    'expressao': ['simb_mais', 'simb_menos', 'id', 'simb_apar', 'num_int', 'num_real'],
    'op_un': ['simb_mais', 'simb_menos'],
    'outros_termos': ['simb_mais', 'simb_menos'],
    'op_ad': ['simb_mais', 'simb_menos'],
    'termo': ['simb_mais', 'simb_menos', 'simb_apar', 'id', 'num_int', 'num_real'],
    'mais_fatores': ['simb_mult', 'simb_div'],
    'op_mul': ['simb_mult', 'simb_div'],
    'fator': ['id', 'num_int', 'num_real', 'simb_fpar'],
    'numero': ['num_int', 'num_real']
}   

get_token()
programa([])
f.close()
