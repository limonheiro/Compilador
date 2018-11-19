def analisadorsintatico(dict1, dict2, programa, args):
    pilha = ["<INICIO>"]#inicializa a pilha com o Não terminal inicial
    if args.ls : #Se verdadeiro mostra a mensagem a seguir
        print ('#'*80)
        print("Foi adcionado a pilha: " + pilha[-1])
        #dicionario para cada token e sua representação no código
    token={"a_parentese":"(" ,"f_parentese":")", "virgula":",","inicio":"{", "fim":"}",	"fim_linha":";","id":"id","numero":"numero", "frase":"frase", 	"programa":"programa" ,"fimprograma":"fimprograma", "inteiro":"declaração", "leia":"leia" ,"escreva":"escreva", "se":"se",
       "senao":"senao","enquanto":"enquanto", "menor":"<",	"maior":">", "recebe":"=", "soma":"+" ,"subtracao":"-","multiplicacao":"*", "divisao": '//'}
    i=0#inicializa a posição
    while i <= (len(programa)-1):
        if pilha[-1] == programa[i][0]:#verifica se o topo da pilha é igual ao token na fila do programa
            if args.ls:#Se verdadeiro mostra a mensagem a seguir
                print("Foi despilhado: " + pilha[-1])
            pilha.pop()
            i += 1
        else:
            if (pilha[-1], programa[i][0]) in dict1:#verifica se existe <Não terminal> junto com inicio da fila forma uma chave
                if dict2[dict1[pilha[-1], programa[i][0]][0]]:#Faz mesma verificação da existencia de chave e imprime na tela se args.ls for verdadeiro para o usuario
                    if args.ls:
                        print("Foi despilhado: " + pilha[-1])
                        print("Foi empilhado: ")
                        a = dict2[dict1[pilha[-1], programa[i][0]][0]]
                        a.reverse()
                        print(f"Expressão {dict1[pilha[-1], programa[i][0]][0]}:", a)#Retorna o numero da expressão que foi adcionado na pilha e expressão na ordem que foi empilhada
                        a.reverse()

                exp = dict2[dict1[pilha[-1], programa[i][0]][0]]#recebe a expressão que vai ser empilhada
                if not exp:
                    if args.ls: #Se verdadeiro mostra a mensagem a seguir
                        print("Foi tirado da pilha: "+pilha[-1])
                    pilha.pop() #desempilha o topo da pilha
                else:
                    pilha.pop()#desempilha o topo da pilha
                    exp.reverse()#inverte a expresão antes de colocar na pilha
                    pilha.extend(exp)#empilha na pilha
                    exp.reverse()#inverte novamente
            else:#Caso não encontre a chave
                a = []
                if '<' in pilha[-1]:
                    dict = []
                    '''
                    cria uma extenção do dicionario, primeirente apresenta todos os itens e os filtra se o topo da pilha
                    estiver nas chaves do dicionario 1 e os adciona
                    '''
                    dict.extend([ele[1] for ele in dict1 if pilha[-1] in ele])#
                    #Adciona apenas os elementos filtrados
                    a.extend([token[ele] for ele in dict if ele])
                else:
                    # se top não for um não terminal ele apenas adciona o topo da pilha
                    a.extend(token[pilha[-1]])
                from colorama import Fore, Style
                t = Fore.CYAN +"Erro Sintatico ".upper()#imprimi bunitinho
                print(t)
                print(f"\'{programa[i][1]}\' inesperado linha {programa[i][2]}, coluna {programa[i][3]}")#
                space = " "*int(programa[i][3])
                texto = []
                with open(args.filename, 'r') as f:
                    for i in range(programa[i][2]):
                        texto = f.readline()
                print(texto+space+'^')
                print(f"Era esperado: {' '.join(a)}"+Style.RESET_ALL)
                args.ls = False
                break
    if args.ls:#Se for True imprime a mensagem
        args.ls=True
        print("Sintatico terminado com Sucesso")