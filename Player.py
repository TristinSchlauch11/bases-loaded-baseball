class Player():
    def __init__(self, id, first, last):
        self.__id = id
        self.__first = first
        self.__last = last

    def get_id(self):
        """
        Returns the unique ID used to store their information in the SQL database
        """
        return self.__id

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

    def get_avg(self):
        """
        Returns a floating point value of the batting average (AVG) of the Batter
        If printing this statistic, you should round to three decimal places and remove leading 0
        """
        if self.__ABs == 0:
            return 0.0
        return self.__hits / self.__ABs
    
    def get_obp(self):
        """
        Returns a floating point value of the on-base percentage (OBP) of the Batter
        If printing this statistic, you should round to three decimal places and remove leading 0
        """
        if self.__PAs == 0:
            return 0.0
        return (self.__hits + self.__BBs) / self.__PAs
    
    def get_slg(self):
        """
        Returns a floating point value of the slugging percentage (SLG) of the Batter
        If printing this statistic, you should round to three decimal places and remove leading 0
        """
        if self.__ABs == 0:
            return 0.0
        return (self.__hits + self.__2Bs * 2 + self.__3Bs * 3 + self.__HRs * 4) / self.__ABs
    
    def get_ops(self):
        """
        Returns a floating point value of the on-base plus slugging (OPS) of the Batter
        If printing this statistic, you should round to three decimal places and remove leading 0
        """
        return self.get_obp() + self.get_slg()
    
    def get_xbh(self):
        """
        Returns an integer value of the extra base hits (XBH) of the Batter
        """
        return self.__2Bs + self.__3Bs + self.__HRs
    
    def get_xbh(self):
        """
        Returns an integer value of the total bases (TB) of the Batter
        """
        return self.__hits + self.__2Bs * 2 + self.__3Bs * 3 + self.__HRs * 4

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
        self.__outs = 0
        self.__TBF = 0

    def groundout(self):
        """
        Accumulates pitcher stats for a groundout
        """
        self.__outs += 1
        self.__GOs += 1
        self.__TBF += 1

    def airout(self):
        """
        Accumulates pitcher stats for an air out
        """
        self.__outs += 1
        self.__AOs += 1
        self.__TBF += 1

    def strikeout(self):
        """
        Accumulates pitcher stats for a strikeout
        """
        self.__outs += 1
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

    def add_outs(self, outs):
        """
        Adds the given number of outs to the pitchers count
        Used to add outs that are collected in ways not included in methods above
        """
        self.__outs += outs
    
    def earned_run(self):
        """
        Adds an earned run to the pitchers count
        """
        self.__ERs += 1

    def get_IP_calc(self):
        """
        Returns the number of innings the Pitcher has pitched
        To be used in calculations for other statistics
        """
        return self.__outs / 3
    
    def get_IP_disp(self):
        """
        Returns the number of innings the Pitcher has pitched
        To be used to display the IP statistic
        """
        return f"{self.__outs // 3}.{self.__outs % 3}"
    
    def get_baa(self):
        """
        Returns a floating point value of the batting average against (BAA) of the Pitcher
        If printing this statistic, you should round to three decimal places and remove leading 0
        """
        if at_bats := self.__hits + self.__GOs + self.__AOs + self.__Ks == 0:
            return 0.0
        return self.__hits / at_bats
    
    def get_obp(self):
        """
        Returns a floating point value of the on base percentage (OBP) of the Pitcher
        If printing this statistic, you should round to three decimal places and remove leading 0
        """
        if self.__TBF == 0:
            return 0.0
        return (self.__hits + self.__BBs) / self.__TBF
    
    def get_whip(self):
        """
        Returns a floating point value of the Walks Plus Hits per Inning Pitched (WHIP) of the Pitcher
        If printing this statistic, you should round to two decimal places
        """
        if self.get_IP_calc() == 0:
            return 0.0
        return (self.__BBs + self.__hits) / self.get_IP_calc()
    
    def get_era(self):
        """
        Returns a floating point value of the earned run average (ERA) of the Pitcher
        If printing this statistic, you should round to two decimal places
        """
        if self.get_IP_calc() == 0:
            return 0.0
        return (self.__ERs / self.get_IP_calc()) * 9

    def get_Kper9(self):
        """
        Returns a floating point value of the strikeouts per 9 (K/9) of the Pitcher
        If printing this statistic, you should round to two decimal places
        """
        if self.get_IP_calc() == 0:
            return 0.0
        return (self.__Ks / self.get_IP_calc()) * 9
    
    def get_KtoBB(self):
        """
        Returns a floating point value of the strikeouts to walks (K/BB) of the Pitcher
        If printing this statistic, you should round to two decimal places
        """
        if self.__BBs == 0:
            return 0.0
        return self.__Ks / self.__BBs

    def print_stats(self):
        """
        Prints the raw statistics of the Pitcher
        NEED TO UPDATE THIS METHOD LATER
        """
        print(f"{self.get_last()}: {self.get_IP_disp()} IP, {self.__ERs} ER, {self.__GOs} GO, {self.__AOs} AO, {self.__Ks} K, {self.__hits} H, {self.__BBs} BB, {self.__TBF} TBF")