from exceptions import *
from util import powerset

import itertools

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
        self.perimiter = set([])

        # in case solver is created after some progress has been made in the
        # game, update fringe and in play accordingly
        for point in self.game.board_iterator():
            if is_fringe_point(self.game,point):
                self.fringe.add(point)
                self.perimiter.update(self.game.blank_neighbors(point))

        self.game.add_move_protocol(self._update_solver_with_move)

    def solve(self):
        known_mines = set(self.perimiter)
        known_free = set(self.perimiter)

        for mine_placement in self._satisfactory_placement_generator():
            known_mines.intersection_update(mine_placement)
            known_free.difference_update(mine_placement)
            if(not known_mines and not known_free):
                break

        return (known_mines,known_free)

    def _satisfactory_placement_generator(self):
        # generates all satisfactory mine placements in the current game

        # note the use of of powerset, a function (not method)
        # defined in this using the recipe from itertools package 
        return filter(self._is_satisfactory_placement, powerset(self.perimiter))

    def _is_satisfactory_placement(self,mines):
        for point in self.fringe:
            is_proposed = lambda x: self.game.is_flagged(x) or x in mines
            num_mines_proposed = len(list(
                filter(is_proposed, self.game.neighbors(point))))

            if num_mines_proposed != self.game.num_mines_surrounding(point):
                return False

        return True

    def _update_solver_with_move(self,point,move_type):
        if move_type == 'reveal' or move_type == 'flag':
            self.perimiter.discard(point)

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
                self.perimiter.update(self.game.blank_neighbors(point))

        if move_type == 'unflag':
            if is_in_play(self.game,point):
                self.perimiter.add(point)
                self.fringe.update(self.game.revealed_neighbors(point))

class ExhaustiveSolver(BruteSolver):

    def _satisfactory_placement_generator(self):
        yield from self._sphelper(list(self.fringe),0,set([]),set([]))

    def _sphelper(self,fringe_list,fringe_index,proposed_mines,
        proposed_free):
        if fringe_index == len(fringe_list):
            # At this point proposed_mines is a satisfactory placement of mines about
            # the fringe thus, we can narrow down known_mines to include only
            # proposed_mines (if any)
            yield proposed_mines.copy()
        else:
            point = fringe_list[fringe_index]
            
            # num_mines is num flags or proposed mines arount point
            proposed = lambda x: x in proposed_mines or self.game.is_flagged(x)
            num_mines = len(list(filter(proposed, self.game.neighbors(point))))
            
            num_needed = self.game.num_mines_surrounding(point) - num_mines

            if(num_needed < 0):
                # at this point we know proposed_mines is invalid (unsatisfactory)
               return
            elif(num_needed == 0):
                # point is satisfied, continue recursing
                self._sphelper(fringe_list,fringe_index + 1, proposed_mines, proposed_free)
            #else: is implicit here
            
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

                yield from self._sphelper(fringe_list,fringe_index + 1,
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

        self.game.add_move_protocol(self._update_solver_with_move)


    def solve(self):

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

    def _update_solver_with_move(self,point,move_type):
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


class HybridSolver():


    def __init__(self,game):
        self.esolver = ExhaustiveSolver(game)
        self.hsolver = HumanSolver(game)

    def solve(self):
        mines,free = self.hsolver.solve()

        if not mines and not free:
            mines,free = self.esolver.solve()

        return mines,free








			


	

	



