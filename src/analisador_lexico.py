#Import nas bibliotecas
import sys
import string

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

#Lê o arquivo de entrada e fecha
texto = f.read()
f.close()

#Tabela de símbolos reservados
tabela_simb_reservados = {
    'program' : 'simb_program',
    'var' : 'simb_var',
    'integer' : 'simb_tipo',
    'real' : 'simb_tipo',
    'begin' : 'simb_begin',
    'while' : 'simb_while',
    'do' : 'simb_do',
    'end' : 'simb_end',
    'if' : 'simb_if',
    'else' : 'simb_else',
    'write' : 'simb_write',
    'read' : 'simb_read',
    'for' : 'simb_for',
    'procedure' : 'simb_procedure',
    'to' : 'simb_to'
}

#Função de saída do estado q2 com retroceder
#Verifica se o id é um símbolo reservado
def funcq2(cadeia, index):
    if(cadeia in tabela_simb_reservados):
        return cadeia + ', ' + tabela_simb_reservados[cadeia] + '\n', index-1
    else:
        return cadeia + ', id\n', index-1

#Função de saída do estado q4
def funcq4(cadeia, index):
    return ':=, simb_atrib\n', index

#Função de saída do estado q5 com retroceder
def funcq5(cadeia, index):
    return ':, simb_dp\n', index-1

#Função de saída do estado q7
def funcq7(cadeia, index):
    return '<=, simb_menor_igual\n', index

#Função de saída do estado q8
def funcq8(cadeia, index):
    return '<>, simb_dif\n', index

#Função de saída do estado q9 com retroceder
def funcq9(cadeia, index):
    return '<, simb_menor\n', index-1

#Função de saída do estado q10
def funcq10(cadeia, index):
    return '=, simb_igual\n', index

#Função de saída do estado q12
def funcq12(cadeia, index):
    return '>=, simb_maior_igual\n', index

#Função de saída do estado q13 com retroceder
def funcq13(cadeia, index):
    return '>, simb_maior\n', index-1

#Função de saída do estado q14
def funcq14(cadeia, index):
    return ';, simb_pv\n', index

#Função de saída do estado q16 com retroceder
def funcq16(cadeia, index):
    return cadeia + ', num_int\n', index-1

#Função de saída do estado q19 com retroceder
def funcq19(cadeia, index):
    return cadeia + ', num_real\n', index-1

#Função de saída do estado q21
def funcq21(cadeia, index):
    return cadeia + ', comentario\n', index

#Função de saída do estado q22
def funcq22(cadeia, index):
    return '(, simb_apar\n', index

#Função de saída do estado q23
def funcq23(cadeia, index):
    return '), simb_fpar\n', index

#Função de saída do estado q24
def funcq24(cadeia, index):
    return '+, simb_mais\n', index

#Função de saída do estado q25
def funcq25(cadeia, index):
    return '-, simb_menos\n', index

#Função de saída do estado q26
def funcq26(cadeia, index):
    return '., simb_p\n', index

#Função de saída do estado q27
def funcq27(cadeia, index):
    return '*, simb_mult\n', index

#Função de saída do estado q28
def funcq28(cadeia, index):
    return '/, simb_div\n', index

#Função de saída do estado q29
def funcq29(cadeia, index):
    return cadeia + ', erro("caractere nao permitido")\n', index

#Função de saída do estado q30
def funcq30(cadeia, index):
    return cadeia + ', erro("numero real mal formado")\n', index

#Função de saída do estado q32
def funcq32(cadeia, index):
    return ',, simb_virg\n', index

#Tabela de estados finais
estados_finais = {
    'q2' : funcq2,
    'q4' : funcq4,
    'q5' : funcq5,
    'q7' : funcq7,
    'q8' : funcq8,
    'q9' : funcq9,
    'q10' : funcq10,
    'q12' : funcq12,
    'q13' : funcq13,
    'q14' : funcq14,
    'q16' : funcq16,
    'q19' : funcq19,
    'q21' : funcq21,
    'q22' : funcq22,
    'q23' : funcq23,
    'q24' : funcq24,
    'q25' : funcq25,
    'q26' : funcq26,
    'q27' : funcq27,
    'q28' : funcq28,
    'q29' : funcq29,
    'q30' : funcq30,
    'q32' : funcq32
    }

