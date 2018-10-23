# The code to run and display a game of Minesweeper
# Jacob C. Slagle, 2018

import sets
import itertools

class MinesweeperGame:
	# A Square is an object representing one square in a minesweeper grid.  It
	# simply packages all data relevant to one coordinate in a single object.
	class Square:
		def __init__(self, contains_mine, num_surrounding, 
					is_revealed = False, is_flagged = False):
			self.contains_mine = contains_mine
			self.num_surrounding = num_surrounding  # number of surounding mines
			self.is_revealed = is_revealed
			self.is_flagged = is_flagged


	def __init__(self, board_dimensions, num_mines):
		# grid is a multidimensional (usually 2D) array of Squares representing 
		# the game board. It is
		# left uninitialized to allow the possiblity that the mines are set
		# on the board *after* the first move is made such that a mine 
		# is never hit on the first move. The function _place_mines 
		# initializes it.
		self.grid = None

		# boardDimensions is a tuple of board dimensions, 
		# usually of length two, i.e. (length, width). However, we allow the 
		# possiblity of 3-dimensional or n-dimensional games of minesweeper
		self.board_dimensions = board_dimensions

		self.num_mines = num_mines

	def get_adjacent_coordinates(coordinates):
		"""Return all coordinate points adjacent to coordinates on game board"""

		# coordinate_ranges will include the range of values included in each dimension
		# e.g. coordinate_ranges[0]
		coordinate_ranges = [] 
		for dim in range(len(self.board_dimensions)):
			coordinate_range = range(max(0,coordinates[dim] - 1),
									 min(coordinates[dim] + 1, self.board_dimensions[dim]))
			coordinate_ranges.append(coordinate_range)

		adjacent_coordinates = Set(itertools.product(*coordinate_ranges))
		adjacent_coordinates.remove(coordinates)
		return adjacent_coordinates

	def _get_adjacent_coordinates_helper(adjacent_list, dim):
		if dim == len(self.board_dimensions):
			adjacent_list.append()


	def _get_square(coordinates):
		cross_section = self.grid

		for dim in len(self.board_dimensions):
			cross_section = cross_section[coordinates[dim]]

		return cross_section

	def _place_mines(mine_list = None, first_move = None):




	def set_flag(flag_coordinates):
