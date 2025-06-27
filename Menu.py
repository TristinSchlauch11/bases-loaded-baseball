# start up code to run for the program to work
# TO BE DELETED LATER
from Player import Batter, Pitcher
from Team import Team

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



def select_team():
    """
    Function used in the Menu module to select teams in the menu
    Continues to prompt the user until a valid team is selected
    Can also view a full list of team codes 

    Returns a Team object
    """
    while True:
        # make selection
        team_code = input("\nPlease enter the team code of the team you wish to use >> ")

        # check if team code is valid
        cursor.execute(f"SELECT COUNT(*) FROM teams WHERE team_code = '{team_code}';")
        if cursor.fetchone()[0]:
            # create the team object
            cursor.execute(f"SELECT name FROM teams WHERE team_code = '{team_code}';")
            (name, ) = cursor.fetchone()
            return Team(name)
        elif team_code == "MLB":
            # print all team codes
            cursor.execute("SELECT * FROM teams;")
            rows = cursor.fetchall()
            for (code, loc, name) in rows:
                print(f"{code:3} | {loc} {name}")
        else:
            # team invalid
            print("Invalid code.")
            print("If you need to view the list of team codes, please type 'MLB'.")

import sqlite3

# connect to DB and make cursor
conn = sqlite3.connect("C:/Users/nmbr1/OneDrive/Documents/bases-loaded-baseball/player_stats.db")
cursor = conn.cursor()

done = False
while not done:
    print("\nWelcome to Bases Loaded Baseball '25!")
    print("Please select an option from the menu below:")
    print("1. Play Game")
    print("2. View Team Stats")
    print("3. Quit Game")
    sel = input("Enter a number >> ")
    if sel == "1":
        # select two teams, then play game
        
        # pick the teams
        print("\nSelect the away team.")
        away = select_team()
        print("\nSelect the home team.")
        home = select_team()

        # confirm teams
        print(f"{away.get_name()} @ {home.get_name()}")
        if input("Ready to play? Type 'y' >> ") == 'y':
            print("Play game...")
        else:
            print("Game not started, returning to main menu")

    elif sel == "2":
        # select a team, then display stats of players
        # can also view a list of all teams if needed
        pass

    elif sel == "3":
        # quit game, confirm that the user wants to quit the game
        print("Would you like to quit the game?")
        if input("Type 'q' to quit >> ") == 'q':
            done = True
    else:
        print("Invalid selection.") 

conn.close()