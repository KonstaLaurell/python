import pygame , os, random
pygame.init()
info = pygame.display.Info()
screen_width,screen_height = info.current_w,info.current_h
window_width,window_height = screen_width-10,screen_height-250
naytto = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
pygame.display.set_caption("game")


def piirraKuva(kuvatiedosto, x, y):
    naytto.blit(kuvatiedosto, (x, y))
def piirtaminen(naytto, hahmot):
    naytto.fill((55, 66, 91))
    for i in hahmot:
        naytto.blit(i[0],(i[1],i[2]))
    
    pygame.display.flip()

clock = pygame.time.Clock()
def kontrolli(hahmot, tapahtuma, enemyt, nopeus ):
    
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_DOWN]:
        päähahmo = hahmot[0]
        if päähahmo[2] <= window_height:
            päähahmo[2] += nopeus  
    if pressed[pygame.K_UP]:
        päähahmo = hahmot[0]
        if päähahmo[2] >= 0:
            päähahmo[2] -= nopeus


nopeus = 2
def main():
    smurf = pygame.transform.scale(pygame.transform.flip(pygame.image.load("smurf.png").convert(),True,False), (244/1.5,407/1.5))
    rocket = pygame.transform.scale(pygame.transform.flip(pygame.image.load("rocket.png").convert(),False,False), (2999/10,1999/10))
    smurf.set_colorkey((0,0,0))
    rocket.set_colorkey((0,0,0))
    kissahahmo = [smurf, 10, 10, True]
    enemy = [rocket, window_width+299, random.randint(0,window_height)]
    hahmot = [kissahahmo,enemy]
    enemyt = [enemy]


    while True:

        enemy[1] = enemy[1] 
        clock.tick(120)
        tapahtuma = pygame.event.poll()
        if tapahtuma.type == pygame.QUIT:
            break
        kontrolli(hahmot, tapahtuma, enemyt, nopeus)
        piirtaminen(naytto, hahmot) 
        for enem in enemyt:
            if enem[1] <= -300:
                enem[1] = window_width+200
                enem[2] = random.randint(0,window_height)
main() 