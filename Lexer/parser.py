import sys
import copy

from tag import Tag
from token import Token
from lexer import Lexer

'''
[TODO-OPC-1]: 
tratar retorno 'None' do Lexer que esta sem Modo Panico
[TODO-OPC-2]: 
para deixar as mensagens de erro sintatico mais esclarecedoras,
a tabela preditiva poderia ser implementada.
'''

class Parser():

   def __init__(self, lexer):
      self.lexer = lexer
      # Leitura inicial obrigatoria do primeiro simbolo
      self.token = lexer.proxToken()
      if self.token is None: # erro no Lexer
        sys.exit(0)

   def sinalizaErroSintatico(self, message):
      print("[Erro Sintatico] na linha " + str(self.token.getLinha()) + " e coluna " + str(self.token.getColuna()) + ": ")
      print(message, "\n")

   # avanca o token
   def advance(self):
      print("[DEBUG] token: ", self.token.toString())
      self.token = self.lexer.proxToken()
      if self.token is None: # erro no Lexer
        sys.exit(0)

   # verifica token esperado t 
   def eat(self, t):
      if(self.token.getNome() == t):
         self.advance()
         return True
      else:
         return False


   # Program -> ‘program’ literal Decl Block EOF
   def Program(self):
      if(self.eat(Tag.KW_PROGRAM)):
         if(not self.eat(Tag.LITERAL)):
            self.sinalizaErroSintatico("Esperado \"um LITERAL\", encontrado " + "\"" + self.token.getLexema() + "\"")
         self.Decl()
         self.Block()
         if(self.token.getNome() != Tag.EOF):
            self.sinalizaErroSintatico("Esperado \"Fim do arquivo \"; encontrado " + "\"" + self.token.getLexema() + "\"")
      

   def Decl(self):
      if(self.eat(Tag.SMB_DOIS_PONTOS)):
         # ‘:’id ‘;’ Decl | ε
         if(not self.eat(Tag.ID)):
            self.sinalizaErroSintatico("Esperado \"ID\", encontrado " + "\"" + self.token.getLexema() + "\""+" Decl não deve começar com um numeral")
            sys.exit(0)
         if(not self.eat(Tag.SMB_PONTO_VIRGULA)):
            self.sinalizaErroSintatico("Esperado \"';'\", encontrado " + "\"" + self.token.getLexema() + "\"")
            sys.exit(0)
         self.Decl()
   
   def Block(self):
      # ‘begin’ StatementList ‘end’
      if(not self.eat(Tag.KW_BEGIN)):
         self.sinalizaErroSintatico("Esperado \"'begin'\", encontrado " + "\"" + self.token.getLexema() + "\""+ " bloco de codigo deve ser iniciado com begin")
         sys.exit(0)
      self.StatementList()
      if(not self.eat(Tag.KW_END)):
         self.sinalizaErroSintatico("Esperado \"'end'\", encontrado " + "\"" + self.token.getLexema() + "\"")
         sys.exit(0)
      
   def StatementList(self):
      # Statement StatementList’
      self.Statement()
      self.StatementListLinha()

   def Statement(self):
      '''
      ‘turn’ Term ‘degrees’ | ‘forward’ Term |
      ‘repeat’ Term ‘do’ Block | ‘print’ literal |
      AssignmentStatement | IfStatement
      '''
      if(self.eat(Tag.KW_TURN)):
         self.Term()
         if(not self.eat(Tag.KW_DEGREES)):
            self.sinalizaErroSintatico("Esperado \"'degrees'\", encontrado " + "\"" + self.token.getLexema() + "\"")
            sys.exit(0)
      elif(self.eat(Tag.KW_FORWARD)):
         self.Term()
      elif(self.eat(Tag.KW_REPEAT)):
         self.Term()
         if(not self.eat(Tag.KW_DO)):
            self.sinalizaErroSintatico("Esperado \"'do'\", encontrado " + "\"" + self.token.getLexema() + "\"")
            sys.exit(0)
         self.Block()
      elif(self.eat(Tag.KW_PRINT)):
        if(not self.eat(Tag.LITERAL)):
            self.sinalizaErroSintatico("Esperado \"LITERAL\", encontrado " + "\"" + self.token.getLexema() + "\"")
            sys.exit(0)
      elif(self.eat(Tag.SMB_DOIS_PONTOS)):
         self.AssignmentStatement()
      elif(self.eat(Tag.KW_IF)):
         self.IfStatement()

   def StatementListLinha(self):
      # ‘;’ StatementList | ε
      if(self.eat(Tag.SMB_PONTO_VIRGULA)):
         self.StatementList()
      
   def AssignmentStatement(self):
      # ‘:’id Expr
      if(not self.eat(Tag.ID)):
         self.sinalizaErroSintatico("Esperado \"ID\", encontrado " + "\"" + self.token.getLexema() + "\"")
         sys.exit(0)
      self.Expr()

   def IfStatement(self):
      # ‘if’ Expr ‘do’ Block
      self.Expr()
      if(not self.eat(Tag.KW_DO)):
         self.sinalizaErroSintatico("Esperado \"DO\", encontrado " + "\"" + self.token.getLexema() + "\"")
         sys.exit(0)
      self.Block()  
         
   def Expr(self):
      # Expr1 Expr’
      self.ExprUm()
      self.ExprLinha()    
   
   def ExprLinha(self):
      # ‘+’ Expr1 Expr’ | ‘-’ Expr1 Expr’ | ε
      if(self.eat(Tag.OP_MAIS) or self.eat(Tag.OP_MENOS)):
         self.ExprUm()
         self.ExprLinha()

   def ExprUm(self):
      # Expr2 Expr1’
      self.ExprDois()
      self.ExprUmLinha() 

   def ExprUmLinha(self):
      # ‘*’ Expr2 Expr1’ | ‘/’ Expr2 Expr1’ | ε
      if(self.eat(Tag.OP_VEZES) or self.eat(Tag.OP_DIVISAO)):
         self.ExprDois()
         self.ExprUmLinha()

   def ExprDois(self):
      # Term
      self.Term() 

   def Term(self):
      # number | ‘:’id
       if(not self.eat(Tag.NUM)):
          if(not self.eat(Tag.SMB_DOIS_PONTOS)):
            self.sinalizaErroSintatico("Esperado \":\", encontrado "  + "\"" + self.token.getLexema() + "\"")
            sys.exit(0)
          if(not self.eat(Tag.ID)):
            self.sinalizaErroSintatico("Esperado \"num, id\", encontrado "  + "\"" + self.token.getLexema() + "\"")
            sys.exit(0)