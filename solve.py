import itertools
import game as gamemodule



def show_algorithm(game,solverClass,displayClass):
    solver = solverClass(game)
    display = displayClass(game)

    if game.num_revealed < 1:
        game.reveal(game.random_point())

    print('Initial game (after random first move):')
    display.display_game()
    (known_mines,known_free) = solver.solve()


    while(known_mines or known_free):
            display.reset_known(mines = known_mines, free = known_free)
            display.display_game()
            display.reset_known()

            input('Press enter to apply the proposed moves (above)')

            try:
                for mine in known_mines:
                    game.place_flag(mine)

                for free in known_free:
                    game.reveal(free)

            except(gamemodule.GameWonException):
                print('Success! The solver beat the game.')
                display.display_game()
                return
            except(gamemodule.GameOverException):
                print('The game is over.')

            display.display_game()

            input('The results are above.'
                ' Press enter to compute the next round of moves.')

            (known_mines,known_free) = solver.solve()

    print('The algorithm didn\'t find any more solutions')

    display.display_game()

def is_fringe_point(game,point):
    if not game.is_revealed(point):
        return False

    try:
        next(game.blank_neighbors(point))
    except StopIteration:
        return False
    else:
        return True

def is_in_play(game,point):
    if game.is_revealed(point) or game.is_flagged(point):
        return False

    try:
        next(game.revealed_neighbors(point))
    except StopIteration:
        return False
    else:
        return True

class BruteSolver():

    def __init__(self,game):
        self.game = game
        self.fringe = set([])
        self.in_play = set([])

        # in case solver is created after some progress has been made in the
        # game, update fringe and in play accordingly
        for point in self.game.board_iterator():
            if is_fringe_point(self.game,point):
                self.fringe.add(point)
                self.in_play.update(self.game.blank_neighbors(point))

        self.move_buffer = self.game.add_move_buffer()

    def solve(self):
        self._update_solver_with_all_moves()
        known_mines = set(self.in_play)
        known_free = set(self.in_play)

        for mine_placement in self._valid_mine_placement_generator():
            known_mines.intersection_update(mine_placement)
            known_free.difference_update(mine_placement)
            if(not known_mines and not known_free):
                break

        return (known_mines,known_free)

    def _valid_mine_placement_generator(self):
        # generates all valid mine placements in the current game

        # note the use of of powerset, a function (not method)
        # defined in this using the recipe from itertools package 
        return filter(self._is_valid_mine_placement, powerset(self.in_play))

    def _is_valid_mine_placement(self,mines):
        for point in self.fringe:
            is_proposed = lambda x: self.game.is_flagged(x) or x in mines
            num_mines_proposed = len(list(
                filter(is_proposed, self.game.neighbors(point))))

            if num_mines_proposed != self.game.num_mines_surrounding(point):
                return False

        return True

    def _update_solver_with_all_moves(self):
        while self.move_buffer:
            self._update_solver_with_move(self.move_buffer.popleft())

    def _update_solver_with_move(self,move):
        (move_type, point) = move

        if move_type == 'reveal' or move_type == 'flag':
            self.in_play.discard(point)

            # We must check to see if the revealed neighbors of point are
            # in the fringe because it may be that after revealing/flagging 
            # point, some of said revealed neighbors have have no blank 
            # neighbors, and must therefore be removed from the fringe
            for rev_neighb in self.game.revealed_neighbors(point):
                if not is_fringe_point(self.game,rev_neighb):
                    self.fringe.discard(rev_neighb)

        if move_type == 'reveal':
            if is_fringe_point(self.game,point):
                self.fringe.add(point)
                self.in_play.update(self.game.blank_neighbors(point))

        if move_type == 'unflag':
            if is_in_play(self.game,point):
                self.in_play.add(point)
                self.fringe.update(self.game.revealed_neighbors(point))

