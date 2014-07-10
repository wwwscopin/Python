"""
Student portion of Zombie Apocalypse mini-project
"""

import random
import poc_grid
import poc_queue
import poc_zombie_gui

# global constants
EMPTY = 0 
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = "obstacle"
HUMAN = "human"
ZOMBIE = "zombie"


class Zombie(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human on grid with
    obstacles
    """

    def __init__(self, grid_height, grid_width, obstacle_list = None, 
                 zombie_list = None, human_list = None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        """
        poc_grid.Grid.__init__(self, grid_height, grid_width)
        if obstacle_list != None:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
            self._obstacle_list = obstacle_list
        else:
            self._obstacle_list = []
        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = list(human_list)  
        else:
            self._human_list = []
        
    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        poc_grid.Grid.clear(self)
        self._zombie_list = []
        self._human_list = []
        
    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        self._zombie_list.append((row, col))
                
    def num_zombies(self):
        """
        Return number of zombies
        """
        return len(self._zombie_list)
          
    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """
        # replace with an actual generator
        for zombie in self._zombie_list:
            yield zombie
        return

    def add_human(self, row, col):
        """
        Add human to the human list
        """
        self._human_list.append((row, col))
        
    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list)
    
    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        # replace with an actual generator
        for human in self._human_list:
            yield human
        return
    
    def obstacle(self):
        """
        Generator that yields the humans in the order they were added.
        """
        # replace with an actual generator
        for obstacle in self._obstacle_list:
            yield obstacle
        return
        
    def compute_distance_field(self, entity_type):
        """
        Function computes a 2D distance field
        Distance at member of entity_queue is zero
        Shortest paths avoid obstacles and use distance_type distances
        """
        visited =  poc_grid.Grid(self._grid_height, self._grid_width)
        visited.clear()
        distance_field =[[self._grid_height * self._grid_width for dummy_col in range(self._grid_width)] 
                       for dummy_row in range(self._grid_height)]
        for obstacle in self.obstacle():
            visited.set_full(obstacle[0], obstacle[1])
        
        boundary = poc_queue.Queue()
        if entity_type == ZOMBIE:
            for zombie in self.zombies():
                boundary.enqueue(zombie) 
        elif entity_type == HUMAN:
            for human in self.humans():
                boundary.enqueue(human) 
        for cell in boundary:
            visited.set_full(cell[0], cell[1])
            distance_field[cell[0]][cell[1]] = 0
    
        while len(boundary) > 0:
            current_cell = boundary.dequeue()
            neighbors = visited.four_neighbors(current_cell[0], current_cell[1])
            for neighbor in neighbors:
                if visited.is_empty(neighbor[0], neighbor[1]):
                    distance_field[neighbor[0]][neighbor[1]] = min(distance_field[neighbor[0]][neighbor[1]], distance_field[current_cell[0]][current_cell[1]] + 1)
                    visited.set_full(neighbor[0], neighbor[1])
                    boundary.enqueue(neighbor)                               
        return distance_field    
    
    def move_humans(self, zombie_distance):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
        human_list = []
        for human in self.humans():
            neighbors = self.eight_neighbors(human[0], human[1])
            distance = [zombie_distance[human[0]][human[1]]]
            loc = [human]
            
            for neighbor in neighbors:
                if self.is_empty(neighbor[0], neighbor[1]):
                    distance.append(zombie_distance[neighbor[0]][neighbor[1]])
                    loc.append(neighbor)
            wbh = loc[distance.index(max(distance))]          
            self.set_empty(human[0], human[1])
            human_list.append(wbh)
        self._human_list = human_list
        return human_list
                                    
    def move_zombies(self, human_distance):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        
        zombie_list = []
        for zombie in self.zombies():
            neighbors = self.four_neighbors(zombie[0], zombie[1])
            distance = [human_distance[zombie[0]][zombie[1]]]
            loc = [zombie]
            
            for neighbor in neighbors:
                if self.is_empty(neighbor[0], neighbor[1]):
                    distance.append(human_distance[neighbor[0]][neighbor[1]])
                    loc.append(neighbor)
            wbh = loc[distance.index(min(distance))]          
            self.set_empty(zombie[0], zombie[1])
            zombie_list.append(wbh)               
        self._zombie_list = zombie_list
        return zombie_list
            
               
                
# Start up gui for simulation - You will need to write some code above
# before this will work without errors

poc_zombie_gui.run_gui(Zombie(30, 40))

#test =Zombie(3, 3, [], [], [(2, 2)])
#print test.compute_distance_field('human')
