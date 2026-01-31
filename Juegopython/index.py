import pygame
import random
import math
import sys
import json
import os

pygame.init()

ANCHO, ALTO = 1280, 720
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Zombies vs Los Watterson")

def cargar_y_escalar(ruta, tamano=(60, 60)):
    try:
        img = pygame.image.load(ruta).convert_alpha()
        return pygame.transform.scale(img, tamano)
    except:
        return pygame.Surface(tamano)

try:
    sonido_disparo = pygame.mixer.Sound("sound/Shoot.wav")
    sonido_muerte = pygame.mixer.Sound("sound/sonido_muerte.mp3")
    sonido_disparo.set_volume(0.3)
except:
    print('No se encontraron efectos en la carpeta')
    sonido_disparo = None
    sonido_muerte = None

gumball_frente = cargar_y_escalar("img/gumball-img-delante.png", (80, 80))
gumball_atras = cargar_y_escalar("img/gumball-img-detras.png", (80, 80))
darwin_frente = cargar_y_escalar("img/darwin-img-delante.png", (80, 80))
darwin_atras = cargar_y_escalar("img/darwin-img-detras.png", (80, 80))
bala_img = cargar_y_escalar("img/disparo.png", (15, 15))
fondo = pygame.image.load("img/fondo-miecraft.jpg").convert()
fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))

zombie_imagenes = []
for i in range(1, 6):
    zombie_imagenes.append(cargar_y_escalar(f"img/zombie{i}.png", (80, 80)))

reloj = pygame.time.Clock()
fuente = pygame.font.SysFont("Arial", 36)
fuente_grande = pygame.font.SysFont("Arial", 80, bold=True)

velocidad_personaje = 5
velocidad_zombis = 3
velocidad_bala = 8
TIEMPO_MAXIMO = 60

def guardar_partida(datos):
    with open("partida.json", "w") as archivo:
        json.dump(datos, archivo)

def cargar_partida():
    if os.path.exists("partida.json"):
        with open("partida.json", "r") as archivo:
            return json.load(archivo)
    return None

