import pygame, sys, os

FPS = 50
size = WIDTH, HEIGHT = 500, 500
pygame.init()
screen = pygame.display.set_mode(size)
screen.fill(pygame.Color('white'))
clock = pygame.time.Clock()
tile_width = tile_height = 50
player = None
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def terminate():
    pygame.quit()
    sys.exit()


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def start_screen():
    global screen, clock
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Нажимайте стрелочки,",
                  "чтобы двигаться"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


start_screen()
tile_images = {'wall': load_image('box.png'), 'empty': load_image('grass.png')}
player_image = load_image('mar.png', (0, 0, 0))


class Tile(pygame.sprite.Sprite):
    global tiles_group, all_sprites, tile_images, tile_width, tile_height

    def __init__(self, tile_type, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * self.pos_x, tile_height * self.pos_y)


class Player(pygame.sprite.Sprite):
    global player_group, player_image

    def __init__(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width * self.pos_x + 15, tile_height * self.pos_y + 5)

    def update(self, *args):
        if len(args) == 2:
            # если аргумента два, значит мы получили координаты, которые могут быть и отрицательными втч
            self.pos_x += args[0]
            self.pos_y += args[1]
        # выполняем отображение персонажа каждый раз, когда пишем all_sprites.update() (а надо ли?)
        self.rect = self.image.get_rect().move(tile_width * self.pos_x + 15, tile_height * self.pos_y + 5)

    def coor(self):
        # возвращает координаты для удобства
        return (self.pos_x, self.pos_y)


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    return new_player, x, y


# name = input()
# if not os.path.isfile("data/" + name):
#    print('Название карты не было введено')
#    terminate()
def main(*args):
    if len(args) == 1:
        if not os.path.isfile("data/" + args[0]):
            print('Название карты не было введено')
            terminate()
        else:
            lvl = load_level(args[0])[:]
    # мы будем использовать список lvl для перемещений (нерационально, но больше ничего в голову не пришло)
    player, level_x, level_y = generate_level(lvl)
    screen.fill((0, 0, 0))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                x, y = player.coor()
                # некрасивое изменение списка и update player-а
                if event.key == pygame.K_LEFT:
                    if lvl[y][x - 1] == '.':
                        lvl[y] = lvl[y][:x - 1] + '@' + lvl[y][x:]
                        lvl[y] = lvl[y][:x] + '.' + lvl[y][x + 1:]
                        player.update(-1, 0)
                if event.key == pygame.K_RIGHT:
                    if lvl[y][x + 1] == '.':
                        lvl[y] = lvl[y][:x + 1] + '@' + lvl[y][x + 2:]
                        lvl[y] = lvl[y][:x] + '.' + lvl[y][x + 1:]
                        player.update(1, 0)
                if event.key == pygame.K_DOWN:
                    if lvl[y + 1][x] == '.':
                        lvl[y + 1] = lvl[y + 1][:x] + '@' + lvl[y + 1][x + 1:]
                        lvl[y] = lvl[y][:x] + '.' + lvl[y][x + 1:]
                        player.update(0, 1)
                if event.key == pygame.K_UP:
                    if lvl[y - 1][x] == '.':
                        lvl[y - 1] = lvl[y - 1][:x] + '@' + lvl[y - 1][x + 1:]
                        lvl[y] = lvl[y][:x] + '.' + lvl[y][x + 1:]
                        player.update(0, -1)
        all_sprites.draw(screen)
        all_sprites.update()
        pygame.display.flip()


main('map2.txt')
