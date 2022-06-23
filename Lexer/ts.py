from tag import Tag
from token import Token
class TS:
   '''
   Classe para a tabela de simbolos representada por um dicionario: {'chave' : 'valor'}
   '''
   def __init__(self):
      self.ts = {}
      self.ts['program'] = Token(Tag.KW_PROGRAM, 'program') 
      self.ts['forward'] = Token(Tag.KW_FORWARD, 'forward')     
      self.ts['begin'] = Token(Tag.KW_BEGIN, 'begin')
      self.ts['turn'] = Token(Tag.KW_TURN, 'turn')
      self.ts['degrees'] = Token(Tag.KW_DEGREES, 'degrees')
      self.ts['if'] = Token(Tag.KW_IF, 'if')
      self.ts['repeat'] = Token(Tag.KW_REPEAT, 'repeat')
      self.ts['do'] = Token(Tag.KW_DO, 'do')
      self.ts['end'] = Token(Tag.KW_END, 'end')
      self.ts['print'] = Token(Tag.KW_PRINT, 'print')

   def getToken(self, lexema):
      token = self.ts.get(lexema)
      return token

   def addToken(self, lexema, token):
      self.ts[lexema] = token

   def printTS(self):
      for k, t in self.ts.items():
         print(k, ":", t.toString())
