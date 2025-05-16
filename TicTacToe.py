import random

"""
Author: jd-paul
Date: May 2022
Description: This module implements a TicTacToe game with various player types including
a Reinforcement Learning agent, a Minimax agent, and a Human player.
"""

# CONSTANTS

RL_AGENT = 1
RANDOM_AGENT = 2
HUMAN_AGENT = 3
MINIMAX_AGENT = 4
TRAINING_MODE = 5
PLAYING_MODE = 6

random.seed(12408123)


def createPlayer(letter, playerType=RANDOM_AGENT):
	"""
	This function creates a player and assigns it a letter

	:param letter: The players letter; single character X or O
	:type letter: String
	:param playerType: The type of player to create, must be RL_AGENT, RANDOM_AGENT, HUMAN_AGENT or MINIMAX_AGENT
	:type playerType: Integer
	:return: Player, RLPlayer, MINIPlayer or HUMANPlayer
	"""

	if playerType == RL_AGENT:
		return RLPlayer(letter, playerType)
	elif playerType == HUMAN_AGENT:
		return HUMANPlayer(letter, playerType)
	elif playerType == MINIMAX_AGENT:
		return MINIPlayer(letter, playerType)

	return Player(letter, playerType)

def train(player1, player2, episodes):
	"""
	This function executes n (episodes) tictactoe games.  Player 1 or 2 must be
	an RL agent.  The RL agent has to play against another player to learn how
	to play.  The second player should be a RANDOM player.

	:param player1: An RL or RANDOM agent.
	:type player1: Player or RLPlayer
	:param player2: An RL or RANDOM agent.
	:type player2: Player or RLPlayer
	:param episodes: Number of episodes to execute
	:type episodes: Integer
	"""

	for i in range(episodes) :
		board = TicTacToe()
		board.setPlayers(player1, player2)
		runEpisode(board)

def runEpisode(board) :
	"""
	This method executes a single tictactoe game and updates
	the state value table after every move played by the RL agent.

	:param board: The tictactoe game board
	:type board: TicTacToe
	"""

	players = board.getPlayers()
	rlplayer = players[0]

	if not rlplayer.getType() == RL_AGENT:
		rlplayer = players[1]

	rlplayer.previousState = board.copy()
	while not board.isGameOver():

		player = board.next()
		player.makeMove(board)

	rlplayer.rewardState(board)


