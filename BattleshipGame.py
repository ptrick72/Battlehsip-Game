import random

class Ship:
    def __init__(self, type, size):
        self.type = type
        self.size = size
        self.alignment = "h" # init value, will be overwritten
        self.coordinates = []
        self.hits = 0
        
    def __repr__(self):
        return "I am a {type} of size {size}".format(type=self.type, size=self.size)

    def get_size(self):
        return self.size
    
    def get_type(self):
        return self.type

    def set_alignment(self, alignment):
        if alignment == "h" or alignment == "v":
            self.alignment = alignment
        else:
            return False
        return True

    def set_coordinates(self, coordinates):
        self.coordinates = coordinates

    def get_hits(self):
        return self.hits

class Grid:
    def __init__(self, type, size):
        self.type = type
        self.size = size
        self.grid = []
        self.build_grid(size)

    def __repr__(self):
        return self.type
    
    def build_grid(self, size):
        # build grid
        gridline = []
        for i in range(size):
            gridline.append(0)
        for i in range(size):
            self.grid.append(list(gridline))
            self.grid.append(list(gridline))
    
    def coordinates_inbound_check(self, coordinates):
        if len(coordinates) == 0: return False
        if int(coordinates[0]) > self.size or int(coordinates[0]) < 1: return False
        if int(coordinates[1]) > self.size or int(coordinates[1]) < 1: return False
        return True

    def check_input_ship_placement(self, ship, info):
        if len(info) == 0: return "no input"
        if info[0] != "h" and info[0] != "v": return "unkown alignment"
        if int(info[1]) > len(self.player_ship_grid) or int(info[1]) < 1: return "x out of scope"
        if int(info[2]) > len(self.player_ship_grid) or int(info[2]) < 1: return "y out of scope"
        if info[0] == "h":
            max_y = len(self.player_ship_grid)
            max_x = len(self.player_ship_grid)-len(ship)+1
        else:
            max_y = len(self.player_ship_grid)-len(ship)+1
            max_x = len(self.player_ship_grid)
        if int(info[2]) > max_y: return "y too big to place ship"
        if int(info[1]) > max_x: return "x too big to place ship"
        x = int(info[1])-1
        y = int(info[2])-1
        if self.player_ship_grid[y][x] != 0: return "already ship there"
        return True
    

class Player:
    def __init__(self, name):
        self.name = name
        self.ship_grid = Grid("ship", 7)
        self.shot_grid = Grid("shot", 7)
        self.warship = Ship("warship", 4)
        self.cruiser = Ship("Cruiser", 3)
        self.destroyer = Ship("Destroyer", 2)
    
    def __repr__(self):
        return "I am {name}".format(name=self.name)

    def place_ship(self, ship, ship_alignment, start_y, start_x):
        # place ships if x, y are in scope
        y = start_y
        x = start_x
        ship_y_position = []
        ship_x_position = []
        if y > len(self.ship_grid.grid) or y < 0: return "y out of scope"
        if x > len(self.ship_grid.grid) or x < 0: return "x out of scope"
        for part in ship.get_size():
            if self.ship_grid.grid[y][x] == 0:
                # place ship only if coordinate is empty
                self.ship_grid.grid[y][x] = ship
                # keep track of the coordinates for restore
                ship_y_position.append(y)
                ship_x_position.append(x)
            else:
                # if a ship is there, restore
                for pos_y in ship_y_position:
                    for pos_x in ship_x_position:
                        self.ship_grid.grid[pos_y][pos_x] = 0
                return "already ship there"
            if ship_alignment == "horizontal":
                x += 1
            elif ship_alignment == "vertical":
                y += 1
            else:
                return "invalid direction"
        return "ship placed"

    def shoot(self, target, y, x):
        # check target grid for ship
        if target.ship_grid[y][x] == 0:
            ship_type = "n"
        elif target.ship_grid[y][x] == "w":
            ship_type = "w"
        elif target.ship_grid[y][x] == "c":
            ship_type = "c"
        elif target.ship_grid[y][x] == "d":
            ship_type = "d"
        else:
            return "shoot error"
        if shot_grid[y][x] != 0: 
            return "already shot"
        else: 
            # mark hit ship on grid
            shot_grid[y][x] = ship_type
            if ship_type == "n": return "miss"
            else: return "hit"

    def update_destroyed_ships(self, whose_ships):
        if whose_ships == "player": 
            # check if ship is destroyed by comparing hit with length
            if self.get_hits(self.warship, self.hal_shot_grid) == len(self.warship):
                self.player_warship_destroyed[0] = True
            if self.get_hits(self.cruiser, self.hal_shot_grid) == len(self.cruiser):
                self.player_cruiser_destroyed[0] = True
            if self.get_hits(self.destroyer, self.hal_shot_grid) == len(self.destroyer):
                self.player_destroyer_destroyed[0] = True
        elif whose_ships == "hal":
             # check if ship is destroyed by comparing hit with length
            if self.get_hits(self.warship, self.player_shot_grid) == len(self.warship):
                self.hal_warship_destroyed[0] = True
            if self.get_hits(self.cruiser, self.player_shot_grid) == len(self.cruiser):
                self.hal_cruiser_destroyed[0] = True
            if self.get_hits(self.destroyer, self.player_shot_grid) == len(self.destroyer):
                self.hal_destroyer_destroyed[0] = True 
        else:
            return "unkown player"
        return "destroyed ships updated"


