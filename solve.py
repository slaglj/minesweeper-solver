import itertools
import game

class AbstractSolver:

    def __init__(self,game):
        self.game = game
        self.fringe = []
        self.known_mines = set([])
        self.known_free = set([])

    def solve(self):
        raise NotImplementedError('solve() not implemented in AbstractSolver')

    def show_algorithm(self,displayClass):
        display = displayClass(self.game)

        self.game.reveal(self.game.random_point())

        print('Initial game (after random first move):')
        display.display_game()
        self.solve()

        while(self.known_mines or self.known_free):
                display.reset_known(mines = self.known_mines, free = self.known_free)
                display.display_game()
                display.reset_known()

                input('Press enter to apply the proposed moves (above)')

                try:
                    for mine in self.known_mines:
                        self.game.place_flag(mine)

                    for blank in self.known_free:
                        self.game.reveal(blank)

                except(game.GameOverException):
                    print('It looks like the algorithm made a mistake! The game is over.')
                    return

                display.display_game()

                input('The results are above. Press enter to compute the next round of moves.')

                self.solve()

        print('The algorithm didn\'t find any more solutions')

        display.display_game()

    def _store_fringe_and_return_in_play(self):
        self.fringe = []
        in_play = set([])
        
        for point in self.game.board_iterator():
                if self.game.is_revealed(point):
                        in_play_neighbs = set(self._in_play_neighbors(point))
                        
                        if in_play_neighbs:
                                self.fringe.append(point)
                                in_play |= in_play_neighbs

        return in_play

    def _in_play_neighbors(self,point):
        return (neighb for neighb
            in self.game.neighbors(point)
            if not self.game.is_revealed(neighb)
            and not self.game.is_flagged(neighb))


# NOTE: Copying and pasting the powerset recipe from the python docs for itertools
# https://docs.python.org/3/library/itertools.html
def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    
    # added import
    from itertools import combinations, chain
    
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

class BruteSolver(AbstractSolver):

    def solve(self):
        in_play = self._store_fringe_and_return_in_play()
        self.known_mines = set(in_play)
        self.known_free = set(in_play)

        for mine_placement in powerset(in_play):
            if self._is_valid_mine_placement(mine_placement):
                self.known_mines.intersection_update(mine_placement)
                self.known_free.difference_update(mine_placement)



    def _is_valid_mine_placement(self,mines):
        for point in self.fringe:
            num_mines_proposed = len([neighb for neighb
                                      in self.game.neighbors(point)
                                      if self.game.is_flagged(neighb)
                                      or neighb in mines])

            if num_mines_proposed != self.game.num_mines_surrounding(point):
                return False

        return True

class ExhaustiveSolver(AbstractSolver):

    def solve(self):
        in_play = self._store_fringe_and_return_in_play()
        self.known_mines = in_play
        self.known_free = in_play.copy()
        self._solve(0,set([]),set([]))

    def _solve(self,fringe_index,proposed_mines,proposed_free):
        if not self.known_mines and not self.known_free:
                # if we've reached a point where no mines or free
                # spaces can be identified, terminate
                return
        
        if fringe_index == len(self.fringe):
                # At this point proposed_mines is a valid placement of mines about the fringe
                # thus, we can narrow down known_mines to include only proposed_mines (if any)

                self.known_mines &= proposed_mines
                self.known_free &= proposed_free
        else:
                point = self.fringe[fringe_index]
                
                #num_mines == num flags or proposed mines arount point
                num_mines = len([neighb for neighb
                     in self.game.neighbors(point)
                     if self.game.is_flagged(neighb)
                     or neighb in proposed_mines])
                
                num_needed = self.game.num_mines_surrounding(point) - num_mines

                if(num_needed < 0):
                   return
                
                # we must subtract the proposed_free points because they are
                # to be revealed (tentatively)
                in_play_neighbs = (set(self._in_play_neighbors(point)) - proposed_free) - proposed_mines

                if len(in_play_neighbs) < num_needed:
                    return

                for added_mines in itertools.combinations(in_play_neighbs,num_needed):
                    added_free = in_play_neighbs.difference(added_mines)
                    
                    proposed_mines.update(added_mines)
                    proposed_free.update(added_free)

                    self._solve(fringe_index + 1,proposed_mines,proposed_free)

                    proposed_mines.difference_update(added_mines)
                    proposed_free.difference_update(added_free)

class HumanSolver(AbstractSolver):

    def __init__(self,game):
        super().__init__(game)
        self.active_fringe


    def solve(self):
        new_mines = []
        new_free = []

        while(not new_mines and not new_free):
            # point = dequeue point

            in_play = set(self._in_play_neighbors(point))

            if not in_play:
                continue

            flags = [neighb for neighb in self.game.neighbors(point) if self.game.is_flagged(neighb)]
            
            # number of additional mines around point that need to be flagged
            num_mines = self.game.num_mines_surrounding(point) - len(flags)

            if num_mines == 0:
                self.known_free.update(in_play)
                return

            if len(in_play) == num_mines:
                self.known_mines.update(in_play)
                return

            hints = set([])
            for inp in in_play:
                hints.update(neighb for neighb in self.game.neighbors(inp) if self.game.is_revealed(neighb))
            hints.remove(point)

            for point2 in hints:
                in_play2 = set(self._in_play_neighbors(point2))

                intersection = in_play & in_play2

                num_mines2 = self.game.num_mines_surrounding(point2) - len([neighb for neighb in self.game.neighbors(point2) if self.game.is_flagged(neighb)])

                inter_max_mines = min(num_mines1,num_mines2,len(intersection))

                if num_mines1 - inter_max_mines == len(in_play) - len(intersection):
                    self.known_mines.update(in_play - intersection)

                if num_mines2 - inter_max_mines == len(in_play2) - len(intersection):
                    self.known_mines.update(in_play2 - intersection)


                inter_min_mines = max(num_mines1 - (len(in_play) - len(intersection)),
                                    num_mines2 - (len(in_play2) - len(intersection)))

                if inter_min_mines == len(intersection):
                    self.known_mines.update(intersection)

                if inter_min_mines == num_mines1:
                    self.known_free.update(in_play)

                if inter_min_mines == num_mines2:
                    self.known_free.update(in_play2)

            


                


"""
    def _get_cluster_map(self,point):
        clusters = {}

        for neighb in self.game.neighbors(point):
            if not self.game.is_revealed(neighb) and not self.game.is_flagged(neighb):
                for hint in self.game.neighbors(neighb):
                    if hint != point and self.game.is_revealed(hint):
                        if hint in clusters:
                            clusters[hint].append(neighb)
                        else:
                            clusters[hint] = [neighb]

        return clusters
"""













			


	

	



