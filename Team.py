from Player import Player

class Team():
    def __init__(self, name):
        self.__name = name
        self.__lineup = []
        self.__rotation = []
        self.__bullpen = []

    def get_name(self):
        """
        Returns the Team's name
        """
        return self.__name
    
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