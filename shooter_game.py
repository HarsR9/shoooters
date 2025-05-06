from pygame import *
from random import randint
window = display.set_mode((900,600))
display.set_caption('bimasakti game')
bg = transform.scale(image.load('galaxy.jpg'),(900,600))

run = True
clock = time.Clock()   
game = True


font.init()
font2 = font.SysFont(None ,60)
text_win = font2.render('YOU WIN', True, (51,51,255))
text_kalah = font2.render('YOU LOSE', True, (255,0,0))

font3 = font.SysFont(None, 40)
text_reload = font3.render('WAIT RELOAD', True , (251, 255, 0))


mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')
font.init()
font1 = font.Font(None, 36)

class Game(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image),(size_x,size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))

bullets = sprite.Group()

sum_bullet = 0
class Player(Game):
    def update(self):
        keys = key.get_pressed()
        if keys[K_RIGHT] and self.rect.x < 850:
            self.rect.x += self.speed
        if keys[K_LEFT] and self.rect.y > 60:
            self.rect.x -= self.speed
        if keys[K_SPACE]:
            self.fire()

    def fire(self):
        global sum_bullet
        if sum_bullet < 28:
            fire_sound.play()
            bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, -15)
            bullets.add(bullet)

        else :
            window.blit(text_reload, (350,550))

        if sum_bullet > 50:
            sum_bullet = 0

        sum_bullet += 1


lose = 0
class Enemy(Game):
    def update(self):
        self.rect.y += self.speed
        global lose 

        if self.rect.y > 600 :
            self.rect.y = -20
            self.rect.x = randint(10, 850)
            self.speed = randint(1, 5)
            lose += 1

class Asteroid(Game):
    def update(self):
        self.rect.y += self.speed

        if self.rect.y > 600 :
            self.rect.y = -20
            self.rect.x = randint(10, 850)
            self.speed = randint(1, 5)

asteroids = sprite.Group()
for i in range(5):
    asteroid = Asteroid('asteroid.png', randint(10, 850), -20, 95, 90, randint(1 ,5))
    asteroids.add(asteroid)


class Bullet(Game):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0 :
            self.kill()

hero = Player('rocket.png',500,500,65,65, 10)

monsters = sprite.Group()
sum_enemy = 6
for i in range(sum_enemy):
    monster = Enemy('ufo.png', randint(10, 850), -20, 95, 90, randint(1 ,5))
    monsters.add(monster)


while run :
    for e in event.get():
        if e.type == QUIT:
            run = False

    window.blit(bg,(0,0))

    if sprite.collide_rect(hero, monster) or lose >= 2 or sprite.collide_rect(hero, asteroid): 
        window.blit(text_kalah, (350,300))
        game = False 

    colides = sprite.groupcollide(bullets, monsters, True, True)

    sprite.groupcollide(bullets, asteroids, True, False)

    if len(monsters) == 0:
        window.blit(text_win, (350,300))
        game = False

    text_lose = font1.render('dilewatkan :' +str(lose), 1, (255,255,255))
    window.blit(text_lose, (10,10))

    if game:
        asteroids.draw(window)
        asteroids.update()

        monsters.draw(window)
        monsters.update()

        bullets.draw(window)
        bullets.update()
           
        hero.reset()
        hero.update()

    display.update()
    clock.tick(60)
