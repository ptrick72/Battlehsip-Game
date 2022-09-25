import random

# ship class with functions and attributes
class Ship:
    def __init__(self, type, size):
        self.type = type
        self.size = size
        self.alignment = ""
        self.start_x = 0
        self.start_y = 0
        self.coordinates = []
        self.hits = 0
        
    def __repr__(self):
        return self.type

    # appends ship coordinates to list
    def add_coordinates(self, coordinates):
        self.coordinates.append(coordinates)

    # checks if ship has been destroyed
    def is_destroyed(self):
        if self.hits == self.size:
            return True
        else: return False

# grid class with functions and attributes
class Grid:
    def __init__(self, type, size):
        self.type = type
        self.size = size
        self.grid = []
        self.build_grid()

    def __repr__(self):
        return self.type
    
    # builds two dimensional grid
    def build_grid(self):
        # build grid
        gridline = []
        for i in range(self.size):
            gridline.append(0)
        for i in range(self.size):
            self.grid.append(list(gridline))
    
    # checks if a point is inside the grid
    def coordinate_inbound_check(self, coordinate):
        if int(coordinate) > self.size or int(coordinate) < 1: return False
        if int(coordinate) > self.size or int(coordinate) < 1: return False
        return True

    # checks if a ships fits in the grid and if it doesn't collide with another ship
    def ship_fits_grid_check(self, ship):
        if ship.alignment == "h":
            max_y = self.size
            max_x = self.size-ship.size+1
        else:
            max_y = self.size-ship.size+1
            max_x = self.size
        if (ship.start_y+1) > max_y: return False, "y too big to place ship"
        if (ship.start_x+1) > max_x: return False, "x too big to place ship"
        x = tmp_x = ship.start_x
        y = tmp_y = ship.start_y
        if self.grid[y][x] != 0: return False, "There is already a ship at this starting point"
        i = 0
        while i < ship.size:
            if self.grid[tmp_y][tmp_x] != 0:
                return False, "There is a ship in the way"
            if ship.alignment == "h":
                tmp_x += 1
            else:
                tmp_y += 1
            i += 1
        return True, "Ship fits grid"

# Shotlist class with functions and attributes
# Needed for computer player to keep track of its shots
class ShotList:
    def __init__(self, type, size):
        self.type = type
        self.size = size
        self.list = []
        self.build_list()

    def __repr__(self):
        return self.type

    # build list with point (x, y) entries
    def build_list(self):
        # build list
        for y in range(self.size):
            for x in range(self.size):
                point = str(x)+str(y)
                self.list.append(point)
    
    # checks if a point is in the list
    def is_in_list(self, point):
        if point in self.list == True: return True
        else: return False

# Player class with functions and attributes
class Player:
    def __init__(self, name):
        self.name = name
        self.ship_grid = Grid("ship", 7)
        self.shot_list = ShotList("shot", 7)
        self.warship = Ship("Warship", 4)
        self.cruiser = Ship("Cruiser", 3)
        self.destroyer = Ship("Destroyer", 2)
    
    def __repr__(self):
        return "I am {name}".format(name=self.name)

    # Place player's ship in the grid
    def place_ship(self, ship):
        y = ship.start_y
        x = ship.start_x
        i = 0
        while i < ship.size:
            self.ship_grid.grid[y][x] = ship
            ship.add_coordinates([x, y])
            if ship.alignment == "h": x += 1
            else: y += 1
            i += 1
        return True

    # shoot target
    def shoot(self, target, x, y):
        # check own shot grid, if already shot at this coordinate
        point = str(x)+str(y)
        if self.shot_list.list.count(point) == 0:
            return False, "> You have already shot this coordinate\n"
        # check target grid for ship
        if target.ship_grid.grid[y][x] == 0:
            self.shot_list.list.remove(point)
            return False, "> {name}'s shot has missed!\n".format(name=self.name)
        else:
            self.shot_list.list.remove(point)
            target.ship_grid.grid[y][x].hits += 1
            if target.ship_grid.grid[y][x].is_destroyed() == True:
                return True, "> {ship} is destroyed\n".format(ship=target.ship_grid.grid[y][x].type)
            else:   
                return True, "> The shot has hit a {ship}\n".format(ship=target.ship_grid.grid[y][x].type)
    
    # checks if all ships are destroyed
    def all_ships_down(self):
        warship = self.warship.is_destroyed()
        cruiser = self.cruiser.is_destroyed()
        destroyer = self.destroyer.is_destroyed()
        if warship == True and cruiser == True and destroyer == True: return True
        else: return False

