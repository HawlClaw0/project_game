import math, time, pygame, pygame.midi, random

pygame.font.init()
BLACK = (255, 255, 255)
col = [(0, 150, 0), (150, 0, 0), (150, 150, 0), (0, 0, 150), (255, 165, 0), (199, 21, 133),
       (128, 0, 128), (245, 222, 179), (112, 128, 144)]
with open('ancestors.json', encoding="utf-8") as json_f:
    lvl = json.load(json_f)
size = 200
scale = .1
pause1 = .1
n = math.ceil(math.sqrt(len(col)))
win_size = 600
mid = 300
wind = pygame.display.set_mode((win_size, win_size))
pygame.display.set_caption("симон")


class Pane:
    def __init__(self, text, pos, font_size=40, color=BLACK, fun=None):
        self.fun = fun
        self.text = text
        font = pygame.font.SysFont('Arial', font_size)
        surf = font.render(text, True, color)
        self.rect = surf.get_rect()
        self.rect.center = pos
        wind.blit(surf, self.rect.topleft)


class But:
    def __init__(self, i):
        self.x = size * (i % n)
        self.y = size * (i // n)
        self.color = col[i]
        self.rect = pygame.Rect((self.x, self.y), (size, size))
        self.draw()

    def draw(self, lit=False, wait=0):
        bright = tuple(255 if i else 0 for i in self.color)
        color = bright if lit else self.color
        pygame.draw.rect(wind, color, self.rect)
        pygame.display.update()
        time.sleep(wait)


def end():
    pygame.quit()
    quit()


def choose_mode(ts=60, ms=40):
    wind.fill((0, 0, 0))
    while True:
        modes = enumerate(sorted(lvl.keys()))
        title = Pane('Сложность', (mid, ts / 2), ts)
        diffs = [Pane(x, (mid, ms * i + 1.5 * ts), ms, ) for i, x in modes]
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for diff in diffs:
                    if diff.rect.collidepoint(event.pos):
                        return diff.text


def simon():
    player, wrong = False, False
    sequence = []
    correct = 0
    mode = choose_mode()
    tiles = [But(i) for i in range(len(col))]
    while True:
        if player:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    end()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for tile in tiles:
                        if tile.rect.collidepoint(event.pos):
                            tile.draw(lit=True)
                            if tile == sequence[correct]:
                                correct += 1
                            else:
                                wrong = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    [tile.draw() for tile in tiles]
                    if wrong:
                        right = sequence[correct]
                        for i in range(4):
                            right.draw(lit=True, wait=.1)
                            right.draw(wait=.1)
                        end_screen(len(sequence), mode, 'проиграли')
                    elif correct == len(sequence):
                        correct = 0
                        player = False
        else:
            chain = len(sequence)
            pause2 = math.exp(-scale * chain)
            if chain == lvl[mode]:
                end_screen(chain, mode)
            time.sleep(pause1 + pause2)
            sequence.append(random.choice(tiles))
            for tile in sequence:
                tile.draw(lit=True, wait=pause2)
                tile.draw(wait=pause1 * pause2)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        end()
            player = True
        pygame.display.update()


def end_screen(streak, mode, result='победили', fsize=40):
    funs = [None, None, simon, end]
    texts = [f'вы {result}',
             f'результат: {streak}',
             'заново', 'выход']
    data = enumerate(zip(texts, funs))
    panes = [Pane(x[0], (mid, (i + 1) * 1.5 * fsize), fsize, fun=x[1]) for i, x in data]
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for pane in panes:
                    if pane.rect.collidepoint(event.pos):
                        if pane.fun:
                            pane.fun()


simon()
