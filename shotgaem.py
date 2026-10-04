#Create your own shooter

from pygame import *
from random import *
from time import sleep

wind = display.set_mode((900,500))
display.set_caption('DOOMSDAY 2')
background = transform.scale(image.load('space.jpg'),(900,500))
clock = time.Clock()
fps = 60

mixer.init()
mixer.music.load('doomday.mp3')
mixer.music.play(0,0)
mixer.music.set_volume(0.1)

hits = 5
life = 150

font.init()
font2 = font.SysFont('Arial', 70)
win = font2.render('YOU WIN', True, (0,255,0))
lose = font2.render('YOU LOSE', True, (255,0,0))


counter = 0

game = True
lost = 0
bullets = sprite.Group()
class GameSprite(sprite.Sprite):
    def __init__(self,spriteimage,xcord,ycord,width,height,speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(spriteimage),(width,height))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = xcord
        self.rect.y = ycord
    def reset(self):
        wind.blit(self.image,(self.rect.x,self.rect.y))

class Player(GameSprite):
    def update(self):
        global counter
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            if counter == 0:
                self.rect.x -= (self.speed + 15)
        if keys[K_d] and self.rect.x < 855:
            if counter == 0:
                self.rect.x += (self.speed - 15)
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < 455:
            self.rect.y += self.speed
        if self.rect.x < 5:
            counter = 0
            self.rect.x = 10
    def fire(self):
        global life
        bullet = Bullet('ring.png',self.rect.centerx,(self.rect.y +10),25,25,-55)
        bullets.add(bullet)
        life -= 1

class Enemy(GameSprite):
    def update(self):
        self.image = self.image
        self.rect.x -= (self.speed)
        global lost
        if self.rect.x < -80:
            self.speed = randint(2,7)
            self.rect.y = randint(0, 420)
            self.rect.x = 980 + randint(-5,5)
            lost += 1
    def die(self):
        self.speed = randint(2,7)
        self.rect.y = randint(0, 420)
        self.rect.x = 980 + randint(-5,5)


class Bullet(GameSprite):
    def update(self):
        self.rect.x -= (self.speed)
        if self.rect.x > 900:
            self.kill()
        
        



hitcolor = (0,0,0)

score = 0
meteors = sprite.Group()
spikeballs = sprite.Group()
imgenemy = 'meteordoomsday.png'
for i in range(1,6):
    size = randint(50,90)
    monster = Enemy(imgenemy,980,randint(0,400),size,size,randint(2,7))
    meteors.add(monster)
for i in range(1,6):
    size = randint(50,90)
    spikeball = Enemy('spikeballcrop.png',980,randint(0,400),size,size,randint(2,7))
    spikeballs.add(spikeball)

ship = Player('ss2.png',80,240,65,60,20)
eggman = sprite.Group()
robotnik = GameSprite('eggman.png',750,200,165,165,0)
emerald = GameSprite('MasterEmerald.png',790,340,70,50,0)
eggman.add(robotnik)
finish = False
reloadtime = 0
shots = 0


while game:

    if not finish:
        life -= 0.08
        wind.blit(background,(0,0))
        robotnik.reset()
        emerald.reset()
        meteors.draw(wind)
        meteors.update()
        spikeballs.draw(wind)
        spikeballs.update()
        bullets.update()
        bullets.draw(wind)
        ship.update()
        ship.reset()
        text = font2.render('Score:'+ str(score),True,(255,255,255))
        text2 = font2.render('Rings:'+ str(round(life)),True,(255,255,255))
        textlose = font2.render('YOU LOSE',True,(255,16,0))
        hitcounter = font2.render(('Hits:' + str(hits)), True, hitcolor)
        wind.blit(text,(10,10))
        wind.blit(text2,(10,60))
        wind.blit(hitcounter,(750,10))
    
    collides = sprite.groupcollide(spikeballs, bullets, True, True)
    for c in collides:
        size = randint(50,90)
        score += 1
        spikeball = Enemy('spikeballcrop.png',980,randint(0,400),size,size,randint(2,7))
        spikeballs.add(spikeball)

    collides2 = sprite.groupcollide(meteors, bullets, True, True)
    for c in collides:
        size = randint(50,90)
        score += 1
        monster = Enemy('meteordoomsday.png',980,randint(0,400),size,size,randint(2,7))
        meteors.add(monster)
    
    if counter == 0:
        if sprite.spritecollide(ship,meteors,False):
            sprite.spritecollide(ship, meteors, True)
            life -= 5
            counter += 5
            size = randint(50,90)
            monster = Enemy('meteordoomsday.png',980,randint(0,400),size,size,randint(2,7))
            meteors.add(monster)
        if sprite.spritecollide(ship,spikeballs,False):
            sprite.spritecollide(ship, spikeballs, True)
            size = randint(50,90)
            life -= 5
            counter += 5
            spikeball = Enemy('spikeballcrop.png',980,randint(0,400),size,size,randint(2,7))
            spikeballs.add(spikeball)

    if life <= 0:
        finish = True
        wind.blit(lose, (200, 200))
    if sprite.spritecollide(ship,eggman,False):
        hits -= 1
        counter = 20
        ship.rect.x -= 150
        hitsound = mixer.Sound('bosshit.mp3')
        hitsound.set_volume(0.1)
        hitsound.play()
    if hits == 0:
        finish = True
        wind.blit(win, (200, 200))
    if counter > 0:
        counter -= 1
        ship.rect.x -= 30
        
    if hits == 5:
        hitcolor = (0,255,0)
    if hits == 4:
        hitcolor = (55,200,0)
    if hits == 3:
        hitcolor = (180,150,0)
    if hits == 2:
        hitcolor = (200,125,0)
    if hits == 1:
        hitcolor = (255,0,0)


    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if reloadtime <= 0:
                    firesound = mixer.Sound('ring.mp3')
                    firesound.set_volume(0.1)
                    firesound.play()
                    ship.fire()
                    shots += 1

    if reloadtime > 0:
        reloadtime -= 1
    else:
        reloadtime = 0

    if shots >= 1:
        reloadtime = 5
        shots = 0


    
    display.update()
    time.delay(50)