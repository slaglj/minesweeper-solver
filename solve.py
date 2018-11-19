from sets import Set


def brute_force_solve(game):
	fringe = get_revealed_fringe(game)
	pass

def brute_force_helper(game,possible_mines,possible_free,fringe,proposed_mines,blocked):
	if not fringe:
		possible_mines &= proposed_mines
		possible_free -= proposed_mines
	else 


def get_revealed_fringe(game):
	fringe = Set([])

	for point in game.board_iterator():
		if game.is_revealed(point) and get_in_play_neighbors(game, point):
			# if point is revealed and has neighbors in play, add point
			fringe.add(point)

	return fringe

def get_in_play_neighbors(game, point):
	return [neighbor for neighbor in game.get_adjacent_points(point) 
	       if not game.is_revealed(neighbor) and not game.is_flagged(neighbor)]









			


	

	