class TicTacToe :
	"""
	This class represents the TicTacToe board. It draws the board and keeps track
	of the moves that have been made.
	"""

	def __init__(self) :
		"""
		This is the constructor.  It creates a new empty board. Internally,
		the board is a 2D list.  Empty squares are denotes with a single
		asterisk '*'
		"""

		self.board = ['*', '*', '*', '*', '*', '*', '*', '*', '*']
		self.moveCount = 0
		self.lastMove = None
		self.remainingMoves = [0,1,2,3,4,5,6,7,8]
		self.player1 = None
		self.player2 = None
		self.userQuit = False

	def setPlayers(self, player1, player2):
		"""
		Sets the players

		:param player1: Player 1
		:type player1: Player, RLPlayer, MINIPlayer or HUMANPlayer
		:param player2: Player 2
		:type player2: Player, RLPlayer, MINIPlayer or HUMANPlayer
		"""

		self.player1 = player1
		self.player2 = player2

		self.player1.winner = False
		self.player2.winner = False

		self.player1.isTurn = True
		self.player2.isTurn = False

	def getPlayers(self):
		"""
		Gets the players

		:return: List of Players
		"""
		return [self.player1, self.player2]

	def next(self):
		"""
		Gets the next player to go

		:return: Player, RLPlayer, MINIPlayer or HUMANPlayer
		"""

		if self.player1.isTurn:
			self.player1.isTurn = False
			self.player2.isTurn = True
			return self.player1
		else:
			self.player1.isTurn = True
			self.player2.isTurn = False
			return self.player2

	def getWinner(self): # // YOU CAN USE GETWINNER FOR THE GETREWARD
		"""
		Gets the player that won the game

		:return: Player, RLPlayer, MINIPlayer, HUMANPlayer or None
		"""
		if self.isGameWon(self.player1.letter):
			return self.player1
		elif self.isGameWon(self.player2.letter):
			return self.player2
		elif self.isGameDraw() or self.userQuit:
			return None

	def isGameOver(self) :
		"""
		This method determines if the game is over.  Returns True if someone has won
		or the game is drawn, otherwise it returns False

		:return: True or False
		"""

		if self.isGameWon('X'):
			return True

		if self.isGameWon('O'):
			return True

		if self.userQuit:
			return True

		if self.moveCount >= 9:
			return True

		return False


	def isGameDraw(self) :
		"""
		This method determines if the game is a draw.  Returns True if game is a
		draw (no has won), otherwise it returns False

		:return: True or False
		"""

		if self.moveCount >= 9:
			return True

		return False

	def isGameWon(self, mark):
		"""
		This method checks to see if a player, specified by mark, has won the
		game.  It returns True if 'mark' has won the game, other False

		:param mark: A letter, e.g., 'X' or 'O'
		:type mark: String
		:return: True or False
		"""

		if self.isSameAs(mark, self.board[0], self.board[1], self.board[2]):
			return True

		if self.isSameAs(mark, self.board[3], self.board[4], self.board[5]):
			return True

		if self.isSameAs(mark, self.board[6], self.board[7], self.board[8]):
			return True

		if self.isSameAs(mark, self.board[0], self.board[3], self.board[6]):
			return True

		if self.isSameAs(mark, self.board[1], self.board[4], self.board[7]):
			return True

		if self.isSameAs(mark, self.board[2], self.board[5], self.board[8]):
			return True

		if self.isSameAs(mark, self.board[0], self.board[4], self.board[8]):
			return True

		if self.isSameAs(mark, self.board[2], self.board[4], self.board[6]):
			return True

		return False

	def isSameAs(self, char, a, b, c):
		"""
		This methods checks if all four parameters are equal.  Returns True if
		all four characters are the same otherwise False.

		:param char:  A character, e.g., 'X' or 'O'
		:type char: String
		:param a: A character, e.g., 'X' or 'O' or '*'
		:type a: String
		:param b: A character, e.g., 'X' or 'O' or '*'
		:type b: String
		:param c: A character, e.g., 'X' or 'O' or '*'
		:type c: String
		:return: True or False
		"""

		if char == a and a == b and b == c:
			return True

		return False

	def drawBoard(self):
		"""
		This method displays the game on the screen.  It can only display the
		letters X and O.
		"""

		letterX = ['  X     X  ', '   X   X   ', '    X X    ', \
					'     X     ', '    X X    ', '   X   X   ', '  X     X  ']
		letterO = ['   OOOOO   ', '  O     O  ', '  O     O  ', \
					'  O     O  ', '  O     O  ', '  O     O  ', '   OOOOO   ']

		tmp = []
		tmp.append((' ' * 11) + '@' + (' ' * 11) + '@' + (' ' * 11))
		lim = [[0,3], [3,6], [6,9]]

		for i in range(3):
			# row = self.board[i]
			limits = lim[i]
			row = self.board[limits[0]:limits[1]]

			for j in range(7):
				msg = ""
				for k in range(3):
					if row[k] == 'X':
						msg += letterX[j]
					elif row[k] == 'O':
						msg += letterO[j]
					else:
						msg += ' ' * 11

					if k != 2:
						msg += '@'

				tmp.append(msg)

			if i != 2:
				tmp.append((' ' * 11) + '@' + (' ' * 11) + '@' + (' ' * 11))
				tmp.append('@' * 35)
				tmp.append((' ' * 11) + '@' + (' ' * 11) + '@' + (' ' * 11))

		tmp.append((' ' * 11) + '@' + (' ' * 11) + '@' + (' ' * 11))
		print("\n\n")
		for line in tmp:
			print(line)
		print("\n\n")

	def makeMove(self, location, mark):
		"""
		This method puts a letter (mark) on the board, at location, if it's
		legal to do so.  Returns True if the location is valid and the square
		has not been marked already; False for all other conditions

		:param location: An Integer between 0 - 8
		:type location: Integer
		:param mark: The letter, 'X' or 'O'
		:type mark: String
		:return: True or False
		"""

		if 0 <= location <= 8:

			if self.board[location] != '*':
				return False

			self.board[location] = mark
			self.moveCount += 1
			self.lastMove = location

			self.remainingMoves.remove(location)

			return True

		return False

	def copy(self) :
		"""
		This method makes a copy of the tictactoe board.  Returns a new
		Tictactoe board.

		:return: TicTacToe
		"""

		newBoard = TicTacToe()

		newBoard.board = self.board[:]
		newBoard.moveCount = self.moveCount
		newBoard.lastMove = self.lastMove
		newBoard.remainingMoves = self.remainingMoves[:]
		newBoard.player1 = self.player1
		newBoard.player2 = self.player2
		newBoard.userQuit = self.userQuit

		return newBoard

	def getKey(self, letter):
		"""
		This method transforms the list which represents the board into
		a single string to be used as a key. In the key, the Xs and Os are
		replaced with L and T where L represents the letter (X or O) used
		by the learning agent and the T is the opponent. This allows
		the agent to learn by playing as X or O.  Returns a string, 9 characters
		long, of Ls, Ts and asterisks.

		:param letter: the letter used by the learning agent.
		:type letter: String
		:return: String
		"""

		r = "".join(self.board)

		r = r.replace(letter, 'L')
		if letter == 'X' :
			r = r.replace('O', 'T')
		else:
			r = r.replace('X', 'T')

		return r


