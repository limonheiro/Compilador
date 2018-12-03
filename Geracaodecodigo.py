'''
    intermediario(token, argumentos, posicao inicial que deseja converter para assembler, posição final, valor inicial das Labels dos loops, texto final)
'''
def intemerdiario(token,args, inicio, fim, loop,condicional, texto):
    L=loop
    C=condicional
    i=inicio
    while i < fim :
        if 'inteiro' in token[i][0]:
            texto.extend(variaveis(token,i))
        elif 'leia' in token[i][0]:
            texto.append('LEIA '+token[i+2][1])
        elif 'escreva' in token[i][0]:
            texto.append('ESCREVA '+ token[i+2][1])
        elif 'recebe' in token[i][0]:
            exp=[]
            from infixtoposfix import infixToPostfix
            exp.append(infixToPostfix(expressao(token, i)))
            simpleexpre(exp,token[i-1][1],texto)
        elif 'enquanto' in token[i][0]:
            texto.append(f'_L{L}: if {token[i+2][1]}'+ (' >' if '<' in token[i+3][1] else ' <')+f' {token[i+4][1]} goto _L{L+1} ')
            i=intemerdiario(token, args, i+6, fim, L+1, C, texto)
            texto.append(f'_L{L+1}:')
            L=L+i
            C=L
        elif 'se' == token[i][0]:
            texto.append(f'_C{C}: if {token[i+2][1]}' + (' >' if '<' in token[i+3][1] else ' <')+f' {token[i+4][1]} goto _C{C+1}')
            i=intemerdiario(token, args, i+6, fim, L, C+1, texto)
            texto.append(f'_C{L+1}:')
            C = C + i
            L = C
        elif '}' in token[i][1]:
            return i
        i=i+1

    with open('intermediario.s','w') as f:
        f.write('\n'.join(texto))
def simpleexpre(exp,var,texto):
    '''
    ADD dest,src1,src2	dest = src1 + src2
    SUB dest,src1,src2	dest = src1 - src2
    ADDI dest,src1,I	dest = src1 + I
    MUL dest,src1,src2	dest = src1 × src2
    DIV[U] dest,src1,src2	dest = src1/src2
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
    texto=[]
    '''
    intermediario(token, args, posicao inicial que deseja converter para assembler, posição final, valor inicial das Labels dos loops, valor inicial das Labels dos condicionais)
    '''
    intemerdiario(token, args, 0, len(token), 0, 0, texto)
    gerar()
def gerar():
    texto=[]
    with open('intermediario.s','r') as f:
        texto=f.readlines()
    i=0
    final=[]
    db=[]
    msg=-1
    final.append('format ELF64 executable 3')
    final.append('segment readable executable')
    final.append('entry main')
    final.append('main:')

    while i < len(texto):
        if 'ESCREVA' in texto[i]:
            if '"' in texto[i]:
                msg += 1
                size = texto[i].strip('ESCREVA')
                size = size.strip('\n').replace('"','')
                final.append(f'lea rdi, [msg{msg}]')
                final.append(f'mov rax, {len(size)}')
                final.append(f'mov rdx, rax')
                final.append(f'mov rsi, rdi')
                final.append(f'mov rdi, 1')
                final.append(f'mov rax, 1')
                final.append(f'syscall')
                db.extend([f'msg{msg} db \'{size.strip()}\', 10,0'])
            else:
                print ()
        i+=1
    final.append('xor rdi,rdi')
    final.append('mov rax, 60')
    final.append('syscall')
    if(msg>-1):
        final.append('segment readable writable')
        final.extend(db)
    with open('final.fasm','w') as f:
        f.write('\n'.join(final))