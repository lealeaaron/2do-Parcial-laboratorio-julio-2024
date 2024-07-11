import pygame
from funciones import *
from class_barco import *
from materiales import *
from modo import *
from menus import *

#Aaron Leale 11/07/2024
#2do parcial
####################################### PANTALLA #######################################

pygame.init()  # Inicializa todos los módulos de pygame
pygame.mixer.init()


choque_sfx = pygame.mixer.Sound("recursos\chocar.mp3")
choque_sfx.set_volume(0.2)


pygame.mixer.music.load("recursos\musica barco.mp3")
pygame.mixer.music.set_volume(0.2)



ALTO = 1000 
ANCHO = 1200

FPS = 60
RELOJ = pygame.time.Clock() #usa los fps en el main

SCREEN = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("primer juego")

font = pygame.font.SysFont(None, 75)


####################################### BORDES #######################################



borde_1 = crear_plataforma(False, (1200,1), (0,899))
borde_2 = crear_plataforma(False, (1,900), (0,0))
borde_3 = crear_plataforma(False, (1,900), (1199,0))
borde_4 = crear_plataforma(False, (1200,1), (0,0))

lista_bordes = [borde_1,borde_2,borde_3,borde_4]



####################################### ANIMACIONES #######################################

#Personaje
diccionario_animaciones = {}
diccionario_animaciones["derecha"] = barco_derecha
diccionario_animaciones["izquierda"] = barco_izquierda
diccionario_animaciones["arriba"] = barco_arriba
diccionario_animaciones["abajo"] = barco_abajo

#obstaculos
diccionario_obstaculos = {}
diccionario_obstaculos["iceberg_1"] = iceberg_1
diccionario_obstaculos["iceberg_2"] = iceberg_2
diccionario_obstaculos["iceberg_3"] = iceberg_3
diccionario_obstaculos["iceberg_4"] = iceberg_4


######################################### JUGADOR #########################################
input_box = pygame.Rect(400, 300, 140, 32)
text = ''
posicion_x = 530
posicion_y = 380
bonus = None
objetivo = None 
al_menu = True



#le pasa los atributos al class_personaje
jugador = Barco(diccionario_animaciones,posicion_x,posicion_y,(70,70), 4, "arriba")


def pausar():
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_p:
                    pygame.mixer.music.unpause()
                    return
        show_pause_screen()

def show_pause_screen():
    text = font.render("Pausa", True, (255,255,255))
    pygame.draw.rect(SCREEN, (0,0,255), (0, 900, 1200, 100), 100)
    SCREEN.blit(text, (540, 920))
    pygame.display.flip()






is_running = True
while is_running:

    while al_menu == True:
        al_menu = main(SCREEN,ALTO,ANCHO,fondo_madera)
        pygame.mixer.music.play(-1)


    RELOJ.tick(FPS)
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            is_running = False
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_TAB:
                cambiar_modo()
            if evento.key == pygame.K_p:
                pygame.mixer.music.pause()
                pausar()


    teclas = pygame.key.get_pressed()


    if teclas[pygame.K_RIGHT]:
        jugador.que_hace = "derecha"
        #jugador.flag_disparo = True
    elif teclas[pygame.K_LEFT]:
        jugador.que_hace = "izquierda"
        #jugador.flag_disparo = True
    elif teclas[pygame.K_DOWN]:
        jugador.que_hace = "abajo"
        #jugador.flag_disparo = True
    elif teclas[pygame.K_UP]:
        jugador.que_hace = "arriba"
        #jugador.flag_disparo = True
    


    # Blitear fondo
    SCREEN.blit(mar,(0,0))

    #blitear panel
    panel = pygame.draw.rect(SCREEN, (0,0,255), (0, 900, 1200, 100), 100)


    #blitear al jugador y verificar colisiones
    objetivo, bonus, al_menu = jugador.actualizar(SCREEN, lista_bordes, objetivo, bonus, al_menu, font, input_box, text, fondo_madera, choque_sfx)



    if obtener_modo():
        pygame.draw.rect(SCREEN, "pink", jugador.hitbox, 3)
        if objetivo is not None:
            pygame.draw.rect(SCREEN, "pink", objetivo["rectangulo"], 3)
        if bonus is not None:
            pygame.draw.rect(SCREEN, "pink", bonus["rectangulo"], 3)
        for borde in lista_bordes:
            pygame.draw.rect(SCREEN, "red", borde["rectangulo"], 3)
        for iceberg in jugador.lista_obstaculos:
            pygame.draw.rect(SCREEN, "red", iceberg["rectangulo"], 3)




    # Actualizar la pantalla
    pygame.display.flip()

pygame.quit()