class Player :
	"""
	This class represents a person or agent playing tictactoe.
	"""

	def __init__(self, letter, playerType=RANDOM_AGENT) :
		"""
		When creating a Player you have to specify a letter and player type.
		The letter is either 'X' or 'O' (both capitilised).  The player type can
		be: RL_AGENT, RANDOM_AGENT, HUMAN_AGENT, or MINIMAX_AGENT. The default
		is RANDOM_AGENT.

		:param letter: The letter the player uses, can only be 'X' or 'O'
		:type letter: String
		:param playerType: The type of player 'HUMAN', 'MINIMAX', 'RL' OR 'RANDOM'
		:type playerType: Integer
		"""

		self.letter = letter
		self.opponent = 'O'

		if letter == 'O':
			self.opponent = 'X'

		self.playerType = playerType

		self.name = "Unknown"
		self.rating = 1200
		self.gamesW = 0
		self.gamesD = 0
		self.gamesL = 0

		self.firstPlayer = True
		self.isTurn = True
		self.winner = False

	def getType(self):
		"""
		Gets the player's type

		:return: RL_AGENT, RANDOM_AGENT, HUMAN_AGENT or MINIMAX_AGENT
		"""
		return self.playerType

	def makeMove(self, board):
		"""
		Selects a random move.

		:param board: The tictactoe game board
		:type board: TicTacToe
		"""

		moveLegal = False

		while not moveLegal:
			loc = random.randint(0,8)
			moveLegal = board.makeMove(loc, self.letter)


