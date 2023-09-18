import pygame
import os
import random
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pew Pew")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'damage.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Laser_shoot.mp3'))
pygame.mixer.Sound.set_volume(BULLET_FIRE_SOUND, 0.2)
pygame.mixer.Sound.set_volume(BULLET_HIT_SOUND, 0.5)

HEALTH_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'health.mp3'))
pygame.mixer.Sound.set_volume(HEALTH_SOUND, 0.5)

ASTEROID_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'asteroid.mp3'))
pygame.mixer.Sound.set_volume(ASTEROID_SOUND, 0.5)

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)


FPS = 60
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 3
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

BLUE_HIT = pygame.USEREVENT + 1
GREEN_HIT = pygame.USEREVENT + 2

BLUE_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_blue.png'))
BLUE_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(BLUE_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)),  270)

GREEN_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_green.png'))
GREEN_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(GREEN_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))

class HealthPowerUp:
    def __init__(self):
        self.powerup_image = pygame.image.load(os.path.join('Assets', 'health_powerup.png'))
        self.image = pygame.transform.scale(self.powerup_image, (58, 40))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(50, WIDTH - 50)
        self.rect.y = random.randint(50, HEIGHT - 50)

    def draw(self):
        WIN.blit(self.image, self.rect)

class Asteroid:
    def __init__(self, x, y, image):
        self.rect = image.get_rect()
        self.rect.topleft = (x, y)
        self.image = image

ASTEROID_IMAGE = pygame.image.load(os.path.join('Assets', 'asteroid.png'))
asteroids = []
def draw_asteroids(asteroids):
    for asteroid in asteroids:
        WIN.blit(asteroid.image, asteroid.rect.topleft)

def draw_window(green, blue, green_bullets, blue_bullets, green_health, blue_health, health_power_ups, asteroids):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    green_health_text = HEALTH_FONT.render("HEALTH: " + str(green_health), 1, WHITE)
    blue_health_text = HEALTH_FONT.render("HEALTH: " + str(blue_health), 1, WHITE)
    WIN.blit(green_health_text, (WIDTH - green_health_text.get_width() - 10, 10))
    WIN.blit(blue_health_text, (10, 10))

    WIN.blit(BLUE_SPACESHIP, (blue.x, blue.y))
    WIN.blit(GREEN_SPACESHIP, (green.x, green.y))

    for bullet in green_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in blue_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    for power_up in health_power_ups:
        power_up.draw()

    for asteroid in asteroids:
        WIN.blit(asteroid.image, asteroid.rect.topleft)

    pygame.display.update()

def blue_handle_movement(keys_pressed, blue):
    if keys_pressed[pygame.K_a] and blue.x - VEL > 0:  # LEFT
        blue.x -= VEL
    if keys_pressed[pygame.K_d] and blue.x + VEL + blue.width < BORDER.x:  # RIGHT
        blue.x += VEL
    if keys_pressed[pygame.K_w] and blue.y - VEL > 0:  # UP
        blue.y -= VEL
    if keys_pressed[pygame.K_s] and blue.y + VEL + blue.height < HEIGHT - 10:  # DOWN
        blue.y += VEL

def green_handle_movement(keys_pressed, green):
    if keys_pressed[pygame.K_LEFT] and green.x - VEL > BORDER.x + BORDER.width:  # LEFT
        green.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and green.x + VEL + green.width < WIDTH:  # RIGHT
        green.x += VEL
    if keys_pressed[pygame.K_UP] and green.y - VEL > 0:  # UP
        green.y -= VEL
    if keys_pressed[pygame.K_DOWN] and green.y + VEL + green.height < HEIGHT - 10:  # DOWN
        green.y += VEL

def handle_bullets(blue_bullets, green_bullets, blue, green):
    for bullet in blue_bullets:
        bullet.x += BULLET_VEL
        if green.colliderect(bullet):
            pygame.event.post(pygame.event.Event(GREEN_HIT))
            blue_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            blue_bullets.remove(bullet)

    for bullet in green_bullets:
        bullet.x -= BULLET_VEL
        if blue.colliderect(bullet):
            pygame.event.post(pygame.event.Event(BLUE_HIT))
            green_bullets.remove(bullet)
        elif bullet.x < 0:
            green_bullets.remove(bullet)


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.mixer.music.pause()
    pygame.time.delay(2000)
def main():
    pygame.mixer.music.load('Assets/game_bg.mp3')
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    blue = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    green = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    green_bullets = []
    blue_bullets = []

    green_health = 5
    blue_health = 5
    health_power_ups = []

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)

        if random.randint(1, 300) <= 1:
            health_power_up = HealthPowerUp()
            health_power_ups.append(health_power_up)

        if random.randint(1, 80) <= 1:
            x = random.randint(50, WIDTH - 20)
            y = random.randint(50, HEIGHT - 20)
            asteroid = Asteroid(x, y, ASTEROID_IMAGE)
            asteroids.append(asteroid)

        for asteroid in asteroids.copy():
            asteroid.rect.x -= 2
            asteroid.rect.y -= 2

            if blue.colliderect(asteroid.rect):
                ASTEROID_SOUND.play()
                blue_health -= 1
                asteroids.remove(asteroid)
            if green.colliderect(asteroid.rect):
                ASTEROID_SOUND.play()
                green_health -= 1
                asteroids.remove(asteroid)

        for power_up in health_power_ups.copy():
            if blue.colliderect(power_up.rect):
                HEALTH_SOUND.play()
                blue_health += 1
                health_power_ups.remove(power_up)

        for power_up in health_power_ups.copy():
            if green.colliderect(power_up.rect):
                HEALTH_SOUND.play()
                green_health += 1
                health_power_ups.remove(power_up)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(blue_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(blue.x + blue.width, blue.y + blue.height//2 - 2, 10, 5)
                    blue_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(green_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(green.x, green.y + green.height//2 - 2, 10, 5)
                    green_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == GREEN_HIT:
                green_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == BLUE_HIT:
                blue_health -=1
                BULLET_HIT_SOUND.play()

        winner_text = ""
        if green_health <=0:
            winner_text = "Blue Wins!"

        if blue_health <=0:
            winner_text = "Green Wins!"

        if winner_text != "":
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        blue_handle_movement(keys_pressed, blue)
        green_handle_movement(keys_pressed, green)

        handle_bullets(blue_bullets, green_bullets, blue, green)

        draw_window(green, blue, green_bullets, blue_bullets, green_health, blue_health, health_power_ups, asteroids)

    main()

if __name__ == "__main__":
    main()