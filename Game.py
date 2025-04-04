from Player import Player
from Team import Team
import Event as e

class Game():
    def __init__(self, home, away):
        self.__teams = self.__away, self.__home = away, home
        self.__outs = 0
        self.__inning = 1
        self.__half = 0
        self.__score = [0, 0]
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

            # print next batter and pitcher
            print(f"Batter: {bat.get_last()}")
            print(f"Pitcher: {pit.get_last()}")

            # execute PA
            sel = input("\nEnter 'h' to hit, 's' to substitute >> ")
            if sel == "h":
                self.at_bat(bat, pit)
                self.__batinds[self.__half] = (self.__batinds[self.__half] + 1) % 9
            elif sel == "s":
                print("Substitution menu under construction.\n")
            else:
                print("Invalid entry.\n")

            # check game status
            self.__over = self.check_game()
            if not self.__over and self.__outs == 3:
                self.update_inning()
        print(f"{self.__away.get_name()} {self.__score[0]} @ {self.__home.get_name()} {self.__score[1]}")

    def at_bat(self, bat, pit):
        """
        Executes an at-bat between Batter bat and Pitcher pit
        """        
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
            # if bases are loaded, score a run and advance all runners
            if None not in self.__bases:
                self.__score[self.__half] += 1
                for i in range(2, 0, -1):
                    self.__bases[i] = self.__bases[i-1]
                self.__bases[0] = bat
            # otherwise advance needed runners only
            else:
                for j in range(0, 3):
                    if j == 2 or self.__bases[j] is None:
                        for k in range(j, 0, -1):
                            self.__bases[k] = self.__bases[k-1]
                        self.__bases[0] = bat
                        break

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
        # scores any runners, if required
        for i in range(2, max(2 - num_bases, -1), -1):
            if self.__bases[i] is not None:
                print(f"{self.__bases[i].get_last()} scores!")
                self.__score[self.__half] += 1

        # update runners already on bases
        for j in range(2, num_bases - 1, -1):
            self.__bases[j] = self.__bases[j - num_bases]
        
        # put batter on bases if not home run, otherwise score the run
        if num_bases < 4:
            self.__bases[num_bases - 1] = b
        else:
            self.__score[self.__half] += 1
        
        # set other bases to empty
        for k in range(num_bases - 2, -1, -1):
            self.__bases[k] = None

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
        
        # extra innings rule
        if self.__inning >= 10:
            self.__bases[1] = self.__batting.get_batter(self.__batinds[self.__half] - 1)

    def clear_bases(self):
        """
        Removes all Players from the bases
        """
        self.__bases = [None, None, None]

    def check_game(self):
        """
        Checks if the game is over

        The game will end if it is the 9th inning or later AND ONE OF:
            1. The home team is winning after the top of the inning ends
            2. The home team takes the lead in the bottom of the inning
            3. The away team is winning after the bottom of the inning ends 
        """
        # check if any of these three conditions are met
        if self.__inning >= 9:
            if self.__half == 0 and self.__outs >= 3 and self.__score[1] > self.__score[0]:
                return True
            if self.__half == 1 and self.__score[1] > self.__score[0]:
                return True
            if self.__half == 1 and self.__outs >= 3 and self.__score[0] > self.__score[1]:
                return True
        # if not in 9th inning or later, or no conditions met:
        return False
        

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