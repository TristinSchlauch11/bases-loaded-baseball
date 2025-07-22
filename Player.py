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
    def __init__(self, id, first, last):
        super().__init__(id, first, last)
        self.__CON = 70
        self.__POW = 70
        self.__EYE = 70
        self.__hits = 0
        self.__2Bs = 0
        self.__3Bs = 0
        self.__HRs = 0
        self.__BBs = 0
        self.__runs = 0
        self.__RBIs = 0
        self.__ABs = 0
        self.__PAs = 0

    def walk_num(self):
        """
        Uses the Batter's EYE rating to determine the threshold number used by the Event
        module to determine if the Batter walks or not during a plate appearance
        """
        # EYE attribute will be "calculated" using IRL stats --> BB% = 0.00464(EYE) - 0.2407
            # EYE = (BB% + 0.2407)/0.00464
        # attributes will be stored as an attribute of the Batter
        return 1.6*self.__EYE - 83
    
    def hit_num(self):
        """
        Uses the Batter's EYE and CON rating to determine the threshold number used by the
        Event module to determine if the Batter gets a hit or not during a plate appearance
        """
        # CON attribute will be "calculated" using IRL stats --> AVG = 0.004(CON) - 0.035
            # CON = (AVG + 0.035)/0.004
        # attribute will be stored as an attribute of the Batter
        return (4737 + (0.004*self.__CON - 0.035)*(29*self.walk_num() - 10000))/47.37

    def base_hit(self, bases, cursor):
        """
        Updates the player stat database by accumulating batter stats for a base hit
        cursor is the cursor for the SQL database
        """

        # determine the hit type to accumulate
        hit_message = "hits = hits + 1,"
        if bases == 2:
            hit_message += " doubles = doubles + 1,"
        if bases == 3:
            hit_message += " triples = triples + 1,"
        if bases == 4:
            hit_message += " homeruns = homeruns + 1, RBIs = RBIs + 1, runs = runs + 1,"

        # create SQL command
        sql_command = f"""UPDATE bat_stats
        SET {hit_message} ABs = ABs + 1, PAs = PAs + 1
        WHERE player_id = '{self.get_id()}'"""

        # execute command
        cursor.execute(sql_command)

    def walk(self, cursor):
        """
        Updates the player stat database by accumulating batter stats for a walk
        cursor is the cursor for the SQL database
        """
    
        # create SQL command
        sql_command = f"""UPDATE bat_stats
        SET walks = walks + 1, PAs = PAs + 1
        WHERE player_id = '{self.get_id()}'"""

        # execute command
        cursor.execute(sql_command)

    def out(self, cursor):
        """
        Updates the player stat database by accumulating batter stats for an out
        cursor is the cursor for the SQL database
        """
    
        # create SQL command
        sql_command = f"""UPDATE bat_stats
        SET ABs = ABs + 1, PAs = PAs + 1
        WHERE player_id = '{self.get_id()}'"""

        # execute command
        cursor.execute(sql_command)

    def sacfly(self, cursor):
        """
        Updates the player stat database by accumulating batter stats for a sacrifice fly
        cursor is the cursor for the SQL database
        """
    
        # create SQL command
        sql_command = f"""UPDATE bat_stats
        SET RBIs = RBIs + 1, PAs = PAs + 1
        WHERE player_id = '{self.get_id()}'"""

        # execute command
        cursor.execute(sql_command)

    def run(self, cursor):
        """
        Updates the player stat database by accumulating batter stats for an out
        cursor is the cursor for the SQL database
        """
    
        # create SQL command
        sql_command = f"""UPDATE bat_stats
        SET runs = runs + 1
        WHERE player_id = '{self.get_id()}'"""

        # execute command
        cursor.execute(sql_command)

    def RBI(self, cursor):
        """
        Updates the player stat database by accumulating batter stats for an out
        cursor is the cursor for the SQL database
        """
    
        # create SQL command
        sql_command = f"""UPDATE bat_stats
        SET RBIs = RBIs + 1
        WHERE player_id = '{self.get_id()}'"""

        # execute command
        cursor.execute(sql_command)

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
    
    def get_tb(self):
        """
        Returns an integer value of the total bases (TB) of the Batter
        """
        return self.__hits + self.__2Bs * 2 + self.__3Bs * 3 + self.__HRs * 4

    def print_stats(self, cursor):
        """
        Prints the raw stats of the Batter
        """
        # get stats from table
        comm = f"""SELECT lname, hits, doubles, triples, homeruns, walks, runs, RBIs, ABs, PAs
        FROM bat_stats
        WHERE player_id = '{self.get_id()}';"""
        cursor.execute(comm)

        # unpack stats
        (name, h, dbls, tpls, hr, bb, r, rbi, ab, pa) = cursor.fetchone()

        # display stats
        print(f"{name}: {h} H, {dbls} 2B, {tpls} 3B, {hr} HR, {bb} BB, {r} R, {rbi} RBI, {ab} AB, {pa} PA")

