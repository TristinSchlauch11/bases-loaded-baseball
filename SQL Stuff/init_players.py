import sqlite3

# connect to DB and make cursor
conn = sqlite3.connect("C:/Users/nmbr1/OneDrive/Documents/bases-loaded-baseball/player_stats.db")
cursor = conn.cursor()

# delete tables to reset them
cursor.execute("DROP TABLE bat_stats;")
cursor.execute("DROP TABLE pit_stats;")

# create table for batter stats
comm = """CREATE TABLE bat_stats (
player_id VARCHAR(8) PRIMARY KEY,
team VARCHAR(3),
fname VARCHAR(12) NOT NULL,
lname VARCHAR(20) NOT NULL,
hits INTEGER DEFAULT 0,
doubles INTEGER DEFAULT 0,
triples INTEGER DEFAULT 0,
homeruns INTEGER DEFAULT 0,
walks INTEGER DEFAULT 0,
runs INTEGER DEFAULT 0,
RBIs INTEGER DEFAULT 0,
ABs INTEGER DEFAULT 0,
PAs INTEGER DEFAULT 0,
FOREIGN KEY (team) REFERENCES Teams(team_code));"""

cursor.execute(comm)

# add batters to table
comm = """INSERT INTO bat_stats (player_id, fname, lname, team) VALUES
('alekir1', 'Alejandro', 'Kirk', 'TOR'),
('vlague1', 'Vladamir', 'Guerrero Jr.', 'TOR'),
('andgim1', 'Andres', 'Gimenez', 'TOR'),
('bobic1', 'Bo', 'Bichette', 'TOR'),
('erncle1', 'Ernie', 'Clement', 'TOR'),
('davsch1', 'Davis', 'Schneider', 'TOR'),
('dauvar1', 'Daulton', 'Varsho', 'TOR'),
('geospr1', 'George', 'Springer', 'TOR'),
('antsan1', 'Anthony', 'Santander', 'TOR'),
('shelee1', 'Sherry', 'Lee', 'JTS'),
('tanmer1', 'Tanner', 'Mergle', 'JTS'),
('samgoe1', 'Sam', 'Goerz', 'JTS'),
('trisch1', 'Tristin', 'Schlauch', 'JTS'),
('sunbyu1', 'Sungwoo', 'Byun', 'JTS'),
('wilbli1', 'William', 'Blimke', 'JTS'),
('ryacha1', 'Ryan', 'Chan', 'JTS'),
('reedri1', 'Reed', 'Drinkle', 'JTS'),
('greliv1', 'Greg', 'Livingood', 'JTS');"""

cursor.execute(comm)

# create table for pitcher stats
comm = """CREATE TABLE pit_stats (
player_id VARCHAR(8) PRIMARY KEY,
team VARCHAR(3),
fname VARCHAR(12) NOT NULL,
lname VARCHAR(20) NOT NULL,
is_sp INTEGER,
outs INTEGER DEFAULT 0,
groundouts INTEGER DEFAULT 0,
airouts INTEGER DEFAULT 0,
strikeouts INTEGER DEFAULT 0,
hits INTEGER DEFAULT 0,
walks INTEGER DEFAULT 0,
ERs INTEGER DEFAULT 0,
TBF INTEGER DEFAULT 0,
FOREIGN KEY (team) REFERENCES Teams(team_code));"""

cursor.execute(comm)

# add pitchers to table
comm = """INSERT INTO pit_stats (player_id, fname, lname, team, is_sp) VALUES
('josber1', 'Jose', 'Berrios', 'TOR', 1),
('jefhof1', 'Jeff', 'Hoffman', 'TOR', 0),
('yimgar1', 'Yimi', 'Garcia', 'TOR', 0),
('kricle1', 'Kris', 'Clements', 'JTS', 1);"""

cursor.execute(comm)

# commit changes and close
conn.commit()
conn.close()