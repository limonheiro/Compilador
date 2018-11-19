def opction(args):
    token = []
    if args.tudo:
        args.lt=True
        args.ls=True
        args.lse=True
        args.lgc=True
    if args.lt:
        vlt(args.filename,token,args)
    else:
        lt(args.filename,token,args)
    ls(token,args)
    lse(token,args)
    lgc(token,args)

def vlt(filename,token,args):
    from lexical import tokenize
    print ('#' * 80)
    file = open(filename, "r")
    arquivo = file.read()
    file.close()
    print('{:15}'.format('Token'), '{:29}'.format('Lexema'), '{:10}'.format('Linha'), '{:10}'.format('Coluna'))
    i = 0
    for tok in tokenize(arquivo,args):
        token.append(tok)
        print('{:15}'.format(token[i][0]), '{:20.11}'.format(token[i][1]), '{:10}'.format(token[i][2]),
              '{:10}'.format(token[i][3]))
        i += 1
def lt(filename, token, args):
    from lexical import tokenize
    file = open(filename, "r")
    arquivo = file.read()
    file.close()
    for tok in tokenize(arquivo,args):
        token.append(tok)
def ls(token,args):
    from beuty import initsintatico
    initsintatico(token,args)
def lse(token,args):
    from semantico import semantico
    semantico(token,args)
def lgc(token,args):
    from  Geracaodecodigo import intemerdiario
    texto = []
    intemerdiario(token,args,0,len(token),0,0, texto)
    '''
    intermediario(token, args, posicao inicial que deseja converter para assembler, posição final, valor inicial das Labels dos loops, valor inicial das Labels dos condicionais)
    '''