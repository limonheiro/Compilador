def opction(args):
    token = []
    erro = []
    if args.tudo:
        args.lt=True
        args.ls=True
        args.lse=True
        args.lgc=True
    if args.lt:
        vlt(args.filename,token,args,erro)
    else:
        lt(args.filename,token,args,erro)
    ls(token,args,erro)
    lse(token,args,erro)
    if len(erro)>0:
        for e in erro:
            print(e)
        if (args.lgc):
            print ("Não foi possivel iniciar a geração de código por causa de erro no código fonte.")
    else:
        lgc(token, args)

def vlt(filename,token,args, erro):
    from lexical import tokenize
    print ('#' * 80)
    file = open(filename, "r")
    arquivo = file.read()
    file.close()
    print('{:15}'.format('Token'), '{:29}'.format('Lexema'), '{:10}'.format('Linha'), '{:10}'.format('Coluna'))
    i = 0
    for tok in tokenize(arquivo,args, erro):
        token.append(tok)
        print('{:15}'.format(token[i][0]), '{:20.11}'.format(token[i][1]), '{:10}'.format(token[i][2]),
              '{:10}'.format(token[i][3]))
        i += 1
def lt(filename, token, args, erro):
    from lexical import tokenize
    file = open(filename, "r")
    arquivo = file.read()
    file.close()
    for tok in tokenize(arquivo,args,erro):
        token.append(tok)
def ls(token,args,erro):
    from beuty import initsintatico
    initsintatico(token,args,erro)
def lse(token,args,erro):
    from semantico import semantico
    semantico(token,args,erro)
def lgc(token,args):
    from  Geracaodecodigo import gerarcodigo
    gerarcodigo(token,args)