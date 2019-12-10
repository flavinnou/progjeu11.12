#set up all the sounds
#tick 45000 spawn du boss
import pygame, random, sys
from pygame.locals import *

WINDOWWIDTH=900
WINDOWHEIGHT=600
TEXTCOLOR = (0, 0, 0)
WINDOWHEIGHTWINDOWWIDTH, WINDOWHEIGHTWINDOWHEIGHT = WINDOWWIDTH , WINDOWHEIGHT   ##pour fond défilant define display surface
AREA = WINDOWWIDTH * WINDOWHEIGHT  ## pour fond défilant define display surface
FPS = 60
BADDIEMINSIZE = 10
BADDIEMAXSIZE = 40
BADDIEMINSPEED = 1
BADDIEMAXSPEED = 8
ADDNEWBADDIERATE = 6
PLAYERMOVERATE = 5
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255, 0, 0)
GREEN = (0, 100, 0)
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

def terminate():
    pygame.quit()
    sys.exit()

def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: # Pressing ESC quits.
                    terminate()
                return



def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def newmob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)
def newstar():
    star = Star()
    all_sprites.add(star)
    mobs.add(star)
def newenemi():
    number = random.randrange(10)
    if number > 1:
        newmob()
    else:
        newstar()

def draw_life(surface, x, y, pct):
    if pct < 0:
        pct = 0 #so we don't have negative value for life
    BAR_LENGTH = 200
    BAR_HEIGHT = 20 #size of the bar
    fill = (pct / 100) * BAR_LENGTH
    outline_rectangle = pygame.Rect (x, y, BAR_LENGTH, BAR_HEIGHT) #the rectangle that doesn't change
    fill_rectangle2 = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)#so we can see the amount of life we lost
    fill_rectangle = pygame.Rect (x, y, fill, BAR_HEIGHT) #the rectangle that display the life, it goes smaller when we get hit
    pygame.draw.rect(surface, RED, fill_rectangle2)  # draw the life lost
    pygame.draw.rect(surface, GREEN, fill_rectangle) #draw the life rectangle
    pygame.draw.rect(surface, WHITE, outline_rectangle, 2) #draw outline_rectangle

# Set up pygame, the window, and the mouse cursor.
pygame.init()
pygame.mixer.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Dodger')
pygame.mouse.set_visible(False)

# Set up the fonts.
font = pygame.font.SysFont(None, 48)
font2= pygame.font.SysFont("Courier",100)

# Set up sounds.
pygame.mixer.music.load('jinglebells.mp3')
pygame.mixer.music.set_volume(0.4) #change the volume of the music
shoot_sound = pygame.mixer.Sound('shoot.ogg')
shoot_sound.set_volume(0.05)
#explosion_sound = pygame.mixer.Sound('Explosion.wav')
#death_sound = pygame.mixer.Sound('Death.wav')


# Set up images.
playerImage = pygame.image.load('perenoel.png')
playerRect = playerImage.get_rect()
starImage = pygame.image.load('star.png')
starRect = playerImage.get_rect()
baddieImage = []
baddie_list = ['pinguin.png', 'pinguin2.png', 'pinguin3.png'] #all the images we want to chose from
for img in baddie_list:
    baddieImage.append(pygame.image.load(img))
background = pygame.image.load("background.png")
backgroundstart=pygame.image.load("backgroundstart.png")
a=0 ##pour fond défilant

background_rect = background.get_rect() #to have a way to locate it
bulletImage = pygame.image.load("gift.png")
explosion_anim = {} #we will need larger and smaller ones, so we do a dictionnary
explosion_anim['lg'] = [] #large ones
explosion_anim['sm'] = [] #small ones
for i in range(7):
    filename = 'explosion{}.png'.format(i+1) #the name of the files is numerated, so we can do a loop to get all of them easily
    img = pygame.image.load(filename)
    img_lg = pygame.transform.scale(img, (75,75))#size of the big explosions
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (32, 32))  # size of the small explosions
    explosion_anim['sm'].append(img_sm)

