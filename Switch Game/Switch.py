import sys, pygame

WIDTH, HEIGHT = 800, 600

class Game():
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Switch Game')
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.white_world = True



    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if self.white_world:
                             self.white_world = False
                        else:
                             self.white_world = True


            all_sprites.update()

            if self.white_world:
                self.screen.fill((255, 255, 255))
            else:
                self.screen.fill((0, 0, 0))

            all_sprites.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(60)

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.image = pygame.Surface((25, 25))
        self.image.fill((144, 238, 144))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.vx = 0
        self.vy = 0
        self.acceleration = 0.5
        self.max_speed = 3
        self.slide_distance = 50
        self.deceleration = (self.max_speed ** 2) / (2 * self.slide_distance)
        self.gravity = 0.2
        self.jump = 5.5
        self.on_ground = True

    def update(self):

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vx -= self.acceleration
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vx += self.acceleration
        else:
            if abs(self.vx) < self.deceleration:
                self.vx = 0
            elif self.vx > 0:
                self.vx -= self.deceleration
            elif self.vx < 0:
                self.vx += self.deceleration

        if self.vx > self.max_speed: self.vx = self.max_speed
        elif self.vx < -self.max_speed: self.vx = -self.max_speed

        self.rect.x += self.vx

        if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.on_ground:
            self.vy -= self.jump
            self.on_ground = False

        self.vy += self.gravity
        self.rect.y += self.vy
        self.on_ground = False

        if self.rect.bottom >= HEIGHT - 10:
            self.rect.bottom = HEIGHT - 10
            self.vy = 0
            self.on_ground = True

class wPlatforms(pygame.sprite.Sprite):
    def __init__(self, x, y, colour, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.fill = (0, 0, 0)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.colour = colour
        self.rect.topleft(x, y)


all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()
player = Player(400, 400)
all_sprites.add(player)

Game().run()