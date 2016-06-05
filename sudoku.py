#sudoku solver

import numpy as np

class Sudoku:
	def __init__(self, order=3):
		#initialize size and order variables and create puzzle
		self.order = int(order)
		self.size = self.order**2
		self.puzzle = np.zeros((self.size, self.size))

		#this was tricky to figure out, but we need to keep track of the 2x2 or 3x3 boxes
		self.boxArray = []
		for row in range(self.order):
			for column in range(self.order):
				self.boxArray.append(self.puzzle[row*order:row*order+order,column*order:column*order+order])
		

	def find_box_3(self,row,column):
		if 0 < row < 3:
			if 0 < column < 3:
				return 0
			elif 3 <= column < 3*2:
				return 1
			elif 3*2 <= column < 3*3:
				return 2
		elif 3 <= row < 3*2:
			if 0 < column < 3:
				return 3
			elif 3 <= column < 3*2:
				return 4
			elif 3*2 <= column < 3*3:
				return 5
		elif 3*2 <= row < 3*3:
			if 0 < column < 3:
				return 6
			elif 3 <= column < 3*2:
				return 7
			elif 3*2 <= column < 3*3:
				return 8

	def find_box_2(self,row,column):
		#based on the row and column number in the puzzle, determine which "quadrant" to check
		if 0 < row < 2:
			if 0 < column < 2:
				return 0
			elif 2 <= column < 4:
				return 1
		elif 2 <= row < 4:
			if 0 < column < 2:
				return 2
			elif 2 <= column < 4:
				return 3
			


	def generate(self):	
		status = True
		#reinitialize the puzzle to all zeros
		self.puzzle = np.zeros((self.size, self.size))
		#populate and randomize first row
		self.puzzle[0] = np.arange(1,self.size+1)
		np.random.shuffle(self.puzzle[0])
		#populate first "quadrant"
		self.boxArray[0] = self.puzzle[0:self.order,0:self.order]
		#populate first column with "quadrant" and row checks to avoid repeat numbers/unsolvable puzzles
		for row in xrange(1,self.size):
			value = np.random.randint(1,self.size+1)
			while value in self.puzzle[:,0] or (row == 1 and value in self.boxArray[0]):
				value = np.random.randint(1,self.size+1)
			self.puzzle[row,0] = value
		
		for row in xrange(1,self.size):
			for column in xrange(1,self.size):
				if self.order == 2:
					boxIndex = self.find_box_2(row, column)
				elif self.order == 3:
					boxIndex = self.find_box_3(row, column)
				print('Row: {}, Column: {}, boxIndex: {}'.format(row, column, boxIndex))
				guess = 0
				value = np.random.randint(1,self.size+1)
				while value in self.puzzle[row] or value in self.puzzle[:,column] or value in self.boxArray[boxIndex]:
					if guess < self.size**2:
						value = np.random.randint(1,self.size+1)
						#print('Guess: {}'.format(value))
						guess += 1
					else:
						status = False
						print('########FAIL########')
						print(self.puzzle)
						break
				self.puzzle[row,column] = value
				i = 0
				for row in range(self.order):
					for column in range(self.order):
						self.boxArray[i] = self.puzzle[row*self.order:row*self.order+self.order,column*self.order:column*self.order+self.order]
						i += 1
				#print(self.puzzle)
		return status

		
def main():
	sudoku = Sudoku(order=3)
	status = False
	while status == False:
		status = sudoku.generate()
	print(sudoku.puzzle)
if __name__ == '__main__':
	main()