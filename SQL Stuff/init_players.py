import sqlite3

conn = sqlite3.connect("C:/Users/nmbr1/OneDrive/Documents/bases-loaded-baseball/player_stats.db")
cursor = conn.cursor()

# delete tables to reset them
cursor.execute("DROP TABLE bat_stats")
cursor.execute("DROP TABLE pit_stats")

# create table for batter stats
comm = """CREATE TABLE bat_stats (
player_id VARCHAR(8) PRIMARY KEY,
fname VARCHAR(12),
lname VARCHAR(20),
hits INTEGER,
doubles INTEGER,
triples INTEGER,
homeruns INTEGER,
walks INTEGER,
runs INTEGER,
RBIs INTEGER,
ABs INTEGER,
PAs INTEGER);"""

cursor.execute(comm)

# add batters to table
comm = """INSERT INTO bat_stats (player_id, fname, lname) VALUES
('alekir1', 'Alejandro', 'Kirk'),
('vlague1', 'Vladamir', 'Guerrero Jr.'),
('andgim1', 'Andres', 'Gimenez'),
('bobic1', 'Bo', 'Bichette'),
('erncle1', 'Ernie', 'Clement'),
('davsch1', 'Davis', 'Schneider'),
('dauvar1', 'Daulton', 'Varsho'),
('geospr1', 'George', 'Springer'),
('antsan1', 'Anthony', 'Santander'),
('shelee1', 'Sherry', 'Lee'),
('tanmer1', 'Tanner', 'Mergle'),
('samgoe1', 'Sam', 'Goerz'),
('trisch1', 'Tristin', 'Schlauch'),
('sunbyu1', 'Sungwoo', 'Byun'),
('wilbli1', 'William', 'Blimke'),
('ryacha1', 'Ryan', 'Chan'),
('reedri1', 'Reed', 'Drinkle'),
('greliv1', 'Greg', 'Livingood');"""

cursor.execute(comm)

# make all stats 0
comm = """UPDATE bat_stats
SET hits = 0, doubles = 0, triples = 0, homeruns = 0, walks = 0, runs = 0, RBIs = 0, ABs = 0, PAs = 0;"""

cursor.execute(comm)

# create table for pitcher stats
comm = """CREATE TABLE pit_stats (
player_id VARCHAR(8) PRIMARY KEY,
fname VARCHAR(12),
lname VARCHAR(20),
outs INTEGER,
groundouts INTEGER,
airouts INTEGER,
strikeouts INTEGER,
hits INTEGER,
walks INTEGER,
ERs INTEGER,
TBF INTEGER);"""

cursor.execute(comm)

# add pitchers to table
comm = """INSERT INTO pit_stats (player_id, fname, lname) VALUES
('josber1', 'Jose', 'Berrios'),
('jefhof1', 'Jeff', 'Hoffman'),
('yimgar1', 'Yimi', 'Garcia'),
('kricle1', 'Kris', 'Clements');"""

cursor.execute(comm)

# make all stats 0
comm = """UPDATE pit_stats
SET outs = 0, groundouts = 0, airouts = 0, strikeouts = 0, hits = 0, walks = 0, ERs = 0, TBF = 0;"""

cursor.execute(comm)

# commit changes and close
conn.commit()
conn.close()