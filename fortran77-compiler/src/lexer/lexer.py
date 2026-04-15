import ply.lex as lex

from dataclasses import dataclass
from .tokens import TOKENS, KEYWORDS, LITERALS
from .preprocessor import Preprocessor, LogicalLine

@dataclass
class LexerError(Exception):
    """
    Erro gerado durante a análise léxica.
    """
    message: str    # mensagem de erro
    line: int       # linha onde ocorreu o erro
    column: int     # coluna onde ocorreu o erro
    
    def __str__(self) -> str:
        return f"[Lexer] Linha {self.line}, Col {self.column}: {self.message}"

class Lexer:
    """
    Class da análise léxica (lexer).
    """
    
    tokens = TOKENS
    literals = LITERALS
    t_ignore = ' \t'
    
    def __init__(self) -> None:
        self._errors: list[LexerError] = [] # lista de erros
        self._current_src: str = ""         # código a ser analisado
        self._token_stream = iter([])       # iterador dos tokens gerados
        
        self._lexer = lex.lex(module=self)
    
    # --- Operadores relacionais ----------------------------------------
    def t_OP_EQ(self, t: lex.LexToken) -> lex.LexToken:
        r'\.EQ\.'
        return t
 
    def t_OP_NE(self, t: lex.LexToken) -> lex.LexToken:
        r'\.NE\.'
        return t
 
    def t_OP_LE(self, t: lex.LexToken) -> lex.LexToken:
        r'\.LE\.'
        return t
 
    def t_OP_LT(self, t: lex.LexToken) -> lex.LexToken:
        r'\.LT\.'
        return t
 
    def t_OP_GE(self, t: lex.LexToken) -> lex.LexToken:
        r'\.GE\.'
        return t
 
    def t_OP_GT(self, t: lex.LexToken) -> lex.LexToken:
        r'\.GT\.'
        return t

    # --- Operadores lógicos --------------------------------------------
    def t_OP_AND(self, t: lex.LexToken) -> lex.LexToken:
        r'\.AND\.'
        return t
 
    def t_OP_OR(self, t: lex.LexToken) -> lex.LexToken:
        r'\.OR\.'
        return t
 
    def t_OP_NOT(self, t: lex.LexToken) -> lex.LexToken:
        r'\.NOT\.'
        return t
    
    # --- Booleans ------------------------------------------------------
    def t_TRUE(self, t: lex.LexToken) -> lex.LexToken:
        r'\.TRUE\.'
        t.value = True
        return t
 
    def t_FALSE(self, t: lex.LexToken) -> lex.LexToken:
        r'\.FALSE\.'
        t.value = False
        return t
    
    # --- Potência -------------------------------------------------------
    def t_POWER(self, t: lex.LexToken) -> lex.LexToken:
        r'\*\*'
        return t
    
    # --- Literais numéricos e string ------------------------------------
    def t_REAL_LIT(self, t: lex.LexToken) -> lex.LexToken:
        r'\d+\.\d*(?:[ED][-+]?\d+)?|\.\d+(?:[ED][-+]?\d+)?|\d+[ED][-+]?\d+'
        t.value = float(t.value.replace('D', 'e').replace('E', 'e'))
        return t
 
    def t_INT_LIT(self, t: lex.LexToken) -> lex.LexToken:
        r'\d+'
        t.value = int(t.value)
        return t
    
    def t_STRING_LIT(self, t: lex.LexToken) -> lex.LexToken:
        r"'([^']|'')*'"
        t.value = t.value[1:-1].replace("''", "'") # Retira as plicas
        return t
    
    # --- Identificadores e keywords -------------------------------------
    def t_IDEN(self, t: lex.LexToken) -> lex.LexToken:
        r'[A-Z][A-Z0-9_]*'
        if t.value in KEYWORDS:
            t.type = t.value # Apanhas as keywords definidas no set
        return t
    
    
    
    def t_newline(self, t: lex.LexToken) -> None:
        r'\n+'
        t.lexer.lineno += len(t.value)
        
    def t_error(self, t: lex.LexToken) -> None:
        col = self._find_column(t)
        self._errors.append(
            LexerError(
                message=f"Caracter inválido '{t.value[0]}'",
                line=t.lexer.lineno,
                column=col,
            )
        )
        t.lexer.skip(1)
        
    @property
    def errors(self) -> list[LexerError]:
        return self._errors # Retorna os erros acumulados
    
    @property
    def has_errors(self) -> bool:
        return len(self._errors) > 0 # Diz se houve erros
    
    def tokenize(self, src: str) -> list[lex.LexToken]:
        """
        Identifica os tokens do código e devolve uma lista deles.
        """
        self._errors = []
        self._current_src = src
        
        preprocessor = Preprocessor(src) # Faz o pré-processamento do código original
        logical_lines = preprocessor.process()
        
        tokens: list[lex.LexToken] = []
        for line in logical_lines:
            tokens.extend(self._tokenize_line(line))
        
        return tokens
    
    def input(self, source: str) -> None:
        self._token_stream = iter(self.tokenize(source))
 
    def token(self) -> lex.LexToken | None:
        return next(self._token_stream, None)
 
    def __iter__(self):
        return self
 
    def __next__(self) -> lex.LexToken:
        tok = self.token()
        if tok is None:
            raise StopIteration
        return tok
 
    def _tokenize_line(self, ll: LogicalLine) -> list[lex.LexToken]:
        """
        Divide uma LogicalLine em tokens, incluindo LABEL e NEWLINE no final.
        """
        result: list[lex.LexToken] = []
 
        # Apanha a LABEL
        if ll.label is not None:
            result.append(self._make_token(
                type_  = 'LABEL',
                value  = int(ll.label),
                lineno = ll.src_line,
            ))
 
        # Conteúdo da linha
        self._lexer.lineno = ll.src_line
        self._lexer.input(ll.content)
        for tok in self._lexer:
            result.append(tok)
 
        # \n (NEWLINE) do fim
        result.append(self._make_token(
            type_  = 'NEWLINE',
            value  = '\n',
            lineno = ll.src_line,
        ))
 
        return result
 
    def _make_token(self, *, type_: str, value, lineno: int) -> lex.LexToken:
        """
        Constrói um LexToken sintético (LABEL, NEWLINE).
        """
        tok        = lex.LexToken()
        tok.type   = type_
        tok.value  = value
        tok.lineno = lineno
        tok.lexpos = 0
        return tok
 
    def _find_column(self, t: lex.LexToken) -> int:
        return t.lexpos + 1