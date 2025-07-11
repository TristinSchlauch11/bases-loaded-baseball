from Player import Player, Batter, Pitcher

class Team():
    def __init__(self, code, loc, name, cursor):
        self.__code = code
        self.__location = loc
        self.__name = name
        self.__lineup = []
        self.__rotation = []
        self.__bullpen = []
        self.init_players(cursor)

    def init_players(self, cursor):
        """
        Initializes and adds all Player objects to the Team
        Used when the Team is queried from the database to play a game
        """
        # get batters
        cursor.execute(f"SELECT player_id, fname, lname FROM bat_stats WHERE team = '{self.get_code()}';")
        batters = cursor.fetchall()
        for (b_id, first, last) in batters:
            self.add_batter(Batter(b_id, first, last))

        # get pitchers
        cursor.execute(f"SELECT player_id, fname, lname, is_sp FROM pit_stats WHERE team = '{self.get_code()}';")
        pitchers = cursor.fetchall()
        for (p_id, first, last, is_sp) in pitchers:
            self.add_pitcher(Pitcher(p_id, first, last), is_sp)

    def get_name(self):
        """
        Returns the Team's name
        """
        return self.__name
    
    def get_code(self):
        """
        Returns the Team's code
        """
        return self.__code
        
    # may not need
    def print_bullpen(self):
        """
        Prints the pitchers in the bullpen to the screen
        """
        for i in range(len(self.__bullpen)):
            print(f"{i+1}. {self.__bullpen[i].get_last()}")

    def get_batter(self, index):
        """
        Returns the Batter from the Team's lineup at the specified index
        """
        return self.__lineup[index]
    
    def select_rp(self, curr_pit, used=[]):
        """
        Prompts the user to select a pitcher in the bullpen to switch to in a game

        Returns None if the user selects to not switch or there are no pitchers to switch to
        Otherwise returns the new Pitcher
        """
        # get a list of all available relief pitchers
        available = self.__bullpen[:]   # create copy of bullpen to use
        for pit in used[1:]:            # removes all pitchers used besides the SP
            available.remove(pit)

        # if no pitchers, immediately exit
        if len(available) == 0:
            print("There are no relief pitchers available!")
            return None
        
        while True:
            # print current pitcher and available pitchers
            print(f"\nCurrently pitching: {curr_pit.get_last()}")
            for i in range(len(available)):
                print(f"{i+1}. {available[i].get_last()}")
            
            # get the desired pitcher
            try:
                sel = int(input("Please enter the number of the pitcher to change to, or 0 to keep the current pitcher >> "))
            except ValueError:
                print("That's not a number!")
            else:
                if sel == 0:
                    return None
                elif 1 <= sel <= len(available):
                    return available[sel - 1]
                else:
                    print("Please pick a number above.")
    
    # A DUMMY METHOD THAT NEEDS TO BE FIXED LATER
    def get_pitcher(self):
        """
        Returns the active Pitcher
        """
        return self.__rotation[0]
    
    ## May need to amend these methods later due to Shohei Ohtani
    def add_batter(self, bat):
        """
        Adds Batter bat to the Team
        """
        self.__lineup.append(bat)
    
    def add_pitcher(self, pit, is_sp):
        """
        Adds Pitcher pit to the Team. Will add the pitcher to the rotation if a starter,
        bullpen if they are a reliever
        """
        # Will likely change the way that the players get sorted into the rotation/bullpen
        if is_sp:
            self.__rotation.append(pit)
        else:
            self.__bullpen.append(pit)

    def print_stats(self, cursor):
        print(f"{self.get_name()} Stats")
        for batter in self.__lineup:
            batter.print_stats(cursor)
        for pitcher in self.__rotation:
            pitcher.print_stats(cursor)