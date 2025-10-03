import pygame
from pygame.locals import *
from sys import *
import random

pygame.init()


FPS = 32
pyclock = pygame.time.Clock()
WIDTH, HEIGHT = 250, 400
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
ICON = pygame.image.load("Assets/Icon.png") 
pygame.display.set_caption("Avi Volans - The Flying Bird")
pygame.display.set_icon(ICON)

MESSAGE = "Assets/Message.png"
BIRD = "Assets/Bird.png"
BIRDUP = "Assets/BirdUp.png"
BIRDDOWN = "Assets/BirdDown.png"
BASE = "Assets/Base.png"
BACKGROUND = "Assets/Background.png"
PIPE = "Assets/Pipe.png"

Game_Sprites = {}
Game_Sprites["message"] = pygame.image.load(MESSAGE).convert_alpha()
Game_Sprites["birdup"] = pygame.image.load(BIRDUP).convert_alpha()
Game_Sprites["birddown"] = pygame.image.load(BIRDDOWN).convert_alpha()
Game_Sprites["bird"] = pygame.image.load(BIRD).convert_alpha()
Game_Sprites["background"] = pygame.image.load(BACKGROUND).convert_alpha()
Game_Sprites["base"] = pygame.image.load(BASE).convert_alpha()
Game_Sprites["pipe"] = pygame.image.load(PIPE).convert_alpha()

score = 0
high_score = 0

def start_screen():
    SCREEN.fill((0, 0, 0))
    global score, high_score
    
    if score > high_score:
        high_score = score
    
    
    running = True
    while running:
        SCREEN.blit(Game_Sprites["background"], (0, 0))
        font = pygame.font.SysFont("comicsansms", 24)
        High_score_text = font.render("High_Score =", True, "White")
        High_score = font.render(str(high_score), True, "red")
    
        SCREEN.blit(High_score_text, (20, 20))
        SCREEN.blit(High_score, (185, 20))
        SCREEN.blit(Game_Sprites["bird"], (50, 120))
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_SPACE, pygame.K_UP]:
                    return
            

        pygame.display.update()
        pyclock.tick(FPS)
    quit()

def random_pipes():
    pipe_height = int(Game_Sprites["pipe"].get_height())
    pipe_gap = 105
    pipe_x = int(WIDTH + 10)

    lower_pipe_y = int(random.randint((325//2), (400 - 180)))
    
    pipe = Game_Sprites["pipe"]
    upper_pipe = {
        "x": pipe_x, 
        "y": lower_pipe_y - pipe_gap - pipe_height,
        "scored": False
    }

    lower_pipe = {
        "x": pipe_x, 
        "y": lower_pipe_y,
        "scored": False
    }

    return upper_pipe, lower_pipe


def game_screen():
    global score, high_score
    scored_pipes = set()
    birdx, birdy = 60, 120
    gravity = 0.7
    velocity = 0
    bird_speedy = 10
    
    pipe_velx = -4
    pipe_spawn_time = 0
    pipes = []

    SCREEN.fill((0, 0, 0))
    score = 0

    while True:
        font1 = pygame.font.SysFont("comicsansms", 22)
        font2 = pygame.font.SysFont("Algerian", 28)
        score_text = font1.render("Score = ", True, "white")
        score_num = font2.render(str(score), True, "lightgreen")
        velocity += gravity
        birdy += velocity
        pipe_spawn_time += 1

        SCREEN.blit(Game_Sprites["background"], (0, 0))

        
        if pipe_spawn_time == 40:
            pipes.append(random_pipes())
            pipe_spawn_time= 0
        
        upper_pipe_img = pygame.transform.rotate(Game_Sprites["pipe"], 180)
        lower_pipe_img = Game_Sprites["pipe"]
        
        for upper_pipe, lower_pipe in pipes:
            SCREEN.blit(upper_pipe_img, (upper_pipe["x"], upper_pipe["y"]))
            SCREEN.blit(lower_pipe_img, (lower_pipe["x"], lower_pipe["y"]))

            upper_pipe["x"] += pipe_velx
            lower_pipe["x"] += pipe_velx

        for upper_pipe, lower_pipe in pipes:
            pipe_mid_pos = lower_pipe["x"] + Game_Sprites["pipe"].get_width() // 2
            if pipe_mid_pos < birdx and not lower_pipe["scored"]:
                score += 1
                lower_pipe["scored"] = True
            
        pipes = [pair for pair in pipes if pair[0]["x"] >= -50]

        SCREEN.blit(Game_Sprites["base"], (0, 325))
        if velocity == 0:
            SCREEN.blit(Game_Sprites["bird"], (birdx, birdy))
        elif velocity >= 1:
            SCREEN.blit(Game_Sprites["birddown"], (birdx, birdy))
        else:
            SCREEN.blit(Game_Sprites["birdup"], (birdx, birdy))
        
        for upper_pipe, lower_pipe in pipes:
            if is_collided(upper_pipe["x"], upper_pipe["y"], birdx, birdy, velocity) or is_collided(lower_pipe["x"], lower_pipe["y"], birdx, birdy, velocity):
                if score > high_score:
                    high_score = score
                pygame.time.wait(1000)
                return
                


        SCREEN.blit(score_num, (170, 13))
        SCREEN.blit(score_text, (70, 10))

        for event in pygame.event.get():
            if event.type == QUIT:
                break
                exit()
            
            if (event.type == KEYDOWN and event.key in [pygame.K_SPACE, pygame.K_UP]) or (event.type == MOUSEBUTTONDOWN):
                velocity = -bird_speedy            

            if birdy <= 2:
                birdy = 2
        if birdy >= 315:
            if score > high_score:
                high_score = score
            pygame.time.wait(1000)
            return
        
        

        pygame.display.update()
        pyclock.tick(FPS)
    
def is_collided(pipex, pipey, birdx, birdy, velocity):
    pipe_width = Game_Sprites["pipe"].get_width()
    pipe_height = Game_Sprites["pipe"].get_height()
    bird_width = Game_Sprites["bird"].get_width()
    bird_height = Game_Sprites["bird"].get_height()
    

    pipe_mask = pygame.mask.from_surface(Game_Sprites["pipe"])
    
    
    if velocity < 0:
        bird_img = Game_Sprites["birdup"]
    elif velocity > 0:
        bird_img = Game_Sprites["birddown"]
    else:
        bird_img = Game_Sprites["bird"]
        

    bird_mask = pygame.mask.from_surface(bird_img)


    if pipe_mask.overlap(bird_mask, (int(birdx - pipex), int(birdy - pipey))):
        return True
    return False

if __name__ == "__main__":
    while True:
        start_screen()
        game_screen()