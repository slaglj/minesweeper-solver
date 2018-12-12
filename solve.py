import itertools
import game

class AbstractSolver:

    def __init__(self,game):
        self.game = game
        self.fringe = []
        self.known_mines = set([])
        self.known_free = set([])

    def solve(self):
        raise NotImplementedError('solve not implemented in AbstractSolver')

    def show_algorithm(self,displayClass):
        display = displayClass(self.game)

        self.game.reveal_square(self.game.random_point())

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
                        self.game.reveal_square(blank)

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
                        in_play_neighbs = self._in_play_neighbors(point)
                        
                        if in_play_neighbs:
                                self.fringe.append(point)
                                in_play |= in_play_neighbs

        return in_play

    def _in_play_neighbors(self,point):
        return {neighb for neighb
            in self.game.get_adjacent_points(point)
            if not self.game.is_revealed(neighb)
            and not self.game.is_flagged(neighb)}


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
                print(mine_placement)
                print('is valid')
                self.known_mines.intersection_update(mine_placement)
                self.known_free.difference_update(mine_placement)



    def _is_valid_mine_placement(self,mines):
        for point in self.fringe:
            num_mines_proposed = len([neighb for neighb
                                      in self.game.get_adjacent_points(point)
                                      if neighb in mines
                                      or self.game.is_flagged(neighb)])

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
                     in self.game.get_adjacent_points(point)
                     if self.game.is_flagged(neighb)
                     or neighb in proposed_mines])
                
                num_needed = self.game.num_mines_surrounding(point) - num_mines

                #if(num_needed < 0):
                #    return
                
                # we must subtract the proposed_free point because they are
                # to be revealed (tentatively)
                in_play_neighbs = (self._in_play_neighbors(point) - proposed_free) - proposed_mines

                if len(in_play_neighbs) < num_needed:
                    return

                for added_mines in itertools.combinations(in_play_neighbs,num_needed):
                    added_mines = set(added_mines)
                    added_free = in_play_neighbs - added_mines
                    
                    proposed_mines |= added_mines
                    proposed_free |= added_free

                    self._solve(fringe_index + 1,proposed_mines,proposed_free)

                    proposed_mines -= added_mines
                    proposed_free -= added_free







			


	

	



