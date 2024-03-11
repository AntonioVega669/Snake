import math
import random
import pygame
import tkinter as tk
from tkinter import simpledialog
import subprocess
import sys 

# Clase hijo
class cube(object):
    rows = 20
    w = 500

    def __init__(self, start, dirnx=1, dirny=0, color=(255, 0, 0)):
        self.pos = start
        self.dirnx = dirnx
        self.dirny = dirny
        self.color = color

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]

        pygame.draw.rect(surface, self.color, (i * dis + 1, j * dis + 1, dis - 2, dis - 2))
        if eyes:
            centre = dis // 2
            radius = 3
            circleMiddle = (i * dis + centre - radius, j * dis + 8)
            circleMiddle2 = (i * dis + dis - radius * 2, j * dis + 8)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle, radius)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle2, radius)


# Clase padre
class snake(object):
    body = []
    turns = {}

    def __init__(self, color, pos, speed=8):
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1
        self.speed = speed

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.dirnx = -1
            self.dirny = 0
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        elif keys[pygame.K_RIGHT]:
            self.dirnx = 1
            self.dirny = 0
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        elif keys[pygame.K_UP]:
            self.dirnx = 0
            self.dirny = -1
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        elif keys[pygame.K_DOWN]:
            self.dirnx = 0
            self.dirny = 1
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body) - 1:
                    self.turns.pop(p)
            else:
                if c.dirnx == -1 and c.pos[0] <= 0:
                    # Muere si choca con el borde izquierdo
                    self.reset((10, 10))
                    break
                elif c.dirnx == 1 and c.pos[0] >= c.rows - 1:
                    # Muere si choca con el borde derecho
                    self.reset((10, 10))
                    break
                elif c.dirny == 1 and c.pos[1] >= c.rows - 1:
                    # Muere si choca con el borde inferior
                    self.reset((10, 10))
                    break
                elif c.dirny == -1 and c.pos[1] <= 0:
                    # Muere si choca con el borde superior
                    self.reset((10, 10))
                    break
                else:
                    c.move(c.dirnx, c.dirny)

    def reset(self, pos):
        global score # Agrega la referencia a la variable global score
        score = 0   # Restablece el marcador a cero
        self.head = cube(pos)
        self.body = [self.head]
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0] - 1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0] + 1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0], tail.pos[1] - 1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0], tail.pos[1] + 1)))

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    def draw(self, surface):
        for i, c in enumerate(self.body):
            c.draw(surface, i == 0)


def drawGrid(w, rows, surface):
    sizeBtwn = w // rows

    x = 0
    y = 0
    for l in range(rows):
        x = x + sizeBtwn
        y = y + sizeBtwn

        pygame.draw.line(surface, (0, 0, 255), (x, 0), (x, w))
        pygame.draw.line(surface, (0, 0, 255), (0, y), (w, y))


def redrawWindow(surface, score):
    global rows, width, s, snack
    surface.fill((0, 0, 0))
    s.draw(surface)
    snack.draw(surface)
    drawGrid(width, rows, surface)
    
    # Agrega la puntuacion en la esquina superior izquierda
    font = pygame.font.Font(None, 25)
    score_text = font.render("Score: " + str(score), True, (255, 255, 255))
    surface.blit(score_text, (10, 10))
    
    pygame.display.update()


def randomSnack(rows, item):
    positions = item.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:
            continue
        else:
            break

    return x, y


from tkinter import messagebox

def message_box(subject, content):
    result = messagebox.askquestion(subject, content + "\n\n¿Quieres jugar de nuevo?")
    
    if result == 'yes':
        main()  # Reinicia el juego
    elif result == 'no':
        subprocess.run(["python", "C:/python/Poo/PruebadeMenu.py"])  # Ejecuta PruebadeMenu.py



def main():
    global width, rows, s, snack, score 
    width = 500
    rows = 20
    win = pygame.display.set_mode((width, width))
    s = snake((255, 0, 0), (10, 10), speed=10)
    snack = cube(randomSnack(rows, s), color=(0, 255, 0))
    flag = True
    score = 0
    
    # Inicializa el modulo de fuentes de pygame
    pygame.font.init()

    clock = pygame.time.Clock()

    while flag:
        pygame.time.delay(50)
        clock.tick(s.speed)
        s.move()
        
        if (
            s.body[0].pos[0] < 0
            or s.body[0].pos[0] >= rows
            or s.body[0].pos[1] < 0
            or s.body[0].pos[1] >=rows
        ):
            
            print('Score: ', score)
            message_box('Perdiste!', '¿Quieres jugar de nuevo?')
            flag = False  # Terminar el juego
            
        if s.body[0].pos == snack.pos:
            s.addCube()
            snack = cube(randomSnack(rows, s), color=(255, 0, 0))
            score += 1
            
        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z: z.pos, s.body[x + 1:])):
                print('Score: ', score)
                message_box('Perdiste!', '¿Quieres jugar de nuevo?')
                flag = False  # Terminar el juego
                break

        redrawWindow(win, score)

    pygame.quit()

main()