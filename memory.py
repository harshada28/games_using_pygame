#! /usr/bin/python

import pygame, random, sys
from pygame.locals import *

#define constants
WIDTH = 800
HEIGHT = 800
TILE_SIZE = 80
NUM_TILES = 16
SPACE_BET_TILES = 10
OFFSET = 200
ROW_DIM = 4
COL_DIM = 4

WHITE = (255, 255, 255)
BLUE  = (153, 204, 255)
BLACK = (0,   0,   0)

image_paths = ("images/bunny.jpg", "images/donald.jpg", "images/duck.jpg", "images/jerry.jpg", 
               "images/mickey.jpg", "images/pooh.jpg", "images/popeye.jpg", "images/tom.jpg")
#define globals
expose = []
symbolList = []
board = []
tile_pos = []
state = 0
exposed_first_card = -1
exposed_second_card = -1

def main():
  global screen
  pygame.init()
  screen = pygame.display.set_mode((WIDTH, HEIGHT))
  pygame.display.set_caption("Memory Puzzle")

  screen.fill(BLUE)
  choose_symbol_list2()
  generate_random_board()
  print board
  while True:
    for event in pygame.event.get():
      if event.type == QUIT:
        sys.exit()
      elif event.type == MOUSEBUTTONUP:
        game_logic(pygame.mouse.get_pos())

      draw_board()
      pygame.display.flip()

# symbolList is list of symbols to be used in the board
def choose_symbol_list():
  global symbolList
  symbolList = range (0, NUM_TILES / 2)
  lis = []
  lis = range (0, NUM_TILES / 2)
  symbolList.extend(lis)


def choose_symbol_list2():
  global symbolList
  symbolList = list(image_paths)
  symbolList.extend(list(image_paths))

# Generates board with symbols placed in random positions
# Also initializes expose[][] to False indicating no card is exposed
def generate_random_board():
  global expose
  global symbolList
  symbols = list(symbolList)
  random.shuffle(symbols)
  print symbols
  for i in range (0, ROW_DIM):
    tmp = []
    for j in range (0, COL_DIM):
      tmp.append(symbols[i * ROW_DIM + j])
    board.append(tmp)

  for i in range (0, ROW_DIM):
    temp = []
    for j in range (0, COL_DIM):
      temp.append(False)
    expose.append(temp)

  print expose


def draw_board():
  global tile_pos
  for i in range (0, ROW_DIM):
    for j in range (0, COL_DIM):
      x = OFFSET + j * (TILE_SIZE + SPACE_BET_TILES)
      y = OFFSET + i * (TILE_SIZE + SPACE_BET_TILES)
      #print x, y, x + TILE_SIZE, y + TILE_SIZE
      tile_pos.append([x, x + TILE_SIZE, y, y + TILE_SIZE])
      if expose[i][j] == False:
        pygame.draw.rect(screen, WHITE, (x, y, TILE_SIZE, TILE_SIZE), 0)
      else:
        #draw_number(board[i][j], x, y)
        draw_image(board[i][j], x, y)

def draw_image(img_path, xpos, ypos):
  imageSurface = pygame.image.load(img_path)
  img = pygame.transform.scale(imageSurface, (TILE_SIZE, TILE_SIZE))
  screen.blit(img, (xpos, ypos))

def draw_number(symbol, xpos, ypos):
  fontObj = pygame.font.Font(None, 40)
  textSurface = fontObj.render(str(symbol), False, BLACK)
  screen.blit(textSurface, (xpos - 10 + TILE_SIZE / 2, ypos - 10 + TILE_SIZE / 2))

# Main  game logic sits here
# pos is co-ordinates of mouse click
def game_logic(pos):
  global tile_pos, state
  global exposed_first_card, exposed_second_card

  x = pos[0]
  y = pos[1]
  clicked_tile = -1
  for p in tile_pos:
    if x >= p[0] and x <= p[1] and y >= p[2] and y <= p[3]:
      clicked_tile = tile_pos.index(p)
      break

  if clicked_tile == -1:
    return

  x = clicked_tile / ROW_DIM
  y = clicked_tile % ROW_DIM
  print clicked_tile, x, y
  if expose[x][y] == True:
    return

  if state == 0:
    state = 1
    exposed_first_card = [x, y]
    expose[x][y] = True
    print "First card", exposed_first_card
  elif state == 1:
    state = 2
    exposed_second_card = [x, y]
    expose[x][y] = True
  elif state == 2:
    state = 1
    i = exposed_first_card[0]
    j = exposed_first_card[1]
    p = exposed_second_card[0]
    q = exposed_second_card[1]
    if not board[i][j] == board[p][q] :
      expose[i][j] = False
      expose[p][q] = False
    expose[x][y] = True
    exposed_first_card = [x, y]
  #print pos

def expose_tile(tile):
  if not tile == None:
    x = tile[0]
    y = tile[1]
    exposeState[x][y] = True


if __name__ == '__main__':
  main()
