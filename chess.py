
class ChessMoves:

	"""
		A Class housing all the necessary functions for 
		finding a piece's minimum distance betweent two 
		squares on a chessboard.
	"""

	def minimum_moves(self, piece, start, goal):

		"""
			The delegating function. Determines the correct 
			subroutine to send execution to based on the inputted piece.
			Also handles the base case when start and goal position are the same.

			@param piece: a string representing the chess piece in question
			@param start: a 2-tuple containing the (x,y) coordinates of the piece's starting position.
			@param goal: a 2-tuple containing the (x,y) coordinates of the piece's goal position.
			@return: 0 if START and GOAL are equal, else the return value of the correct subroutine.
		"""

		if start == goal:
			return 0
		if piece.lower() == "king":
			return self.king_dist(start, goal)
		if piece.lower() == "knight":
			return self.knight_dist(start, goal)
		if piece.lower() == "bishop":
			return self.bishop_dist(start, goal)

	def bishop_dist(self, start, goal):

		"""
			A subroutine to handle calculating a bishop's START to GOAL distance.

			@param start: a 2-tuple containing the (x,y) coordinates of the bishop's starting position.
			@param goal: a 2-tuple containing the (x,y) coordinates of the bishop's goal position.
			@return: the minimum number of moves required for the bishop to reach GOAL from START. This is always
					either 1 or 2 for reachable positions for a bishop. If the bishop cannot reach GOAL from START,
					-1 is returned.
		"""

		if abs(start[0]-start[1]) % 2 != 0 and abs(goal[0]-goal[1]) % 2 == 0:
			return -1
		elif abs(start[0]-start[1]) % 2 == 0 and abs(goal[0]-goal[1]) % 2 != 0:
			return -1
		elif abs(start[0] - goal[0]) == abs(start[1] - goal[1]):
			return 1
		else:
			return 2

	def king_dist(self, start, goal):

		"""
			A subroutine to handle calculating a king's START to GOAL distance.
			We make the key observation that, since a king moves exactly one place
			in any direction per move, this value is simply the greater of the
			differences between the two x-values and the two y-values.

			@param start: a 2-tuple containing the (x,y) coordinates of the king's starting position.
			@param goal: a 2-tuple containing the (x,y) coordinates of the king's goal position.
			@return: the minimum number of moves required for the king to reach GOAL from START.
		"""

		return max(abs(start[0] - goal[0]), abs(start[1] - goal[1]))


	def get_knight_next_moves(self, curr):

		"""
			A helper function for `knight_dist()` that gets the 8 possible moves 
			a knight can make from any position CURR and returns a list of those
			which are valid (aka those which result in a position still on the board).

			@param curr: a tuple of the knight's current position in (x,y) format.
			@return: a list of valid knight moves from CURR.
		"""

		currx, curry = curr
		possible_moves = [(currx + 1, curry + 2), (currx - 1, curry + 2), (currx + 2, curry +1), (currx - 2, curry + 1), 
						(currx + 1, curry - 2), (currx - 1, curry - 2), (currx + 2, curry - 1), (currx - 2, curry - 1)]

		return [move for move in possible_moves if self.validate_input(move)]

	def knight_dist(self, start, goal):

		"""
			A subroutine implementing a Breadth-First Search to determine a knight's
			START to GOAL distance.

			@param start: a 2-tuple containing the (x,y) coordinates of the knight's starting position.
			@param goal: a 2-tuple containing the (x,y) coordinates of teh knight's goal position.
			@return: the minimum number of moves required for the knight to reach GOAL from START.
		"""

		visited = {}
		stack = [(start, 0)]
		while len(stack) > 0:
			curr, dist = stack.pop(0)
			if curr == goal: 
				return dist
			else: 
				next_moves = self.get_knight_next_moves(curr)
				for move in next_moves:
					if self.validate_input(move) and move not in visited:
						stack.append((move, dist + 1))
						visited[move] = True
		return -1

	def validate_input(self, pos):

		"""
			A function to handle checking that a position is a valid tuple with
			coordinates inside the bounds of an 8x8 chessboard.

			@param pos: a 2-tuple containing the (x,y) coordinates of the position in question.
			@return: True if POS is a valid position, else FALSE.
		"""

		if type(pos) != tuple or len(pos) != 2:
			return False

		for coord in pos:
			if coord < 0 or coord > 7:
				return False

		return True

def execute():

	"""
		A function to execute the program from the command line. Prompts the user
		for PIECE, START, and GOAL inputs; handles validation of these inputs and 
		reprompting the user in the event any inputs are invalid; outputs information
		to the user describing the result of using the `ChessMoves` class to determine
		the minimum moves on the given inputs.

		Sample input:

		'king'
		(0,0)
		(4,6)

		'bishop'
		(0,0)
		(2,7)

		Sample output:

		'The king can reach the target position in 6 moves!'

		'The bishop cannot reach the target position :('
	"""

	chess_moves = ChessMoves()

	print("\nWelcome to Chess Moves Calculator!\n")

	piece = raw_input("What kind of piece do you have? (Please enter one of 'Bishop', 'King', or 'Knight'): ")
	legal_pieces = ["bishop", "king", "knight"]
	while piece.lower() not in legal_pieces:
		piece = raw_input("\nInvalid piece. Please try again: ")

	start_string = raw_input("\nWhat is your piece's starting postion? (Please use the format (x,y)): ")
	while len(start_string) != 5 or start_string[0] != '(' or start_string[2] != ',' or start_string[4] != ')' \
	or not chess_moves.validate_input((int(start_string[1]), int(start_string[3]))):
		start_string = raw_input("\nInvalid starting poistion. Please ensure the input is formatted correctly,\nand that both values are in [0,7]: ")

	goal_string = raw_input("\nWhat is your piece's target position? (Please use the format (x,y)): ")
	while len(goal_string) != 5 or goal_string[0] != '(' or goal_string[2] != ',' or goal_string[4] != ')' \
	or not chess_moves.validate_input((int(goal_string[1]), int(goal_string[3]))):
		goal_string = raw_input("\nInvalid target poistion. Please ensure the input is formatted correctly,\nand that both values are in [0,7]: ")

	start = (int(start_string[1]), int(start_string[3]))
	goal = (int(goal_string[1]), int(goal_string[3]))

	min_moves = chess_moves.minimum_moves(piece, start, goal)

	if min_moves >= 0:
		print("\nThe " + piece + " can reach the target position in " + str(min_moves) + " moves!\n")
	else:
		print("\nThe " + piece + " cannot reach the target position :(\n")

execute()
