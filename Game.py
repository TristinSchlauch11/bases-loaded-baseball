from Player import Player
from Team import Team
import Event as e

class Game():
    def __init__(self, home, away):
        self.__outs = 0
        self.__inning = 1
        self.__half = 0
        self.__away_info = {"team" : away, "score" : 0, "bat_ind" : 0, "pitcher" : away.get_pitcher(), "used" : [away.get_pitcher()]}
        self.__home_info = {"team" : home, "score" : 0, "bat_ind" : 0, "pitcher" : home.get_pitcher(), "used" : [home.get_pitcher()]}
        self.__bases = [None, None, None]
        self.__batting = self.__away_info       # attempting new approach
        self.__pitching = self.__home_info      # attempting new approach
        self.__over = False

    def play(self):
        """
        Operates the main gameplay loop
        """
        while not self.__over:
            # get batter and pitcher
            bat = self.__batting["team"].get_batter(self.__batting["bat_ind"])
            pit = self.__pitching["pitcher"]

            # print next batter and pitcher
            print(f"Batter: {bat.get_last()}")
            print(f"Pitcher: {pit.get_last()}")

            # make next selection
            # sel = input("\nEnter 'h' to hit, 's' to substitute, or 'q' to quit game >> ")
            sel = "h"       # TESTING

            # execute next PA
            if sel == "h":
                self.plate_app(bat, pit)
                self.__batting["bat_ind"] = (self.__batting["bat_ind"] + 1) % 9
            # attempt to make substitution
            elif sel == "s":
                if (new_pitch := self.__pitching["team"].select_rp(self.__pitching["pitcher"], self.__pitching["used"])) is not None:
                    self.__pitching["pitcher"] = new_pitch
                    self.__pitching["used"].append(new_pitch)
                print(f"Now pitching: {self.__pitching['pitcher'].get_last()}\n")
            # request to quit game, confirm with user
            elif sel == "q":
                quit_sel = input("You are trying to quit the game. Enter 'y' to quit >> ")
                if quit_sel == "y":
                    break   # need to break completely from loop, otherwise check_game will make self.__over False again
            else:
                print("Invalid entry.\n")

            # check game status
            self.__over = self.check_game()
            if not self.__over and self.__outs == 3:
                self.update_inning()
        self.print_score()

    def plate_app(self, bat, pit):
        """
        Executes a plate appearance between Batter bat and Pitcher pit
        """        
        result = e.pa(bat, pit)

        if result == 1:
            print(f"{bat.get_last()} singles")
            self.base_hit(1, bat)

        elif result == 2:
            print(f"{bat.get_last()} doubles")
            self.base_hit(2, bat)

        elif result == 3:
            print(f"{bat.get_last()} triples")
            self.base_hit(3, bat)

        elif result == 4:
            print(f"{bat.get_last()} hits a home run!")
            self.base_hit(4, bat)

        elif result == 5:
            print(f"{bat.get_last()} walks")
            # if bases are loaded, score a run and advance all runners
            if None not in self.__bases:
                print(f"{self.__bases[2].get_last()} scores!")
                self.__batting["score"] += 1
                self.print_score()
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
            print(f"{bat.get_last()} strikes out!")
            self.__outs += 1

        elif result == 7:

            # determine if a double play is possible
            if self.__outs < 2 and self.__bases[0] is not None:
                gidp_result = e.gidp()

                if gidp_result == 1:
                    # GIDP (out at 2nd and 1st)
                    print(f"{bat.get_last()} grounds into a double play")
                    print(f"{self.__bases[0].get_last()} out at 2nd")
                    self.__outs += 2

                    # if runner on 3rd and inning is not over, runner scores
                    if self.__bases[2] is not None and self.__outs != 3:
                        print(f"{self.__bases[2].get_last()} scores!")
                        self.__batting["score"] += 1
                        self.print_score()

                    # advance other runner
                    self.__bases[2] = self.__bases[1]
                    self.__bases[1] = None
                    self.__bases[0] = None

                elif gidp_result == 2:
                    # FC (out at 2nd)
                    print(f"{bat.get_last()} grounds into a fielder's choice")
                    print(f"{self.__bases[0].get_last()} out at 2nd")
                    self.__outs += 1

                    # if runner on 3rd, runner scores
                    # inning can't end in this scenario, so don't need to check it
                    if self.__bases[2] is not None:
                        print(f"{self.__bases[2].get_last()} scores!")
                        self.__batting["score"] += 1
                        self.print_score()

                    # advance other runners
                    self.__bases[2] = self.__bases[1]
                    self.__bases[1] = None
                    self.__bases[0] = bat

                elif gidp_result == 3:
                    # groundout (out at 1st)
                    print(f"{bat.get_last()} grounds out")
                    self.__outs += 1

                    # if runner on 3rd, runner scores
                    # inning can't end in this scenario, so don't need to check it
                    if self.__bases[2] is not None:
                        print(f"{self.__bases[2].get_last()} scores!")
                        self.__batting["score"] += 1
                        self.print_score()

                    # advance other runners
                    self.__bases[2] = self.__bases[1]
                    self.__bases[1] = self.__bases[0]
                    self.__bases[0] = None

            # if no runner on first, other runners are not forced and will not advance
            else:
                print(f"{bat.get_last()} grounds out")
                self.__outs += 1

        elif result == 8:
            # determine if there is a sac fly
            if self.__outs < 2 and self.__bases[2] is not None and e.sf() == 1:
                print(f"{bat.get_last()} hits a sacrifice fly")
                print(f"{self.__bases[2].get_last()} scores!")
                self.__batting["score"] += 1
                self.print_score()
                self.__bases[2] = None
            
            # no sac fly
            else:
                print(f"{bat.get_last()} flies out")
            
            # in both cases
            self.__outs += 1

        # self.print_bases()
        print("")

    def base_hit(self, num_bases, b):
        """
        Updates the Game after a base hit by batter b of the provided number of 
        bases, num_bases (between 1-4)
        """
        runs_scored = False
        # scores any runners, if required
        for i in range(2, max(2 - num_bases, -1), -1):
            if self.__bases[i] is not None:
                print(f"{self.__bases[i].get_last()} scores!")
                self.__batting["score"] += 1
                runs_scored = True

        # update runners already on bases
        for j in range(2, num_bases - 1, -1):
            self.__bases[j] = self.__bases[j - num_bases]
        
        # put batter on bases if not home run, otherwise score the run
        if num_bases < 4:
            self.__bases[num_bases - 1] = b
        else:
            self.__batting["score"] += 1
            runs_scored = True
        
        # set other bases to empty
        for k in range(num_bases - 2, -1, -1):
            self.__bases[k] = None

        # print updated score if necessary
        if runs_scored:
            self.print_score()

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

    def print_score(self):
        """
        Prints the current score in the Game
        """
        print(f"{self.__away_info['team'].get_name()} {self.__away_info['score']} @ {self.__home_info['team'].get_name()} {self.__home_info['score']}")

    def update_inning(self):
        """
        Updates the game after an inning has ended
        """
        self.__inning += self.__half
        self.__half = (self.__half + 1) % 2
        self.__outs = 0
        self.clear_bases()
        self.print_score()
        if self.__half == 0:
            print(f"\nTOP {self.__inning}")
            self.__batting = self.__away_info       # attempting new approach
            self.__pitching = self.__home_info      # attempting new approach
        else:
            print(f"\nBOT {self.__inning}")
            self.__batting = self.__home_info       # attempting new approach
            self.__pitching = self.__away_info      # attempting new approach
        self.__bases[0] = self.__batting["team"].get_batter(self.__batting["bat_ind"] - 1)      # TESTING

        # extra innings rule
        if self.__inning >= 10:
            self.__bases[1] = self.__batting["team"].get_batter(self.__batting["bat_ind"] - 1)

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
            if self.__half == 0 and self.__outs >= 3 and self.__home_info["score"] > self.__away_info["score"]:
                return True
            if self.__half == 1 and self.__home_info["score"] > self.__away_info["score"]:
                return True
            if self.__half == 1 and self.__outs >= 3 and self.__home_info["score"] < self.__away_info["score"]:
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
bluejays.add_pitcher(Player("Jose", "Berrios"), True)
bluejays.add_pitcher(Player("Jeff", "Hoffman"), False)
bluejays.add_pitcher(Player("Yimi", "Garcia"), False)

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
swansons.add_pitcher(Player("Kris", "Clements"), True)

g = Game(bluejays, swansons)
g.play()