from Player import Player
import Event as e

class Game():
    def __init__(self):
        self.results = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0}     # TESTING

    def at_bat(self, bat, pit):
        """
        Executes an at-bat between Batter bat and Pitcher pit
        """
        print("Batter: " + bat.get_last())
        print("Pitcher: " + pit.get_last())
        
        result = e.ab(bat, pit)
        self.results[result] += 1       # TESTING

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
        elif result == 7:
            print("ground out")
        elif result == 8:
            print("air out")

# for testing purposes
b = Player("Gunnar", "Henderson")
p = Player("Paul", "Skenes")

g = Game()
for i in range(100000):
    g.at_bat(b, p)

print(g.results)