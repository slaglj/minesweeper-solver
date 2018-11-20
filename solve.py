import itertools

class ExhaustiveSolver:

        def __init__(self,game):
                self.game = game
                self.fringe = []
                self.known_mines = set([])
                self.known_free = set([])

        def solve(self):
                self.fringe = []
                in_play = set([])
                
                for point in self.game.board_iterator():
                        if self.game.is_revealed(point):
                                in_play_neighbs = self.in_play_neighbors(point)
                                
                                if in_play_neighbs:
                                        self.fringe.add(point)
                                        self.in_play |= in_play_neighbs

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
                        
                        # we must subtract the proposed_free point because they are
                        # to be revealed (tentatively)
                        in_play_neighbs = self.in_play_neighbors(point) - proposed_free

                        if len(in_play_neighbs) < num_needed:
                                return

                        for added_mines in itertools.combinations(adjacent_in_play,num_needed):
                                added_free = adjacent_in_play - added_mines
                                
                                proposed_mines |= added_mines
                                proposed_free |= added_free

                                _solve(fringe_index + 1,proposed_mines,proposed_free):

                                proposed_mines -= added_mines
                                proposed_free -= added_free
"""
        def _num_proposed_mines(self,point,guesses):
                #Strictly a helper to _solve to declutter code
                num = 0
                for neighb in game.get_adjacent_points(point):
                        if game.is_flagged(point) or point in guesses:
                                        num += 1
                return num
"""
                                

        def _in_play_neighbors(self,point):
                return {neighb for neighb
                        in self.game.get_adjacent_points(point)
                        if not self.game.is_revealed(neighb)
                        and not self.game.is_flagged(neighb)}







			


	

	