# Show the "Start" screen.
windowSurface.blit(backgroundstart,(0,0))
drawText('SantaWars', font2, windowSurface,(WINDOWWIDTH / 5), (WINDOWHEIGHT / 10))
drawText('Arrows to move and space to shoot!', font, windowSurface, (WINDOWWIDTH / 4) - 50, (WINDOWHEIGHT / 2) + 200)
drawText('Press a key to start.', font, windowSurface, (WINDOWWIDTH / 2.5) - 50, (WINDOWHEIGHT / 1.75) + 200)
pygame.display.update()
waitForPlayerToPressKey()

topScore = 0
### fonction fond défilant
def events():
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

#player class
class Player(pygame.sprite.Sprite):
    playerRecty = 0  # so we can use player's coordonate
    playerRectx = 0
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(playerImage,(150 ,110)) #to scale down our image
        self.rect = self.image.get_rect()
        self.radius = 60 #we can chose this way the size of the circle of the player's hitbox
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius) #this line serve to display how big the circle is, but we don't need it in the final game, only to test
        self.rect.bottom = WINDOWHEIGHT / 2
        self.speedx = 0
        self.speedy = 0
        self.life = 100 #setup life so we don't get oneshoted everytime we get hit
        self.shoot_delay = 250 #delay between each shot
        self.last_shot = pygame.time.get_ticks() #so the system know when we last shooted

    #update the player sprite
    def update(self):
        self.speedx = 0
        self.speedy = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.speedy = 0
            self.speedx = -8
        if keys[pygame.K_RIGHT]:
            self.speedy = 0
            self.speedx = 8
        if keys[pygame.K_UP]:
            self.speedx = 0
            self.speedy = -8
        if keys[pygame.K_DOWN]:
            self.speedx = 0
            self.speedy = 8
        if self.rect.right > WINDOWWIDTH:
            self.rect.right = WINDOWWIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > WINDOWHEIGHT:
            self.rect.bottom = WINDOWHEIGHT
        if keys[pygame.K_SPACE]:
            self.shoot()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        Player.playerRectx = self.rect.x
        Player.playerRecty = self.rect.y
        if self.life < 100: #we slowly regen life every tick
            self.life += 0.15

    #allow the player to shoot
    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.rect.right, self.rect.centery) #do the bullet spawn at the center extremity of the player
            all_sprites.add(bullet)
            bullets.add(bullet)
            shoot_sound.play()

#class of the ennemies
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = random.choice(baddieImage)
        self.rect = self.image.get_rect()
        self.radius = 20 #same as player
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius) #same as player
        self.rect.y = random.randrange(500) #random spawn on axe Y
        self.rect.x = (WINDOWWIDTH+100) #to get smooth animations, not that they spawn into existence at the right of the screen, instead they appear naturally from the extremity of the screen
        self.speedx = random.randrange(-8, -3) #random speed on X
        self.speedy = random.randrange(-3, 3)#random speed on Y

    #update the ennemies sprite
    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top < 0: #if an enemi hits a extremity of the screen it bounces and continue his trajectory instead of being stuck to the extremity
            self.rect.top = 0
            self.speedy = -self.speedy
        if self.rect.bottom > WINDOWHEIGHT:
            self.rect.bottom = WINDOWHEIGHT
            self.speedy = -self.speedy
        if self.rect.left < -25:
            self.rect.y = random.randrange(500)
            self.rect.x = (WINDOWWIDTH+100)
            self.speedx = random.randrange(-8, -3)
            self.speedy = random.randrange(-3, 3)

class Star(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = starImage
        self.rect = self.image.get_rect()
        self.radius = 20
        self.rect.y = random.randrange(500)
        self.rect.x = (WINDOWWIDTH -100)
        self.speedx = 0
        self.speedy = 0

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.x > Player.playerRectx:
            self.speedx = -8
        elif self.rect.x < Player.playerRectx:
            self.speedx = 8
        if self.rect.y > Player.playerRecty:
            self.speedy = -8
        elif self.rect.y < Player.playerRecty:
            self.speedy = 8




class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(bulletImage,(40,40))
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedx= 10
    #update bullet sprite
    def update(self):
        self.rect.x += self.speedx
        #kill it if it moves off the screen
        if self.rect.right > WINDOWWIDTH:
            self.kill() #remove completely the sprite if it goes of the screen

#class of the explosion
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size): #so it starts at the center of the enemi, and so we can choose the size of the explosion
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0] #so we choose between big or small, and we start with the first element of the list
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0 #we start at frame 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]): #to check how far in the list we are
                self.kill()
            else: #we spawn the next image of the explosion
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

