'''
    intermediario(token, argumentos, posicao inicial que deseja converter para assembler, posição final, valor inicial das Labels dos loops, texto final)
'''
def intemerdiario(token,args):
    if (args.lgc):
        print ("Gerando código intermediário")
    L=0
    C=0
    pilha=[]
    i=0
    texto=[]
    while i < len(token) :
        if 'inteiro' in token[i][0]:
            if (args.lgc):
                print ("Inteiro identificado:")
            texto.extend(variaveis(token,i))
        elif 'leia' in token[i][0]:
            if (args.lgc):
                print ("leia identificado:")
            texto.append('LEIA '+token[i+2][1])
        elif 'escreva' in token[i][0]:
            if (args.lgc):
                print ("escreva identificado:")
            texto.append('ESCREVA '+ token[i+2][1])
        elif 'recebe' in token[i][0]:
            if (args.lgc):
                print ("Atribuição identificada:")
            exp=[]
            from infixtoposfix import infixToPostfix
            exp.append(infixToPostfix(expressao(token, i)))
            simpleexpre(exp,token[i-1][1],texto)
        elif 'enquanto' in token[i][0]:
            if (args.lgc):
                print ("função enquanto identificado:")
            texto.append(f'_L{L}: if {token[i+2][1]}'+ (' >=' if '<' in token[i+3][1] else ' <=')+f' {token[i+4][1]} goto _L{L+1} ')
            pilha.append(f'_L{L+1}')
            L+=2
        elif 'se' == token[i][0]:
            if (args.lgc):
                print ("\'se\' identificado:")
            texto.append(f'_C{C}: if {token[i+2][1]}' + (' =>' if '<' in token[i+3][1] else ' <=')+f' {token[i+4][1]} goto _C{C+1}')
            pilha.append(f'_C{C + 1}')
            C += 2
        elif 'senao' == token[i][0]:
            if (args.lgc):
                print ("\'senao\' identificado:")
            pilha.append(f'{int(texto[-1].split("_C")[1].split(":")[0])-1}')
        elif '}' in token[i][1]:
            if 'L' in pilha[-1]:
                p= pilha.pop()
                texto.append(f'goto _L{int(p.split("_L")[1])-1}')
                texto.append(f'{p}:')
            elif 'C' in pilha[-1]:
                p = pilha.pop()
                texto.append(f'goto EXIT_C{int(p.split("_C")[1]) - 1}')
                texto.append(f'{p}:')
                if 'senao' not in  token[i+1][0]:
                    texto.append (f'EXIT_C{int(p.split("_C")[1])-1}:')
            elif pilha[-1]:
                texto.append(f'EXIT_C{pilha.pop()}:')
        #print (pilha)
        i=i+1

    with open('intermediario.s','w') as f:
        if (args.lgc):
            print ("Escrevendo no arquivo:")
        f.write('\n'.join(texto))
def simpleexpre(exp,var,texto):
    '''
    ADD dest,src1,src2	dest = src1 + src2
    SUB dest,src1,src2	dest = src1 - src2
    ADDI dest,src1,I	dest = src1 + I
    MUL dest,src1,src2	dest = src1 × src2
    DIV dest,src1,src2	dest = src1/src2
    '''
    t=1
    exp=exp[0].split()
    values=[]
    operador=['+','-','*','/']
    for i in range(len(exp)):
        if exp[i] in operador:
            a = values.pop()
            b = values.pop()
            if i == len(exp)-1:
                texto.append(f'{var} := {b} {a} {exp[i]}')
            else:
                texto.append(f'T{t} := {b} {a} {exp[i]}')
                values.append(f'T{t}')
                t+=1
        else:
            values.append(exp[i])
    if len(values) > 0:
        texto.append(f'{var} := {values[0]}')

def expressao(token, i):
    l=i+1
    var=[]
    while not('fim_linha' in token[l][0]):
        var.append(token[l][1])
        l+=1
    return ' '.join(var)
