from enum import Enum
# A linguagem Mini Logo
# Program → ‘program’ literal Decl Block EOF
# Decl → ‘:’id ‘;’ Decl | ε
# Block → ‘begin’ StatementList ‘end’
# StatementList → Statement ‘;’ StatementList | Statement
# Statement → ‘turn’ term ‘degrees’ | ‘forward’ term |
# ‘repeat’ term ‘do’ Block | ‘print’ literal |
# AssignmentStatement | IfStatement

# AssignmentStatement → ‘:’id Expr
# IfStatement → ‘if’ Expr ‘do’ Block
# Expr → Expr ‘+’ Expr | Expr ‘–‘ Expr |
# Expr ‘*’ Expr | Expr ‘/’ Expr | term

# term → number | ‘:’id



class Tag(Enum):
   '''
   Uma representacao em constante de todos os nomes 
   de tokens para a linguagem.
   '''

   # Fim de arquivo
   EOF = -1

   # Palavras-chave
   KW_PROGRAM = 1
   KW_FORWARD = 2
   KW_BEGIN = 3
   KW_TURN = 4
   KW_DEGREES = 5
   KW_REPEAT = 6
   KW_DO = 7
   KW_END = 8
   KW_IF = 9
   KW_PRINT = 10

   # Operadores 
   OP_MENOS = 11
   OP_MAIS= 12
   OP_VEZES = 13
   OP_DIVISAO = 14
   
   # Simbolos
   SMB_ABRE_CHAVES = 15
   SMB_FECHA_CHAVES = 16
   SMB_DOIS_PONTOS = 17
   SMB_PONTO_VIRGULA = 18
   
   # Identificador
   ID = 21

   # Numeros
   NUM = 22
    # String
   LITERAL = 23