'''

@author: Paulo Cheque (paulocheque@gmail.com)

Commom constants, do: from cardgameengine.constants import *
'''

# Common values
JOKER = '0'
AS = 'AS'
J = 'J'
Q = 'Q'
K = 'K'

# Commom suits

# Anglo-American
SPADES = 1
HEARTS = 2
DIAMONDS = 3
CLUBS = 4

# Italian
COINS = DIAMONDS
SWORDS = SPADES
CUPS = HEARTS
CLUBS = CLUBS

# German
HEARTS = HEARTS
BELLS = DIAMONDS
LEAVES = SPADES
ACORNS = CLUBS

# Portuguese
ESPADAS = SPADES
COPAS = HEARTS
OUROS = DIAMONDS
PAUS = CLUBS

# Spanish
ESPADAS = SPADES
COPAS = HEARTS
OROS = DIAMONDS
BASTOS = CLUBS

# SUITS CODES: Unicode, Decimal, Hexadecimal, shortcut / http://en.wikipedia.org/wiki/Playing_cards

def decimalToHtml(code):
  return '&#' + code + ';'

def hexadecimalToHtml(code):
  return '&#x' + code + ';'

def shortcutToHtml(code):
  return '&' + code + ';'

def unicode(code):
  return 'U+' + code

BLACK_SPADE_SUIT_DECIMAL = '9824'
BLACK_SPADE_SUIT_HEXADECIMAL = '2660'
BLACK_SPADE_SUIT_SHORTCUT = '&spades;'

WHITE_SPADE_SUIT_DECIMAL = '9828'
WHITE_SPADE_SUIT_HEXADECIMAL = '2664'

WHITE_HEART_SUIT_DECIMAL = '9825'
WHITE_HEART_SUIT_HEXADECIMAL = '2661'

BLACK_HEART_SUIT_DECIMAL = '9829'
BLACK_HEART_SUIT_HEXADECIMAL = '2665'
BLACK_HEART_SUIT_SHORTCUT = 'hearts'

WHITE_DIAMOND_SUIT_DECIMAL = '9826'
WHITE_DIAMOND_SUIT_HEXADECIMAL = '2662'

BLACK_DIAMOND_SUIT_DECIMAL = '9830'
BLACK_DIAMOND_SUIT_HEXADECIMAL = '2666'
BLACK_DIAMOND_SUIT_SHORTCUT = 'diams'

BLACK_CLUB_SUIT_DECIMAL = '9827'
BLACK_CLUB_SUIT_HEXADECIMAL = '2663'
BLACK_CLUB_SUIT_SHORTCUT = 'clubs'

WHITE_CLUB_SUIT_DECIMAL = '9831'
WHITE_CLUB_SUIT_HEXADECIMAL = '2667'