class RLPlayer(Player) :
	"""
	This class represents a Reinforcement Learning agent.
	"""

	def __init__(self, letter, playerType=RL_AGENT) :
		"""
		When creating an RLPlayer you must specify a letter, either 'X' or 'O'
		(both capitilised).  Do not specify the playerType.

		:param letter: The letter the player uses, can only be 'X' or 'O'
		:type letter: String
		:param playerType: RL_AGENT
		:type playerType: Integer
		"""

		super().__init__(letter, playerType)

		self.learningRate = 0.0
		self.discountRate = 0.0
		self.epsilon = 0.0
		self.valueFunction = {}
		self.previousState = None
		self.mode = PLAYING_MODE

	def initTraining(self, learning, discount, epsilon):
		"""
		This method initialises the RL agent's learning parameters.

		:param learning: Learning rate
		:type learning: Float
		:param discount: Discount rate
		:type discount: Float
		:param epsilon: Epsilon (epsilon-Greedy Algorithm)
		:type epsilon: Float
		"""

		self.learningRate = learning
		self.discountRate = discount
		self.epsilon = epsilon
		self.previousState = None
		self.mode = TRAINING_MODE

	def setMode(self, mode):
		"""
		This method sets the RL agent's mode:

		:param mode: The RL agent's mode
		:type mode: TRAINING_MODE or PLAYING_MODE
		"""
		self.mode = mode

	def getMode(self):
		"""
		This method gets the RL agent's mode:

		:return: TRAINING_MODE or PLAYING_MODE
		"""

		return self.mode

	def makeMove(self, board):
		"""
		This method is responsible for making a move for the RL agent.
		It follows the Epsilon-Greedy Algorithm which balances the need for
		exploitation and exploration.

		:param board: The tictactoe game board
		:type board: TicTacToe
		"""

		if self.mode == TRAINING_MODE:
			n = random.uniform(0, 1)

			if n < self.epsilon:
				anyMove = random.choice(board.remainingMoves)
				moveLegal = board.makeMove(anyMove, self.letter)

				if not moveLegal:
					print('*** WARNING ILLEGAL MOVE BY RL ***')

			else:
				self.getRLMove(board)

			# Call rewardState (make sure to pass board and previousState as arguments)
			# Set previousState equal to a copy of the board

			self.previousState = board.copy()
			return self.rewardState(board, self.previousState)

		else:
			self.getRLMove(board)


		# *** NOT IMPLEMENTED YET!! ***
		pass

	def rewardState(self, board, prevBoard=None):
		"""
		This method updates the policy (the valueFunction dictionary)

		:param board: The tictactoe game board
		:type board: TicTacToe
		:param prevBoard: The previous tictactoe game board
		:type prevBoard: TicTacToe
		"""

		# *** NOT IMPLEMENTED YET!! ***

		if prevBoard == None:
			reward = self.getReward(board)
			key = board.getKey(self.letter)
			value = self.valueOfState(key)

			self.valueFunction[key] = value + self.learningRate * reward

			# Get the reward for board, call getReward ☑️
			# Get the key for the board (board.getKey(self.letter)) ☑️
			# Get the value associated with the key, call valueOfState(key) ☑️
			# Update the dictionary, valueFunction, using key to: value + self.learningRate * reward ☑️

		else: #
			reward = self.getReward(board)
			key = board.getKey(self.letter)
			currentValue = self.valueOfState(key)

			prevKey = prevBoard.getKey(self.letter)
			prevValue = self.valueOfState(prevKey)

			self.valueFunction[prevKey] = prevValue + self.learningRate * (reward + self.discountRate * currentValue) - prevValue

			# Get the reward for board, call getReward ☑️
			# Get the key for the current board (board.getKey(self.letter)) ☑️
			# Get the value associated with the current board key, call valueOfState(key) ☑️
			# Get the key for the previous board (prevBoard.getKey(self.letter)) ☑️
			# Get the value associated with the previous board key, call valueOfState(previous␣ ˓→key) ☑️
			# Update the dictionary, valueFunction, using the previous board key to: ☑️
			# valuePrev␣ ˓→+ self.learningRate * (reward +(self.discountRate * valueCurrent) - valuePrev) ☑️

		pass

	def getRLMove(self, board) :
		"""
		This method performs moves for the RL agent while it's in training. It
		will either select a move at random (for exploration) or select the best
		move according to the state value table (for exploitation).

		:param board: The tictactoe game board
		:type board: TicTacToe
		"""

		bestMove = None
		bestValue = -99999

		for location in board.remainingMoves:
			cboard = board.copy()
			cboard.makeMove(location, self.letter)
			key = cboard.getKey(self.letter)

			if key in self.valueFunction :
				if self.valueFunction[key] >= bestValue :
					bestValue = self.valueFunction[key]
					bestMove = location

		if bestMove is not None:
			move = bestMove
		else:
			move = random.choice(board.remainingMoves)

		moveLegal = board.makeMove(move, self.letter)

		if not moveLegal:
			print('*** WARNING ILLEGAL MOVE BY RL ***')

	def valueOfState(self, key) :
		"""
		This method returns the value of a state; helper method

		:param key: The state of the game board
		:type key: String
		:return: Float
		"""

		if key in self.valueFunction :
			return self.valueFunction[key]
		else :
			self.valueFunction[key] = 0
			return 0

	def getReward(self, board):
		"""
		Advanced reward function with strategic tactical considerations:
		1. Win/Loss/Draw with proper incentive hierarchy
		2. Fork creation and prevention
		3. Strategic position control
		4. Time-based reward adjustments
		5. Defensive and offensive tactics

		:param board: The tictactoe game board
		:type board: TicTacToe
		:return: Float representing the reward value
		"""
		winner = board.getWinner()
		
		# Terminal state rewards with enhanced differentiation
		if board.isGameOver():
			if winner is not None and winner.letter == self.letter:
				# Win: higher reward for faster wins
				return 10.0 + max(0, (9 - board.moveCount))  # Bonus for quick wins
			elif winner is not None:
				# Loss: clear negative reinforcement
				return -10.0
			else:
				# Draw: positive but less than win (clear hierarchy)
				return 2.0  # Significantly better than losing, worse than winning
		
		# Non-terminal state rewards
		reward = 0.0
		
		# Strategic position control
		if board.board[4] == self.letter:  # Center
			reward += 0.8
		elif board.board[4] == self.opponent:
			reward -= 0.6  # Penalty if opponent controls center
		
		# Corners are strategically important
		corners = [0, 2, 6, 8]
		for corner in corners:
			if board.board[corner] == self.letter:
				reward += 0.3
			elif board.board[corner] == self.opponent:
				reward -= 0.2
		
		# Tactical analysis
		winning_patterns = [
			[0,1,2], [3,4,5], [6,7,8],  # Rows
			[0,3,6], [1,4,7], [2,5,8],  # Columns
			[0,4,8], [2,4,6]            # Diagonals
		]
		
		my_two_in_a_row_count = 0
		opponent_two_in_a_row_count = 0
		
		# Enhanced pattern analysis
		for pattern in winning_patterns:
			line = [board.board[i] for i in pattern]
			
			# Offensive opportunities
			if line.count(self.letter) == 2 and line.count('*') == 1:
				my_two_in_a_row_count += 1
				reward += 1.5  # Strong incentive to create winning opportunities
				
			# Defensive necessities
			elif line.count(self.opponent) == 2 and line.count('*') == 1:
				opponent_two_in_a_row_count += 1
				reward -= 1.8  # Strong incentive to block opponent wins
				
			# Building potential (one marker with two empty spaces)
			elif line.count(self.letter) == 1 and line.count('*') == 2:
				reward += 0.3
				
			# Opponent building potential
			elif line.count(self.opponent) == 1 and line.count('*') == 2:
				reward -= 0.2
		
		# Fork detection and prevention (having multiple winning paths)
		if my_two_in_a_row_count >= 2:
			reward += 3.0  # Major reward for creating a fork
			
		if opponent_two_in_a_row_count >= 2:
			reward -= 3.5  # Stronger penalty for allowing opponent forks
		
		# Game progression weighting
		if board.moveCount <= 2:  # Opening moves
			reward *= 0.8  # Focus on strategic positioning early
		elif board.moveCount >= 6:  # Late game
			reward *= 1.4  # Emphasize tactical plays in late game
			
		return reward
		