class Hal(Player):    
    def choose_ship_starting_point(self, ship, ship_alignment):
        # define function vars
        ship_placement = False
        ship_length = len(ship)
        time_out = 100
        # loop as long as we haven't found a starting point in grid
        # or time out is under 100
        while (ship_placement == False) or (time_out < 100):
            # get randon y and x for horizontal alignment
            if ship_alignment == "horizontal":
                start_y = random.randint(0,(7-1))
                start_x = random.randint(0, (7-ship_length))
            # get random y and x for vertical alignment
            else:
                start_y = random.randint(0, (7-ship_length))
                start_x = random.randint(0,(7-1))
            # temp y and x to increase in for loop
            y = start_y
            x = start_x
            # loop through ship length and check if coordinate is
            # already occupied
            for part in ship:
                if self.hal_ship_grid[y][x] == 0:   
                    ship_placement = True
                    if ship_alignment == "horizontal": x += 1
                    else: y +=1
                else:
                    ship_placement = False
            time_out += 1
        return start_y, start_x

    def place_hal_ships(self):
        # Warship
        y, x = self.get_hal_starting_point(self.warship, "horizontal")
        self.place_ship(self.hal_ship_grid, self.warship, "horizontal", y, x)
        # Cruiser
        y, x = self.get_hal_starting_point(self.cruiser, "vertical")
        self.place_ship(self.hal_ship_grid, self.cruiser, "vertical", y, x)
        # Destroyer
        y, x = self.get_hal_starting_point(self.destroyer, "horizontal")
        self.place_ship(self.hal_ship_grid, self.destroyer, "horizontal", y, x)
        # return affirmative message
        return "hal ships placed"



class Battleship:
    def __repr__(self):
        txt = """
        #####     #####    #######   #######   #        ######   ######   #    #   #   ######
        #    #   #     #      #         #      #        #        #        #    #   #   #    #
        #    #   #     #      #         #      #        #        #        #    #   #   #    #
        # ###    #######      #         #      #        ####     ######   ######   #   ######
        #    #   #     #      #         #      #        #             #   #    #   #   #
        #    #   #     #      #         #      #        #             #   #    #   #   #
        #####    #     #      #         #      ######   ######   ######   #    #   #   #
        
        ----------------------------------------------------------------------------------------------
        This is a simple Battleship game in which a human player can play against the computer (HAL).
        ----------------------------------------------------------------------------------------------

        The rules for battleship are as follows:

        - HAL places his ships on a 7x7 grid.
        
        - You place your ships on a 7x7 grid.
        
        - You have these ships:

        Ship Type | Size |
        Warship   |  4   |
        Cruiser   |  3   |
        Destroyer |  2   |

        - You and HAL take turns in shooting.

        - The grid looks as follows:

        0|1  |2  |3  |4  |5  |6  |7  |
        1|11 |21 |31 |41 |51 |61 |71 |
        2|12 |22 |32 |42 |52 |62 |72 |
        3|13 |23 |33 |43 |53 |63 |73 |
        4|14 |24 |34 |44 |54 |64 |74 |
        5|15 |25 |35 |45 |55 |65 |75 |
        6|16 |26 |36 |46 |56 |66 |76 |
        7|17 |27 |37 |47 |57 |67 |77 |

        - Btw, HAL isn't very intelligent, he just shoots randomly

        """
        return txt
    
    def __init__(self):
        print(self)
    
    def input_handler(self, input_type, input):
        # End
        # Display Grid
        # Enter Player Name
        # Enter Player Shot
        pass

    def check_gameover(self):
        pass

    def play(self):
       # Ask player for his name
       name = input("Please enter your name: ")
       self.human = Player(name)
       return self.human.name

        
game1 = Battleship()
msg = game1.play()
print(msg)