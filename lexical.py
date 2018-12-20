import collections
import re
def tokenize(code,args,erro):
    token = collections.namedtuple('Token', ['tipo', 'lexema', 'linha', 'coluna'])
    token_especificacao = [
        ('inicio'       ,r'\{'), #inicio {
        ('fim'          ,r'\}'), # fim }
        ('a_parentese'  ,r'\('), #parentese de abertura
        ('f_parentese'  ,r'\)'), #parentese de fechamento
        ('leia'         ,r'leia'), #leia
        ('escreva'      ,r'escreva'), #escreva
        ('senao', r'senao'),  # senao
        ('se'           ,r'se'), #se
        ('enquanto'     ,r'enquanto'), #enquanto
        ('programa'     ,r'programa'), #programa
        ('fimprograma'  ,r'fimprograma'), #fimprograma
        ('inteiro'      ,r'inteiro'),     #variavel
        ('numero'       ,r'[+-]?[0-9]+'),  # inteiro
        ("fim_linha"    ,r';'), #fim de linha
        ("virgula"      ,r','), # virgula
        ('recebe'       ,r'='),           # recebe
        ('id'           ,r'[A-Za-z]([A-Za-z0-9_])*'),    # Id
        ('subtracao'    ,r'\-'),            #subtração
        ('soma'         ,r'\+'),           #soma
        ('multiplicacao',r'\*'),            #multiplicação
        ('divisao'      ,r'/'),             #divisão
        ('WS'           ,r' +'),           # espaço
        ('menor'        ,r'<'),             #operadore lógico menor
        ('maior'        ,r'>'),             #operador lógico maior
        ('frase'        ,r'".*?"'),         #frase
        ('ERRO'         ,r'.'),            # qualquer caracter não identificado
        ('Linha'        ,r'\n'),	    #fim de linha
    ]

    token_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_especificacao)
    linha = 1
    linha_inicia = 0
    for mo in re.finditer(token_regex, code):
        tipo = mo.lastgroup
        valor = mo.group(tipo)
        if (tipo == 'Linha'):
            linha_inicia = mo.end()
            linha += 1
        elif tipo == 'tab':
            pass
        elif tipo == 'ERRO':
            erro.append('########################################################')
            erro.append(f'Erro lexico')
            erro.append(f'{valor!r} não esperado na linha {linha} e coluna {coluna}')
            if valor == '"':
                erro.append(f'" de fechamento não encontrada')
            else:
                erro.append(f'caracter desconhecido')
            pass

        coluna = mo.start() - linha_inicia
        if (tipo != 'ERRO') and (tipo != 'Linha') and (tipo != 'WS'):
            yield token(tipo, valor, linha, coluna)