class MINIPlayer(Player) :

	"""
	This class represents a MiniMax player.
	"""

	def __init__(self, letter, playerType=MINIMAX_AGENT) :
		"""
		When creating a MINIPlayer you must specify a letter, either 'X' or 'O'
		(both capitilised).  Do not specify the playerType.

		:param letter: The letter the player uses, can only be 'X' or 'O'
		:type letter: String
		:param playerType: MINIMAX_AGENT
		:type playerType: Integer
		"""

		super().__init__(letter, playerType)

	def makeMove(self, board):
		"""
		This method performs a move for the Minimax player.

		:param board: The tictactoe game board
		:type board: TicTacToe
		"""

		playerMove = self.minimax(board)
		moveLegal = board.makeMove(playerMove, self.letter)

		if not moveLegal:
			print('*** WARNING ILLEGAL MOVE BY MINIMAX ***')

	def minimax(self, board):
		"""
		This method will be implemented by the student as part of the lab. It
		uses a recursive helper method to search the game tree for an optimal
		move.  It returns the best possible move.

		:param board: The tictactoe game board
		:type board: TicTacToe
		:return: Integer
		"""

		# *** NOT IMPLEMENTED YET!! ***

		# Define a variable, children, that contains the all remaining moves
		# Define a variable bestScore and initialise it to -999
		# Define a variable bestMove and initialise it to None
		# for each move in children:
		# Make a copy of board
		# Make move on the copy of board
		# Call minimaxHelper(copy of board, False) and save the score it returns if score > bestScore then
		# Assign score to bestScore
		# Assign move to bestMove
		# return bestMove


		# children = []
		# for i in range(len(board)):
			

		# 		new_board = board.copy()
		# 		new_board[i] = self.firstPlayer

		# bestScore = -999
		# bestMove = None


	def minimaxHelper(self, board, maximiser):
		"""
		This method will be implemented by the student as part of the lab. It
		is a recursive method that will search a game tree for an optimal move.
		It returns the score of the move (board) based on the minimax algorithm.

		:param board: The tictactoe game board
		:type board: TicTacToe
		:param maximiser: True if it's the maximiser's turn otherwise False
		:type maximiser: Boolean
		:return: Integer
		"""

		# *** NOT IMPLEMENTED YET!! ***

		return 0


	def scoreGame(self, board):
		"""
		This method will be implemented by the student as part of the lab. This
		method will assign a score to the board.  It returns 10 if the player
		won, -10 if the opponent won, and 0 for all other conditions.

		:param board: The tictactoe game board
		:type board: TicTacToe
		:return: Integer
		"""

		# *** NOT IMPLEMENTED YET!! ***

		return 0

