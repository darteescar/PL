import argparse

from lexer import Lexer

def main():
    arg_parser = argparse.ArgumentParser(description="Compilador de Fortran 77")
    
    arg_parser.add_argument("file", help="Path para o ficheiro Fortran 77")

    group = arg_parser.add_mutually_exclusive_group()
    group.add_argument("-l", "--lexer", action="store_true", help="Executa o lexer")
    group.add_argument("-p", "--parser", action="store_true", help="Executa o lexer e depois o parser")
    group.add_argument("-s", "--semantic", action="store_true", help="Executa o lexer, parser e a análise semântica")
    group.add_argument("-t", "--translate", action="store_true", help="Executa a tradução completa")

    args = arg_parser.parse_args()

    if not (args.lexer or args.parser or args.semantic): # Por defualt temos a tradução completa
        args.translate = True
        
    if args.lexer:
        print("=" * 25)
        print("=> Modo Lexer...")
        print("=" * 25)
        
        try:
            with open(args.file, "r", encoding="utf-8") as f:
                src = f.read()
                
            lexer = Lexer()
            lexer.input(src)
            
            for token in lexer:
                print(token)

        except FileNotFoundError:
            print(f"Erro: O ficheiro '{args.file}' não foi encontrado.")
        
    elif args.parser:
        print("=" * 25)
        print("=> Modo Parser...")
        print("=" * 25)
        # TODO: Executar Preprocessor + Lexer + Parser
        
    elif args.semantic:
        print("=" * 25)
        print("=> Modo Semantic...")
        print("=" * 25)
        # TODO: Executar Preprocessor + Lexer + Parser + Semântica
        
    elif args.translate:
        print("=" * 25)
        print("=> Modo Translate...")
        print("=" * 25)
        # TODO: Executar toda a pipeline (Lexer, Parser, Semântica e Tradutor)

if __name__ == '__main__':
    main()