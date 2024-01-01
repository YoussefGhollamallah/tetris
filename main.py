import pygame
from shapes import shapes, colors
import random
import os

pygame.init()
#taille grille
width = 300
height = 600
block = 30  # 600//30 -> 20 300 // 30 -> 10  # la dimension des blocks
#taille fenetre
screen_w = 600 
screen_h = 650
black = (0, 0, 0) # le blackground

tlx = 50
tly = 50

class Piece:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape#les piece de jeu 
        self.color = colors[shapes.index(shape)]
        self.rotate = 0
        

def valide(shape, grille):
    accept = [[(j, i) for j in range (10)if grille[i][j] == black] for i in range (20)]
    accept = [i for sub in accept for i in sub]

    piece = convert(shape)

    for pos in piece:
        if pos not in accept:
            if pos[1] > -1:
                return False
    return True

def show_score(screen, score, best):
    font = pygame.font.SysFont('arial', 30)
    label = font.render(f'Score : {score*10}', 1, (255, 255, 255))
    label2 = font.render(f'Best Score : {best * 10}', 1, (255, 255, 255))
    x = tlx + width + 50
    y = tly + height // 4 + 100
    screen.blit(label, (x, y))
    screen.blit(label2, (x, y - 100))
    
def lire_best_score():
    if os.path.exists("score.txt"):
        with open("score.txt", "r") as fichier:
            try:
                best_score = int(fichier.read())
            except ValueError:
                best_score = 0
    else:
        best_score = 0
    return best_score

def enregistrer_best_score(best_score):
    with open("score.txt", "w") as fichier:
        fichier.write(str(best_score))
        
        best_score = lire_best_score()


def convert(shape): #convertir piece
    pos = []
    piece = shape.shape[shape.rotate % len(shape.shape)]
    for i, line in enumerate(piece):
        for j, case in enumerate(line):
            if case == '0':
                pos.append((shape.x+j, shape.y+i))
                
    return pos


def cree_grille(static): # def pour créer les variable I et J pour creer la grille et choisir la couleur des cases
    grille = [[black for _ in range(10)] for _ in range(20)]
    for i in range (len(grille)):
        for j in range(len(grille[i])):
            if (j, i) in static:
                grille[i] [j] = static[(j, i)]
                
    return grille


def draw_grille(screen, grille): # grille du plateau de jeu
    for i in range(len(grille)):
        pygame.draw.line(screen, (255, 255, 255), (tlx, tly+i*block), (tlx + width, tly +i*block)) #ligne x
        for j in range(len(grille[i])):
            pygame.draw.line(screen, (255, 255, 255), (tlx + j*block, tly), (tlx + j*block, tly + height)) #ligne y
        pygame.draw.rect(screen, (0, 255, 0), (tlx, tly, width, height), 4) #bordure de la grille de jeu 
        
            
# dessiner la fenetre
def draw_windows(screen, grille):
    screen.fill(black)
    for i in range(len(grille)):   
        for j in range(len(grille[i])):
            pygame.draw.rect(screen, grille[i][j], (tlx + j*block, tly + i*block, block, block), 0)
    draw_grille(screen, grille)  


def draw_next(screen, shape):
    font = pygame.font.SysFont('arial', 25)
    label = font.render('Next Piece', 1, (255, 255, 255))
    x = tlx + width + 50
    y = tly + height // 2 + 100
    piece = shape.shape[shape.rotate % len(shape.shape)]
    for i, line in enumerate(piece):
        for j, case in enumerate(line):
            if case == '0':
                pygame.draw.rect(screen, shape.color, (x + (1 +j) * block, y + (1 + i) * block, block, block), 0)
    screen.blit(label, (x + 5, y - 30))
    
def play_sound(sound):
    music = pygame.mixer.Sound(sound)
    music.play(-1)
    

    
def get_piece():
    return Piece(4, 0, random.choice(shapes)) #placer les pieces au coordonnées 4, 0

def check_row(grille, static): #verifier si ils sont en ligne ou  pas
    inc = 0
    for i in range(len(grille)-1, -1, -1):
        if black not in grille[i]: #verifier si la ligne n'est plus noir
            inc += 1
            ind = i
            for j in range(len(grille[i])):
                try:
                    del static[(j, i)] #supprimer la ligne pleine
                except:
                    continue
    if inc > 0:
        for key in sorted(list(static), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                new_key = (x, y + inc)
                static[new_key] = static.pop(key)
    return inc
 

def lost(static):
    for pos in static:
        x, y = pos
        if y < 1:
            return True
    return False

def main(screen):
    static = {}
    change = False
    run = True
    grille = cree_grille(static)
    current = get_piece()
    next_piece = get_piece()
    
    clock = pygame.time.Clock()
    time = 0
    speed = 0.30
    score = 0
    
    while run:
        with open('score.txt', 'r') as file:
            best_score = int(file.read())
            
        grille = cree_grille(static)
        clock.tick()
        time += clock.get_rawtime()
        
        if time / 1000 > speed:
            time = 0
            current.y += 1
            if not valide(current, grille):
                current.y -= 1
                change = True
            score += check_row(grille, static)
                
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current.x -= 1
                    if not valide(current, grille):
                        current.x += 1
                if event.key == pygame.K_RIGHT:
                    current.x += 1
                    if not valide(current, grille):
                        current.x -= 1
                if event.key == pygame.K_UP:
                    current.rotate += 1
                    if not valide(current, grille):
                        current.rotate -= 1
                if event.key == pygame.K_DOWN:
                    current.y += 1
                    if not valide(current, grille):
                        current.y -= 1

                    

        shape_pos = convert(current)
        for i in shape_pos:
            x, y = i
            if y > -1:
                grille[y][x] = current.color

        if change:
            for pos in shape_pos:
                static[pos] = current.color
            current = next_piece
            next_piece = get_piece()
            change = False

        
                    
        draw_windows(screen, grille)
        draw_next(screen, next_piece)
        show_score(screen, score, best_score)
        pygame.display.flip()
        if lost(static):
            run = False
        if score > best_score:
            best_score = score
            enregistrer_best_score(best_score)  # Enregistre le meilleur score
        elif score < best_score:
            enregistrer_best_score(best_score)  # Ne modifie le fichier que si le score actuel est supérieur
        play_sound('Tetris.wav')

screen = pygame.display.set_mode((screen_w, screen_h))    
main(screen)
pygame.quit()       