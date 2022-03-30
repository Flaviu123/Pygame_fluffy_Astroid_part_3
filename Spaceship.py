import pygame
import os
import math
import random


#Klasse Settings mit Globalen Variabeln und Einstellungen
class Settings(object):
    window_width = 900
    window_height = 600
    fps = 60
    file_path = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(file_path, "images")
    sound_path = os.path.join(file_path, "sounds") 
    caption = "Space Ship"
    rotate = 0
    countspeed = 0
    astroide_big = 60
    astroide_mid = 45
    astroide_small = 30
    max_astroide = 6
    max_shoots = 11

#Klasse Background hier wird ein passendes bitmap als Hintergrund hinzugefügt. wird von run aufgerufen
class Background(object):
    def __init__(self, filename="background.png"):
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.image_path, filename)).convert()
        self.image = pygame.transform.scale(self.image, (Settings.window_width, Settings.window_height))

    def draw(self, screen):
        screen.blit(self.image, (0, 0))
        
#Player Klasse hier sind wird der Spieler abgelegt tranformiert und skaliert
class Player(pygame.sprite.Sprite):
    def __init__(self, picturefile):
        super().__init__()
        self.image_orig = pygame.image.load(os.path.join(Settings.image_path, picturefile)).convert_alpha()
        self.image_orig = pygame.transform.scale(self.image_orig, (40, 35))
        self.image = self.image_orig
        self.rect = self.image.get_rect()
        self.radius = self.rect.width // 2
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.centerx = 10
        self.rect.centery = 10
        self.speed_v = 0
        self.speed_h = 0
        self.rect.centerx = Settings.window_width / 2
        self.rect.bottom = Settings.window_height / 2

    def shoot(self, bullet):
        bullet.speed_h = 3 * - math.sin(math.radians(Settings.rotate)) + self.speed_h
        bullet.speed_v = 3 * - math.cos(math.radians(Settings.rotate)) + self.speed_v
        bullet.rect.center = self.rect.center

#update updatet die rotate, wall collison und die bewegung
    def update(self):
        self.rotate()
        self.wall_collision()
        self.rect.move_ip((self.speed_h, self.speed_v))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

#Überprüft ob sich der Spieler am rand in richtung rand bewegt und setzt die neu Position fest
    def wall_collision(self):
        if self.rect.top + self.speed_v < 0:
            self.rect.centery = Settings.window_height - 25
        if self.rect.bottom + self.speed_v > Settings.window_height:
            self.rect.centery = 25
        if self.rect.left + self.speed_h < 0:
            self.rect.centerx = Settings.window_width -25
        if self.rect.right + self.speed_h > Settings.window_width:
            self.rect.centerx = 25
 
 #Rotate lässte den spieler sich drehen und sorgt dafür das das alte center auch das neue center ist. wird von Watch for events aufgerufen
    def rotate(self):
        c = self.rect.center
        self.image = pygame.transform.rotate(self.image_orig, Settings.rotate)
        self.rect = self.image.get_rect()
        self.rect.center = c        

#Up Rechnet die geschwindigkeit aus mit dem Winkel und dem speed und setzt eine Obergrenze von 10 für alle Richtungen fest
    def up(self):
        self.speed_h = self.speed_h - math.sin(math.radians(Settings.rotate))
        self.speed_v = self.speed_v - math.cos(math.radians(Settings.rotate))
        if self.speed_h <= -10:
            self.speed_h = -10
        if self.speed_h >= 10:
            self.speed_h = 10
        if self.speed_v <= -10:
            self.speed_v = -10
        if self.speed_v >= 10:
            self.speed_v = 10


class Bullet(pygame.sprite.Sprite):
    def __init__(self, picturefile):
        super().__init__()
        self.image_orig = pygame.image.load(os.path.join(Settings.image_path, picturefile)).convert_alpha()
        self.image_orig = pygame.transform.scale(self.image_orig, (7, 10))
        self.image = self.image_orig
        self.rect = self.image.get_rect()
        self.radius = self.rect.width // 2
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.centerx = 10
        self.rect.centery = 10
        self.bullet_delete_timer = Timer(5000, False)
        self.speed_v = 0
        self.speed_h = 0
        self.rect.centerx = Settings.window_width / 2
        self.rect.bottom = Settings.window_height / 2

    def update(self):
        self.rect.move_ip((self.speed_h, self.speed_v))
        if self.bullet_delete_timer.is_next_stop_reached():
            self.kill()


class Timer(object):
    def __init__(self, duration, with_start = True):
        self.duration = duration
        if with_start:
            self.next = pygame.time.get_ticks()
        else:
            self.next = pygame.time.get_ticks() + self.duration

    def is_next_stop_reached(self):
        if pygame.time.get_ticks() > self.next:
            self.next = pygame.time.get_ticks() + self.duration
            return True
        return False

    def change_duration(self, delta=10):
        self.duration += delta
        if self.duration < 0:
            self.duration = 0