class Pitcher(Player):
    """
    A subclass of Player, a Pitcher will only be able to pitch and have pitching methods
    """
    def __init__(self, id, first, last):
        super().__init__(id, first, last)
        self.__CMD = 70
        self.__STF = 70
        self.__VEL = 70
        self.__GOs = 0
        self.__AOs = 0
        self.__Ks = 0
        self.__hits = 0
        self.__BBs = 0
        self.__ERs = 0
        self.__outs = 0
        self.__TBF = 0
    
    def walk_num(self):
        """
        Uses the Pitcher's CMD rating to determine the threshold number used by the Event
        module to determine if the Pitcher issued a walk or not during a plate appearance
        """
        # CMD attribute will be "calculated" using IRL stats --> BB% = 0.2262 - 0.00203(CMD)
            # CMD = (0.2262 - BB%)/0.00203
        # attributes will be stored as an attribute of the Pitcher
        return 78 - 0.7*self.__CMD
    
    def hit_num(self):
        """
        Uses the Pitcher's CMD and STF rating to determine the threshold number used by the Event
        module to determine if the Pitcher issued a hit or not during a plate appearance
        """
        # STF attribute will be "calculated" using IRL stats --> BAA = 0.42 - 0.0025(STF)
            # CMD = (0.2262 - BB%)/0.00203
        # attributes will be stored as an attribute of the Pitcher
        return (4737 + (0.42 - 0.0025*self.__STF)*(29*self.walk_num() - 10000))/47.37

    def groundout(self, cursor):
        """
        Updates the player stat database by accumulating pitcher stats for a groundout
        cursor is the cursor for the SQL database
        """
    
        # create SQL command
        sql_command = f"""UPDATE pit_stats
        SET outs = outs + 1, groundouts = groundouts + 1, TBF = TBF + 1
        WHERE player_id = '{self.get_id()}'"""

        # execute command
        cursor.execute(sql_command)

    def airout(self, cursor):
        """
        Updates the player stat database by accumulating pitcher stats for an air out
        cursor is the cursor for the SQL database
        """
    
        # create SQL command
        sql_command = f"""UPDATE pit_stats
        SET outs = outs + 1, airouts = airouts + 1, TBF = TBF + 1
        WHERE player_id = '{self.get_id()}'"""

        # execute command
        cursor.execute(sql_command)

    def strikeout(self, cursor):
        """
        Updates the player stat database by accumulating pitcher stats for a strikeout
        cursor is the cursor for the SQL database
        """
    
        # create SQL command
        sql_command = f"""UPDATE pit_stats
        SET outs = outs + 1, strikeouts = strikeouts + 1, TBF = TBF + 1
        WHERE player_id = '{self.get_id()}'"""

        # execute command
        cursor.execute(sql_command)

    def hit(self, cursor):
        """
        Updates the player stat database by accumulating pitcher stats for a hit
        cursor is the cursor for the SQL database
        """
    
        # create SQL command
        sql_command = f"""UPDATE pit_stats
        SET hits = hits + 1, TBF = TBF + 1
        WHERE player_id = '{self.get_id()}'"""

        # execute command
        cursor.execute(sql_command)

    def walk(self, cursor):
        """
        Updates the player stat database by accumulating pitcher stats for a walk
        cursor is the cursor for the SQL database
        """
    
        # create SQL command
        sql_command = f"""UPDATE pit_stats
        SET walks = walks + 1, TBF = TBF + 1
        WHERE player_id = '{self.get_id()}'"""

        # execute command
        cursor.execute(sql_command)

    def add_outs(self, outs, cursor):
        """
        Updates the player stat database by adding the given number of outs to the pitchers count
        Used to add outs that are collected in ways not included in methods above
        cursor is the cursor for the SQL database
        """
    
        # create SQL command
        sql_command = f"""UPDATE pit_stats
        SET outs = outs + {outs}
        WHERE player_id = '{self.get_id()}'"""

        # execute command
        cursor.execute(sql_command)
    
    def earned_run(self, cursor):
        """
        Updates the player stat database by adding an earned run to the pitchers count
        Used to add outs that are collected in ways not included in methods above
        cursor is the cursor for the SQL database
        """
    
        # create SQL command
        sql_command = f"""UPDATE pit_stats
        SET ERs = ERs + 1
        WHERE player_id = '{self.get_id()}'"""

        # execute command
        cursor.execute(sql_command)

    def get_IP_calc(self, cursor):
        """
        Returns the number of innings the Pitcher has pitched
        To be used in calculations for other statistics
        """
        # query required stats
        cursor.execute(f"SELECT outs FROM pit_stats WHERE player_id = '{self.get_id()}'")
        (outs, ) = cursor.fetchone()

        # return desired stat
        return outs / 3
    
    def get_IP_disp(self, cursor):
        """
        Returns the number of innings the Pitcher has pitched
        To be used to display the IP statistic
        """
        # query required stats
        cursor.execute(f"SELECT outs FROM pit_stats WHERE player_id = '{self.get_id()}'")
        (outs, ) = cursor.fetchone()

        # return desired stat
        return f"{outs // 3}.{outs % 3}"
    
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

    def print_stats(self, cursor):
        """
        Prints the raw statistics of the Pitcher
        """
        # get stats from table
        comm = f"""SELECT lname, groundouts, airouts, strikeouts, hits, walks, ERs, TBF
        FROM pit_stats
        WHERE player_id = '{self.get_id()}';"""
        cursor.execute(comm)

        # unpack stats
        (name, go, ao, k, h, bb, er, tbf) = cursor.fetchone()

        # display stats
        print(f"{name}: {self.get_IP_disp(cursor)} IP, {er} ER, {go} GO, {ao} AO, {k} K, {h} H, {bb} BB, {tbf} TBF")