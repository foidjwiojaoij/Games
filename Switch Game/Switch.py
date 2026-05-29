import sys, pygame, os

WIDTH, HEIGHT = 800, 600

global current_level
current_level = 'tutorial'
tile_size = 50
level_width = WIDTH
level_height = HEIGHT

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
            camera.update(player)

            if self.white_world:
                self.screen.fill((255, 255, 255))
            else:
                self.screen.fill((0, 0, 0))

            for sprite in all_sprites:
                self.screen.blit(sprite.image, camera.apply(sprite))

            pygame.display.flip()
            self.clock.tick(60)

class Camera():
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.centerx + int(WIDTH / 2)
        y = -target.rect.centery + int(HEIGHT / 2)

        self.camera.topleft = (x, y)

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

class Platforms(pygame.sprite.Sprite):
    def __init__(self, x, y, colour, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        if colour == 'white':
            self.image.fill((255, 255, 255))
            border = (0, 0, 0)
        elif colour == 'black':
            self.image.fill((0, 0, 0))
            border = (255, 255, 255)
        elif colour == 'all':
            self.image.fill((0, 128, 128))
            border = (0, 128, 128)


        pygame.draw.rect(self.image, border, self.image.get_rect(), 2)

def read_map():
    try:
        max_rows = 0
        max_cols = 0
        script_dir = os.path.dirname(__file__)
        map_path = os.path.join(script_dir, 'Maps', f'{current_level}.txt')
        with open(map_path, 'r') as file:

            for row, line in enumerate(file):
                line = line.strip('\n')
                max_rows = row + 1
                for col, char in enumerate(line):
                    x = col * tile_size
                    y = row * tile_size

                    max_cols = max(max_cols, col + 1)

                    if char == 'w':
                        block = Platforms(x, y, 'white', tile_size, tile_size)
                        all_sprites.add(block)
                        white_platforms.add(block)
                    elif char == 'b':
                        block = Platforms(x, y, 'black', tile_size, tile_size)
                        all_sprites.add(block)
                        black_platforms.add(block)
                    elif char == 'a':
                        block = Platforms(x, y, 'all', tile_size, tile_size)
                        all_sprites.add(block)
                        white_platforms.add(block)
                        black_platforms.add(block)

        global level_width, level_height
        level_width = max_cols * tile_size
        level_height = max_rows * tile_size

    except FileNotFoundError:
        print(f'Maps/{current_level}.txt file not found')

all_sprites = pygame.sprite.Group()
white_platforms = pygame.sprite.Group()
black_platforms = pygame.sprite.Group()
player = Player(400, 400)

all_sprites.add(player)

read_map()

camera = Camera(level_width, level_height)


Game().run()