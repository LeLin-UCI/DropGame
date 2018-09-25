class GameState:
	def __init__(self):
		self.legal_jewels = 'STVWXYZ'
		self.col = None
		self._landed_counter = 0 # Count of 0 means not landed; faller is free to fall.
					 # Count of 1 means that the faller has landed, but is not frozen.
					 # Count of 2 means that the faller is frozen, and cannot be manipulated anymore.

	def build_board(self, rows: int, cols: int) -> 'board':
		"""Takes two integers representing the rows and columns of the board respectively
		and returns a 2D-list representing the board.
		"""
		# self.board = [['   ']*cols]*rows # -1 for stupid
		self.board = [['   ' for _ in range(cols)] for _ in range(rows)]

	def make_faller(self):
		"""Method that constructs a new Faller class instance.
		"""
		b_jwl, m_jwl, t_jwl = Jewel('Z'), Jewel('Y',-2), Jewel('X',-3)
		self.faller = [b_jwl, m_jwl, t_jwl]

	def inc_faller(self, col: int):
		"""Takes a column argument and increments the faller until it cannot move downward anymore
		in the given column of the board.
		"""
		if self.col == None:
			self.col = self._shift_zero_ind(col)
		for j in self.faller:
			self.clear(j)
		self.faller = [j.fall() for j in self.faller]
		self._update()

	def shift(self, dir: str):
		"""The dir parameter can either be '<' or '>'. The faller is shifted respectively.
		"""
		try:
			if dir == '<':
				for j in self.faller:
					self.clear(j)
				self.col -= 1
			elif dir == '>':
				for j in self.faller:
					self.clear(j)
				self.col += 1  ## Both aren't working, but I'm too tired to continue atm. 5:40 AM
			self._update() ## Fixed
			# print(self.col)

		except IndexError:
			pass

	def rotate(self):
		"""Uses a tuple unpacking technique to rotate the jewels by swapping their position attributes.
		"""
		self.faller[0].pos, self.faller[1].pos, self.faller[2].pos = \
		self.faller[2].pos, self.faller[0].pos, self.faller[1].pos
		self._update()

	# Need to make a clear function to get rid of jewels
	def clear(self, jewel):
		"""Clear jewels first, then put the jewels in the new location every loop.
		"""
		self.board[jewel.pos][self.col] = '   '
		pass

	def _update(self):
		"""Updates any changes that have been made to the board, via rotating, falling, etc.
		"""
		self._check_landed()
		for j in self.faller:
			if j.pos >= 0:
				self.board[j.pos][self.col] = repr(j)

	def _check_landed(self):
		"""Checks whether or not a faller has landed by looking at the the index of the bottom
		jewel of the faller and whether or not there is anything below it.
		"""
		pfaller = list(self.faller) # Copy the faller so that bugs here don't modify the real faller.
		bottom = pfaller[0]         # Taking the last jewel to check whats below it.

		if bottom.pos + 1 > len(self.board)-1 or self.board[bottom.pos+1][self.col] != '   ':
			if self._landed_counter == 0:
				self._inc_landed_counter()
				for j in self.faller:
					j.landed = True
				self.faller = [j.change_clothes() for j in self.faller]
			elif self._landed_counter == 1:
				self._inc_landed_counter()
				for j in self.faller:
					j.frozen = True
		else:
			self._reset_landed_counter()
			for j in self.faller:
				j.landed = False
			self.faller = [j.change_clothes() for j in self.faller]

		## Checking landed is in the wrong place. Should check every time the user tries to increment
		## the faller. Fix it later. 6/10/2018. 3:13PM
		## Check landed is also broken when trying to rotate. 6/12/2018. 3:16AM

	def _inc_landed_counter(self):
		"""Increments the _landed_counter instance attribute by 1.
		"""
		self._landed_counter += 1

	def _reset_landed_counter(self):
		"""Resets the _landed_counter instance attribute to 0.
		"""
		self._landed_counter = 0

	def _shift_zero_ind(self, arg: int) -> int:
		"""Makes user-input more intuitive by adjusting for zero-based indexing.
		"""
		return arg-1


class Jewel:
	def __init__(self, rep: str, start=-1, lbound='[', rbound=']'):
		assert len(rep) == 1, 'Jewel.__init__; Jewel must be one letter'
		self.rep = str(rep).upper() #Ensures that the jewel is a string
		self.pos = start

		self.lbound, self.rbound = lbound, rbound # [self.rep] by default

		# The three states that a faller can possibly be in.
		self.landed = False
		self.frozen = False
		self.matched = False

	def fall(self):
		"""Instead of keeping the original jewel, I decided to construct a new jewel object
		with the same attributes of the original version, except the position is shifted down one.
		This allows me to condense the code for when the jewel is incremented in the GameBoard class.
		"""
#		self.pos += 1
		return Jewel(self.rep, self.pos + 1)

	def change_clothes(self):
		"""Following the same concept as the fall method, I elected to return a new jewel object when
		the state of the jewel has changed.
		"""
		if self.landed:
			# print('here2')
			return Jewel(self.rep, self.pos, lbound='|', rbound='|')
		elif self.matched:
			return Jewel(self.rep, self.pos, lbound='*', rbound='*')
		else:   # else just returns a new Jewel object for whatever it was
			return Jewel(self.rep, self.pos)

	def __repr__(self):
		return self.lbound + self.rep + self.rbound

## Obsolete. Tried to make a faller class, but it ended up being too complicated.
#class Faller:
#	def __init__(self):
#		self.b_jewel = Jewel()
#		self.m_jewel = Jewel(-2)
#		self.t_jewel = Jewel(-3)
#
#	def f_fall(self):
#		self.b_jewel.fall()
#		self.m_jewel.fall()
#		self.t_jewel.fall()


def print_board(board: [[int]]) -> None:
	"""Takes a 2D-list representing a board and prints it out accordingly.
	"""
	for row in range(len(board)):
		print('|', end = '')
		for col in range(len(board[0])):
			print(board[row][col], end = '')
		print('|')
	print(' ', (len(board[0])*3)*'-', sep = '')


if __name__ == "__main__":
	# Main Loop
	x = GameState()
	x.build_board(4, 3)
	x.make_faller()
	print_board(x.board)
	while True:
		inp = input()
		if inp == '':
			x.inc_faller(2)
			print_board(x.board)
			# print(x.board)
		elif inp == '<' or inp == '>':
			x.shift(inp)
			print_board(x.board)
			# print(x.board)
		elif inp == 'R':
			# print(x.faller, x.board)
			x.rotate()
			print_board(x.board)
			# print(x.faller, x.board)

	pass
