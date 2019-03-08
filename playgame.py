from game import MinesweeperGame
from display import MinesweeperGraphicDisplay
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-d","--display",
                    choices=['classic', 'monokai'],
                    default = 'monokai',
                    help="display style (monokai is defualt)")
parser.add_argument("-l","--level",
                    choices=['easy','medium','hard'],
                    default = 'medium')
args = parser.parse_args()

level_to_dimensions = {'easy':(9,9),'medium':(16,16),'hard':(30,16)}

game = MinesweeperGame(dimensions = level_to_dimensions[args.level])
MinesweeperGraphicDisplay.play_game(game,colorscheme=args.display)