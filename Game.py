from Player import Player
import Event as e

class Game():
    def __init__(self):
        self.__outs = 0
        self.__inning = 1
        self.__half = 0
        self.__over = False

    def play(self):
        """
        Operates the main gameplay loop
        """
        while not self.__over:
            self.at_bat(b, p)
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
            print(f"OUTS: {self.__outs}")
        elif result == 7:
            print("ground out")
            self.__outs += 1
            print(f"OUTS: {self.__outs}")
        elif result == 8:
            print("air out")
            self.__outs += 1
            print(f"OUTS: {self.__outs}")

    def update_inning(self):
        """
        Updates the game after an inning has ended
        """
        self.__inning += self.__half
        self.__half = (self.__half + 1) % 2
        self.__outs = 0
        if self.__half == 0:
            print(f"TOP {self.__inning}")
        else:
            print(f"BOT {self.__inning}")

    def check_game(self):
        """
        Checks if the game is over

        FOR NOW, this is a dummy method that needs to be updated later
        """
        return self.__inning >= 9 and self.__half == 1 and self.__outs >= 3

# for testing purposes
b = Player("Gunnar", "Henderson")
p = Player("Paul", "Skenes")

g = Game()
g.play()