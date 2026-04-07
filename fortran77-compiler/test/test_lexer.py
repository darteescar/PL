import os
import sys
import ply.lex as lex

current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.insert(0, parent_dir)

from src.lexer import Lexer

"""
Funções auxiliares para os testes.
"""

def get_tokens(src: str) -> list[lex.LexToken]:
    return Lexer().tokenize(src)

def token_types(src: str) -> list[str]:
    return [t.type for t in get_tokens(src) if t.type != "NEWLINE"]

def token_values(src: str) -> list:
    return [t.value for t in get_tokens(src) if t.type != 'NEWLINE']
 
def find_token(tokens, type_: str):
    return next((t for t in tokens if t.type == type_), None)
 
def all_of_type(tokens, type_: str) -> list:
    return [t for t in tokens if t.type == type_]

"""
Exemplos do professor.
"""

CODE_DIR = os.path.join(os.path.dirname(__file__), 'code')

F77_FILES = ['helloworld.f77', 'fatorial.f77', 'isprime.f77', 'listsum.f77', 'conversor.f77']

src_code = []

for file in F77_FILES:
    with open(os.path.join(CODE_DIR, file), 'r') as f:
        src_code.append(f.read())
        
src_hello, src_fatorial, src_isprime, src_listsum, src_conversor = src_code

"""
Testar se os exemplos do professor têm erros.
"""

def test_hello_no_errors():
    lexer = Lexer()
    lexer.tokenize(src_hello)
    assert not lexer.has_errors
 
def test_fatorial_no_errors():
    lexer = Lexer()
    lexer.tokenize(src_fatorial)
    assert not lexer.has_errors

def test_isprime_no_errors():
    lexer = Lexer()
    lexer.tokenize(src_isprime)
    assert not lexer.has_errors

def test_listsum_no_errors():
    lexer = Lexer()
    lexer.tokenize(src_listsum)
    assert not lexer.has_errors

def test_conversor_no_errors():
    lexer = Lexer()
    lexer.tokenize(src_conversor)
    assert not lexer.has_errors

"""
Testar se algumas keywords são reconhecidas nos exemplos do professor.
"""

def test_program_keyword_in_hello():
    assert "PROGRAM" in token_types(src_hello)

def test_end_keyword_in_hello():
    assert "END" in token_types(src_hello)

def test_do_keyword_in_fatorial():
    assert "DO" in token_types(src_fatorial)

def test_continue_keyword_in_fatorial():
    assert "CONTINUE" in token_types(src_fatorial)

def test_if_then_else_endif_in_primo():
    types = token_types(src_isprime)
    assert "IF"    in types
    assert "THEN"  in types
    assert "ELSE"  in types
    assert "ENDIF" in types

def test_goto_in_primo():
    assert "GOTO" in token_types(src_isprime)

def test_function_in_conversor():
    assert "FUNCTION" in token_types(src_conversor)

def test_return_in_conversor():
    assert "RETURN" in token_types(src_conversor)

def test_mod_intrinsic_in_primo():
    assert "MOD" in token_types(src_isprime)

def test_mod_intrinsic_in_conversor():
    assert "MOD" in token_types(src_conversor)
    
"""
Testar se as keywords não são confundidas com identificadores.
"""

def test_endif_is_single_token():
    src = "      ENDIF\n"
    tokens = get_tokens(src)
    types = [t.type for t in tokens if t.type != 'NEWLINE']
    assert types == ["ENDIF"]

def test_goto_is_single_token():
    src = "      GOTO 10\n"
    types = token_types(src)
    assert types[0] == "GOTO"

def test_identifier_starting_with_keyword():
    src = "      IFFY = 1\n"
    types = token_types(src)
    assert types[0] == "IDEN"

def test_identifier_do_not_match_do_keyword():
    src = "      DOUBLE = 1\n"
    types = token_types(src)
    assert types[0] == "IDEN"

def test_program_name_is_iden():
    tokens = get_tokens(src_hello)
    prog_idx = next(i for i, t in enumerate(tokens) if t.type == 'PROGRAM')
    assert tokens[prog_idx + 1].type == "IDEN"
    assert tokens[prog_idx + 1].value == "HELLO"
    
"""
Testar identificadores.
"""

def test_simple_identifier():
    src = "      FAT = 1\n"
    tokens = get_tokens(src)
    assert tokens[0].type  == "IDEN"
    assert tokens[0].value == "FAT"

def test_identifier_uppercased():
    src = "      fat = 1\n"
    tokens = get_tokens(src)
    assert tokens[0].value == "FAT"