#Tabela de transições do autômato
automato = {
    'q0' : {' ' : 'q0',
            '\t' : 'q0',
            '\n' : 'q0',
            ':' : 'q3',
            '<' : 'q6',
            '=' : 'q10',
            '>' : 'q11',
            '{' : 'q20',
            ';' : 'q14',
            '(' : 'q22',
            ')' : 'q23',
            '+' : 'q24',
            '-' : 'q25',
            '*' : 'q27',
            '/' : 'q28',
            '.' : 'q26',
            ',' : 'q32'
            },
    'q1' : {},
    'q3' : {'=' : 'q4'},
    'q6' : {'=' : 'q7'},
    'q6' : {'>' : 'q8'},
    'q11' : {'=' : 'q12'}, 
    'q20' : {'}' : 'q0'},
    'q15' : {'.' : 'q17'},
    'q17' : {},
    'q18' : {}
}
#Define as transições com letras 
for letter in string.ascii_letters:
    automato['q0'][letter] = 'q1'
    automato['q1'][letter] = 'q1'

#Define as transições com dígitos
for digit in string.digits:
    automato['q0'][digit] = 'q15'
    automato['q1'][digit] = 'q1'
    automato['q15'][digit] = 'q15'
    automato['q17'][digit] = 'q18'
    automato['q18'][digit] = 'q18'

#Tabela que define transições para outros caracteres
tabela_outros = {
    'q0' : 'q29',
    'q1' : 'q2',
    'q3' : 'q5',
    'q6' : 'q9',
    'q11' : 'q13',
    'q15' : 'q16',
    'q17' : 'q30',
    'q18' : 'q19',
    'q20' : 'q20'
}

#Lista de estados de erro
estados_erro = ['q29', 'q30']

#Estado inicial do autômato
estado_inicial = 'q0'

#Estado referente à leitura de comentário
estado_comentario = 'q20'

#Cabeça de leitura que irá percorrer o texto
index = 0

#Saída geral do analisador léxico
output = ''

#Cadeia formada por cada símbolo identificado
cadeia = ''

#Estado atual do autômato
estado = ''

#Teste de verificação para erro de leitura fora do vetor
#Indica que o texto acabou antes de uma cadeia ser reconhecida
try:
    #Enquanto o texto não finaliza
    while(True):
        #Inicia a leitura de uma cadeia
        #Autômato é setado em q0
        cadeia = ''
        estado = estado_inicial
        #Enquanto a cadeia não é reconhecida
        while(True):
            #Lê um item da cadeia
            c = texto[index]
            #Avança a cabeça de leitura
            index += 1
            #Se o caracter lido não é definido para o estado atual:
            if(c not in automato[estado].keys()):
                #Reconhece os outros caracteres (não definidos) e muda o estado
                estado = tabela_outros[estado]
                #Se o estado atual é um estado final:
                if(estado in estados_finais.keys()):
                    #Se o estado final é um estado de erro:
                    if(estado in estados_erro):   
                        #Adiciona o caractere lido à cadeia
                        cadeia += c
                    #Insere a cadeia lida no texto de saída e atualiza a cabeça de leitura
                    func_output, index = estados_finais[estado](cadeia, index)
                    output += func_output
                    break
            #Se o autômato possui transição definida para o caractere:
            else:
                #Realiza a transição de estado
                estado = automato[estado][c]

                #Se continua no estado inicial ou no estado de comentário, leu um caractere ou cadeia inútil
                if(estado != estado_inicial and estado != estado_comentario):
                    #Adiciona o caractere lido à cadeia
                    cadeia += c
                
                #Se o estado atual é um estaado final:
                if(estado in estados_finais.keys()):
                    #Insere a cadeia lida no texto de saída e atualiza a cabeça de leitura
                    func_output, index = estados_finais[estado](cadeia, index)
                    output += func_output
                    break
#Tratamento do erro EOF (fim inesperado do arquivo)
except IndexError:
    #Se terminou em um estado de comentário:
    if(estado == estado_comentario):
        #Adiciona a mensagem de erro para comentário não finalizado
        output += '{, erro("comentario nao finalizado")\n'
    #Se terminou durante uma iteração não finalizada do autômato
    elif(estado != estado_inicial):
        #Finaliza a transição e escreve a cadeia lida no texto de saída 
        func_output, index = estados_finais[tabela_outros[estado]](cadeia, index)
        output += func_output

#Abre o arquivo de saída
output_file = open("output.txt", 'w')
#Escreve o texto de saída no arquivo de saída
output_file.write(output)
#Fecha o arquivo de saída
output_file.close()

