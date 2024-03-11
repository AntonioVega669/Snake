import pygame
import sys
import subprocess

pygame.init()

# Define colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Inicializa la pantalla
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Menú Pygame")

# Nueva constante para representar el estado del juego Snake
STATE_SNAKE = "snake"

# Estado inicial
current_state = "menu"

# Función para mostrar texto en la pantalla
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

# Función para abrir el juego Snake
def abrir_juego_snake():
    subprocess.run(['python', 'C:\python\Poo\snake.py'])

# Función principal del menú
def main_menu():
    while True:
        screen.fill(WHITE)
        draw_text('Menú Principal', pygame.font.Font(None, 36), BLACK, screen, 200, 30)

        mx, my = pygame.mouse.get_pos()

        button_start = pygame.Rect(150, 100, 200, 50)
        pygame.draw.rect(screen, BLACK, button_start)
        if button_start.collidepoint((mx, my)):
            if pygame.mouse.get_pressed()[0]:
                print('Iniciar Juego')
                return "game"  # Cambia al estado de juego

        button_members = pygame.Rect(150, 160, 200, 50)
        pygame.draw.rect(screen, BLACK, button_members)
        if button_members.collidepoint((mx, my)):
            if pygame.mouse.get_pressed()[0]:
                print('Ver Integrantes')
                return "members"  # Cambia al estado de integrantes

        button_exit = pygame.Rect(150, 220, 200, 50)
        pygame.draw.rect(screen, BLACK, button_exit)
        if button_exit.collidepoint((mx, my)):
            if pygame.mouse.get_pressed()[0]:
                print('Salir del Juego')
                pygame.quit()
                sys.exit()

        draw_text('     Iniciar Snake', pygame.font.Font(None, 24), WHITE, screen, 200, 115)
        draw_text('     Ver Integrantes', pygame.font.Font(None, 24), WHITE, screen, 200, 175)
        draw_text('     Salir del Juego', pygame.font.Font(None, 24), WHITE, screen, 200, 235)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()

# Función para mostrar información sobre los integrantes
def show_members():
    while True:
        screen.fill(WHITE)
        draw_text('Programa creado por:', pygame.font.Font(None, 30), BLACK, screen, 200, 50)
        draw_text('Jesus Antonio Vega Barbosa', pygame.font.Font(None, 24), BLACK, screen, 200, 100)
        draw_text('Angel Miguel Reyes Velasco', pygame.font.Font(None, 24), BLACK, screen, 200, 150)

        mx, my = pygame.mouse.get_pos()

        button_back = pygame.Rect(150, 220, 200, 50)
        pygame.draw.rect(screen, BLACK, button_back)
        if button_back.collidepoint((mx, my)):
            if pygame.mouse.get_pressed()[0]:
                print('Regresar al Menú Principal')
                return "menu"  # Cambia al estado del menú principal

        draw_text('Regresar al Menú', pygame.font.Font(None, 24), WHITE, screen, 200, 235)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if button_back.collidepoint(event.pos):
                    return "menu"

        pygame.display.update()

# Función principal del juego
def game():
    while True:
        screen.fill(WHITE)
        draw_text('¡Bienvenido al Juego!', pygame.font.Font(None, 36), BLACK, screen, 200, 30)

        mx, my = pygame.mouse.get_pos()

        # Nuevo botón para iniciar el juego Snake
        button_snake = pygame.Rect(150, 150, 200, 50)
        pygame.draw.rect(screen, BLACK, button_snake)
        if button_snake.collidepoint((mx, my)):
            if pygame.mouse.get_pressed()[0]:
                print('Iniciar Snake')
                abrir_juego_snake()
                return "menu"  # Regresar al menú después de salir del juego Snake

        draw_text('Iniciar Snake', pygame.font.Font(None, 24), WHITE, screen, 200, 175)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()

# Ciclo principal del programa
while True:
    if current_state == "menu":
        current_state = main_menu()
    elif current_state == "game":
        current_state = game()
    elif current_state == "members":
        current_state = show_members()