# Hal class which inherits from the Player class
class Hal(Player):    
    def get_random_starting_point(self, ship):
        # get randon y and x for horizontal alignment
        if ship.alignment == "h":
            y = random.randint(0,(7-1))
            x = random.randint(0, (7-ship.size))
        # get random y and x for vertical alignment
        else:
            y = random.randint(0, (7-ship.size))
            x = random.randint(0,(7-1))
        return x, y

    def get_shooting_point(self):
        # pick a point from shotgrid
        idx = random.randint(0, len(self.shot_list.list)-1)
        return self.shot_list.list[idx]

    def get_random_alignment(self):
        if random.randint(0,1) == 0:
            return "h"
        else: return "v"
    
    # places hal ship in the grid
    def place_hal_ships(self):
        # Warship
        ship_placement = False
        self.warship.alignment = self.get_random_alignment()
        while ship_placement == False:
            x, y = self.get_random_starting_point(self.warship)
            self.warship.start_x = x
            self.warship.start_y = y
            fits_grid, msg = self.ship_grid.ship_fits_grid_check(self.warship)
            # Place warship in grid
            if fits_grid == True:
                self.place_ship(self.warship)
                ship_placement = True
                #print("{ship} has been placed".format(ship=self.warship.type))
                #print(self.warship.coordinates)
        # Cruiser
        ship_placement = False
        self.cruiser.alignment = self.get_random_alignment()
        while ship_placement == False:
            x, y = self.get_random_starting_point(self.cruiser)
            self.cruiser.start_x = x
            self.cruiser.start_y = y
            fits_grid, msg = self.ship_grid.ship_fits_grid_check(self.cruiser)
            # Place warship in grid
            if fits_grid == True:
                self.place_ship(self.cruiser)
                ship_placement = True
                #print("{ship} has been placed".format(ship=self.cruiser.type))
                #print(self.cruiser.coordinates)
        # Destroyer
        ship_placement = False
        self.destroyer.alignment = self.get_random_alignment()
        while ship_placement == False:
            x, y = self.get_random_starting_point(self.destroyer)
            self.destroyer.start_x = x
            self.destroyer.start_y = y
            fits_grid, msg = self.ship_grid.ship_fits_grid_check(self.destroyer)
            # Place warship in grid
            if fits_grid == True:
                self.place_ship(self.destroyer)
                ship_placement = True
                #print("{ship} has been placed".format(ship=self.destroyer.type))
                #print(self.destroyer.coordinates)
        return True


