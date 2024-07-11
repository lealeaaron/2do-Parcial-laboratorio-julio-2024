import pygame
from materiales import *
from funciones import *
from menus import *

class Barco:
    def __init__(self, animaciones, pos_x, pos_y, tamaño, velocidad, que_hace):
        self.hitbox = pygame.Rect(pos_x, pos_y, *tamaño)
        self.posicion_inicial = (pos_x, pos_y)

        #movimiento
        self.velocidad = velocidad
        self.que_hace = que_hace
        self.contador_pasos = 0
        self.desplazamiento_y = 0
        self.desplazamiento_x = 0

        #estadisticas
        self.contador_puntos = 0
        self.contador_colisiones_objetivo = 0
        self.vidas = 3
        self.lista_obstaculos = []


        #animaciones
        self.animaciones = animaciones
        reescalar_imagenes(self.animaciones, tamaño)
        self.animacion_actual = self.animaciones[self.que_hace]





    def desplazar(self):
        if self.que_hace == "derecha":
            self.desplazamiento_x = self.velocidad
            self.desplazamiento_y = 0
        if self.que_hace == "izquierda":
            self.desplazamiento_x = self.velocidad * -1
            self.desplazamiento_y = 0
        if self.que_hace == "abajo":
            self.desplazamiento_y = self.velocidad
            self.desplazamiento_x = 0
        if self.que_hace == "arriba":
            self.desplazamiento_y = self.velocidad * -1
            self.desplazamiento_x = 0

        self.hitbox.x += self.desplazamiento_x
        self.hitbox.y += self.desplazamiento_y



    def animar(self, screen):
        screen.blit(self.animacion_actual, self.hitbox.topleft)



################################################################################################################################################################################
                        

    def actualizar(self, pantalla,lista_bordes, objetivo, bonus, al_menu, font, input_box, text, fondo_madera,choque_sfx):
        
        ##################### movimientos

        match self.que_hace:
            case "derecha":
                self.animacion_actual = self.animaciones["derecha"]
                self.desplazar()
            case "izquierda":
                self.animacion_actual = self.animaciones["izquierda"]
                self.desplazar()
            case "abajo":
                self.animacion_actual = self.animaciones["abajo"]
                self.desplazar()
            case "arriba":
                self.animacion_actual = self.animaciones["arriba"]
                self.desplazar()


        ####################puntaje
        puntaje = font.render("Puntaje: " + str(self.contador_puntos), True, red)
        puntaje_rect = puntaje.get_rect(center=(150, 950))
        pantalla.blit(puntaje, puntaje_rect)

        ####################vidas
        vidas = font.render("vidas: " + str(self.vidas), True, red)
        vidas_rect = vidas.get_rect(center=(1050, 950))
        pantalla.blit(vidas, vidas_rect)


        ################### verificacion de colisiones
        objetivo, al_menu = self.verificar_obstaculos(pantalla, objetivo, bonus, al_menu,input_box, text, fondo_madera,choque_sfx)
        objetivo, bonus, al_menu = self.verificar_colisiones(lista_bordes, objetivo, bonus,pantalla, al_menu,input_box, text, fondo_madera,choque_sfx)
        self.animar(pantalla)
        return objetivo, bonus, al_menu



################################################################################################################################################################################



    def verificar_colisiones(self, lista_bordes, objetivo,bonus,pantalla, al_menu,input_box, text, fondo_madera, choque_sfx):
        
        if self.hitbox.colliderect(objetivo["rectangulo"]):
            self.velocidad = self.velocidad + 1
            self.contador_colisiones_objetivo += 1
            self.contador_puntos += 1
            while True:
                nuevo_objetivo = crear_plataforma(True, (60, 60), (randint(1,1140),randint(1,840)), r"recursos\caja objetivo.png")
                if not colisiona_con_lista(nuevo_objetivo["rectangulo"], self.lista_obstaculos) and not colisiona_con_jugador(nuevo_objetivo["rectangulo"], self):
                    objetivo = nuevo_objetivo
                    break
            

        if self.contador_colisiones_objetivo > 0 and self.contador_colisiones_objetivo % 3 == 0:
                if bonus is None:
                    while True:
                        nuevo_bonus = crear_plataforma(True, (60, 60), (randint(1, 1140), randint(1, 840)), r"recursos\caja bonus.png")
                        if not colisiona_con_lista(nuevo_bonus["rectangulo"], self.lista_obstaculos) and not colisiona_con_jugador(nuevo_bonus["rectangulo"], self):
                            bonus = nuevo_bonus
                            break
                    

        if bonus is not None:
            pantalla.blit(bonus["superficie"], bonus["rectangulo"])
            if self.hitbox.colliderect(bonus["rectangulo"]):
                self.velocidad = self.velocidad - 2
                bonus = None
                self.contador_colisiones_objetivo = 0
            

        for borde in lista_bordes:
            if self.hitbox.colliderect(borde["rectangulo"]):
                al_menu = self.perder_vida(pantalla, al_menu,input_box, text,fondo_madera,choque_sfx)

        return objetivo, bonus, al_menu





################################################################################################################################################################################





    def verificar_obstaculos(self, screen, objetivo,bonus, al_menu,input_box, text, fondo_madera, choque_sfx):
    

        ########################### objetivo ##############################
        if objetivo is None:
            while True:
                nuevo_objetivo = crear_plataforma(True, (60,60), (randint(1,1140),randint(1,840)), r"recursos\caja objetivo.png")
                if not colisiona_con_lista(nuevo_objetivo["rectangulo"], self.lista_obstaculos) and not colisiona_con_jugador(nuevo_objetivo["rectangulo"], self):
                    objetivo = nuevo_objetivo
                    break
                

        screen.blit(objetivo["superficie"], objetivo["rectangulo"])




        ###########################  obstaculos #########################

        ########## revisa 
        if len(self.lista_obstaculos) < 10:
            crear_iceberg(self.lista_obstaculos, self, objetivo, bonus)
            


        ########## verifica las colisiones
        for obstaculo in self.lista_obstaculos:
            screen.blit(obstaculo["superficie"], obstaculo["rectangulo"])
            if self.hitbox.colliderect(obstaculo["rectangulo"]):
                al_menu = self.perder_vida(screen, al_menu, input_box, text, fondo_madera,choque_sfx)


        #########
        return objetivo, al_menu




################################################################################################################################################################################






    def perder_vida(self, screen, al_menu,input_box, text,fondo_madera, choque_sfx):
        choque_sfx.play()
        self.vidas -= 1
        print("vidas: " + str(self.vidas))
        pygame.time.delay(500)  # Retraso de 500 ms (medio segundo)
        if self.vidas > 0:
            self.reaparecer()
        else:
            pygame.mixer.music.stop()
            self.lista_obstaculos = []
            print("perdiste")
            al_menu = perdiste(screen,self.contador_puntos, input_box, text, fondo_madera)
            self.velocidad = 4
            self.vidas = 3
            self.contador_puntos = 0 
            self.posicion_inicial = (530,680)
            return al_menu



################################################################################################################################################################################


    def reaparecer(self):
        self.hitbox.x, self.hitbox.y = self.posicion_inicial

