# The code to run and display a game of Minesweeper
# Jacob C. Slagle, 2018

import sets
import itertools

class GameOverException(Exception):
	pass

class MinesweeperGame:
	def __init__(self, board_dimensions):
		self.is_over = False

		# boardDimensions is a tuple of board dimensions, 
		# usually of length two, i.e. (length, width). However, we allow the 
		# possiblity of 3-dimensional or n-dimensional games of minesweeper
		self.board_dimensions = board_dimensions
		
		# grid is the game board, initially just an array of Squares, each
		# of which has default values for members
		self.grid = _build_grid(0)

		
		


	
	def _build_grid(self, dim):
		# Build a game board, i.e. an n-dimensional array of Squares
		# where n == len(self.board_dimensions) and the dimensions are given by 
		# self.board_dimensions
		#
		# Squares are created with default values, to be updated by _place_mines

		if dim == len(self.board_dimensions):
    		return Square()

		return [_build_grid(dim+1) for _ in xrange(self.board_dimensions[dim])]

	# A Square is an object representing one square in a minesweeper grid.  It
	# simply packages all data relevant to one coordinate in a single object.
	class Square:
		def __init__(self, contains_mine = False, num_surrounding = -1, 
					is_revealed = False, is_flagged = False):
			self.contains_mine = contains_mine
			self.num_surrounding = num_surrounding  # number of mines in adjacent squares
			self.is_revealed = is_revealed
			self.is_flagged = is_flagged

	def board_iterator(self):
		return itertools.product(*[range(dim) for dim in range(len(self.board_dimensions))])

	def get_adjacent_points(self, point):
		"""Return all coordinate points adjacent (or diagonally adjacent) to a point on game board

		point -- a tuple representing a point on the board
		
		Include all points directly and diagonally adjacent, exclude point itself.
		"""

		# coordinate_ranges will include the range of values included in each dimension
		# e.g. coordinate_ranges[0] will give the range of x-values to be included.
		coordinate_ranges = [] 
		for dim in range(len(self.board_dimensions)):
			# make sure ranges lie within game board
			coordinate_range = range(max(0,point[dim] - 1),
									 min(point[dim] + 1, self.board_dimensions[dim] - 1))
			coordinate_ranges.append(coordinate_range)

		# Take the cartesian product of the coordinate ranges, put it in a list.
		adjacent_points = list(itertools.product(*coordinate_ranges))

		# Remove point
		adjacent_points.remove(point)
		return adjacent_points

	def _get_square(self, point):
		cross_section = self.grid

		for dim in xrange(len(self.board_dimensions)):
			cross_section = cross_section[point[dim]]

		return cross_section


	def _place_mines(self, mines = None, num_mines = 0, first_move = None):
		""" Place mines on game board, update adjacent squares with numbers

		Keyword arguments:
		mines -- an optional list of points at which to place mines
		num_mines -- number of mines to be placed (0 <= num_mines < board spaces)
		first_move -- an optional point where no mines are to be placed

		Either mines or num_mines must be supplied by the caller. If
		mines is used (!= None), num_mines and first_move will be ignored. 
		If mines is not supplied, num_mines points on the board will be randomly 
		selected as mines and if first_move != None, none of those mines will be 
		placed at the point given by first_move. 
		"""

		if mines == None:
			from random import randint

			mines = Set([])
			while len(mines) < num_mines:
				# rpoint is a random point on the board
				rpoint = tuple([randint(0, self.board_dimensions[dim] - 1) 
								for dim in len(self.board_dimensions)])

				if (first_move == None) or (rpoint != first_move):
					mines.add(rpoint)

		for mine in mines:
			square = _get_square(mine)
			square.contains_mine = True


		# update num_surrounding field for each Square in the board
		for point in board_iterator():
			square = _get_square(point)

			adj_squares = [_get_square(adj_point) for adj_point in get_adjacent_points(point)]

			square.num_surrounding = [adj_square.contains_mine for adj_square in adj_squares].count(True)


	#TODO: consider whether or not function bodies should be contained in if(not self.is_over) clause

	def place_flag(self, point):
		if self.is_over:
			raise GameOverException

		square = _get_square(point)
		square.is_flagged = True

	def remove_flag(self, point):
		if self.is_over:
			raise GameOverException

		square = _get_square(point)
		square.is_flagged = False

	def toggle_flag(self, point):
		if self.is_over:
			raise GameOverException

		square = _get_square(point)
		square.is_flagged = not square.is_flagged

	def reveal_square(self, point):
		if self.is_over:
			raise GameOverException

		square = _get_square(point)

		if (not square.is_flagged) and  (not square.is_revealed):
			square.is_revealed = True

			if square.contains_mine:
				# End the game.
				self.is_over = True
			elif: square.num_surrounding == 0:
				for adj_point in self.get_adjacent_points(point):
					self.reveal_square(adj_point)

		


