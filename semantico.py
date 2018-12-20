def semantico(token, args, erro):
    Avariaveis(token, args,erro)
def divisao(token, args, lista,erro):
    linha = []
    i=0
    if args.lse:
        print("Verificando Divisão por Zero.")
    while (i < len(token)):
        if 'recebe' in token[i][0]:
            j=i+1
            variavel = token[i-1][1]
            try:
                while not 'fim_linha' in token[j][0]:
                    if (str(token[j][1][0])).isdigit():
                        linha.append(str(token[j][1][0]))
                    else:
                        linha.append(token[j][1])
                    j+=1
            except IndexError:
                break
            if verificando(variavel, linha, lista, erro):
                erro.append(f'linha:{token[i][2]}')
            linha.clear()
        i+=1

def verificando(variavel, linha, lista,erro):
    i=0
    antigo=''.join(linha)
    while i<len(linha):
        if linha[i].isidentifier:
            if linha[i] in lista:
                linha[i]=lista[linha[i]]
            else:
                pass
        i+=1
    try:
        expre=''.join(linha)
        eval(expre)
    except ZeroDivisionError:
        erro.append('########################################################')
        erro.append('Erro semantico:')
        erro.append(f'Divisão por Zero {antigo}')
        return 1
    lista[variavel]=str(eval(''.join(linha)))
    return 0

def trocandoValores(lista,a,key):
    import re
    for exp in lista.keys():
        if exp in a:
            a=re.sub(r''+exp, (''.join(lista[exp])),''.join(a))
    lista[key] = ''.join(a)

def Avariaveis(token, args,erro):
    variaveis = {}
    if args.lse:
        print ('#' * 80)
        print('Carregando Tabela de Variveis.')
        print("Verificando Variaveis Duplicadas.")
    for var in token:
        if 'id' in var and var[2] == 2:
            if var[1] not in variaveis:
                variaveis[var[1]] = '0'
            else:
                erro.append('########################################################')
                erro.append('Erro semantico:')
                erro.append(f'\'{var[1]}\' declaração duplicada: ')

    if args.lse:
        print("Variaveis declaradas: ")
        for var in variaveis.items():
            print(var[0])
        print("Verificando Variaveis não declaradas.")

    for code in token:
        if 'id' in code:
            if not (code[1] in variaveis):
                erro.append('########################################################')
                erro.append('Erro semantico:')
                erro.append(f'Variavel \'{code[1]}\' não declarado: linha{code[2]} : coluna{code[3]}')
    divisao(token, args, variaveis, erro)