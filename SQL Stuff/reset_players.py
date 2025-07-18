# This file will reset all player statistics to 0
# This avoids having to scrape the web again, as well as initializing the teams again

import sqlite3

# establish connection
conn = sqlite3.connect("C:/Users/nmbr1/OneDrive/Documents/bases-loaded-baseball/player_stats.db")
cursor = conn.cursor()

# reset batter stats
comm = """UPDATE bat_stats
SET hits = 0, doubles = 0, triples = 0, homeruns = 0, walks = 0, runs = 0, RBIs = 0, ABs = 0, PAs = 0;
"""
cursor.execute(comm)

# reset pitcher stats
comm = """UPDATE pit_stats
SET outs = 0, groundouts = 0, airouts = 0, strikeouts = 0, hits = 0, walks = 0, ERs = 0, TBF = 0;
"""
cursor.execute(comm)

# commit and close
conn.commit()
conn.close()