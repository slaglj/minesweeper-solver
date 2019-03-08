from game import MinesweeperGame
from display import MinesweeperGraphicDisplay
from solve import HumanSolver,ExhaustiveSolver,HybridSolver
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-d","--display",
                    choices=['classic', 'monokai'],
                    default = 'monokai',
                    help="display style (monokai is defualt)")
parser.add_argument("-l","--level",
                    choices=['easy','medium','hard'],
                    default = 'medium')
parser.add_argument("-m","--method",
                    choices=['human','exhaustive','hybrid'],
                    default = 'hybrid')
args = parser.parse_args()

dimensions = {'easy':(9,9),'medium':(16,16),'hard':(30,16)}[args.level]
solver = {'human':HumanSolver,'exhaustive':ExhaustiveSolver,'hybrid':HybridSolver}[args.method]

game = MinesweeperGame(dimensions = dimensions)
MinesweeperGraphicDisplay.show_algorithm(game,solver,colorscheme=args.display)