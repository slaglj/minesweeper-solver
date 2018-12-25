import game
import time
import threading

class Minesweeper2dConsoleDisplay():

	def __init__(self,game):
		self.game = game
		self.known_mines = set([])
		self.known_free = set([])

	def display_game(self):
		max_x = self.game.board_dimensions[0]

		print(''.join(['_' for x in range(max_x)]))
		print(self.game_as_string())

	def game_as_string(self):
		max_x = self.game.board_dimensions[0]
		max_y = self.game.board_dimensions[1]

		char_rep = self._char_representation_game_over if self.game.is_over else self._char_representation_in_play

		game_rows = []
		for y in range(max_y):
			row = ''.join([char_rep((x,y)) for x in range(max_x)])

			game_rows.append(row + '\n')

		return ''.join(game_rows)

	def reset_known(self, mines = set([]), free = set([])):
		self.known_mines = mines
		self.known_free = free



	def _char_representation_in_play(self, point):
		if self.game.is_flagged(point):
			# f for flagged
			return 'f'
		if self.game.is_revealed(point):
			# digit number of mines surrounding
			return str(self.game.num_mines_surrounding(point))
		elif point in self.known_mines:
			# m for mine
			return 'm'
		elif point in self.known_free:
			# b for blank
			return 'b'
		else:
			# '#' for unrevealed 
			return '#'

	def _char_representation_game_over(self, point):
		has_mine = self.game.contains_mine(point)
		has_flag = self.game.is_flagged(point)

		if has_mine and has_flag:
			return 'F'
		elif has_mine:
			return 'm'
		elif has_flag:
			return 'x'
		else:
			return str(self.game.num_mines_surrounding(point))