# This is the class controls the game flow
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
        
        - You place your ships on a 7x7 grid by giving alignment and starting point coordinates.
          Alignment must be h for horizontal or v for vertical.
          Starting point must be in the grid. Make sure the ships fits in the grid.
        
        - You have these ships:

        Ship Type | Size |
        Warship   |  4   |
        Cruiser   |  3   |
        Destroyer |  2   |

        - You and HAL take turns in shooting.

        - Btw, HAL isn't very intelligent, he just shoots randomly.

        - You can enter q or Q to quit the game.

        - The grid looks as follows:

        0|1  |2  |3  |4  |5  |6  |7  |
        1|11 |21 |31 |41 |51 |61 |71 |
        2|12 |22 |32 |42 |52 |62 |72 |
        3|13 |23 |33 |43 |53 |63 |73 |
        4|14 |24 |34 |44 |54 |64 |74 |
        5|15 |25 |35 |45 |55 |65 |75 |
        6|16 |26 |36 |46 |56 |66 |76 |
        7|17 |27 |37 |47 |57 |67 |77 |
        
        """
        return txt
    
    # print out intructions and create HAL
    def __init__(self):
        print(self)
        self.hal = Hal("Hal")
        # Place HAL ships
        self.hal.place_hal_ships()

    # Validates the player inputs
    def input_validation(self, input_type, input):
        # Validate player name
        if input_type == "name":
            if input != "": return True
            else: return False
        # Validate starting point
        if input_type == "starting_point":
            alignment = False
            x = False
            y = False
            if input == "": return False
            if input[0] == "h" or input[0] == "v": alignment = True
            if input[1].isnumeric() and input[2].isnumeric():
                if self.human.ship_grid.coordinate_inbound_check(int(input[1])) == True and self.human.ship_grid.coordinate_inbound_check(int(input[2])) == True:
                    x = True
                    y = True
            if alignment == True and x == True and y == True: return True
            else: return False
        # Validate shot
        if input_type == "shot":
            x = False
            y = False
            if input == "": return False
            if input[0].isnumeric() and input[1].isnumeric():
                if self.human.ship_grid.coordinate_inbound_check(int(input[0])) == True and self.human.ship_grid.coordinate_inbound_check(int(input[1])) == True:
                    x = True
                    y = True
            if x == True and y == True: return True
            else: return False
    
    def print_stop_msg(self, type):
        if type == "quit": 
            print("\nYou've quit the game. Maybe you play to the end the next time. Have a nice day!\n")
        if type == "game_over":
            print("\nThanks for playing to the end! Have a nice day!\n")
        

    # This starts the game
    def play(self):
        # Ask player for his name
        player_input = False
        while player_input == False:
            str = input("Please enter your name: ")
            if str == "q" or str == "Q": 
                self.print_stop_msg("quit")
                return False
            elif self.input_validation("name", str) == True:
                self.human = Player(str)
                print("")
                player_input = True
        # Ask player for alignment and starting point coordinates of warship
        player_input = False
        while player_input == False:
            str = input("{name} enter warship (size 4) alignment (h or v) and starting point coordinates in 7x7 grid (x and y), make sure the ship fits in the grid, f.e. h21: ".format(name=self.human.name))
            if str == "q" or str == "Q": 
                self.print_stop_msg("quit")
                return False
            if self.input_validation("starting_point", str) == True:
                self.human.warship.alignment = str[0]
                self.human.warship.start_x = int(str[1])-1
                self.human.warship.start_y = int(str[2])-1
                fits_grid, msg = self.human.ship_grid.ship_fits_grid_check(self.human.warship)
                # Place warship in grid
                if fits_grid == True:
                    self.human.place_ship(self.human.warship)
                    print("> {ship} has been placed\n".format(ship=self.human.warship.type))
                    player_input = True
                else:
                    print(msg)
            else:
                print("> It is a 7x7 grid with two possible alignments (h or v). Please enter valid starting point!\n")
        # Ask player for alignment and starting point coordinates of cruiser
        player_input = False
        while player_input == False:
            str = input("{name} enter cruiser (size 3) alignment (h or v) and starting point coordinates in 7x7 grid (x and y), make sure the ship fits in the grid, f.e. h21: ".format(name=self.human.name))
            if str == "q" or str == "Q": 
                self.print_stop_msg("quit")
                return False
            if self.input_validation("starting_point", str) == True:
                self.human.cruiser.alignment = str[0]
                self.human.cruiser.start_x = int(str[1])-1
                self.human.cruiser.start_y = int(str[2])-1
                fits_grid, msg = self.human.ship_grid.ship_fits_grid_check(self.human.cruiser)
                # Place cruiser in grid
                if fits_grid == True:
                    self.human.place_ship(self.human.cruiser)
                    print("> {ship} has been placed\n".format(ship=self.human.cruiser.type))
                    player_input = True
                else:
                    print(msg)
            else:
                print("> It is a 7x7 grid with two possible alignments (h or v). Please enter valid starting point!\n")
        # Ask player for alignment and starting point coordinates of destroyer
        player_input = False
        while player_input == False:
            str = input("{name} enter destroyer (size 2) alignment (h or v) and starting point coordinates in 7x7 grid (x and y), make sure the ship fits in the grid, f.e. h21: ".format(name=self.human.name))
            if str == "q" or str == "Q": 
                self.print_stop_msg("quit")
                return False
            if self.input_validation("starting_point", str) == True:
                self.human.destroyer.alignment = str[0]
                self.human.destroyer.start_x = int(str[1])-1
                self.human.destroyer.start_y = int(str[2])-1
                fits_grid, msg = self.human.ship_grid.ship_fits_grid_check(self.human.destroyer)
                # Place cruiser in grid
                if fits_grid == True:
                    self.human.place_ship(self.human.destroyer)
                    print("> {ship} has been placed\n".format(ship=self.human.destroyer.type))
                    player_input = True
                else:
                    print(msg)
            else:
                print("> It is a 7x7 grid with two possible alignments (h or v). Please enter valid starting point!\n")
        # Shootes take turns
        game_over = False
        while game_over == False:
            # Ask player for shooting coordinates
            player_input = False
            while player_input == False:
                str = input("{name} it is your turn to shoot. Please enter coordinates (x and y): ".format(name=self.human.name))
                if str == "q" or str == "Q":
                    self.print_stop_msg("quit")
                    return False
                if self.input_validation("shot", str) == True:
                    shot_x = int(str[0])-1
                    shot_y = int(str[1])-1
                    shot, msg = self.human.shoot(self.hal, shot_x, shot_y)
                    if shot == False:
                        print(msg)
                    else:
                        print(msg)
                        #print(self.hal.shot_list.list)
                        if self.hal.all_ships_down() == True:
                            msg = "Congratulations {name}! You have won!".format(name=self.human.name)
                            print(msg)
                            self.print_stop_msg("game_over")
                            game_over = True
                            return False
                    player_input = True
                else:
                    print("> It is a 7x7 grid. Please enter valid coordinates!\n")
            # HAL shoots
            print("Now {name} shoots".format(name=self.hal.name))
            valid_shot = False
            while valid_shot == False:
                point = self.hal.get_shooting_point()
                shot_x = int(point[0])
                shot_y = int(point[1])
                shot, msg = self.hal.shoot(self.human, shot_x, shot_y)
                if shot == False:
                    print(msg)
                else:
                    print(msg)
                    if self.human.all_ships_down() == True:
                        msg = "{computer_name} has won! {human_name} you have lost!".format(computer_name=self.hal.name, human_name=self.human.name)
                        print(msg)
                        self.print_stop_msg("game_over")
                        game_over = True
                        return False
                valid_shot = True
        return True
        
game1 = Battleship()
game1.play()