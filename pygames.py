import pygame, os, random, time, csv, datetime

pygame.init()
info = pygame.display.Info()
screen_width, screen_height = info.current_w, info.current_h
window_width, window_height = screen_width - 10, screen_height
naytto = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("game")

def piirraKuva(kuvatiedosto, x, y):
    naytto.blit(kuvatiedosto, (x, y))

def piirtaminen(naytto, hahmot, points):
    naytto.fill((55, 66, 91))
    for i in hahmot:
        naytto.blit(i[0], i[1].topleft) 
    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render("points: "+ str(points), True, (255,0,255),(0,0,0))
    textRect = text.get_rect()
    textRect.topleft = (0, 0)
    naytto.blit(text, textRect)
    pygame.display.flip()

clock = pygame.time.Clock()
def write_to_csv(data):
    with open('points.csv', 'a', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        for row in data:
            csvwriter.writerow(row)
def get_best_score():
    try:
        with open('points.csv', 'r', newline='') as csvfile:
            csvreader = csv.reader(csvfile)
            scores = [int(row[1]) for row in csvreader]
            if scores:
                return max(scores)
            else:
                return 0
    except FileNotFoundError:
        return 0 
def kontrolli(hahmot, tapahtuma, enemyt, nopeus):
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_DOWN]:
        päähahmo = hahmot[0]
        if päähahmo[1].bottom <= window_height:
            päähahmo[1].move_ip(0, nopeus)  
    if pressed[pygame.K_UP]:
        päähahmo = hahmot[0]
        if päähahmo[1].top >= 0:
            päähahmo[1].move_ip(0, -nopeus)  

def clone_enemy(enemy_image):
    enemy_rect = enemy_image.get_rect() 
    enemy_rect.topleft = (window_width + 299, random.randint(0, window_height))
    return [enemy_image, enemy_rect]

nopeus = 5

def main():
    data= []
    smurf = pygame.transform.scale(pygame.transform.flip(pygame.image.load("smurf.png").convert(), True, False),(int(244 / 1.5), int(407 / 1.5)))
    rocket = pygame.transform.scale(pygame.transform.flip(pygame.image.load("rocket.png").convert(), False, False),(int(2999 / 10), int(1999 / 10)))
    smurf.set_colorkey((0, 0, 0))
    rocket.set_colorkey((0, 0, 0))
    kissahahmo_rect = pygame.Rect(10, 10, smurf.get_width(), smurf.get_height())
    kissahahmo = [smurf, kissahahmo_rect]
    hahmot = [kissahahmo]
    enemy_image = rocket
    enemyt = []
    points = 0
    game_over = False
    tapahtuma = pygame.event.poll()
    new_enemy = clone_enemy(enemy_image)
    hahmot.append(new_enemy)
    raja = 10
    enemy_speed = 2
    while not game_over:
        clock.tick(120)
        font = pygame.font.SysFont('Arial', 32)
        text = font.render("points"+str(points), True, (255,0,255))
        textRect = text.get_rect()
        textRect.center = (0, 0)
        naytto.blit(text, textRect)
        
        tapahtuma = pygame.event.poll()
        if tapahtuma.type == pygame.QUIT:
            break

        if points == raja: 
            new_enemy = clone_enemy(enemy_image)
            hahmot.append(new_enemy)
            raja = raja * 2.5
            enemy_speed = enemy_speed * 0.3

        kontrolli(hahmot, tapahtuma, enemyt, nopeus)
        piirtaminen(naytto, hahmot, points)

        player_rect = hahmot[0][1]
        for enem in hahmot[1:]:
            if player_rect.colliderect(enem[1]):
                game_over = True
                break
    
        for enem in hahmot[1:]:
            enem[1].move_ip(-enemy_speed, 0)  
            if enem[1].right <= 0:
                points += 1
                enemy_speed = enemy_speed *1.1
                enem[1].center = (window_width + 400, random.randint(0, window_height))
    if game_over:
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        data.append([current_date, points])
        write_to_csv(data)
        best = get_best_score()        
        clock.tick(120)
        hahmot= []
        naytto.fill((0,0,0)) 
        pygame.display.flip()
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render('You lose. you got '+str(points)+ ' pooints.', True, (255,0,0),(0,0,0))
        if points < best:
            text2 = font.render('best score '+str(best), True, (255,0,0),(0,0,0))
        else:
            text2 = font.render('you got best score', True, (255,0,0),(0,0,0))
        textRect = text.get_rect()
        textRect2 = text2.get_rect()
        textRect.center = (window_width // 2, window_height // 2)
        textRect2.center = ((window_width // 2), window_height // 2+32)
        naytto.blit(text, textRect)
        naytto.blit(text2, textRect2)
        pygame.display.update()
        time.sleep(5)
        game_over = False
        main()
    
main()
