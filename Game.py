from Player import Player
from Team import Team
import Event as e

class Game():
    def __init__(self, home, away):
        self.__teams = self.__away, self.__home = away, home
        self.__outs = 0
        self.__inning = 1
        self.__half = 0
        self.__bases = [None, None, None]
        self.__batting = self.__away    # attempting new approach
        self.__pitching = self.__home   # attempting new approach
        self.__batinds = [0, 0]
        self.__over = False

    def play(self):
        """
        Operates the main gameplay loop
        """
        while not self.__over:
            # get batter and pitcher
            bat = self.__batting.get_batter(self.__batinds[self.__half])
            pit = self.__pitching.get_pitcher()

            # execute PA
            self.at_bat(bat, pit)
            self.__batinds[self.__half] = (self.__batinds[self.__half] + 1) % 9

            # check game status
            self.__over = self.check_game()
            if not self.__over and self.__outs == 3:
                self.update_inning()

    def at_bat(self, bat, pit):
        """
        Executes an at-bat between Batter bat and Pitcher pit
        """
        print(f"Batter: {bat.get_last()}")
        print(f"Pitcher: {pit.get_last()}")
        
        result = e.ab(bat, pit)

        if result == 1:
            print("single")
            self.base_hit(1, bat)
        elif result == 2:
            print("double")
            self.base_hit(2, bat)
        elif result == 3:
            print("triple")
            self.base_hit(3, bat)
        elif result == 4:
            print("home run")
            self.base_hit(4, bat)
        elif result == 5:
            print("walk")
            self.base_hit(1, bat)   ## INCORRECT!!
        elif result == 6:
            print("strikeout")
            self.__outs += 1
        elif result == 7:
            print("ground out")
            self.__outs += 1
        elif result == 8:
            print("air out")
            self.__outs += 1

        self.print_bases()
        print("")
        
    def base_hit(self, num_bases, b):
        """
        Updates the Game after a base hit by batter b of the provided number of 
        bases, num_bases (between 1-4)
        """
        # update runners already on bases
        for i in range(2, num_bases - 1, -1):
            self.__bases[i] = self.__bases[i - num_bases]
        # put batter on bases (if not home_run)
        if num_bases < 4:
            self.__bases[num_bases - 1] = b
        # set other bases to empty
        for i in range(num_bases - 2, -1, -1):
            self.__bases[i] = None

    def print_bases(self):
        """
        A TESTING METHOD FOR THE BASES
        """
        message = "["
        for item in self.__bases:
            if item is None:
                message += "None, "
            else:
                message += f"{item.get_last()}, "
        message = message[:-2]
        message += "]"
        print(message)

    def update_inning(self):
        """
        Updates the game after an inning has ended
        """
        self.__inning += self.__half
        self.__half = (self.__half + 1) % 2
        self.__batting = self.__teams[self.__half]
        self.__pitching = self.__teams[self.__half - 1]
        self.__outs = 0
        self.clear_bases()
        if self.__half == 0:
            print(f"\nTOP {self.__inning}")
        else:
            print(f"\nBOT {self.__inning}")

    def clear_bases(self):
        """
        Removes all Players from the bases
        """
        self.__bases = [None, None, None]

    def check_game(self):
        """
        Checks if the game is over

        FOR NOW, this is a dummy method that needs to be updated later
        """
        return self.__inning >= 9 and self.__half == 1 and self.__outs >= 3

# for testing purposes
bluejays = Team("Blue Jays")
bluejays.add_batter(Player("Alejandro", "Kirk"))
bluejays.add_batter(Player("Vladamir", "Guerrero Jr."))
bluejays.add_batter(Player("Andres", "Gimenez"))
bluejays.add_batter(Player("Bo", "Bichette"))
bluejays.add_batter(Player("Ernie", "Clement"))
bluejays.add_batter(Player("Davis", "Schneider"))
bluejays.add_batter(Player("Daulton", "Varsho"))
bluejays.add_batter(Player("George", "Springer"))
bluejays.add_batter(Player("Anthony", "Santander"))
bluejays.add_pitcher(Player("Jose", "Berrios"))

swansons = Team("Swansons")
swansons.add_batter(Player("Sherry", "Lee"))
swansons.add_batter(Player("Tanner", "Mergle"))
swansons.add_batter(Player("Teresa", "Three"))
swansons.add_batter(Player("Tristin", "Schlauch"))
swansons.add_batter(Player("Sungwoo", "Byun"))
swansons.add_batter(Player("William", "Blimke"))
swansons.add_batter(Player("Ryan", "Chan"))
swansons.add_batter(Player("Reed", "Drinkle"))
swansons.add_batter(Player("Jason", "Nine"))
swansons.add_pitcher(Player("Kris", "Clements"))

g = Game(bluejays, swansons)
g.play()