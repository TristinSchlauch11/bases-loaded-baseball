import sqlite3

# connect to DB and make cursor
conn = sqlite3.connect("C:/Users/nmbr1/OneDrive/Documents/bases-loaded-baseball/player_stats.db")
cursor = conn.cursor()

# delete table to reset them
cursor.execute("DROP TABLE teams;")

# create table for teams
comm = """CREATE TABLE teams (
team_code VARCHAR(3) PRIMARY KEY,
location VARCHAR(15),
name VARCHAR(18));"""

cursor.execute(comm)

# add teams to table
comm = """INSERT INTO teams VALUES
('TOR', 'Toronto', 'Blue Jays'),
('JTS', 'Jig Town', 'Swansons');"""

cursor.execute(comm)

# commit changes and close
conn.commit()
conn.close()