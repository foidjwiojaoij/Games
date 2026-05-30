import sys, pygame, os

WIDTH, HEIGHT = 800, 600

global current_level
current_level = 'tutorial'
tile_size = 20
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
        return entity.rect.move(-self.camera.x, -self.camera.y)

    def update(self, target):
        x = target.rect.centerx - int(WIDTH / 2)
        y = target.rect.centery - int(HEIGHT / 2)
        self.camera.topleft = (x, y)

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.image = pygame.Surface((25, 25), pygame.SRCALPHA)
        pygame.draw.rect(self.image, (144, 238, 144), self.image.get_rect())
        self.rect = self.image.get_rect()

        self.spawn_x = x
        self.spawn_y = y
        self.rect.center = (self.spawn_x, self.spawn_y)

        self.fading = False
        self.fading_speed = 2
        self.alpha = 255

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

        if self.vx > self.max_speed:
            self.vx = self.max_speed
        elif self.vx < -self.max_speed:
            self.vx = -self.max_speed

        solid_blocks = black_platforms if game.white_world else white_platforms

        self.rect.x += self.vx

        hits = pygame.sprite.spritecollide(self, solid_blocks, False)

        for hit in hits:
            if self.vx > 0:
                self.rect.right = hit.rect.left
                self.vx = 0
            elif self.vx < 0:
                self.rect.left = hit.rect.right
                self.vx = 0

        if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.on_ground:
            self.vy -= self.jump
            self.on_ground = False

        self.vy += self.gravity
        self.rect.y += self.vy
        self.on_ground = False

        hits = pygame.sprite.spritecollide(self, solid_blocks, False)
        for hit in hits:
            if self.vy > 0:
                self.rect.bottom = hit.rect.top
                self.vy = 0
                self.on_ground = True
            if self.vy < 0:
                self.rect.top = hit.rect.bottom
                self.vy = 0

        if self.rect.bottom >= level_height:
            self.rect.center = (self.spawn_x, self.spawn_y)
            self.vx = 0
            self.vy = 0
            self.alpha = 0
            self.fading = True

        if self.fading:
            self.alpha += self.fading_speed
            if self.alpha >= 255:
                self.alpha = 255
                self.fading = False
            self.image.set_alpha(self.alpha)

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
            self.image.fill((99, 102, 241))
            border = (99, 102, 241)

        pygame.draw.rect(self.image, border, self.image.get_rect(), 1)

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
        return level_width, level_height

    except FileNotFoundError:
        print(f'Maps/{current_level}.txt file not found')
        return WIDTH, HEIGHT

all_sprites = pygame.sprite.Group()
white_platforms = pygame.sprite.Group()
black_platforms = pygame.sprite.Group()
player = Player(100, 100)

all_sprites.add(player)

level_width, level_height = read_map()

camera = Camera(WIDTH, HEIGHT)

game = Game()
game.run()
