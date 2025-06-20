from Player import Batter, Pitcher
from Team import Team
import Event as e

class Game():

    class Base():
        """
        Defines an inner class Bases that is used by the Game class to track baserunners and the
        Pitchers responsible for putting them on base
        """
        def __init__(self):
            self.__runner = None
            self.__pitcher = None

        def runner(self):
            """
            Returns the runner on this Base
            """
            return self.__runner
        
        def pitcher(self):
            """
            Returns the pitcher responsible for the runner on this Base
            """
            return self.__pitcher
        
        def get_on_base(self, runner, pitcher):
            """
            Puts the given runner on this base. The given pitcher is responsible for the runner
            """
            self.__runner = runner
            self.__pitcher = pitcher

        def advance(self, prev_base):
            """
            Moves the runner from the the prev_base to this one
            """
            self.__runner = prev_base.runner()
            self.__pitcher = prev_base.pitcher()

        def clear(self):
            """
            Removes any runner from the base
            """
            self.__runner = None
            self.__pitcher = None

        def is_empty(self):
            """
            Checks if the base is empty
            """
            return self.__runner is None

    def __init__(self, home, away):
        self.__outs = 0
        self.__inning = 1
        self.__half = 0
        self.__away_info = {"team" : away, "score" : 0, "bat_ind" : 0, "pitcher" : away.get_pitcher(), "used" : [away.get_pitcher()]}
        self.__home_info = {"team" : home, "score" : 0, "bat_ind" : 0, "pitcher" : home.get_pitcher(), "used" : [home.get_pitcher()]}
        self.__bases = [Game.Base(), Game.Base(), Game.Base()]
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
            sel = "h"

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
            # single
            print(f"{bat.get_last()} singles")
            self.base_hit(1, bat, pit)
            bat.single()
            pit.hit()

        elif result == 2:
            # double
            print(f"{bat.get_last()} doubles")
            self.base_hit(2, bat, pit)
            bat.double()
            pit.hit()

        elif result == 3:
            # triple
            print(f"{bat.get_last()} triples")
            self.base_hit(3, bat, pit)
            bat.triple()
            pit.hit()

        elif result == 4:
            # home run
            print(f"{bat.get_last()} hits a home run!")
            self.base_hit(4, bat, pit)
            bat.homerun()
            pit.hit()

        elif result == 5:
            # walk
            print(f"{bat.get_last()} walks")
            bat.walk()
            pit.walk()

            # if bases are loaded, score a run and advance all runners
            if self.bases_loaded():
                self.score_runner(self.__bases[2])
                bat.RBI()
                self.print_score()
                for i in range(2, 0, -1):
                    self.__bases[i].advance(self.__bases[i-1])
                self.__bases[0].get_on_base(bat, pit)
            # otherwise advance needed runners only
            else:
                for j in range(0, 3):
                    if j == 2 or self.__bases[j].is_empty():
                        for k in range(j, 0, -1):
                            self.__bases[k].advance(self.__bases[k-1])
                        self.__bases[0].get_on_base(bat, pit)
                        break

        elif result == 6:
            # strikeout
            print(f"{bat.get_last()} strikes out!")
            self.__outs += 1
            bat.out()
            pit.strikeout()

        elif result == 7:
            # ground out
            bat.out()
            pit.groundout()

            # determine if a double play is possible
            if self.__outs < 2 and not self.__bases[0].is_empty():

                # determine the type of double play scenario and call the appropriate gidp function
                if self.bases_loaded():             # bases loaded
                    gidp_result = e.gidp(3)
                elif not self.__bases[1].is_empty:  # runners on 1st and 2nd
                    gidp_result = e.gidp(2)
                else:                               # runners on 1st and 3rd, or only on 1st
                    gidp_result = e.gidp(1)

                if gidp_result == 1:
                    # groundout (out at 1st)
                    print(f"{bat.get_last()} grounds out")
                    self.__outs += 1

                    # if runner on 3rd, runner scores
                    # inning can't end in this scenario, so don't need to check it
                    if not self.__bases[2].is_empty():
                        self.score_runner(self.__bases[2])
                        bat.RBI()
                        self.print_score()

                    # advance other runners
                    self.__bases[2].advance(self.__bases[1])    # runner on 2nd (if any) goes to 3rd
                    self.__bases[1].advance(self.__bases[0])    # runner safe at 2nd
                    self.__bases[0].clear()                     # batter out at 1st

                elif gidp_result == 2:
                    # FC (out at 2nd)
                    print(f"{bat.get_last()} grounds into a fielder's choice")
                    print(f"{self.__bases[0].runner().get_last()} out at 2nd")
                    self.__outs += 1

                    # if runner on 3rd, runner scores
                    # inning can't end in this scenario, so don't need to check it
                    if not self.__bases[2].is_empty():
                        self.score_runner(self.__bases[2])
                        bat.RBI()
                        self.print_score()

                    # advance other runners
                    self.__bases[2].advance(self.__bases[1])    # runner on 2nd (if any) goes to 3rd
                    self.__bases[1].clear()                     # runner out at 2nd
                    self.__bases[0].get_on_base(bat, pit)       # batter safe at 1st

                elif gidp_result == 3:
                    # GIDP (out at 2nd and 1st)
                    print(f"{bat.get_last()} grounds into a double play")
                    print(f"{self.__bases[0].runner().get_last()} out at 2nd")
                    self.__outs += 2
                    pit.add_outs(1)

                    # if runner on 3rd and inning is not over, runner scores
                    if not self.__bases[2].is_empty() and self.__outs != 3:
                        self.score_runner(self.__bases[2])
                        # batter does not get RBI on DP
                        self.print_score()

                    # advance other runner
                    self.__bases[2].advance(self.__bases[1])    # runner on 2nd (if any) goes to 3rd
                    self.__bases[1].clear()                     # runner out at 2nd
                    self.__bases[0].clear()                     # batter out at 1st

                elif gidp_result == 4:
                    # FC (out at home)
                    print(f"{bat.get_last()} grounds into a fielder's choice")
                    print(f"{self.__bases[2].runner().get_last()} out at home")
                    self.__outs += 1

                    # no runner will score

                    # advance other runners
                    self.__bases[2].advance(self.__bases[1])    # runner on 2nd goes to 3rd
                    self.__bases[1].advance(self.__bases[0])    # runner on 1st goes to 2nd
                    self.__bases[0].get_on_base(bat, pit)       # batter safe at 1st

                elif gidp_result == 5:
                    # GIDP (out at home and 1st)
                    print(f"{bat.get_last()} grounds into a double play")
                    print(f"{self.__bases[2].runner().get_last()} out at home")
                    self.__outs += 2
                    pit.add_outs(1)

                    # no runner will score

                    # advance other runners
                    self.__bases[2].advance(self.__bases[1])    # runner on 2nd goes to 3rd
                    self.__bases[1].advance(self.__bases[0])    # runner on 1st goes to 2nd
                    self.__bases[0].clear()                     # batter out at 1st

            # if no runner on first, other runners are not forced and will not advance
            else:
                print(f"{bat.get_last()} grounds out")
                self.__outs += 1

        elif result == 8:
            # fly out
            pit.airout()

            # determine if there is a sac fly
            if self.__outs < 2 and not self.__bases[2].is_empty() and e.sf() == 1:
                print(f"{bat.get_last()} hits a sacrifice fly")
                bat.sacfly()
                self.score_runner(self.__bases[2])
                self.print_score()
                self.__bases[2].clear()
            
            # no sac fly
            else:
                print(f"{bat.get_last()} flies out")
                bat.out()
            
            # in both cases
            self.__outs += 1

        print("")

    def base_hit(self, num_bases, bat, pit):
        """
        Updates the Game after a base hit by Batter bat of the provided number of 
        bases, num_bases (between 1-4). Pitcher pit is responsible for the batter
        """
        runs_scored = False
        # scores any runners, if required
        for i in range(2, max(2 - num_bases, -1), -1):
            if not self.__bases[i].is_empty():
                self.score_runner(self.__bases[i])
                bat.RBI()
                runs_scored = True

        # update runners already on bases
        for j in range(2, num_bases - 1, -1):
            self.__bases[j].advance(self.__bases[j - num_bases])
        
        # put batter on bases if not home run, otherwise score the run
        if num_bases < 4:
            self.__bases[num_bases - 1].get_on_base(bat, pit)
        else:
            self.__batting["score"] += 1
            pit.earned_run()
            runs_scored = True
        
        # set other bases to empty
        for k in range(num_bases - 2, -1, -1):
            self.__bases[k].clear()

        # print updated score if necessary
        if runs_scored:
            self.print_score()

    def score_runner(self, base):
        """
        Scores the given runner on the given base
        """
        print(f"{base.runner().get_last()} scores!")
        self.__batting["score"] += 1
        if base.pitcher() is not None:
            base.pitcher().earned_run()
        base.runner().run()

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

        # extra innings rule
        if self.__inning >= 10:
            # no pitcher is responsible for the ghost runner
            self.__bases[1].get_on_base(self.__batting["team"].get_batter(self.__batting["bat_ind"] - 1), None)

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

    def bases_loaded(self):
        """
        Checks if the bases are loaded
        """
        for base in self.__bases:
            if base.is_empty():
                return False
        return True

    def clear_bases(self):
        """
        Removes all Players from the bases
        """
        for base in self.__bases:
            base.clear()

    def print_score(self):
        """
        Prints the current score in the Game
        """
        print(f"{self.__away_info['team'].get_name()} {self.__away_info['score']} @ {self.__home_info['team'].get_name()} {self.__home_info['score']}")
        

