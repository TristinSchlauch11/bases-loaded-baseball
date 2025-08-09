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
    
    def hr_num(self):
        """
        Uses the Batter's POW rating to determine the threshold number used by the
        Event module to determine if the Batter hit a home run or not during a Hit event
        """
        # POW attribute will be "calculated" using IRL stats --> HR% = HR / H = 0.01(POW) + 0.843
            # POW = ((HR/H) - 0.843)/0.01
        # attribute will be stored as an attribute of the Batter
        return 155.7 - self.__POW

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

    def get_avg(self, cursor):
        """
        Returns a floating point value of the batting average (AVG) of the Batter
        If printing this statistic, you should round to three decimal places and remove leading 0
        """
        # query required stats
        comm = f"""SELECT hits, ABs
        FROM bat_stats
        WHERE player_id = '{self.get_id()}';"""
        cursor.execute(comm)

        # unpack stats
        (h, ab) = cursor.fetchone()

        # compute and return AVG
        if ab == 0:
            return 0.0
        return h / ab
    
    def get_obp(self, cursor):
        """
        Returns a floating point value of the on-base percentage (OBP) of the Batter
        If printing this statistic, you should round to three decimal places and remove leading 0
        """
        # query required stats
        comm = f"""SELECT hits, walks, PAs
        FROM bat_stats
        WHERE player_id = '{self.get_id()}';"""
        cursor.execute(comm)

        # unpack stats
        (h, bb, pa) = cursor.fetchone()

        # compute and return OBP
        if pa == 0:
            return 0.0
        return (h + bb) / pa
    
    def get_slg(self, cursor):
        """
        Returns a floating point value of the slugging percentage (SLG) of the Batter
        If printing this statistic, you should round to three decimal places and remove leading 0
        """
        # query required stats
        comm = f"""SELECT ABs
        FROM bat_stats
        WHERE player_id = '{self.get_id()}';"""
        cursor.execute(comm)

        # unpack stats
        (ab, ) = cursor.fetchone()

        if ab == 0:
            return 0.0
        return self.get_tb(cursor) / ab
    
    def get_ops(self, cursor):
        """
        Returns a floating point value of the on-base plus slugging (OPS) of the Batter
        If printing this statistic, you should round to three decimal places and remove leading 0
        """
        return self.get_obp(cursor) + self.get_slg(cursor)
    
    def get_xbh(self, cursor):
        """
        Returns an integer value of the extra base hits (XBH) of the Batter
        """
        # query required stats
        comm = f"""SELECT doubles, triples, homeruns
        FROM bat_stats
        WHERE player_id = '{self.get_id()}';"""
        cursor.execute(comm)

        # unpack stats
        (dbls, tpls, hr) = cursor.fetchone()

        # compute and return XBH
        return dbls + tpls + hr
    
    def get_tb(self, cursor):
        """
        Returns an integer value of the total bases (TB) of the Batter
        """
        # query required stats
        comm = f"""SELECT hits, doubles, triples, homeruns
        FROM bat_stats
        WHERE player_id = '{self.get_id()}';"""
        cursor.execute(comm)

        # unpack stats
        (h, dbls, tpls, hr) = cursor.fetchone()

        # compute and return TB
        return h - self.get_xbh(cursor) + dbls * 2 + tpls * 3 + hr * 4

    def print_stats(self, cursor):
        """
        Prints the raw stats of the Batter
        """
        # query required stats
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
        self.__gbrate = 0.42   # This number will be used to determine if the pitcher is a Ground Ball/Fly Ball pitcher --> avg. 42%
    
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
            # STF = (0.42 - BAA)/0.0025
        # attributes will be stored as an attribute of the Pitcher
        return (4737 + (0.42 - 0.0025*self.__STF)*(29*self.walk_num() - 10000))/47.37
    
    def k_num(self):
        """
        Uses the Pitcher's VEL rating to determine the threshold number used by the Event
        module to determine if the Pitcher struckout a Batter or not during an Out Event
        """
        # VEL will be "calculated" using IRL stats --> K/(TBF - H - BB) = 0.0095(VEL) - 0.3437
            # VEL = K/(0.0095*(TBF - H - BB)) + 36.18
        return 0.95*self.__VEL - 34.37
    
    def gb_num(self):
        """
        Uses the Pitcher's gbrate determine the threshold number used by the Event
        module to determine if the Pitcher grounded out a Batter or not during an Out Event
        """
        # gbrate will be the raw GB% of the Pitcher
        return self.k_num() + self.__gbrate*(100 - self.k_num())

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
    
    def get_baa(self, cursor):
        """
        Returns a floating point value of the batting average against (BAA) of the Pitcher
        If printing this statistic, you should round to three decimal places and remove leading 0
        """
        # query required stats
        comm = f"""SELECT hits, groundouts, airouts, strikeouts
        FROM pit_stats
        WHERE player_id = '{self.get_id()}';"""
        cursor.execute(comm)

        # unpack stats
        (h, go, ao, k) = cursor.fetchone()

        # compute and return BAA
        if (ab := h + go + ao + k) == 0:
            return 0.0
        return h / ab
    
    def get_obp(self, cursor):
        """
        Returns a floating point value of the on base percentage (OBP) of the Pitcher
        If printing this statistic, you should round to three decimal places and remove leading 0
        """
        # query required stats
        comm = f"""SELECT hits, walks, TBF
        FROM pit_stats
        WHERE player_id = '{self.get_id()}';"""
        cursor.execute(comm)

        # unpack stats
        (h, bb, tbf) = cursor.fetchone()

        # compute and return OBP
        if tbf == 0:
            return 0.0
        return (h + bb) / tbf
    
    def get_whip(self, cursor):
        """
        Returns a floating point value of the Walks Plus Hits per Inning Pitched (WHIP) of the Pitcher
        If printing this statistic, you should round to two decimal places
        """
        # query required stats
        comm = f"""SELECT hits, walks
        FROM pit_stats
        WHERE player_id = '{self.get_id()}';"""
        cursor.execute(comm)

        # unpack stats
        (h, bb) = cursor.fetchone()

        # compute and return WHIP
        if self.get_IP_calc(cursor) == 0:
            return 0.0
        return (h + bb) / self.get_IP_calc(cursor)
    
    def get_era(self, cursor):
        """
        Returns a floating point value of the earned run average (ERA) of the Pitcher
        If printing this statistic, you should round to two decimal places
        """
        # query required stats
        comm = f"""SELECT ERs
        FROM pit_stats
        WHERE player_id = '{self.get_id()}';"""
        cursor.execute(comm)

        # unpack stats
        (er, ) = cursor.fetchone()

        # compute and return ERA
        if self.get_IP_calc(cursor) == 0:
            return 0.0
        return (er / self.get_IP_calc(cursor)) * 9

    def get_Kper9(self, cursor):
        """
        Returns a floating point value of the strikeouts per 9 (K/9) of the Pitcher
        If printing this statistic, you should round to two decimal places
        """
        # query required stats
        comm = f"""SELECT strikeouts
        FROM pit_stats
        WHERE player_id = '{self.get_id()}';"""
        cursor.execute(comm)

        # unpack stats
        (k, ) = cursor.fetchone()

        # compute and return K/9
        if self.get_IP_calc(cursor) == 0:
            return 0.0
        return (k / self.get_IP_calc(cursor)) * 9
    
    def get_KtoBB(self, cursor):
        """
        Returns a floating point value of the strikeouts to walks (K/BB) of the Pitcher
        If printing this statistic, you should round to two decimal places
        """
        # query required stats
        comm = f"""SELECT strikeouts, walks
        FROM pit_stats
        WHERE player_id = '{self.get_id()}';"""
        cursor.execute(comm)

        # unpack stats
        (k, bb) = cursor.fetchone()

        # compute and return K/BB
        if bb == 0:
            return 0.0
        return k / bb

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