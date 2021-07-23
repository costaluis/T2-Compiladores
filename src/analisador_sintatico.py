from os import linesep
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


erro_regex = 'erro\\(\\"(.*)\\"\\)'
def get_token():
    global linha
    global cont_linha
    global token
    
    fim = False
    token = analisador_lexico(linha)
    cadeia = token.split(', ')
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

def programa():
    if(token == 'simb_program'):
        get_token()
        if(token == 'id'):
            get_token()
            if(token == 'simb_pv'):
                get_token()
                corpo()
                if(token == 'simb_p'):
                    return
                else:
                    print('Erro')
            else:
                print('Erro')
        else:
            print('Erro')
    else:
        print('Erro')


def corpo():
    dc()
    if(token == 'simb_begin'):
        get_token()
        comandos()
        if(token == 'simb_end'):
            get_token()
        else:
            print("Erro")
    else:
        print("Erro")


def dc():
    dc_c()
    dc_v()
    dc_p()
    return


def dc_c():
    if(token == 'simb_const'):
        get_token()
        if(token == 'id'):
            get_token()
            if(token == 'simb_igual'):
                get_token()
                numero()
                if(token == 'simb_pv'):
                    get_token()
                    dc_c()
                    return
                else:
                    print("Erro")
            else:
                print("Erro")
        else:
            print("Erro")
    else:
        return


def dc_v():
    if(token == 'simb_var'):
        get_token()
        variaveis()
        if(token == 'simb_dp'):
            get_token()
            tipo_var()
            if(token == 'simb_pv'):
                get_token()
                dc_v()
                return
            else:
                print("Erro")
        else:
            print("Erro")
    else:
        return


def tipo_var():
    if(token == 'simb_tipo'):
        return
    else:
        print("Erro")


def variaveis():
    if(token == 'id'):
        get_token()
        mais_var()
        return
    else:
        print("Erro")


def mais_var():
    if(token == 'simb_virg'):
        get_token()
        variaveis()
        return
    else:
        return


def dc_p():
    if(token == 'simb_procedure'):
        get_token()
        if(token == 'id'):
            get_token()
            parametros()
            if(token == 'simb_pv'):
                corpo_p()
                dc_p()
                return
            else:
                print("Erro")
        else:
            print("Erro")
    else:
        return


def parametros():
    if(token == 'simb_apar'):
        get_token()
        lista_par()
        if(token == 'simb_fpar'):
            return
        else:
            print("Erro")
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
        print("Erro")


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
        if(token == 'simb_end'):
            get_token()
            if(token == 'simb_pv'):
                get_token()
                return
            else:
                print("Erro")
        else:
            print("Erro")
    else:
        print("Erro")


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
            print("Erro")
    else:
        return


def argumentos():
    if(token == 'id'):
        get_token()
        mais_ident()
        return
    else:
        print("Erro")


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
            print("Erro")
    else:
        return





        

def __main__():
    get_token()
    programa()
    f.close()
