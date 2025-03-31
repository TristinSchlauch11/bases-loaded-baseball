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