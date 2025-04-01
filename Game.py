from Player import Player
from Team import Team
import Event as e

class Game():
    def __init__(self, home, away):
        self.__teams = self.__away, self.__home = away, home
        self.__outs = 0
        self.__inning = 1
        self.__half = 0
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
        elif result == 2:
            print("double")
        elif result == 3:
            print("triple")
        elif result == 4:
            print("home run")
        elif result == 5:
            print("walk")
        elif result == 6:
            print("strikeout")
            self.__outs += 1
        elif result == 7:
            print("ground out")
            self.__outs += 1
        elif result == 8:
            print("air out")
            self.__outs += 1

    def update_inning(self):
        """
        Updates the game after an inning has ended
        """
        self.__inning += self.__half
        self.__half = (self.__half + 1) % 2
        self.__batting = self.__teams[self.__half]
        self.__pitching = self.__teams[self.__half - 1]
        self.__outs = 0
        if self.__half == 0:
            print(f"\nTOP {self.__inning}")
        else:
            print(f"\nBOT {self.__inning}")

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