class HUMANPlayer(Player) :
	"""
	This class represents a person playing tictactoe.
	"""

	def __init__(self, letter, playerType=HUMAN_AGENT):
		"""
		When creating a HUMANPlayer you must specify a letter, either 'X' or 'O'
		(both capitilised).  Do not specify the playerType.

		:param letter: The letter the player uses, can only be 'X' or 'O'
		:type letter: String
		:param playerType: HUMAN_AGENT
		:type playerType: Integer
		"""

		super().__init__(letter, playerType)

	def requestMove(self):
		"""
		This method ask the user to enter a move.  There's no input validation.
		The user should enter a number between 0 and 8 (inclusive).

		:return: Integer
		"""

		userInput = input("Player " + self.letter + ", enter a move (e.g. 0...8) : ")
		userInput = userInput.strip()

		if userInput == "quit":
			return None

		return int(userInput)

	def makeMove(self, board):
		"""
		This method allows a user, HUMAN, to enter his or her move

		:param board: The tictactoe game board
		:type board: TicTacToe
		"""

		moveLegal = False

		while not moveLegal:
			playerMove = self.requestMove()

			if playerMove is None :
				board.userQuit = True
				moveLegal = True
			else :
				moveLegal = board.makeMove(playerMove, self.letter)


class Tournament :
	"""
	This class performs a tournament between two tictactoe players. Four games
	are played where each player gets to go first twice twice.  By default the
	board is not drawn.  If a human is playing in the tournament, call
	enableHumanPlayer() to show the board.
	"""

	def __init__(self):
		self.humanPlaying = False

	def enableHumanPlayer(self) :
		"""
		This method enables board drawing, i.e., if called the board is
		drawn during the tournament.  This should only be used if one of the
		players is human.
		"""

		self.humanPlaying = True

	def start(self, player1, player2, games=1) :
		"""
		This method performs the tournament.  Four games are played.
		Each player gets to go first in 2 of the four games.

		:param player1: Player 1
		:type player1: Player, RLPlayer, MINIPlayer or HUMANPlayer
		:param player2: Player 2
		:type player2: Player, RLPlayer, MINIPlayer or HUMANPlayer
		:param games: The number of games to play
		:type games: Integer
		"""

		for _ in range(games):

			self.game(player1, player2)
			self.elo(player1, player2)

			if self.humanPlaying:
				if player1.winner:
					print(f'Winner: {player1.name}')
				elif player2.winner:
					print(f'Winner: {player2.name}')
				else:
					print(f'Draw')

	def game(self, p1, p2) :
		"""
		This method executes a single game of tictactoe between
		player1 and player2

		:param p1: Player 1
		:type p1: Player, RLPlayer, MINIPlayer or HUMANPlayer
		:param p2: Player 2
		:type p2: Player, RLPlayer, MINIPlayer or HUMANPlayer
		"""

		board = TicTacToe()
		board.setPlayers(p1, p2)

		if self.humanPlaying :
			board.drawBoard()

		while not board.isGameOver():

			player = board.next()
			player.makeMove(board)

			if self.humanPlaying :
				board.drawBoard()

		player = board.getWinner()

		if player:
			player.winner = True

	def elo(self, player1, player2) :
		"""
		This method updates each players rating according to the ELO rating
		system

		:param player1: Player 1
		:type player1: Player, RLPlayer, MINIPlayer or HUMANPlayer
		:param player2: Player 2
		:type player2: Player, RLPlayer, MINIPlayer or HUMANPlayer
		"""

		K = 30
		qa = 10**(player1.rating/400)
		qb = 10**(player2.rating/400)

		e1 = qa / (qa + qb)
		e2 = qb / (qa + qb)

		if player1.winner:
			r1 = player1.rating + K * (1 - e1)
			r2 = player2.rating + K * (0 - e2)
			player1.gamesW += 1
			player2.gamesL += 1
		elif player2.winner :
			r1 = player1.rating + K * (0 - e1)
			r2 = player2.rating + K * (1 - e2)
			player2.gamesW += 1
			player1.gamesL += 1
		else :
			r1 = player1.rating + K * (1 - e1)
			r2 = player2.rating + K * (1 - e2)
			player1.gamesD += 1
			player2.gamesD += 1

		player1.rating = r1
		player2.rating = r2

	def printStats(self, players) :
		"""
		This method prints the stats (number of games won, lost, drawn
		and rating) for player1 and player2

		:param players: List of Players
		"""

		for player in players :
			print(player.name  + " " + str(player.gamesW) +  "W " +
			str(player.gamesL) + "L " + str(player.gamesD) + "D " +
			str(round(player.rating,2)))
