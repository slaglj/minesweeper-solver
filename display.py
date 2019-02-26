from exceptions import *
import pygame

class Minesweeper2dConsoleDisplay():

    def __init__(self,game):
        self.game = game
        self.known_mines = set([])
        self.known_free = set([])

    def display_game(self):
        max_x = self.game.dimensions[0]

        print(''.join(['_' for x in range(max_x)]))
        print(self.game_as_string())

    def game_as_string(self):
        max_x = self.game.dimensions[0]
        max_y = self.game.dimensions[1]

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

    def __init__(self,game,colorscheme='monokai'):
        self.sprites = {}
        self._load_sprites(colorscheme)

        self.game = game
        if len(self.game.dimensions) != 2:
            raise ValueError('MinesweeperGraphicDisplay only works with 2D games')

        pygame.display.set_caption('Minesweeper')
        screenwidth = SQUARE_WIDTH * self.game.dimensions[0]
        screenlength = SQUARE_WIDTH * self.game.dimensions[1]
        self.screen = pygame.display.set_mode((screenwidth,screenlength))

        self.render_board()
        self.game.add_move_protocol(self.move_protocol)

    def _load_sprites(self,colorscheme):
        names = list(map(str,range(9)))
        names.extend(['blank','flag','mine','goodflag','badflag','boom'])

        for name in names:
            file = 'sprites/' + colorscheme + '/' + name + '.png'
            self.sprites[name] = pygame.image.load(file)
        

    @classmethod
    def play_game(cls,game):
        disp = cls(game)

        running = True
        while running:
          for event in pygame.event.get():
            if event.type == pygame.QUIT:
              running = False
              pygame.quit()
            elif event.type == pygame.MOUSEBUTTONUP:
                point = disp.pixel_to_point(event.pos)
                if event.button == 1:
                    try:
                        disp.game.reveal(point)
                    except(GameWonException):
                        disp.render_board()
                    except(GameLostException):
                        disp.render_board()

                elif event.button == 3:
                    disp.game.toggle_flag(point)

    @classmethod
    def show_algorithm(cls,game,solverclass):
        disp = cls(game)
        solver = solverclass(game)

        if game.num_revealed < 1:
            game.reveal(game.random_point())
        pygame.event.pump()

        (known_mines, known_free) = solver.solve()

        while(known_mines or known_free):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            for mine in known_mines:
                game.place_flag(mine)

            for free in known_free:
                game.reveal(free)

            (known_mines,known_free) = solver.solve()
            """try:
                game.reveal(free)
            except(gm.GameWonException):
                disp.render_board()
            except(gm.GameLostException):
                disp.render_board()"""
        while(True):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
            



            
    def render_board(self):
        for point in self.game.board_iterator():
            self.blit_square(point)
        pygame.display.update()

    def blit_square(self,point):
        revealed = self.game.is_revealed(point)
        flagged = self.game.is_flagged(point)

        if self.game.is_over:
            mined = self.game.contains_mine(point)
            
            if mined and revealed:
                sprite = self.sprites['boom']
            elif mined and flagged:
                sprite = self.sprites['goodflag']
            elif mined:
                sprite = self.sprites['mine']
            elif flagged:
                sprite = self.sprites['badflag']
            else:
                sprite = self.sprites[str(self.game.num_mines_surrounding(point))]

        else:
            if revealed:
                sprite = self.sprites[str(self.game.num_mines_surrounding(point))]
            elif flagged:
                sprite = self.sprites['flag']
            else:
                sprite = self.sprites['blank']

        pos = (point[0]*SQUARE_WIDTH, point[1]*SQUARE_WIDTH)

        return self.screen.blit(sprite,pos)

    def move_protocol(self,point,move_type):
        pygame.display.update(self.blit_square(point))

    def pixel_to_point(self,pixel):
        #TODO, consider cases where the screen conists of more than the board
        x = pixel[0] // SQUARE_WIDTH
        y = pixel[1] // SQUARE_WIDTH
        return (x,y)

    def save_board_image(self,filename):
        pygame.image.save(self.screen,filename)