# for testing purposes
bluejays = Team("Blue Jays")
bluejays.add_batter(Batter("alekir1", "Alejandro", "Kirk"))
bluejays.add_batter(Batter("vlague1", "Vladamir", "Guerrero Jr."))
bluejays.add_batter(Batter("andgim1", "Andres", "Gimenez"))
bluejays.add_batter(Batter("bobic1", "Bo", "Bichette"))
bluejays.add_batter(Batter("erncle1", "Ernie", "Clement"))
bluejays.add_batter(Batter("davsch1", "Davis", "Schneider"))
bluejays.add_batter(Batter("dauvar1", "Daulton", "Varsho"))
bluejays.add_batter(Batter("geospr1", "George", "Springer"))
bluejays.add_batter(Batter("antsan1", "Anthony", "Santander"))
bluejays.add_pitcher(Pitcher("josber1", "Jose", "Berrios"), True)
bluejays.add_pitcher(Pitcher("jefhof1", "Jeff", "Hoffman"), False)
bluejays.add_pitcher(Pitcher("yimgar1", "Yimi", "Garcia"), False)

swansons = Team("Swansons")
swansons.add_batter(Batter("shelee1", "Sherry", "Lee"))
swansons.add_batter(Batter("tanmer1", "Tanner", "Mergle"))
swansons.add_batter(Batter("samgoe1", "Sam", "Goerz"))
swansons.add_batter(Batter("trisch1", "Tristin", "Schlauch"))
swansons.add_batter(Batter("sunbyu1", "Sungwoo", "Byun"))
swansons.add_batter(Batter("wilbli1", "William", "Blimke"))
swansons.add_batter(Batter("ryacha1", "Ryan", "Chan"))
swansons.add_batter(Batter("reedri1", "Reed", "Drinkle"))
swansons.add_batter(Batter("greliv1", "Greg", "Livingood"))
swansons.add_pitcher(Pitcher("kricle1", "Kris", "Clements"), True)

finished = False
while not finished:
    g = Game(bluejays, swansons)
    g.play()
    while True:
        choice = input("Would you like to play again? y/n >> ")
        if choice == "y":   # play again
            print("Playing again!")
            break
        if choice == "n":
            finished = True
            break
        print("Please enter a valid option!")

swansons.print_stats()
bluejays.print_stats()