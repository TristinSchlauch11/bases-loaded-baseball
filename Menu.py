from Team import Team
from Game import Game

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
        if cursor.fetchone()[0]:    # True if team_code is found
            # create the team object
            cursor.execute(f"SELECT team_code, location, name FROM teams WHERE team_code = '{team_code}';")
            (code, loc, name) = cursor.fetchone()
            return Team(code, loc, name, cursor)
        elif team_code == "MLB":
            # print all team codes
            cursor.execute("SELECT * FROM teams;")
            teams = cursor.fetchall()
            for (code, loc, name) in teams:
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
            g = Game(home, away)
            g.play()
        else:
            print("Game not started, returning to main menu")

    elif sel == "2":
        # select a team, then print the stats of all players
        team = select_team()
        team.print_stats(cursor)

    elif sel == "3":
        # quit game, confirm that the user wants to quit the game
        print("Would you like to quit the game?")
        if input("Type 'q' to quit >> ") == 'q':
            done = True
    else:
        print("Invalid selection.") 

conn.close()