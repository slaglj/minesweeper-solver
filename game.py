# The code to run and display a game of Minesweeper
# Jacob C. Slagle, 2018

import sets
import itertools

class GameOverException(Exception):
	pass



class MinesweeperGame:
	"""
	A MinesweeperGame object tracks the state of a game of MineSweeper

	Methods:
		board_iterator: Return an iterator over all points on the game board

		get_adjacent_points: Return list of all points adjacent to a given 
			point.

		place_mines: Place mines on the game board after game. Should be
			called shortly after game is instantiated

		is_flagged: Indicate whether a given point on the board is flagged
			for a mine

		place_flag: place a flag at a given point if not already flagged

		remove_flag: remove a flag from a given point if flagged

		toggle_flag: place a flag at a given point if not flagged, or
			remove a flag if flagged

		reveal_square: select a point on the board to reveal either a
			mine or an empty square with a number hint
	"""

	def __init__(self, board_dimensions):
		self.is_over = False
		self.mines_placed = False

		# boardDimensions is a tuple of board dimensions, 
		# usually of length two, i.e. (length, width). However, we allow the
		# possiblity of 3-dimensional or n-dimensional games of minesweeper
		self.board_dimensions = board_dimensions
		
		# grid is the game board, initially just an array of Squares, each
		# of which has default values for members
		self.grid = self._build_grid(0)

		
	def _build_grid(self, dim):
		if dim == len(self.board_dimensions):
    			return self.Square()
		# Build a game board, i.e. an n-dimensional array of Squares
		# where n == len(self.board_dimensions) and the dimensions are given 
		# by self.board_dimensions
		#
		# Squares are created with default values, to be updated by 
		# _place_mines
		
		return [self._build_grid(dim+1) for _ in xrange(self.board_dimensions[dim])]

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
		"""Return an iterator which iterates over all points on the game board"""
		return itertools.product(*[range(self.board_dimensions[dim]) for dim in xrange(len(self.board_dimensions))])

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
									 min(point[dim] + 2, self.board_dimensions[dim]))
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


	def place_mines(self, mines = None, num_mines = 0, first_move = None):
		""" Place mines on game board, update adjacent squares with numbers

		Keyword arguments:
			mines (iterable) -- an optional collection of points at which to place mines
			num_mines (int) -- number of mines to be placed (0 <= num_mines < board spaces)
			first_move (tuple) -- an optional point where no mines are to be placed

		Either mines or num_mines must be supplied by the caller. If
		mines is used (!= None), num_mines and first_move will be ignored. 
		If mines is not supplied, num_mines points on the board will be randomly 
		selected as mines and if first_move != None, none of those mines will be 
		placed at the point given by first_move. 
		"""

		if mines == None:
			from random import randint
			from sets import Set

			mines = Set([])
			while len(mines) < num_mines:
				# rpoint is a random point on the board
				rpoint = tuple([randint(0, self.board_dimensions[dim] - 1) 
								for dim in xrange(len(self.board_dimensions))])

				if (first_move == None) or (rpoint != first_move):
					mines.add(rpoint)

		for mine in mines:
			square = self._get_square(mine)
			square.contains_mine = True


		# update num_surrounding field for each Square in the board
		for point in self.board_iterator():
			square = self._get_square(point)

			adj_squares = [self._get_square(adj_point) for adj_point in self.get_adjacent_points(point)]

			square.num_surrounding = [adj_square.contains_mine for adj_square in adj_squares].count(True)



	def is_flagged(self,point):
		"""Return true if point is flagged
		
		Args:
			point (tuple of ints) -- coordinate point on the game board

		Returns:
			bool -- indicates presence of flag

		"""
		square = self._get_square(point)
		return square.is_flagged

	def place_flag(self, point):
		"""Place flag at point whether or not there already was a a flag there

		Args:
			point (tuple of ints) -- coordinate point on the game board

		Raises:
			GameOverException -- raised if the game is already over
		"""
		if self.is_over:
			raise GameOverException

		square = self._get_square(point)
		square.is_flagged = True

	def remove_flag(self, point):
		"""Remove flag from point whether or not there already was a flag 
		there

		Args:
			point (tuple of ints) -- coordinate point on the game board

		Raises:
			GameOverException -- raised if the game is already over
		"""
		if self.is_over:
			raise GameOverException

		square = self._get_square(point)
		square.is_flagged = False

	def toggle_flag(self, point):
		"""Change a point from flagged to unflagged, or vice versa

		Args:
			point (tuple of ints) -- coordinate point on the game board

		Raises:
			GameOverException -- raised if the game is already over
		"""
		if self.is_over:
			raise GameOverException

		square = self._get_square(point)
		square.is_flagged = not square.is_flagged


	# TODO: decide if flagged squares can be revealed

	def reveal_square(self, point):
		"""Reveal the square at point

		Args:
			point (tuple of ints) -- coordinate point on the game board

		Raises:
			GameOverException -- raised if the game is already over
		"""


		if self.is_over:
			raise GameOverException

		square = self._get_square(point)
		square.is_revealed = True

		if square.is_flagged:
			# Don't allow player to reveal flagged mines
			return

		if square.contains_mine:
			# End the game.
			self.is_over = True
			return

		
		if square.num_surrounding == 0:
			# Save player time revealing squares in adjacent squares when none
			# of them contain mines.
			for adj_point in self.get_adjacent_points(point):
				self.reveal_square(adj_point)
			return



		


