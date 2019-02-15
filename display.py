import game
import pygame

class Minesweeper2dConsoleDisplay():

    def __init__(self,game):
        self.game = game
        self.known_mines = set([])
        self.known_free = set([])

    def display_game(self):
        max_x = self.game.board_dimensions[0]

        print(''.join(['_' for x in range(max_x)]))
        print(self.game_as_string())

    def game_as_string(self):
        max_x = self.game.board_dimensions[0]
        max_y = self.game.board_dimensions[1]

        char_rep = self._char_representation_game_over if self.game.is_over else self._char_representation_in_play

        game_rows = []
        for y in range(max_y):
            row = ''.join([char_rep((x,y)) for x in range(max_x)])

            game_rows.append(row + '\n')

        return ''.join(game_rows)

    def reset_known(self, mines = set([]), free = set([])):
        self.known_mines = mines
        self.known_free = free



    def _char_representation_in_play(self, point):
        if self.game.is_flagged(point):
            # f for flagged
            return 'f'
        if self.game.is_revealed(point):
            # digit number of mines surrounding
            return str(self.game.num_mines_surrounding(point))
        elif point in self.known_mines:
            # m for mine
            return 'm'
        elif point in self.known_free:
            # b for blank
            return 'b'
        else:
            # '#' for unrevealed 
            return '#'

    def _char_representation_game_over(self, point):
        has_mine = self.game.contains_mine(point)
        has_flag = self.game.is_flagged(point)

        if has_mine and has_flag:
            return 'F'
        elif has_mine:
            return 'm'
        elif has_flag:
            return 'x'
        else:
            return str(self.game.num_mines_surrounding(point))


SQUARE_WIDTH = 16 # pixels, based on sprites
BLACK = (0,0,0)
GREY =  (192,192,192)

class MinesweeperGraphicDisplay():
    pygame.init()

    sprite_map = {}
    sprite_map['blank'] = pygame.image.load('sprites/blank.png')
    sprite_map['flag'] = pygame.image.load('sprites/flag.png')
    sprite_map['mine'] = pygame.image.load('sprites/mine.png')
    sprite_map[0] = pygame.image.load('sprites/zero.png')
    sprite_map[1] = pygame.image.load('sprites/one.png')
    sprite_map[2] = pygame.image.load('sprites/two.png')
    sprite_map[3] = pygame.image.load('sprites/three.png')
    sprite_map[4] = pygame.image.load('sprites/four.png')
    sprite_map[5] = pygame.image.load('sprites/five.png')
    sprite_map[6] = pygame.image.load('sprites/six.png')
    sprite_map[7] = pygame.image.load('sprites/seven.png')
    sprite_map[8] = pygame.image.load('sprites/eight.png')


    def __init__(self,game):
        self.game = game
        if len(self.game.board_dimensions) != 2:
            raise ValueError('MinesweeperGraphicDisplay only works with 2D games')
        screenwidth = SQUARE_WIDTH * self.game.board_dimensions[0]
        screenlength = SQUARE_WIDTH * self.game.board_dimensions[1]
        self.screen = pygame.display.set_mode((screenwidth,screenlength))

        pygame.display.set_caption('Minesweeper')
        self.game.add_move_protocol(self.move_protocol)

        self.screen.fill((0,0,0))
        for point in self.game.board_iterator():
            self.blit_square(point)
        pygame.display.flip()

    def run_game(self):
        pygame.display.update()

        running = True
        while running:
          for event in pygame.event.get():
            if event.type == pygame.QUIT:
              running = False

    def blit_square(self,point):
        sprites = MinesweeperGraphicDisplay.sprite_map

        if self.game.is_revealed(point):
            sprite = sprites[self.game.num_mines_surrounding(point)]
        elif self.game.is_flagged(point):
            sprite = sprites['flag']
        else:
            sprite = sprites['blank']

        pos = (point[0]*SQUARE_WIDTH, point[1]*SQUARE_WIDTH)

        return self.screen.blit(sprite,pos)

    def move_protocol(self,point,move_type):
        pygame.display.update(self.blit_square(point))
        pygame.event.pump()












