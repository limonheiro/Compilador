def beut(tabela1, tabela2):
    from bs4 import BeautifulSoup
    with open('tabela.html', 'r') as file:
        soup = BeautifulSoup(file, "html5lib")
        soup.prettify()#reorganiza as tags

        tabela_all = soup.find_all('tbody')

        coluna1 = tabela_all[0].find_all('tr')
        coluna2 = tabela_all[1].find_all('tr')

        valores_return(coluna1, tabela1)
        valores_return(coluna2, tabela2)


def valores_return(colunas, tabela):

    for coluna in colunas:
        celula = coluna.find_all('td')
        celula = [ele.text.strip() for ele in celula]
        tabela.append([ele for ele in celula if ele])

def separar(palavra):
    numero = []
    for word in palavra:
        if word.isdigit():
            numero += word
    return (''.join(numero))

def initsintatico(token, args):
    import os
    if not(os.path.isfile('dicionario1.dtc')and os.path.isfile('dicionario2.dtc')):
        save()

    from sintatico import analisadorsintatico
    dict_tabela1 = load("dicionario1.dtc")
    dict_tabela2 = load("dicionario2.dtc")
    analisadorsintatico(dict_tabela1, dict_tabela2, token, args)

def load(filename):
    import pickle
    file = open(filename, "rb")
    return pickle.load(file)

def save():
    tabela1 = []
    tabela2 = []
    beut(tabela1, tabela2)
    topo = tabela1[0]
    del tabela1[0]
    dict_tabela1 = {}
    dict_tabela2 = {}
    for linhas in tabela1:
        i = 0;
        for linha in linhas:
            if linha.isdigit() and i <= len(topo):
                dict_tabela1[(linhas[0], topo[i - 1])] = [int(linha)]
            i += 1
    for i in range(len(tabela2)):
        if (((tabela2[i][1]).split('::= '))[1]).split(" ")[0] != 'î':
            dict_tabela2[int(separar(tabela2[i][0]))] = ((((tabela2[i][1]).split('::= '))[1]).split())
        else:
            dict_tabela2[int(separar(tabela2[i][0]))] = []
    saveFile(dict_tabela1, "dicionario1.dtc")
    saveFile(dict_tabela2, "dicionario2.dtc")

def saveFile(dict, filename):
    import pickle
    dicionario = open(filename, "wb")
    pickle.dump(dict, dicionario)
    dicionario.close()