def variaveis(token,i):
    l=i+1
    var=[]
    while not('fim_linha' in token[l][0]):
        if not('virgula' in token[l][0]):
            var.append('INTEIRO '+token[l][1])
        l+=1
    return var
def gerarcodigo(token,args):
    '''
    intermediario(token, args, posicao inicial que deseja converter para assembler, posição final, valor inicial das Labels dos loops, valor inicial das Labels dos condicionais)
    '''
    intemerdiario(token, args)
    gerar(args)
def gerar(args):
    nome = args.filename.split('.')[0]
    texto=[]
    if (args.lgc):
        print ("Gerando código final")
    with open('intermediario.s','r') as f:
        texto=f.read().splitlines()
    i=0
    final=[]
    db=[]
    msg=-1
    if (args.lgc):
        print ("Gerando cabeçalho")
    final.append(';flat assembler  version 1.73.02')
    final.append(f';fasm {nome}.asm')
    final.append(f';ld -lc -e main -dynamic-linker /lib/ld-linux.so.2  {nome}.o -o {nome} -m elf_i386')
    final.append(';OS: Ubuntu 18.04.1 LTS x86_64 ')
    final.append(';Kernel: 4.15.0-42-generic ')
    final.append(';CPU: Intel i5-2520M (4) @ 3.200GHz\n')
    final.append(f'format ELF')
    final.append('public main as \'main\' ')
    final.append('extrn \'exit\'as exit')
    final.append('extrn \'printf\' as printf')
    final.append('extrn \'scanf\'as scanf\n')

    final.append('section \'.text\' executable')

    final.append('main:')

    while i < len(texto):
        if (args.lgc):
            print ("Gerando o comando escreva")
        if 'INTEIRO' in texto[i].split()[0]:
            db.append(f'{texto[i].split()[1]} dd 0')
        if 'ESCREVA' in texto[i].split('"')[0]:
            final.append(';Impressão na tela')
            if '"' in texto[i]:
                msg += 1
                text = texto[i].split('ESCREVA')[1]
                text= text.strip()
                text= "".join(text)
                text = text.replace('\"', '')
                if (args.lgc):
                    print ("Gerando comandos para o escrever uma mensagem")
                final.append(f'push msg{msg}')
                final.append(f'call printf')
                final.append(f'add esp, 4\n')

                txt=text.replace('\\n', '\',10,0,\'')
                db.append(f'msg{msg} db \'{txt}\', 0,0')
            else:
                if (args.lgc):
                    print ("Gerando comandos para o escrever uma variavel")
                expre = texto[i].split()
                final.append(f'push {"["+expre[1]+"]" if expre[1].isidentifier() else expre[1] }')
                final.append(f'push formatacao')
                final.append(f'call printf')
                final.append(f'add esp, 4\n')
        if 'LEIA' in texto[i].split()[0]:
            if (args.lgc):
                print ("Gerando o comando leia")
            final.append(';Ler do Teclado')
            final.append(f'push {texto[i].split()[1]}')
            final.append(f'push formatacao')
            final.append(f'call scanf')
            final.append(f'add esp, 8\n')
        if 'if' in texto[i]:
            '''
            je - jump if op1 = op2 (op1 is "equal to" op2)
            ja - jump if op1 > op2 (op1 is "above" op2)
            jb - jump if op1 < op2 (op1 is "below" op2)
            jae - jump if op1 >= op2 (op1 is "above or equal to" op2)
            jbe - jump if op1 <= op2 (op1 is "below or equal to" op2) 
            '''
            if (args.lgc):
                print ("Comando condicional/repetição identificado")
                print ("Gerando os comandos condicões/repetição")
            expre=texto[i].split()
            final.append(';Label')
            final.append(f'{expre[0]}')
            #final.append(f'xor eax,eax')
            final.append(f'xor ebx, ebx')
            final.append(f'mov eax, {"["+expre[2]+"]" if expre[2].isidentifier() else expre[2] }')
            final.append(f'mov ebx, {"["+expre[4]+"]" if expre[4].isidentifier() else expre[4] }')
            final.append(f'cmp eax, ebx')
            final.append(f'j{"ae" if ">=" is expre[3] else "be"} {expre[6]}')
        if 'goto' in texto[i].split()[0]:
            final.append(f'jmp {texto[i].split()[1]}')
        if len(texto[i].split())<2:
            final.append(f'{texto[i]}')
        if len(texto[i].split())>2:
            if (args.lgc):
                print ("Comando de atribuição identificado")
                print ("Gerando...")
            if ':=' in texto[i].split()[1]:
                expre = texto[i].split()
                if len(expre)==3:
                    if (args.lgc):
                        print ("Comando de atribuição para com um valor")
                        print ("Gerando...")
                    final.append(f';Atribuição')
                    final.append(f'mov eax,[{expre[0]}]')
                    final.append(f'mov eax, {"["+expre[2]+"]" if expre[2].isidentifier() else expre[2] }')
                    final.append(f'mov [{expre[0]}],eax')
                    final.append(f'xor eax,eax\n')
                elif '+' is expre[4]:
                    if (args.lgc):
                        print ("Comando de soma")
                        print ("Gerando...")
                    final.append(f';Adicção')
                    final.append(f'mov eax, {"["+expre[2]+"]" if expre[2].isidentifier() else expre[2] }')
                    final.append(f'mov edx, {"["+expre[3]+"]" if expre[3].isidentifier() else expre[3] }')
                    final.append(f'add eax, edx')
                    final.append(f'mov {"["+expre[0]+"]"}, eax')
                    final.append(f'xor eax,eax\n')
                elif '-' is expre[4]:
                    if (args.lgc):
                        print ("Comando de subtração")
                        print ("Gerando...")
                    final.append(f';Subtração')
                    final.append(f'mov eax, {"["+expre[2]+"]" if expre[2].isidentifier() else expre[2] }')
                    final.append(f'mov edx, {"["+expre[3]+"]" if expre[3].isidentifier() else expre[3] }')
                    final.append(f'sub eax, edx')
                    final.append(f'mov {"["+expre[0]+"]"}, eax')
                    final.append(f'xor eax,eax\n')
                elif '*' is expre[4]:
                    if (args.lgc):
                        print ("Comando de multiplicação")
                        print ("Gerando...")
                    final.append(f';Multiplicação')
                    final.append(f'mov eax, {"[" + expre[2] + "]" if expre[2].isidentifier() else expre[2] }')
                    final.append(f'mov edx, {"[" + expre[3] + "]" if expre[3].isidentifier() else expre[3] }')
                    final.append(f'imul eax, edx')
                    final.append(f'mov {"[" + expre[0] + "]"}, eax')
                    final.append(f'xor eax,eax\n')
                elif '/' is expre[4]:
                    if (args.lgc):
                        print ("Comando de divisão")
                        print ("Gerando...")
                    final.append(f';Divisao')
                    final.append(f'xor edx, edx')
                    final.append(f'mov ebx, {"[" + expre[2] + "]" if expre[2].isidentifier() else expre[2] }')
                    final.append(f'mov eax, {"[" + expre[2] + "]" if expre[2].isidentifier() else expre[2] }')
                    final.append(f'div ebx')
                    final.append(f'mov {"[" + expre[0] + "]"}, eax')
                    final.append(f'xor eax,eax\n')

        i+=1
    final.append('sair:')
    final.append('push 0')
    final.append('call exit\n')

    if(len(db)>0):
        final.append('section \'.data\' writeable')
        final.append('formatacao db \'%d\' , 0')
        final.extend(db)

    with open(nome+'.asm','w') as f:
        f.write('\n'.join(final))
    import os
    if args.lgc:
        print (f"Compilando arquivo fonte: {args.filename}")
    os.system(f'fasm {nome}.asm')
    os.system(f'ld -lc -e main -dynamic-linker /lib/ld-linux.so.2  {nome}.o -o {nome} -m elf_i386')
    if args.lgc:
        print (f"Arquivo executavel pronto: {nome}")
        print ("pronto")