TOKENS: tuple[str, ...] = (
    # ! KEYWORDS ! #
    # Estrutura do programa
    "PROGRAM",
    "END",
    "RETURN",
    
    # Subprogramas
    "FUNCTION",
    "SUBROUTINE",
    "CALL",
    
    # Data types
    "INTEGER",
    "LOGICAL",
    "REAL",
    "CHARACTER",
    
    # Controlo de fluxo
    "IF",
    "THEN",
    "ELSE",
    "ENDIF",
    "DO",
    "CONTINUE",
    "GOTO",
    
    # I/O
    "READ",
    "PRINT",
    
    # Algumas funções intrínsecas
    "MOD",
    "SQRT",
    "INT",
    "FLOAT",
    "MAX",
    "MIN",
    
    # Power
    "POWER",    # **
    
    # ! TOKENS ! #
    # Identificadores
    "IDEN",
    
    # Labels
    "LABEL",
    
    # Literais numéricos e de string
    "INT_LIT",
    "REAL_LIT",
    "STRING_LIT",
    
    # Operadores relacionais
    "OP_EQ",   # .EQ.
    "OP_NE",   # .NE.
    "OP_LT",   # .LT.
    "OP_LE",   # .LE.
    "OP_GT",   # .GT.
    "OP_GE",   # .GE.
    
    # Operadores lógicos
    "OP_AND",  # .AND.
    "OP_OR",   # .OR.
    "OP_NOT",  # .NOT.
    
    # Booleans
    "TRUE",    # .TRUE.
    "FALSE",   # .FALSE.
)

LITERALS: str = "+-*/=(),'"