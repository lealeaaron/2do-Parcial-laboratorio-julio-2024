import pygame
from funciones import *

#COLORES
AZUL_MARINO = (0, 0, 128)
ROJO = (255, 0, 0)
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)

#ANIMACIONES
barco_derecha = pygame.image.load(r"recursos\barco derecha.png")
barco_izquierda = girar_imagenes(barco_derecha, True, False)

barco_abajo = pygame.image.load(r"recursos\barco abajo.png")
barco_arriba = pygame.image.load(r"recursos\barco arriba.png")

barco_arriba_derecha = pygame.image.load(r"recursos\barco arriba-derecha.png")
barco_abajo_derecha = pygame.image.load(r"recursos\barco abajo-derecha.png")

barco_arriba_izquierda = girar_imagenes(barco_arriba_derecha, True, False)
barco_abajo_izquierda = girar_imagenes(barco_abajo_derecha, True, False)

#FONDO

#oceano =  [pygame.image.load(r"recursos\oceano_1.png"),
#            pygame.image.load(r"recursos\oceano_2.png"),
#            pygame.image.load(r"recursos\oceano_3.png"),
#            pygame.image.load(r"recursos\oceano_4.png"),]

#reescalar_animaciones(oceano,(1200,900))

mar = pygame.image.load(r"recursos\oceano_1.png")


mar = pygame.transform.scale(mar, (1200, 900))


iceberg_1 = pygame.image.load(r"recursos\iceberg 1.png")
iceberg_2 = pygame.image.load(r"recursos\iceberg 2.png")
iceberg_3 = pygame.image.load(r"recursos\iceberg 3.png")
iceberg_4 = pygame.image.load(r"recursos\iceberg 4.png")


pygame.image.load(r"recursos\caja objetivo.png")
pygame.image.load(r"recursos\caja bonus.png")

fondo_madera =pygame.image.load(r"recursos\fondo madera.png")
fondo_madera = pygame.transform.scale(fondo_madera, (1200, 1000))