def test_identifier_with_digits():
    src = "      NUMS1 = 0\n"
    tokens = get_tokens(src)
    assert tokens[0].type  == "IDEN"
    assert tokens[0].value == "NUMS1"

def test_variables_in_fatorial():
    tokens = get_tokens(src_fatorial)
    iden_values = {t.value for t in tokens if t.type == "IDEN"}
    assert "N"   in iden_values
    assert "I"   in iden_values
    assert "FAT" in iden_values
    
"""
Testar inteiros e reais literais e strings.
"""

def test_simple_integer():
    src = "      N = 42\n"
    tokens = get_tokens(src)
    int_tok = find_token(tokens, 'INT_LIT')
    assert int_tok is not None
    assert int_tok.value == 42

def test_integer_value_is_int_type():
    src = "      N = 10\n"
    tokens = get_tokens(src)
    int_tok = find_token(tokens, 'INT_LIT')
    assert isinstance(int_tok.value, int)

def test_real_value_is_float_type():
    src = "      X = 3.14\n"
    tokens = get_tokens(src)
    real_tok = find_token(tokens, 'REAL_LIT')
    assert isinstance(real_tok.value, float)

def test_real_before_int():
    src = "      X = 3.14\n"
    types = token_types(src)
    assert 'REAL_LIT' in types
    assert types.count('INT_LIT') == 0
    
def test_simple_string():
    src = "      PRINT *, 'Ola'\n"
    tokens = get_tokens(src)
    str_tok = find_token(tokens, 'STRING_LIT')
    assert str_tok is not None
    assert str_tok.value == "OLA"

def test_string_quotes_removed():
    src = "      PRINT *, 'Ola'\n"
    tokens = get_tokens(src)
    str_tok = find_token(tokens, 'STRING_LIT')
    assert "'" not in str_tok.value
    
def test_escaped_quote_in_string():
    src = "      PRINT *, 'It''s ok'\n"
    tokens = get_tokens(src)
    str_tok = find_token(tokens, 'STRING_LIT')
    assert str_tok.value == "IT'S OK"

def test_string_in_hello():
    tokens = get_tokens(src_hello)
    str_tok = find_token(tokens, 'STRING_LIT')
    assert str_tok is not None
    assert str_tok.value == "OLA, MUNDO!"
    
"""
Testar operadores relacionais e lógicos.
"""

def test_op_le_in_primo():
    assert "OP_LE" in token_types(src_isprime)

def test_op_eq_in_primo():
    assert "OP_EQ" in token_types(src_isprime)
    
def test_true_literal():
    src = "      ISPRIM = .TRUE.\n"
    tokens = get_tokens(src)
    true_tok = find_token(tokens, 'TRUE')
    assert true_tok is not None
    assert true_tok.value is True
    
"""
Testar operadores aritméticos.
"""

def test_power_operator():
    src = "      X = A**2\n"
    assert "POWER" in token_types(src)
    
def test_addition_literal():
    src = "      X = A + B\n"
    assert '+' in token_types(src)

def test_subtraction_literal():
    src = "      X = A - B\n"
    assert '-' in token_types(src)
    
"""
Testar "LABEL" e "NEWLINE".
"""

def test_label_token_emitted():
    tokens = get_tokens(src_fatorial)
    label_tokens = all_of_type(tokens, 'LABEL')
    assert len(label_tokens) == 1
    assert label_tokens[0].value == 10

def test_two_labels_in_conversor():
    tokens = get_tokens(src_conversor)
    label_values = [t.value for t in tokens if t.type == 'LABEL']
    assert 10 in label_values
    assert 20 in label_values
    
def test_hello_newline_count():
    tokens = get_tokens(src_hello)
    assert len(all_of_type(tokens, 'NEWLINE')) == 3
    
"""
Testar se erros são detectados.
"""

def test_invalid_char_reported():
    src = "      X = @\n"
    lexer = Lexer()
    lexer.tokenize(src)
    assert lexer.has_errors
    assert len(lexer.errors) == 1

def test_error_contains_invalid_char():
    src = "      X = @\n"
    lexer = Lexer()
    lexer.tokenize(src)
    assert "@" in lexer.errors[0].message
    
def test_multiple_errors_reported():
    src = "      @ # $\n"
    lexer = Lexer()
    lexer.tokenize(src)
    assert len(lexer.errors) == 3
    
def test_lexer_continues_after_error():
    src = "      X = @ + 1\n"
    lexer = Lexer()
    tokens = lexer.tokenize(src)
    assert lexer.has_errors
    types = [t.type for t in tokens if t.type != 'NEWLINE']
    assert 'INT_LIT' in types