class Astroids(pygame.sprite.Sprite):
    def __init__(self, picturefile):
        super().__init__()
        self.width = Settings.astroide_big
        self.image_orig = pygame.image.load(os.path.join(Settings.image_path, picturefile)).convert_alpha()
        self.image_orig = pygame.transform.scale(self.image_orig, (self.width, self.width))
        self.image = self.image_orig
        self.rect = self.image.get_rect()
        self.rect.centery = random.randint(0, Settings.window_width - 25)
        self.rect.centerx = random.randint(0, Settings.window_height - 25)
        self.speed_x = random.randint(-3, 3)
        self.speed_y = random.randint(-3, 3)

    def update(self):
        self.rect.move_ip((self.speed_x, self.speed_y))
        self.wall_collision_astroide()

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def wall_collision_astroide(self):
        if self.rect.right < 0:
            self.rect.left = Settings.window_width
        if self.rect.left > Settings.window_width:
            self.rect.right = 0
        if self.rect.bottom < 0:
            self.rect.top = Settings.window_height
        if self.rect.top > Settings.window_height:
            self.rect.bottom = 0

class Game(object):
    def __init__(self):
        super().__init__()
        pygame.init()
        os.environ['SDL_VIDEO_WINDOW_POS'] = "10, 50"
        pygame.display.set_caption(Settings.caption)
        pygame.display.set_caption("Fingerübung \"Sound\"")

        self.font = pygame.font.Font(pygame.font.get_default_font(), 24)
        self.screen = pygame.display.set_mode((Settings.window_width, Settings.window_height))
        self.clock = pygame.time.Clock()
        self.background = Background()
        self.player = pygame.sprite.GroupSingle()
        self.player.add(Player("ship.png"))
        self.bullets = pygame.sprite.Group()
        self.astroids = pygame.sprite.Group()
        self.astroid_spawn_timer = Timer(3000)
        self.running = False
        self.pause = False
        self.setup_sound()

    def setup_sound(self):
        self.volume = 0.05
        self.pause = False
        pygame.mixer.music.load(os.path.join(Settings.sound_path, "Asteroids.mp3"))        
        pygame.mixer.music.set_volume(self.volume)
        self.music_start()
    
    def music_start(self):
        pygame.mixer.music.play(-1, 0.0)

#Run startet die wichtigsten Funktionen und lässt sie wiederholen
    def run(self):
        self.start()
        self.running = True
        while self.running:
            self.clock.tick(Settings.fps)
            self.watch_for_events()
            self.update()
            self.draw()
        pygame.quit()

#Watch for events überprüft ob events in form von tastendruck vorliegt. wird von run aufgerufen
    def watch_for_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_UP:
                    self.player.sprite.up()
                elif event.key == pygame.K_RIGHT:
                    if Settings.rotate == 0:
                        Settings.rotate = 337.5
                    elif Settings.rotate == 22.5:
                        Settings.rotate = 0
                    else:
                        Settings.rotate -= 22.5
                elif event.key == pygame.K_LEFT:
                    if Settings.rotate >= 337.5:
                        Settings.rotate = 0
                    else:
                        Settings.rotate += 22.5
                elif event.key == pygame.K_RETURN:
                    self.shoot_bullet()

#Start startet den Background und lässt den spieler Spawnen. wird von run aufgerufen
    def start(self):
        self.background = Background()
        
    def spawn(self):
        if Settings.max_astroide > len(self.astroids.sprites()) and self.astroid_spawn_timer.is_next_stop_reached():
            self.astroids.add(Astroids("Asteroid.png"))

    def shoot_bullet(self):
        if Settings.max_shoots > len(self.bullets.sprites()):
            bullet = Bullet("shoot.png")
            self.player.sprite.shoot(bullet)
            self.bullets.add(bullet)

    def update(self):
        self.spawn()
        self.player.update()
        self.bullets.update()
        self.astroids.update()
        self.check_for_collision()

    def draw(self):
        self.background.draw(self.screen)
        self.player.draw(self.screen)
        self.bullets.draw(self.screen)
        self.astroids.draw(self.screen)

        pygame.display.flip()

    def check_for_collision(self):                      #Überprüft ob eine kolision zwischen dem player und einem Metheor vorliegt wenn ja zieht er ein leben ab
        self.player.hit = pygame.sprite.groupcollide(self.player, self.astroids, True, False, pygame.sprite.collide_mask)
        if self.player.hit:
            self.running = False
            

if __name__ == '__main__':

    game = Game()
    game.run()