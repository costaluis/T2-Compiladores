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

def error_func():
    raise RuntimeError('Erro')


erro_regex = 'erro\\(\\"(.*)\\"\\)'
def get_token():
    global linha
    global cont_linha
    global token
    
    fim = False
    token = analisador_lexico(linha)
    cadeia = token.split(', ')
    token = cadeia[1].replace('\n', '')
    var = re.match(erro_regex, cadeia[1])
    if(var):
        print('Erro léxico na linha {}: '.format(cont_linha), var.groups()[0])
    linha = linha.replace(cadeia[0],'', 1)
    linha = linha.strip()
    if(linha):
        if(linha[0]=='{' and linha[len(linha)-1]=='}'):
            linha=''
    if(not linha):
        linha = f.readline()
        cont_linha += 1
        if(not linha):
            fim = True

    return fim


def programa(S):
    if(token == 'simb_program'):
        get_token()
    else:
        print("Erro sintático na linha {}: 'program' esperado".format(cont_linha))
        error_func(S + 'id')
    if(token == 'id'):
        get_token()
    else:
        print("Erro sintático na linha {}: identificador esperado".format(cont_linha))
        error_func(S + 'simb_pv')
    if(token == 'simb_pv'):
        get_token()
    else:
        print("Erro sintático na linha {}: ';' esperado".format(cont_linha))
        error_func(S + P['corpo'])
    corpo('simb_p' + S)
    
    if(token == 'simb_p'):
        get_token()
    else:
        print("Erro sintático na linha {}: '.' esperado".format(cont_linha))
        error_func(S)
    

def corpo(S):
    dc('simb_begin' + S)
    if(token == 'simb_begin'):
        get_token()
    else:
        print("Erro sintático na linha {}: 'begin' esperado".format(cont_linha))
        error_func(S + P['comandos'])
    comandos('simb_end' + S)
    
    if(token == 'simb_end'):
        get_token()
    else:
        print("Erro sintático na linha {}: 'end' esperado".format(cont_linha))
        error_func(S)
    

def dc(S):
    dc_c(P['dc_v'] + S)
    dc_v(P['dc_p'] + S)
    dc_p(S)


def dc_c(S):
    if(token == 'simb_const'):
        get_token()
        if(token == 'id'):
            get_token()
        else:
            print("Erro sintático na linha {}: identificador esperado".format(cont_linha))
            error_func(S + 'simb_igual')
        if(token == 'simb_igual'):
            get_token()
        else:
            print("Erro sintático na linha {}: '=' esperado".format(cont_linha))
            error_func(S, P['numero'])
        numero('simb_pv' + S)
        
        if(token == 'simb_pv'):
            get_token()
        else:
            print("Erro sintático na linha {}: ';' esperado".format(cont_linha))
            error_func(S, P['dc_c'])
        dc_c(S)
        
    else:
        return

def dc_v(S):
    if(token == 'simb_var'):
        get_token()
    else:
        print("Erro sintático na linha {}: 'var' esperado".format(cont_linha))
        error_func(S + P['variaveis'])
    variaveis('simb_pv' + S)
    
    if(token == 'simb_dp'):
        get_token()
    else:
        print("Erro sintático na linha {}: ':' esperado".format(cont_linha))
        error_func(S + P['tipo_var'])
    tipo_var('simb_pv' + S)
    
    if(token == 'simb_pv'):
        get_token()
    else:
        print("Erro sintático na linha {}: ';' esperado".format(cont_linha))
        error_func(S + P['dc_v'])
    dc_v(S)


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
        error_func(S + P['mais_var'])
    mais_var(S)


def mais_var(S):
    if(token == 'simb_virg'):
        get_token()
    else:
        return
    variaveis(S)


def dc_p():
    if(token == 'simb_procedure'):
        get_token()
        if(token == 'id'):
            get_token()
            parametros()
        else:
            error_func()
        if(token == 'simb_pv'):
            corpo_p()
            dc_p()
            return
        else:
            error_func()
    else:
        return


def parametros():
    if(token == 'simb_apar'):
        get_token()
        lista_par()
        if(token == 'simb_fpar'):
            get_token()
            return
        else:
            error_func()
    else:
        return

def lista_par():
    variaveis()
    if(token == 'simb_dp'):
        get_token()
        tipo_var()
        mais_par()
        return
    else:
        error_func()

def mais_par():
    if(token == 'simb_pv'):
        get_token()
        lista_par()
        return
    else:
        return

def corpo_p():
    dc_loc()
    if(token == 'simb_begin'):
        get_token()
        comandos()
    else:
        error_func()
    if(token == 'simb_end'):
        get_token()
    else:
        error_func()
    if(token == 'simb_pv'):
        get_token()
        return
    else:
        error_func()
        
    

