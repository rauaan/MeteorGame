import pygame
import math, random
import time

score = 0
player_speed=5
FPS = 60 
WIDTH = 600#1900
HEIGHT = 400#1080
speed = 3
SPAWN_RATE = 2
scroll = 0


def main():
  pygame.init()
  clock = pygame.time.Clock()
  
  #create game window
  screen = pygame.display.set_mode((WIDTH, HEIGHT))
  pygame.display.set_caption("Orion Hunter GAVI Edition")


  #FOR MOVING BACKGROUND
  bg = pygame.image.load("bgspace.png").convert()
  bg_width = bg.get_width()
  
  tiles = math.ceil(WIDTH / bg_width) + 1

  #my player
  player = pygame.image.load("mainchar.png")
  p1 = pygame.transform.scale(player, (50, 50))

  for i in range(0, 5):
    t1 = time.time()
    gameLoop(screen, bg, p1, tiles, bg_width, t1)
  #FOR MOVING METEORITES

  #we also (by we i mean rauan but this was written by altynay) mixed update and clock.fps functions koroche swap
  clock.tick(FPS)
  pygame.quit()

def GAMEOVER(screen, bg):
  global score
  score = 0 #global bc this function doesnt know score its outside the function gameover
  screen.blit(bg, (0, 0))
  print("Game over: YOU DIED")
  pygame.display.flip()  # Update the display
  pygame.time.delay(4000)

def gameLoop(screen, bg, p1, tiles, bg_width, t1):
  x=0
  y=0
  badrectangles = []

  meteor=pygame.image.load('meteor.png').convert_alpha()
  m1=pygame.transform.scale(meteor, (50, 50))
  
  run = True
  while run:
    global scroll

    #moving bg
    for i in range(0, tiles):
      screen.blit(bg, (i * bg_width + scroll, 0))

    #scroll background
    scroll -= 5

    #reset scroll
    if abs(scroll) > bg_width:
      scroll = 0

    #event handler
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False

    #MOVES GAVI
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
      x -= player_speed
    if keys[pygame.K_RIGHT]:
      x += player_speed
    if keys[pygame.K_UP]:
      y -= player_speed
    if keys[pygame.K_DOWN]:
      y += player_speed
    screen.blit(p1, (x,y))


    #CHANCE OF A METEORITE SPAWNING
    if random.randint(0, 100) < SPAWN_RATE:
      new_rect = pygame.Rect(WIDTH, random.randint(0, HEIGHT), 50, 50)
      screen.blit(m1, new_rect)
      badrectangles.append(new_rect)

    #THATS HOW METEORITES MOVE
    for rect in badrectangles:
      rect.x = rect.x - speed
      screen.blit(m1, rect)
    #REMOVES OFF SCREEN METEORITES
      if rect.x < 0:
        badrectangles.remove(rect)

    #FOR SCORE
    font=pygame.font.SysFont("Times New Roman", 28)
    white=(255,255,255)
    global score
    t2 = time.time()
    score=int(t2-t1)
    Text=font.render("score: "+ str(score), True, white)
    screen.blit(Text, (10, 10))

    #CHECKS FOR COLLISIONS
    if p1.get_rect().collidelist(badrectangles) != -1:
      GAMEOVER(screen, bg)
      run = False
    pygame.display.update()

main()