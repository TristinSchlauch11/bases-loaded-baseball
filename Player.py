class Player():
    def __init__(self, first, last):
        self.__first = first
        self.__last = last

    def get_first(self):
        """
        Gets the first name of the player
        """
        return self.__first
    
    def get_last(self):
        """
        Gets the last name of the player
        """
        return self.__last
    
class Batter(Player):
    """
    A subclass of Player, a Batter will only be able to hit and have batting methods
    """
    def __init__(self, first, last):
        super().__init__(first, last)
        self.__hits = 0
        self.__2Bs = 0
        self.__3Bs = 0
        self.__HRs = 0
        self.__BBs = 0
        self.__runs = 0
        self.__RBIs = 0
        self.__ABs = 0
        self.__PAs = 0

class Pitcher(Player):
    """
    A subclass of Player, a Pitcher will only be able to pitch and have pitching methods
    """
    def __init__(self, first, last):
        super().__init__(first, last)
        self.__GOs = 0
        self.__AOs = 0
        self.__Ks = 0
        self.__hits = 0
        self.__BBs = 0
        self.__ERs = 0
        self.__IP = 0
        self.__TBF = 0