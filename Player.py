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

    def single(self):
        """
        Accumulates batter stats for a single
        """
        self.__hits += 1
        self.__ABs += 1
        self.__PAs += 1

    def double(self):
        """
        Accumulates batter stats for a double
        """
        self.__hits += 1
        self.__2Bs += 1
        self.__ABs += 1
        self.__PAs += 1

    def triple(self):
        """
        Accumulates batter stats for a triple
        """
        self.__hits += 1
        self.__3Bs += 1
        self.__ABs += 1
        self.__PAs += 1

    def homerun(self):
        """
        Accumulates batter stats for a home run
        """
        self.__hits += 1
        self.__HRs += 1
        self.__RBIs += 1
        self.__runs += 1
        self.__ABs += 1
        self.__PAs += 1

    def walk(self):
        """
        Accumulates batter stats for a walk
        """
        self.__BBs += 1
        self.__PAs += 1

    def out(self):
        """
        Accumulates batter stats for an out
        """
        self.__ABs += 1
        self.__PAs += 1

    def sacfly(self):
        """
        Accumulates batter stats for hitting a sacrifice fly
        """
        self.__PAs += 1
        self.__RBIs += 1

    def run(self):
        """
        Accumulates batter stats for scoring a run
        """
        self.__runs += 1

    def RBI(self):
        """
        Accumulates batter stats for getting an RBI
        """
        self.__RBIs += 1

    def print_stats(self):
        """
        Prints the raw stats of the Batter
        NEED TO EDIT THIS METHOD LATER
        """
        print(f"{self.get_last()}: {self.__hits} H, {self.__2Bs} 2B, {self.__3Bs} 3B, {self.__HRs} HR, {self.__BBs} BB, {self.__runs} R, {self.__RBIs} RBI, {self.__ABs} AB, {self.__PAs} PA")

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

    def groundout(self):
        """
        Accumulates pitcher stats for a groundout
        """
        self.__GOs += 1
        self.__TBF += 1

    def airout(self):
        """
        Accumulates pitcher stats for an air out
        """
        self.__AOs += 1
        self.__TBF += 1

    def strikeout(self):
        """
        Accumulates pitcher stats for a strikeout
        """
        self.__Ks += 1
        self.__TBF += 1

    def hit(self):
        """
        Accumulates pitcher stats for a hit
        """
        self.__hits += 1
        self.__TBF += 1

    def walk(self):
        """
        Accumulates pitcher stats for a walk
        """
        self.__BBs += 1
        self.__TBF += 1

    def print_stats(self):
        """
        Prints the raw statistics of the Pitcher
        NEED TO UPDATE THIS METHOD LATER
        """
        print(f"{self.get_last()}: {self.__GOs} GO, {self.__AOs} AO, {self.__Ks} K, {self.__hits} H, {self.__BBs} BB, {self.__TBF} TBF")