#Создай собственный Шутер!
from time import *
from pygame import *
from random import randint
mixer.init()
win_width = 700
win_height = 500
mixer.music.load('space.ogg')
mixer.music.play()
window = display.set_mode((win_width,win_height))
display.set_caption('Shooter Game')
background = transform.scale(image.load('galaxy.jpg'),(win_width,win_height))
FPS = 60
run = True


class GameSprite(sprite.Sprite):
    def __init__(self,p_image,p_x,p_y,p_speed):
        super().__init__()
        self.image = transform.scale(image.load(p_image),(100,100))
        self.speed = p_speed
        self.rect = self.image.get_rect()
        self.rect.x = p_x
        self.rect.y = p_y
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))
    
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x  < win_width - 80:
            self.rect.x += self.speed
        if keys[K_SPACE]:
            player.fire()

    def fire(self):
        bullet = Bullet('bullet.png',self.rect.centerx - 25,self.rect.top - 10,10)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80,win_width - 80)
            self.rect.y = 0
            lost = lost + 1

class Bullet(GameSprite):
    def __init__(self,picture,speed,x,y):
        super().__init__(picture,speed,x,y)
        self.image = transform.scale(image.load(picture),(50,50)).convert_alpha()

    def update(self):
        self.rect.y -= self.speed
        if self.rect.y > win_height:
            self.kill() 

font.init()
font2 = font.Font('Arial',36)

score = 0
lost = 0
max_lost = 5
goal = 1000

player = Player('rocket.png',400,350,4)
enemies = sprite.Group()
bullets = sprite.Group()
finish = False

for i in range(1,6):
    ran_x = randint(80,randint(80,win_width - 80))
    enemy = Enemy('ufo.png',ran_x,0,randint(1,5))
    enemies.add(enemy)

def stats():
    global score
    for enemy in enemies:
        for bullet in bullets:
            if enemy.rect.colliderect(bullet.rect):
                score += 100
rel_time = False
num_fire  = 0
while run:
    stats()
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire = num_fire + 1
                    player.fire()
                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True
    if finish != True:
        text = font2.render('счет:' + str(score),1,(255,255,255))
        text_lose = font2.render('Пропущено:' + str(lost),1,(255,255,255))
        window.blit(background,(0,0))
        player.update()
        player.reset()

        window.blit(text,(20,30))
        window.blit(text_lose,(20,50))
    
        sprites_list = sprite.spritecollide(player,enemies,False)
    
        group_list = sprite.groupcollide(enemies,bullets,True,True)
        if sprites_list or lost >= max_lost:
            finish = True
        if score >= goal:
            finish = True

    
        enemies.update()
        enemies.draw(window)
        bullets.update()
        bullets.draw(window)

    display.update()
    time.delay(50)
