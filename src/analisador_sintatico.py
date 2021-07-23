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
    else:
        print('Erro')
        return False
    if(token == 'id'):
        get_token()
        



def __main__():
    get_token()
    programa()
    f.close()
