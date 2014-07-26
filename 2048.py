"""
Clone of 2048 game.
"""

import poc_2048_gui  
import random

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.    
OFFSETS = {UP: (1, 0), 
           DOWN: (-1, 0), 
           LEFT: (0, 1), 
           RIGHT: (0, -1)} 
   
def merge(line):
    """
    Helper function that merges a single row or column in 2048
    """
    # replace with your code
    temp=[0]*len(line)
    new_line=[0]*len(line)
    jdx=0
    for idx in range(len(line)):
        if line[idx] != 0:
            temp[jdx]=line[idx]
            jdx +=1
    comp=temp[1:]
    comp.append(0)
    idx=0
    jdx=0
    while idx <=len(line)-1:
        if temp[idx]==comp[idx]:
            new_line[jdx]=2*temp[idx]
            idx +=2
        else:  
            new_line[jdx]=temp[idx]
            idx +=1
        jdx +=1       
    return new_line

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        # replace with your code
        self.height=grid_height
        self.width=grid_width
        self.cells=[[0 for dummy_col in range(grid_width)] for dummy_row in range(grid_height)]
    
    def reset(self):
        """
        Reset the game so the grid is empty.
        """
        # replace with your code
        self.cells=[[0 for dummy_col in range(self.width)] for dummy_row in range(self.height)]
    
    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        # replace with your code
        return str([self.height,self.width])

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        # replace with your code
        return self.height
    
    def get_grid_width(self):
        """
        Get the width of the board.
        """
        # replace with your code
        return self.width

    def get_row(self, row):
        """return the row, starting at 0"""
        return self.cells[row]

    def get_col(self, col):
        """return the column, starting at 0"""
        return [self.get_tile(idx,col) for idx in range(self.height)]
    
    def set_row(self, row, lst):
        """set the row, starting at 0"""
        self.cells[row] = lst[:]

    def set_col(self, col, lst):
        """set the y-th column, starting at 0"""
        for idx in range(self.height):
            self.set_tile(idx, col, lst[idx])
    
    def get_empty_tiles(self):
        """return a (row, col) pair for each empty cell"""
        return [(row, col)
                for row in range(self.height)
                for col in range(self.width) if self.get_tile(row, col) == 0]
                            
    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        # replace with your code
        if direction ==UP:
            for idx in range(self.width):
                line=self.get_col(idx)
                self.set_col(idx, merge(line))
        elif direction ==DOWN:
            for idx in range(self.width):
                line=self.get_col(idx)
                line.reverse()
                wbh=merge(line)
                wbh.reverse()
                self.set_col(idx, wbh)
        elif direction==LEFT:
            for idx in range(self.height):
                line=self.get_row(idx)
                self.set_row(idx,merge(line))
        elif direction==RIGHT:
            for idx in range(self.height):
                line=self.get_row(idx)
                line.reverse()
                wbh=merge(line)
                wbh.reverse()
                self.set_row(idx,wbh)
        self.new_tile()
            
        
    def new_tile(self):
        """
        Create a new tile in a randomly selected empty 
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        # replace with your code
        val= random.choice([2]*9+[4])
        empty = self.get_empty_tiles()
        if empty:
            row, col = random.choice(empty)
            self.set_tile(row, col, val)
        
    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """        
        # replace with your code
        self.cells[row][col]=value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """        
        # replace with your code       
        return self.cells[row][col] 
 
    
poc_2048_gui.run_gui(TwentyFortyEight(4, 4))
