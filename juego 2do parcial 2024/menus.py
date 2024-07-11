import pygame
from funciones import *
from materiales import *
import sys


black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 255)
red =  (255,0,0)


font = None

################### FUNCIONES DE CONSTRUCCION ######################

def initialize_font():
    global font
    font = pygame.font.SysFont(None, 50)

def draw_button(text, x, y, w, h, screen):
    pygame.draw.rect(screen, white, (x, y, w, h))
    button_text = font.render(text, True, black)
    text_rect = button_text.get_rect(center=(x + w / 2, y + h / 2))
    screen.blit(button_text, text_rect)

#####################################################################


def main_menu(screen,fondo_madera):
    while True:
        screen.blit(fondo_madera,(0,0))
        draw_button("Jugar", 400, 300, 450, 100, screen)
        draw_button("Puntajes", 400, 500, 450, 100, screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if 400 <= mouse_x <= 750:
                    if 300 <= mouse_y <= 400:
                        return "Jugar"
                    elif 500 <= mouse_y <= 600:
                        return "Puntajes"
        
        pygame.display.flip()

def show_message(screen,fondo_madera):
    while True:
        screen.blit(fondo_madera,(0,0))
        conjunto_puntajes = leer_datos()
        y_offset = 50
        for puntaje in conjunto_puntajes:
            texto = f"Nombre: {puntaje['nombre']} Puntaje: {puntaje['puntaje']}"
            texto_superficie = font.render(texto, True, (0, 0, 255))
            screen.blit(texto_superficie, (50, y_offset))
            y_offset += 70
        


        draw_button("Volver al Menú", 400, 700, 450, 100, screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if 400 <= mouse_x <= 750 and 700 <= mouse_y <= 800:
                    return
        
        pygame.display.flip()

def main(screen,alto,ancho,fondo_madera):
    initialize_font()
    while True:
        option = main_menu(screen,fondo_madera)
        if option == "Jugar":
            return False
        elif option == "Puntajes":
            show_message(screen,fondo_madera)



########################### Pantalla Perdiste ###########################

def perdiste(screen,puntaje,input_box, text, fondo_madera):
    initialize_font()
    while True:
        option = menu_perdiste(screen, fondo_madera)
        if option == "Volver al menu":
            return True
        elif option == "Guardar puntaje":
            guardar(screen,puntaje, input_box, text, fondo_madera)
            return True

def menu_perdiste(screen,fondo_madera):
    while True:
        screen.blit(fondo_madera,(0,0))
        draw_button("Volver al menu", 400, 300, 450, 100, screen)
        draw_button("Guardar puntaje", 400, 500, 450, 100, screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if 400 <= mouse_x <= 750:
                    if 300 <= mouse_y <= 400:
                        return "Volver al menu"
                    elif 500 <= mouse_y <= 600:
                        return "Guardar puntaje"
        
        pygame.display.flip()

def guardar(screen,puntaje,input_box, text, fondo_madera):
    guardado = True
    while guardado == True:
        screen.blit(fondo_madera,(0,0))
        pygame.display.flip()
        guardado = agregar_dato(puntaje, screen,input_box,font, text)

    message = font.render("datos guardados", True, blue)
    message_rect = message.get_rect(center=((1200 / 2), 1000 / 2))
    screen.blit(message, message_rect)

    while True:
        draw_button("Volver al Menú", 400, 700, 450, 100, screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if 400 <= mouse_x <= 750 and 700 <= mouse_y <= 800:
                    return
            
            pygame.display.flip()