from Player import Player

class Team():
    def __init__(self, name):
        self.__name = name
        self.__lineup = []
        self.__rotation = []

    def get_name(self):
        """
        Returns the Team's name
        """
        return self.__name
    
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
    
    def add_pitcher(self, pit):
        """
        Adds Pitcher pit to the Team
        """
        self.__rotation.append(pit)