def show_gameover_screen():
    windowSurface.blit(backgroundstart,(0,0))
    drawText("GAME OVER", font2, windowSurface, WINDOWWIDTH/5, WINDOWHEIGHT/8)
    drawText("Your Score was %s" % (score), font, windowSurface, WINDOWWIDTH /2, WINDOWHEIGHT /1.1)
    drawText("Your Top Score is %s" % (topScore), font, windowSurface, WINDOWWIDTH / 2, WINDOWHEIGHT / 1.3)
    drawText("Press a key to try again", font, windowSurface, WINDOWWIDTH / 2, WINDOWHEIGHT / 1.2)
    pygame.display.flip() #it allows only a portion of the screen to get updated
    waiting = True
    while waiting: #we wait for the player to press a key
        clock.tick(FPS) #to control speed of the loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                #start the music again
                pygame.mixer.music.set_volume(0.4)
                waiting = False

all_sprites = pygame.sprite.Group() #all the sprites are there so they can be drawn and updated
mobs = pygame.sprite.Group() #we make them all the enemies in the same group so it's easier to work with the them (hitboxes...)
bullets = pygame.sprite.Group() #same but for the bullets
player = Player()
all_sprites.add(player)
for i in range(8): #spawn a specific number of mobs on the screen
    newmob()
for i in range(1):
    newstar()

pygame.mixer.music.play(loops=-1) #the music will loop if we play for a long time
while True:
    # Set up the start of the game.
    score = 0
    playerRect.topleft = (WINDOWWIDTH -900, WINDOWHEIGHT / 2)
    moveLeft = moveRight = moveUp = moveDown = False
    #so the game keeps running at the right speed
    clock.tick(FPS)
    while True: # The game loop runs while the game part is playing.
        score += 1 # Increase score.
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == pygame.KEYDOWN: #when you press the key it does something, not when you release the key
                if event.key == pygame.K_ESCAPE:
                    terminate()

        #Update the sprites
        all_sprites.update()

        #check to see if a bullet hit a mob
        hits = pygame.sprite.groupcollide(mobs, bullets, True, True) #if a bullet hit a mobs, both get deleted
        for hit in hits: #we have to add new mobs for each mobs that got deleted from the game
            score += 20
            #explosion_sound.play()
            expl = Explosion(hit.rect.center, 'lg')
            all_sprites.add(expl)
            newenemi()



        #check to see if a mob hit the player
        hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle) #if a mobs collide, it is stocked it the list "hits", the last element allow us to use the circle of the hitboxes we made in classes
        for hit in hits:
            player.life -= 40 #we lose life when we get hit
            expl = Explosion(hit.rect.center, 'sm') #there is a smaller explosion when the mob hit the player
            all_sprites.add(expl)
            newenemi()
            if player.life <= 0:
                if score > topScore:
                    topScore = score  # set new top score
                #death_sound.play()
                show_gameover_screen()
                #we reset the game
                all_sprites = pygame.sprite.Group()  # all the sprites are there so they can be drawn and updated
                mobs = pygame.sprite.Group()  # we make them all the enemies in the same group so it's easier to work with the them (hitboxes...)
                bullets = pygame.sprite.Group()  # same but for the bullets
                player = Player()
                all_sprites.add(player)
                for i in range(8):  # spawn a specific number of mobs on the screen
                    newmob()
                for i in range(1):
                    newstar()



        #Draw everything
        events()  ##met le fond de la fenêtre

        rel_x = a % background.get_rect().width
        windowSurface.blit(background, (rel_x - background.get_rect().width, 0)) ##mettre l'image du background
        if rel_x < WINDOWWIDTH:
            windowSurface.blit(background, (rel_x, 0))
        a -= 1

        all_sprites.draw(windowSurface)
        drawText('Score: %s' % (score), font, windowSurface, 600, 0)
        drawText('Top Score: %s' % (topScore), font, windowSurface, 600, 40)
        draw_life(screen, 5,5,player.life) #draw the life bar
        #after drawing everything, flip the display
        pygame.display.flip()
        mainClock.tick(FPS)

    # Stop the game and show the "Game Over" screen.
    pygame.mixer.music.stop()
    pygame.mixer.quit()
    gameOverSound.play()


    gameOverSound.stop()