class ExhaustiveSolver(BruteSolver):

    def _valid_mine_placement_generator(self):
        yield from self._vmpg_helper(list(self.fringe),0,set([]),set([]))

    def _vmpg_helper(self,fringe_list,fringe_index,proposed_mines,
        proposed_free):
        if fringe_index == len(fringe_list):
            # At this point proposed_mines is a valid placement of mines about
            # the fringe thus, we can narrow down known_mines to include only
            # proposed_mines (if any)
            yield proposed_mines
        else:
            point = fringe_list[fringe_index]
            
            # num_mines is num flags or proposed mines arount point
            proposed = lambda x: x in proposed_mines or self.game.is_flagged(x)
            num_mines = len(list(filter(proposed, self.game.neighbors(point))))
            
            num_needed = self.game.num_mines_surrounding(point) - num_mines

            if(num_needed < 0):
                # at this point we know proposed_mines is invalid
               return
            
            # we must subtract the proposed_free points because they are
            # to be revealed (tentatively)
            in_play_neighbs = set(self.game.blank_neighbors(point)) \
                 - proposed_free - proposed_mines

            if len(in_play_neighbs) < num_needed:
                return

            for added_mines in itertools.combinations(in_play_neighbs,num_needed):
                added_free = in_play_neighbs.difference(added_mines)
                
                proposed_mines.update(added_mines)
                proposed_free.update(added_free)

                yield from self._vmpg_helper(fringe_list,fringe_index + 1,
                    proposed_mines,proposed_free)

                proposed_mines.difference_update(added_mines)
                proposed_free.difference_update(added_free)

class HumanSolver():

    def __init__(self,game):
        self.game = game
        self.active_fringe = []

        for point in self.game.board_iterator():
            if is_fringe_point(self.game,point):
                self.active_fringe.append(point)

        self.move_buffer = self.game.add_move_buffer()


    def solve(self):
        self._update_solver_with_all_moves()

        new_mines = []
        new_free = []
        while(self.active_fringe and not (new_free or new_mines)):
            point = self.active_fringe.pop()

            in_play = set(self.game.blank_neighbors(point))

            if not in_play:
                continue

            flags = list(self.game.flagged_neighbors(point))
            
            # number of additional mines around point that need to be flagged
            num_mines = self.game.num_mines_surrounding(point) - len(flags)

            if num_mines == 0:
                return ([],in_play)

            if len(in_play) == num_mines:
                return (in_play,[])

            hints = set([])
            for inp in in_play:
                hints.update(self.game.revealed_neighbors(inp))
            hints.remove(point)

            for point2 in hints:
                in_play2 = set(self.game.blank_neighbors(point2))

                intersection = in_play & in_play2

                num_mines2 = self.game.num_mines_surrounding(point2) \
                    - len(list(self.game.flagged_neighbors(point2)))

                inter_max_mines = min(num_mines,num_mines2,len(intersection))

                if num_mines - inter_max_mines == len(in_play) - len(intersection):
                    new_mines.extend(in_play - intersection)

                if num_mines2 - inter_max_mines == len(in_play2) - len(intersection):
                    new_mines.extend(in_play2 - intersection)


                inter_min_mines = max(num_mines - (len(in_play) - len(intersection)),
                                    num_mines2 - (len(in_play2) - len(intersection)))

                if inter_min_mines == len(intersection):
                    new_mines.extend(intersection)

                if inter_min_mines == num_mines:
                    new_free.extend(in_play - intersection)

                if inter_min_mines == num_mines2:
                    new_free.extend(in_play2 - intersection)

        return (new_mines,new_free)

    def _update_solver_with_all_moves(self):
        while self.move_buffer:
            self._update_solver_with_move(self.move_buffer.popleft())

    def _update_solver_with_move(self,move):
        (move_type, point) = move

        if move_type == 'reveal' or move_type == 'flag':

            for rev_neighb in self.game.revealed_neighbors(point):
                if is_fringe_point(self.game,rev_neighb):
                    # we must (re)add any points in the fringe that were
                    # rendered inactive (removed from active_fringe) after
                    # being checked by self because revealing (or flagging)
                    # point gives new information about it's neighbors in the
                    # fringe making them active again
                    self.active_fringe.append(rev_neighb)

        if move_type == 'reveal':
            if is_fringe_point(self.game,point):
                self.active_fringe.append(point)

        if move_type == 'unflag':
            if self.game.is_in_play(self.game,point):
                self.active_fringe.extend(self.game.revealed_neighbors(point))


# Code copied from python docs (powerset recipe):
# https://docs.python.org/3/library/itertools.html
def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    
    # added import
    from itertools import combinations, chain
    
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

# Code copied from stackoverflow answer:
# stackoverflow.com/questions/4941753/is-there-a-math-ncr-function-in-python
import operator as op
from functools import reduce

def ncr(n, r):
    r = min(r, n-r)
    numer = reduce(op.mul, range(n, n-r, -1), 1)
    denom = reduce(op.mul, range(1, r+1), 1)
    return numer // denom










			


	

	



