#! /usr/bin/python

import pygame, random, sys
from pygame.locals import *

# constants
NUM_TILES    = 16
TILE_SIZE    = 80
BOARD_WIDTH  = 700
BOARD_HEIGHT = 500
X_OFFSET     = 120
Y_OFFSET     = 80
COL_DIM      = 4
ROW_DIM      = 4

BLUE   = (51,  153, 255)
PURPLE = (204, 204, 255)
WHITE  = (255, 255, 255)
BLACK  = (0,   0,   0)
GREEN  = (0,   153, 0)

KEYS = (K_UP, K_DOWN, K_RIGHT, K_LEFT)

# define globals
blank_tile_pos = []
state = []
def main():
  global screen
  pygame.init()
  screen = pygame.display.set_mode((BOARD_WIDTH, BOARD_HEIGHT))
  pygame.display.set_caption("Sliding Puzzle")

  generate_board()
  screen.fill(PURPLE)
  while True:
    for event in pygame.event.get():
      if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
        sys.exit(0)
      elif event.type == KEYDOWN and event.key in (KEYS):
        game_logic(event.key)

      draw_board()
    pygame.display.update()


def draw_board():
  global screen, state
  screen.fill(GREEN, (X_OFFSET, Y_OFFSET, TILE_SIZE * (NUM_TILES / 4), TILE_SIZE * (NUM_TILES / 4)))
  for i in range(NUM_TILES / 4):
    for j in range(NUM_TILES / 4):
      x = X_OFFSET + j * (TILE_SIZE)
      y = Y_OFFSET + i * (TILE_SIZE)
      if state[i][j] != None:
        pygame.draw.rect(screen, BLACK, (x, y, TILE_SIZE, TILE_SIZE), 1)
        fontObj = pygame.font.Font(None, 30)
        textSurface = fontObj.render(str(state[i][j]), False, WHITE)
        screen.blit(textSurface, (x - 5 + TILE_SIZE / 2, y - 5 + TILE_SIZE / 2))
      else:
        pygame.draw.rect(screen, PURPLE, (x, y, TILE_SIZE, TILE_SIZE), 0)
        pygame.draw.rect(screen, BLACK, (x, y, TILE_SIZE, TILE_SIZE), 1)

#generates random board
def generate_board():
  global state, blank_tile_pos
  lis = list(range(1, NUM_TILES)) 
  random.shuffle(lis)
  lis.append(None)
  for i in range(NUM_TILES / 4):
    tmp = []
    for j in range(NUM_TILES / 4):
      tmp.append(lis[0])
      lis.pop(0)
    state.append(tmp)

  blank_tile_pos = [ROW_DIM - 1, COL_DIM - 1]
  #print state

# Main game logic sits here
def game_logic(key):
  global blank_tile_pos, state
  if not validate_keypress(key):
    return

  x = blank_tile_pos[0]
  y = blank_tile_pos[1]
  if key == K_RIGHT:
    state[x][y] = state[x][y-1]
    blank_tile_pos = [x, y-1] 
    state[x][y - 1] = None
  elif key == K_LEFT:
    state[x][y] = state[x][y + 1]
    blank_tile_pos = [x, y + 1] 
    state[x][y + 1] = None
  elif key == K_DOWN:
    state[x][y] = state[x-1][y]
    blank_tile_pos = [x - 1, y] 
    state[x - 1][y] = None
  elif key == K_UP:
    state[x][y] = state[x + 1][y]
    blank_tile_pos = [x + 1, y] 
    state[x + 1][y] = None
  #print state
  
def validate_keypress(key):
  global blank_tile_pos
  x = blank_tile_pos[0]
  y = blank_tile_pos[1]

  #print x, y
  if key == K_UP and x == ROW_DIM - 1:
    return False
  elif key == K_DOWN and x == 0:
    return False
  elif key == K_LEFT and y == COL_DIM - 1:
    return False
  elif key == K_RIGHT and y == 0:
    return False

  return True

if __name__ == '__main__':
  main()
