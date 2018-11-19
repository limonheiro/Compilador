def main():

    parser = argparse.ArgumentParser(description='Compilador para uma linguagem do tipo LL(1)')
    parser.add_argument("-lt", help="Mostra o LOG de Tokens e Lexemas do analisador lexico", action='store_true')
    parser.add_argument("-ls", help="Mostra o Log das operações do analisador sintatico", action='store_true')
    parser.add_argument("-lse", help="Mostra o Log das operações do analisador semantico", action='store_true')
    parser.add_argument("-lgc", help="Mostra o Log da geração de codigo", action='store_true')
    parser.add_argument("filename", type=str, help="Filename")
    parser.add_argument('-tudo', help='Show all logs', action='store_true')
    args=parser.parse_args()
    opction(args)

#executa a funcao main()
if __name__ == "__main__":
    import sys
    import argparse
    from selection import opction
    main()