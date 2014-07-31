"""
Loyd's Fifteen puzzle - solver and visualizer
Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors
"""

import poc_fifteen_gui

class Puzzle:
    """
    Class representation for the Fifteen puzzle
    """

    def __init__(self, puzzle_height, puzzle_width, initial_grid=None):
        """
        Initialize puzzle with default height and width
        Returns a Puzzle object
        """
        self._height = puzzle_height
        self._width = puzzle_width
        self._grid = [[col + puzzle_width * row
                       for col in range(self._width)]
                      for row in range(self._height)]

        if initial_grid != None:
            for row in range(puzzle_height):
                for col in range(puzzle_width):
                    self._grid[row][col] = initial_grid[row][col]

    def __str__(self):
        """
        Generate string representaion for puzzle
        Returns a string
        """
        ans = ""
        for row in range(self._height):
            ans += str(self._grid[row])
            ans += "\n"
        return ans

    #####################################
    # GUI methods

    def get_height(self):
        """
        Getter for puzzle height
        Returns an integer
        """
        return self._height

    def get_width(self):
        """
        Getter for puzzle width
        Returns an integer
        """
        return self._width

    def get_number(self, row, col):
        """
        Getter for the number at tile position pos
        Returns an integer
        """
        return self._grid[row][col]

    def set_number(self, row, col, value):
        """
        Setter for the number at tile position pos
        """
        self._grid[row][col] = value

    def clone(self):
        """
        Make a copy of the puzzle to update during solving
        Returns a Puzzle object
        """
        new_puzzle = Puzzle(self._height, self._width, self._grid)
        return new_puzzle

    ########################################################
    # Core puzzle methods

    def current_position(self, solved_row, solved_col):
        """
        Locate the current position of the tile that will be at
        position (solved_row, solved_col) when the puzzle is solved
        Returns a tuple of two integers        
        """
        solved_value = (solved_col + self._width * solved_row)

        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == solved_value:
                    return (row, col)
        assert False, "Value " + str(solved_value) + " not found"

    def update_puzzle(self, move_string):
        """
        Updates the puzzle state based on the provided move string
        """
        zero_row, zero_col = self.current_position(0, 0)
        for direction in move_string:
            if direction == "l":
                assert zero_col > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col - 1]
                self._grid[zero_row][zero_col - 1] = 0
                zero_col -= 1
            elif direction == "r":
                assert zero_col < self._width - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col + 1]
                self._grid[zero_row][zero_col + 1] = 0
                zero_col += 1
            elif direction == "u":
                assert zero_row > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row - 1][zero_col]
                self._grid[zero_row - 1][zero_col] = 0
                zero_row -= 1
            elif direction == "d":
                assert zero_row < self._height - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row + 1][zero_col]
                self._grid[zero_row + 1][zero_col] = 0
                zero_row += 1
            else:
                assert False, "invalid direction: " + direction

    ##################################################################
    # Phase one methods

    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean
        """
        # replace with your code
        
        if  self._grid[target_row][target_col] == 0:
            for row in range(target_row +1, self._height):
                for col in range(self._width):
                    if self._grid[row][col] != col + self._width * row:
                        return False
            for col in range(target_col +1, self._width):
                if self._grid[target_row][col] != col + self._width * target_row:
                    return False
            if target_row +1 == self._height:
                for col in range(target_col +1, self._width):
                    if self._grid[target_row][col] != col + self._width * target_row:
                        return False        
            return True         
        return False 
    
    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        """
        # replace with your code
        
        move_string = ""
        assert self.lower_row_invariant(target_row, target_col), "Not satisfy invariant!"
        cur_pos = self.current_position(target_row, target_col)
        move_string += "u" * (target_row - cur_pos[0])    
        if  cur_pos[1] < target_col:
            move_string += "l" * (target_col - cur_pos[1])
            if cur_pos[0] == target_row:
                move_string += "urdlu" + "drulrdrul" * (target_col - cur_pos[1] -1)
                move_string += "druld" 
            else:
                move_string += "drulrdrul" * (target_col - cur_pos[1] -1)
                move_string += "druld" * (target_row - cur_pos[0]) 
        elif cur_pos[1] == target_col:            
            if cur_pos[0] == target_row - 1:
                move_string += "ld"
            else:
                move_string += "lrdlu" + "druld" * (target_row - cur_pos[0])
        elif cur_pos[1] > target_col:
            move_string += "r" * (cur_pos[1] - target_col -1)
            if cur_pos[0] == target_row - 1:
                move_string += "urdlu" + "rdlulrdlu" * (cur_pos[1] - target_col)
                move_string += "druld" * 2
            else:    
                move_string += "rdlulrdlu" * (cur_pos[1] - target_col)
                move_string += "druld" * (target_row - cur_pos[0])
        self.update_puzzle(move_string)
        return move_string
    
    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        "rdlulrdlu" move to left one position
        "druld" move to down one position
        "drulrdrul" move to right one position
        """
        
        # replace with your code
        move_string = ""
        if self._grid[target_row -1][0] == self._width * target_row:
            move_string += "u" + "r" * (self._width - 1)
        else:
            cur_pos = self.current_position(target_row, 0)
            move_string += "u" * (target_row - cur_pos[0] )+ "r" * cur_pos[1]
            if cur_pos[1] == 0:
                move_string += "drul" + "druld" * (target_row - cur_pos[0] -1)
            elif target_row -1 == cur_pos[0]:
                move_string += "lurdlu" + "rdlulrdlu" * (cur_pos[1] -1)
                move_string += "druld" * (target_row - cur_pos[0]) 
            else:
                move_string += "l" + "rdlulrdlu" * (cur_pos[1] -1)
                move_string += "druld" * (target_row - cur_pos[0] -1)
            move_string += "ruldrdlurdluurddlu" + "r" * (self._width - 1) 
        self.update_puzzle(move_string)
        return move_string  

    #############################################################
    # Phase two methods

    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        # replace with your code
        if self._grid[0][target_col] == 0:
            for col in range(target_col + 1, self._width):
                if self._grid[0][col] != col:
                    return False
            for col in range(target_col, self._width):
                if self._grid[1][col] != col + self._width:
                    return False
            for row in range(2, self._height):
                for col in range(self._width):
                    if self._grid[row][col] != col + self._width * row :
                        return False
            return True
        return False   
    
    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        # replace with your code
        if self._grid[1][target_col] == 0:
            for row in range(2):
                for col in range(target_col + 1, self._width):
                    if self._grid[row][col] != col + self._width * row:
                        return False
            for row in range(2, self._height):
                for col in range(self._width):
                    if self._grid[row][col] != col + self._width * row :
                        return False
            return True
        return False

    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        # replace with your code
        move_string = ""
        if self._grid[0][target_col - 1] == target_col:
            move_string += "ld"
        else:
            cur_pos = self.current_position(0, target_col)
            if cur_pos[1] < target_col:
                move_string += "l" * (target_col - cur_pos[1])
            if cur_pos[0]  == 0:
                move_string += "rdlu" 
            move_string += "rdlur" * (target_col - cur_pos[1] -1) + "ldurdlurrdluldrruld"
        self.update_puzzle(move_string)
        return move_string 

    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        # replace with your code
        move_string = ""
        cur_pos = self.current_position(1, target_col)
        if cur_pos[1] < target_col:
            move_string += "l" * (target_col - cur_pos[1])
        move_string += "u"
        if cur_pos[0]  == 0:
            move_string += "rdlur" * (target_col - cur_pos[1])
        else:
            move_string += "r" + "rdlur" * (target_col - cur_pos[1] -1)
        self.update_puzzle(move_string)
        return move_string
    
    ###########################################################
    # Phase 3 methods

    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        # replace with your code
        move_string = ""
        cur_pos = self.current_position(0, 0)
        if cur_pos[0] > 0:
            move_string += "u"
        if cur_pos[1] > 0:
            move_string += "l"
        if self.get_number(0, 1) != 1:
            if self.get_number(0, 1) < self.get_number(1, 0):
                move_string += "rdlu"
            else:
                move_string += "drul"
        self.update_puzzle(move_string)            
        return move_string
    
    def move_zero(self, target_row, target_col):
        """
        Move zero to target position,
        Updates the puzzle and returns a move string
        """
        # replace with your code
        move_string = ""
        zero_row, zero_col = self.current_position(0, 0)
        if zero_col > target_col:
            move_string += "l" * (zero_col - target_col)
        elif zero_col < target_col:
            move_string += "r" * (target_col - zero_col)
        move_string += "d" * (target_row - zero_row)
        self.update_puzzle(move_string)            
        return move_string
    
    def opt_solution(self, move_str):
        """
        To remove redudant move step and return updated move_strings
        """

        prev_len = len(move_str) + 1
        while len(move_str) < prev_len:
            prev_len = len(move_str)
            move_str = move_str.replace("lr", "").replace("rl", "").replace("ud", "").replace("du", "")
        return move_str
    
    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        # replace with your code
        move_string = ""
        test = self.clone()
        if test.lower_row_invariant(0,0) == False:
            for row0 in range(test.get_height()):
                for col0 in range(test.get_width()):
                    row = test.get_height() - row0 - 1
                    col = test.get_width() - col0 - 1
                    if row > 1 and col > 0:
                        if test.get_number(row, col) != col + test.get_width() * row:
                            move_string += test.move_zero(row, col)
                            move_string += test.solve_interior_tile(row, col)
                    elif row > 1 and col == 0:
                        if test.get_number(row, 0) !=  test.get_width() * row:
                            move_string += test.move_zero(row, 0)
                            move_string += test.solve_col0_tile(row)
                    elif row == 1  and col > 1:
                        if test.get_number(1, col) != col +  test.get_width():
                            move_string += test.move_zero(1, col)
                            assert test.row1_invariant(col), "Puzzle not satisfied invariant"
                            move_string += test.solve_row1_tile(col)
                            move_string += test.move_zero(0, col)
                            assert test.row0_invariant(col), "Puzzle not satisfied invariant"
                            move_string += test.solve_row0_tile(col)
                            assert test.row1_invariant(col -1), "Puzzle not satisfied invariant"
                    elif row <= 1 and col <= 1:
                        move_string += test.solve_2x2()
        out_str = test.opt_solution(move_string)                        
        self.update_puzzle(out_str)
        return out_str 
    
# Start interactive simulation
#poc_fifteen_gui.FifteenGUI(Puzzle(4, 4))
#wbh = obj.solve_puzzle()
#print obj, len(wbh)
#print len(obj.solve_puzzle())
#print obj.solve_interior_tile(2, 2)
#poc_fifteen_gui.FifteenGUI(obj)
#print obj.solve_interior_tile(2, 1)
#poc_fifteen_gui.FifteenGUI(obj)