def dc_loc():
    dc_v()
    return

def lista_arg():
    if(token == 'simb_apar'):
        get_token()
        argumentos()
        if(token == 'simb_fpar'):
            get_token()
            return
        else:
            error_func()
    else:
        return

def argumentos():
    if(token == 'id'):
        get_token()
        mais_ident()
        return
    else:
        error_func()

def mais_ident():
    if(token == 'simb_pv'):
        get_token()
        argumentos()
        return
    else:
        return

def pfalsa():
    if(token == 'simb_else'):
        get_token()
        cmd()
        return
    else:
        return

def comandos():
    if(token in P['cmd']):
        cmd()
        if(token == 'simb_pv'):
            get_token()
            comandos()
            return
        else:
            error_func()
    else:
        return

def cmd():
    if(token == 'simb_read'):
        get_token()
        if(token == 'simb_apar'):
            get_token()
            variaveis()
        else:
            error_func()
        if(token == 'simb_fpar'):
            get_token()
            return
        else:
            error_func()
    elif(token == 'simb_write'):
        get_token()
        if(token == 'simb_apar'):
            get_token()
            variaveis()
        else:
            error_func()
        if(token == 'simb_fpar'):
            get_token()
            return
        else:
            error_func()

    elif(token == 'simb_while'):
        get_token()
        if(token == 'simb_apar'):
            get_token()
            condicao()
        else:
            error_func()
        if(token == 'simb_fpar'):
            get_token()
        else:
            error_func()
        if(token == 'simb_do'):
            get_token()
            cmd()
            return
        else:
            error_func()
        
    elif(token == 'simb_if'):
        get_token()
        condicao()
        if(token == 'simb_then'):
            get_token()
            cmd()
            pfalsa()
            return
        else:
            error_func()

    elif(token == 'id'):
        get_token()
        ident()
        return

    elif(token == 'simb_begin'):
        get_token()
        comandos()
        if(token == 'simb_end'):
            get_token()
            return
        else:
            error_func()

    elif(token == 'simb_for'):
        get_token()
        if(token == 'id'):
            get_token()
        else:
            error_func()
        if(token == 'simb_atrib'):
            get_token()
            expressao()
        else:
            error_func()
        if(token == 'simb_to'):
            get_token()
            expressao()
        else:
            error_func()
        if(token == 'simb_do'):
            get_token()
            cmd()
            return
        else:
            error_func()

    else:
        error_func()

def ident():
    if(token == 'simb_atrib'):
        get_token()
        expressao()
        return
    else:
        lista_arg()
        return


def condicao():
    expressao() 
    relacao()
    expressao()
    return

def relacao():
    if(token == 'simb_igual'):
        get_token()
        return
    elif(token == 'simb_dif'):
        get_token()
        return
    elif(token == 'simb_maior_igual'):
        get_token()
        return
    elif(token == 'simb_menor_igual'):
        get_token()
        return
    elif(token == 'simb_maior'):
        get_token()
        return
    elif(token == 'simb_menor'):
        get_token()
        return
    else:
        error_func()

def expressao():
    termo()
    outros_termos()
    return

def op_un():
    if(token == 'simb_mais'):
        get_token()
        return
    elif(token == 'simb_menos'):
        get_token()
        return
    else:
        return

def outros_termos():
    if(token in P['op_ad']):
        op_ad()
        termo()
        outros_termos()
    else:
        return

def op_ad():
    if(token == 'simb_mais'):
        get_token()
        return
    elif(token == 'simb_menos'):
        get_token()
        return
    else:
        error_func()

def termo():
    op_un()
    fator()
    mais_fatores()
    return

def mais_fatores():
    if(token in P['op_mul']):
        op_mul()
        fator()
        mais_fatores()
        return
    else:
        return

def op_mul():
    if(token == 'simb_mult'):
        get_token()
        return
    elif(token == 'simb_div'):
        get_token()
        return
    else:
        error_func()

def fator():
    if(token == 'id'):
        get_token()
        return
    elif(token == 'simb_apar'):
        get_token()
        expressao()
        if(token == 'simb_fpar'):
            get_token()
            return
        else:
            error_func()
    elif(token in P['numero']):
        numero()
        return
    else:
        error_func()

def numero():
    if(token == 'num_int'):
        get_token()
        return
    elif(token == 'num_real'):
        get_token()
        return
    else:
        error_func()

P = {
    'numero': ['num_int', 'num_real'],
    'cmd': ['simb_read', 'simb_write', 'simb_while', 'simb_if', 'id', 'simb_begin', 'simb_for'],
    'op_mul': ['simb_mult', 'simb_div'],
    'op_ad': ['simb_mais', 'simb_menos']
}   

get_token()
programa()
f.close()
