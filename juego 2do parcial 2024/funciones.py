import pygame
from random import randint
import json
import os
import sys


def crear_rectangulo(screen, color, x, y, width, height, thickness=0):
    """
    Dibuja un rectángulo en la pantalla.

    Parámetros:
    screen -- superficie donde se dibujará el rectángulo
    color -- color del rectángulo (tuple RGB)
    x -- coordenada x del rectángulo
    y -- coordenada y del rectángulo
    width -- ancho del rectángulo
    height -- altura del rectángulo
    thickness -- grosor del borde del rectángulo (0 para rectángulo lleno)
    """

    pygame.draw.rect(screen, color, (x, y, width, height), thickness)

##############################################################################################################


# SE UTILIZA PARA LA CREACION DE ICEBERGS Y OBJETIVOS 

def crear_plataforma(es_visible, tamaño, posicion, path = "" ) -> dict:
    plataforma = {}
    if es_visible:
        plataforma["superficie"] = pygame.image.load(path)
        plataforma["superficie"] = pygame.transform.scale(plataforma["superficie"], tamaño)
    else:
        plataforma["superficie"] = pygame.Surface(tamaño)
    
    plataforma["rectangulo"] = plataforma["superficie"].get_rect()

    x, y = posicion

    plataforma["rectangulo"].x = x
    plataforma["rectangulo"].y = y

    return plataforma

##############################################################################################################


# CREA LOS CONJUNTOS DE ICEBERGS

def crear_iceberg(lista_obstaculos, jugador, objetivo, bonus):
    while True:
        nuevo_iceberg = crear_plataforma(True, (60,60), (randint(1,1140),randint(1,840)),r"recursos\iceberg 1.png")
        colisiona = False

        for obstaculo in lista_obstaculos:
            if nuevo_iceberg["rectangulo"].colliderect(obstaculo["rectangulo"]):
                colisiona = True
                break

        if objetivo is not None:
            if nuevo_iceberg["rectangulo"].colliderect(objetivo["rectangulo"]):
                colisiona = True

        if bonus is not None:
            if nuevo_iceberg["rectangulo"].colliderect(bonus["rectangulo"]):
                colisiona = True

        if nuevo_iceberg["rectangulo"].colliderect(jugador.hitbox):
            colisiona = True

        if not colisiona:
            lista_obstaculos.append(nuevo_iceberg)
            break

            


##############################################################################################################


### evita que el objetivo se sobreponga sobre el jugador/los icebergs 

#icebergs
def colisiona_con_lista(rectangulo, lista_obstaculos):
    for obstaculo in lista_obstaculos:
        if rectangulo.colliderect(obstaculo["rectangulo"]):
            return True
    return False

#jugador
def colisiona_con_jugador(rectangulo, jugador):
    return rectangulo.colliderect(jugador.hitbox)









############################ IMAGENES Y ANIMACIONES ##########################

def reescalar_imagenes(animaciones, tamaño):# se usa en los class
    for clave in animaciones:
        animaciones[clave] = pygame.transform.scale(animaciones[clave], tamaño)


def girar_imagenes(imagen, flip_x, flip_y ):# se usa en materiales
    imagen_girada = pygame.transform.flip(imagen, flip_x, flip_y)
    return imagen_girada




#def reescalar_animaciones(animaciones, tamaño):# se usa en los materiales
#    for i in range(len(animaciones)):
#        superficie = animaciones[i]
#        animaciones[i] = pygame.transform.scale(superficie, tamaño)



#def animar_fondo(conjunto,screen):
#    largo = len(conjunto)
#    for imagen in conjunto:
#        contador_posicion += 1
#        if contador_posicion >= largo:
#            contador_posicion = 0
#
#       
#        screen.blit(conjunto[contador_posicion],(0,0))



########################## carga de datos ######################

def agregar_dato(numero, screen,input_box,font,text):
    
    # Solicitar el nombre por pantalla
    nombre = ingreso_nombre(input_box,screen,font,text)


    # Crear un diccionario con los datos ingresados
    datos = {
        "nombre": nombre,
        "puntaje": numero
    }

    # Verificar si el archivo json ya existe
    if os.path.exists("puntajes.json"):
        # Si el archivo existe, cargar los datos previos
        with open("puntajes.json", "r") as archivo:
            datos_previos = json.load(archivo)
    else:
        # Si el archivo no existe, crear una lista vacía para almacenar los datos
        datos_previos = []

    # Agregar los nuevos datos a la lista de datos previos
    datos_previos.append(datos)

    # Guardar todos los datos en el archivo json
    with open("puntajes.json", "w") as archivo:
        json.dump(datos_previos, archivo, indent=4)
    return False




def ingreso_nombre(input_box,screen,font,text):
    done = False
    active = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Si el usuario hace clic en el cuadro de entrada de texto
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        return text
                        text = ''
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode


        screen.fill((30, 30, 30))
        draw_input_box(screen, text, (255,0,0), input_box, font)

        pygame.display.flip()


    pygame.quit()
    sys.exit()

def draw_input_box(screen, text, color, input_box, font):
    # Renderizar el texto
    txt_surface = font.render(text, True, color)
    # Ajustar el tamaño del cuadro de entrada de texto
    width = max(200, txt_surface.get_width() + 100)
    input_box.w = width
    # Dibujar el texto
    screen.blit(txt_surface, (input_box.x, input_box.y))
    # Dibujar el cuadro de entrada de texto
    pygame.draw.rect(screen, color, input_box , 2)


def leer_datos():
    if os.path.exists("puntajes.json"):
        with open("puntajes.json", "r") as archivo:
            datos = json.load(archivo)
            return datos
    else:
        return []
    
