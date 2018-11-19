def semantico(token, args):
    Avariaveis(token, args)
def divisao(token, args, lista):
    linha = []
    if args.lse:
        print("Verificando Divisão por Zero.")

def verificando(lista):
    for exp in lista.values():
        if 'î' not in exp:
            try:
                eval(''.join(exp))
            except ZeroDivisionError:
                from colorama import Style
                Color()
                print (f' Divisão por Zero {exp} '+ Style.RESET_ALL)
def trocandoValores(lista,a,key):
    import re
    for exp in lista.keys():
        if exp in a:
            a=re.sub(r''+exp, (''.join(lista[exp])),''.join(a))
    lista[key] = ''.join(a)

def Avariaveis(token, args):
    variaveis = {}
    if args.lse:
        print ('#' * 80)
        print('Carregando Tabela de Variveis.')
        print("Verificando Variaveis Duplicadas.")
    for var in token:
        if 'id' in var and var[2] == 2:
            if var[1] not in variaveis:
                variaveis[var[1]] = 'î'
            else:
                Color()
                print(f'\'{var[1]}\' declaração duplicada: ' + reset(var))

    if args.lse:
        print("Variaveis declaradas: ")
        for var in variaveis.items():
            print(var[0])
        print("Verificando Variaveis não declaradas.")

    for code in token:
        if 'id' in code:
            if not (code[1] in variaveis):
                Color();
                print(f'Variavel \'{code[1]}\' não declarado: ' + reset(code))
    divisao(token, args, variaveis)

def Color():
    from colorama import Fore, Back
    print(Fore.CYAN + 'Erro semantico:')


def reset(linha):
    from colorama import Style
    return f'linha{linha[2]} : coluna{linha[3]}' + Style.RESET_ALL
