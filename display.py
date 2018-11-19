import game

class Minesweeper2dConsoleInterface():

	def __init__(self,game):
		self.game = game

	def display_game(self):
		max_x = self.game.board_dimensions[0]

		print(''.join(['_' for _ in xrange(max_x)]))
		print(self.game_as_string())

	def game_as_string(self):
		max_x = self.game.board_dimensions[0]
		max_y = self.game.board_dimensions[1]

		char_rep = self._char_representation_game_over if self.game.is_over else self._char_representation_in_play

		game_rows = []
		for y in xrange(max_y):
			row = ''.join([char_rep((x,y)) for x in xrange(max_x)])
			game_rows.append(row + '\n')

		return ''.join(game_rows)

	def _char_representation_in_play(self, point):
		if self.game.is_flagged(point):
			return 'F'

		if self.game.is_revealed(point):
			return str(self.game.num_mines_surrounding(point))
		else:
			return '?'

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

	def reveal_square(self,x,y):
		try:
			self.game.reveal_square((x,y))
			self.display_game()
		except game.GameOverException:
			print('The game is over!')

	def place_flag(self,x,y):
		try:
			self.game.place_flag((x,y))
			self.display_game()
		except game.GameOverException:
			print('The game is over!')