def mostrar_como_jugar():
    viendo = True
    while viendo:
        pantalla.fill((0, 0, 0))

        titulo = fuente_grande.render("COMO JUGAR", True, (255, 255, 255))
        pantalla.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 80))

        instrucciones = [
            "Hay 2 personajes:",
            "- Gumball se mueve con W A S D",
            "- Darwin se mueve con las FLECHAS",
            "",
            "Disparos:",
            "- Gumball: ESPACIO",
            "- Darwin: ENTER",
            "",
            "Sobrevive a los zombies hasta que se acabe el tiempo.",
            "",
            "Pulsa ESC para volver al menu"
        ]

        y = 220
        for linea in instrucciones:
            txt = fuente.render(linea, True, (255, 255, 255))
            pantalla.blit(txt, (ANCHO//2 - txt.get_width()//2, y))
            y += 40

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    viendo = False

def mostrar_game_over():
    pygame.mixer.music.stop()
    if sonido_muerte:
        sonido_muerte.play()

    pausa = True
    while pausa:
        s_oscuro = pygame.Surface((ANCHO, ALTO))
        s_oscuro.set_alpha(180) 
        s_oscuro.fill((0, 0, 0))
        pantalla.blit(s_oscuro, (0,0))

        txt_muerto = fuente_grande.render("HAS MUERTO", True, (250, 0, 0))
        pantalla.blit(txt_muerto, (ANCHO//2 - txt_muerto.get_width()//2, 150))

        mouse_pos = pygame.mouse.get_pos()

        rect_reintentar = pygame.Rect(ANCHO//2 - 150, 350, 300, 60)
        col_rein = (50, 150, 50) if rect_reintentar.collidepoint(mouse_pos) else (0, 100, 0)
        pygame.draw.rect(pantalla, col_rein, rect_reintentar)
        pygame.draw.rect(pantalla, (255, 255, 255), rect_reintentar, 3)
        txt_rein = fuente.render("REINTENTAR", True, (255, 255, 255))
        pantalla.blit(txt_rein, (rect_reintentar.centerx - txt_rein.get_width()//2, rect_reintentar.centery - txt_rein.get_height()//2))

        rect_salir = pygame.Rect(ANCHO//2 - 150, 450, 300, 60)
        col_sal = (150, 50, 50) if rect_salir.collidepoint(mouse_pos) else (100, 0, 0)
        pygame.draw.rect(pantalla, col_sal, rect_salir)
        pygame.draw.rect(pantalla, (255, 255, 255), rect_salir, 3)
        txt_sal = fuente.render("SALIR", True, (255, 255, 255))
        pantalla.blit(txt_sal, (rect_salir.centerx - txt_sal.get_width()//2, rect_salir.centery - txt_sal.get_height()//2))

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if rect_reintentar.collidepoint(evento.pos):
                    return "reintentar"
                if rect_salir.collidepoint(evento.pos):
                    pygame.quit(); sys.exit()

def mostrar_menu():
    menu_activo = True
    while menu_activo:
        pantalla.blit(fondo, (0, 0))
        texto_t = "ZOMBIES VS LOS WATTERSON"
        titulo = fuente_grande.render(texto_t, True, (255, 255, 255))
        ancho_t, alto_t = titulo.get_width(), titulo.get_height()
        rect_titulo = pygame.Rect(ANCHO//2 - (ancho_t+40)//2, 100, ancho_t+40, alto_t+20)
        pygame.draw.rect(pantalla, (0,0,0), rect_titulo)
        pygame.draw.rect(pantalla, (255,255,255), rect_titulo, 5)
        pantalla.blit(titulo, (ANCHO//2 - ancho_t//2, rect_titulo.centery - alto_t//2))

        mouse_pos = pygame.mouse.get_pos()

        rect_jugar = pygame.Rect(ANCHO//2 - 150, 350, 300, 60)
        col_j = (50, 150, 50) if rect_jugar.collidepoint(mouse_pos) else (0, 100, 0)
        pygame.draw.rect(pantalla, col_j, rect_jugar)
        txt_j = fuente.render("INICIAR JUEGO", True, (255, 255, 255))
        pantalla.blit(txt_j, (rect_jugar.centerx - txt_j.get_width()//2, rect_jugar.centery - txt_j.get_height()//2))

        rect_como = pygame.Rect(ANCHO//2 - 150, 430, 300, 60)
        col_c = (50, 50, 150) if rect_como.collidepoint(mouse_pos) else (0, 0, 120)
        pygame.draw.rect(pantalla, col_c, rect_como)
        txt_c = fuente.render("COMO JUGAR", True, (255, 255, 255))
        pantalla.blit(txt_c, (rect_como.centerx - txt_c.get_width()//2, rect_como.centery - txt_c.get_height()//2))

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if rect_jugar.collidepoint(evento.pos):
                    menu_activo = False
                if rect_como.collidepoint(evento.pos):
                    mostrar_como_jugar()

def jugar():
    try:
        pygame.mixer.music.load("sound/hit_the_womp.mp3")
        pygame.mixer.music.play(-1)
    except:
        print('No se ha podido cargar la musica de fondo')

    global inicio_tiempo
    gumball = pygame.Rect(100, 300, 80, 80)
    darwin = pygame.Rect(600, 300, 80, 80)
    g_img, d_img = gumball_frente, darwin_frente
    dir_g, dir_d = 'r', 'l'
    zombis, balas = [], []
    inicio_tiempo = pygame.time.get_ticks()
    
    ejecutando = True
    while ejecutando:
        reloj.tick(60)
        pantalla.blit(fondo, (0, 0))
        t_restante = max(0, TIEMPO_MAXIMO - (pygame.time.get_ticks() - inicio_tiempo) // 1000)
        if t_restante <= 0:
            ejecutando = False

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    balas.append({"rect": pygame.Rect(gumball.centerx, gumball.centery, 15, 15), "dir": dir_g})
                    if sonido_disparo:
                        sonido_disparo.play()
                if evento.key == pygame.K_RETURN:
                    balas.append({"rect": pygame.Rect(darwin.centerx, darwin.centery, 15, 15), "dir": dir_d})
                    if sonido_disparo:
                        sonido_disparo.play()

        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_w]: gumball.y -= velocidad_personaje; g_img = gumball_atras; dir_g = 'u'
        if teclas[pygame.K_s]: gumball.y += velocidad_personaje; g_img = gumball_frente; dir_g = 'd'
        if teclas[pygame.K_a]: gumball.x -= velocidad_personaje; dir_g = 'l'
        if teclas[pygame.K_d]: gumball.x += velocidad_personaje; dir_g = 'r'
        if teclas[pygame.K_UP]: darwin.y -= velocidad_personaje; d_img = darwin_atras; dir_d = 'u'
        if teclas[pygame.K_DOWN]: darwin.y += velocidad_personaje; d_img = darwin_frente; dir_d = 'd'
        if teclas[pygame.K_LEFT]: darwin.x -= velocidad_personaje; dir_d = 'l'
        if teclas[pygame.K_RIGHT]: darwin.x += velocidad_personaje; dir_d = 'r'

        gumball.clamp_ip(pantalla.get_rect())
        darwin.clamp_ip(pantalla.get_rect())

        for b in balas[:]:
            if b["dir"] == 'u': b["rect"].y -= velocidad_bala
            elif b["dir"] == 'd': b["rect"].y += velocidad_bala
            elif b["dir"] == 'l': b["rect"].x -= velocidad_bala
            elif b["dir"] == 'r': b["rect"].x += velocidad_bala
            if not pantalla.get_rect().colliderect(b["rect"]):
                balas.remove(b)
            else:
                pantalla.blit(bala_img, b["rect"])

        if random.randint(1, 30) == 1:
            x_z = random.choice([-30, ANCHO])
            y_z = random.randint(0, ALTO - 30)
            zombis.append({"rect": pygame.Rect(x_z, y_z, 80, 80), "imagen": random.choice(zombie_imagenes)})

        for z in zombis[:]:
            rz = z["rect"]
            obj = gumball if math.hypot(gumball.x-rz.x, gumball.y-rz.y) < math.hypot(darwin.x-rz.x, darwin.y-rz.y) else darwin
            dx, dy = obj.centerx - rz.centerx, obj.centery - rz.centery
            dist = math.hypot(dx, dy)
            if dist != 0:
                rz.x += int(dx/dist * velocidad_zombis)
                rz.y += int(dy/dist * velocidad_zombis)

            if rz.colliderect(gumball) or rz.colliderect(darwin):
                if mostrar_game_over() == "reintentar":
                    jugar()
                return

            for b in balas[:]:
                if rz.colliderect(b["rect"]):
                    if b in balas:
                        balas.remove(b)
                        zombis.remove(z)
                        break

            pantalla.blit(z["imagen"], rz)

        pantalla.blit(g_img, gumball)
        pantalla.blit(d_img, darwin)

        txt_t = fuente.render(f"Tiempo: {t_restante}", True, (255, 255, 255))
        pantalla.blit(txt_t, (10, 10))
        pygame.display.flip()

mostrar_menu()
jugar()
pygame.quit()
