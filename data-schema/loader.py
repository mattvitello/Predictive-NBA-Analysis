from sqlalchemy import create_engine, Table
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import insert
import personnel
import glob, os
from pkg import  Base, db_url
import json

engine = create_engine(db_url, echo=False)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

players = Table('players', Base.metadata, autoload=True)
players_stats = Table('players_stats', Base.metadata, autoload=True)
players_seasons_stats = Table('players_seasons_stats', Base.metadata, autoload=True)
players_seasons_home_stats = Table('players_seasons_home_stats', Base.metadata, autoload=True)
players_seasons_away_stats = Table('players_seasons_away_stats', Base.metadata, autoload=True)

teams_stats = Table('teams_stats', Base.metadata, autoload=True)
leagues = Table('leagues', Base.metadata, autoload=True)
matches = Table('matches', Base.metadata, autoload=True)
scores = Table('scores', Base.metadata, autoload=True)


os.chdir("/Users/mattvitello/Documents/AI/matches/2016-2017")
for file in glob.glob("*.json"):
	#file = "200310280LAL.json"
	#load json
	with open(file) as f:
	    data=f.read()
	    jsondata=json.loads(data)

	#add league
	try:
		engine.execute(leagues.insert(), name = jsondata['league'], season = jsondata['season'], country_id = 1)
	except:
		x = 0


	################ Retrieve ID's for match #####################

	#get homeTeam_id
	t = 'SELECT id FROM teams WHERE name = \'' + jsondata['home']['name'] + '\';'
	homeTeamId = 0
	result = engine.execute(t)
	for i in result:
	    homeTeamId = i[0]

	#get awayTeam_id
	t = 'SELECT id FROM teams WHERE name = \'' + jsondata['away']['name'] + '\';'
	awayTeamId = 0
	result = engine.execute(t)
	for i in result:
	    awayTeamId = i[0]

	#get city_id
	t = 'SELECT city_id FROM cities_teams WHERE team_id = ' + str(homeTeamId) + ';'
	cityId = 0
	result = engine.execute(t)
	for i in result:
	    cityId = i[0]

	#get league_id
	t = 'SELECT id FROM leagues WHERE season = \'' + jsondata['season'] + '\';'
	leagueId = 0
	result = engine.execute(t)
	for i in result:
	    leagueId = i[0]

	#get stadium_id
	t = 'SELECT stadium_id FROM stadiums_teams WHERE team_id = ' + str(homeTeamId) + ';'
	stadiumId = 0
	result = engine.execute(t)
	for i in result:
	    stadiumId = i[0]


	#get result
	MatchResult = jsondata['away']['name'] + ": " + jsondata['away']['scores']['T'] + '\n' + jsondata['home']['name'] + ": " + jsondata['home']['scores']['T']

	#misc
	playerId = 0


	################ Insert data #####################

	#add match
	try:
		engine.execute(matches.insert(), date = jsondata['date'], time = jsondata['time'], city_id = cityId, league_id = leagueId, type = jsondata['type'], home_id = homeTeamId, away_id = awayTeamId, stadium_id = stadiumId, result = MatchResult)
	except:
		x = 0

	#get match_id
	t = 'SELECT id FROM matches WHERE date = \'' + jsondata['date'] + '\' AND home_id = ' + str(homeTeamId) + 'AND away_id = ' + str(awayTeamId) + ';'
	matchId = 0
	result = engine.execute(t)
	for i in result:
	    matchId = i[0]

	#add scores
	try:
		engine.execute(scores.insert(), match_id = matchId, home_1 = jsondata['home']['scores']['1'], away_1 = jsondata['away']['scores']['1'], home_2 = jsondata['home']['scores']['2'], away_2 = jsondata['away']['scores']['2'], home_3 = jsondata['home']['scores']['3'], away_3 = jsondata['away']['scores']['3'], home_4 = jsondata['home']['scores']['4'], away_4 = jsondata['away']['scores']['4'], home_t = jsondata['home']['scores']['T'], away_t = jsondata['away']['scores']['T'])
	except:
		x = 0

	#away team players
	for i in jsondata['away']['players']:
		m = jsondata['away']['players'][i]
		
		name = m['name']
		if("'" in name):
			name = name.replace("'", "")
		

	    #add players
		try:
			engine.execute(players.insert(), name = name, birth_date = m['birth_date'], position = m['position'], height = m['height'], weight = m['weight'], experience = m['experience'])
		except:
			x = 0

	    #get playerID
		t = 'SELECT id FROM players WHERE name = \'' + name + '\' AND birth_date = \'' + m['birth_date'] + '\';'
		playerId = 0
		result = engine.execute(t)
		for y in result:
			playerId = y[0]

	    #add player stats
		try:
			engine.execute(players_stats.insert(), team_id = awayTeamId, league_id = leagueId, player_id = playerId, date = jsondata['season'], STLP = m['STL%'], FT = m['FT'], THR = m['3P'], TOV = m['TOV'], MP = m['MP'], STL_to_TOV = m['STL/TOV'], TSA = m['TSA'], TWOA = m['2PA'], FG = m['FG'], THRA = m['3PA'], DRB = m['DRB'], ORBP = m['ORB%'], BLKP = m['BLK%'], AST_to_TOV = m['AST/TOV'], AST = m['AST'], FTP = m['FT%'], THRAr = m['3PAr'], PF = m['PF'], PTS = m['PTS'], FGA = m['FGA'], DRBr = m['DRBr'], ORBr = m['ORBr'], TWO = m['2P'], STL = m['STL'], TRB = m['TRB'], TOVP = m['TOV%'], ASTP = m['AST%'], FTAr = m['FTAr'], FTA = m['FTA'], FIC = m['FIC'], EFGP = m['eFG%'], BLK = m['BLK'], FGP = m['FG%'], TWOAr = m['2PAr'], PLUS_MINUS = m['+/-'], USGP = m['USG%'], DRBP = m['DRB%'], TSP = m['TS%'], TWOP = m['2P%'], DRtg = m['DRtg'], ORtg = m['ORtg'], TRBP = m['TRB%'], FT_to_FGA = m['FT/FGA'], ORB = m['ORB'], THRP = m['3P%'], HOB = m['HOB'])
		except:
			x = 0


	#home team players
	for i in jsondata['home']['players']:
		m = jsondata['home']['players'][i]

		name = m['name']
		if("'" in name):
			name = name.replace("'", "")
		

	    #add players
		try:
			engine.execute(players.insert(), name = name, birth_date = m['birth_date'], position = m['position'], height = m['height'], weight = m['weight'], experience = m['experience'])
		except:
			x = 0

	  	#get playerID
		t = 'SELECT id FROM players WHERE name = \'' + name + '\' AND birth_date = \'' + m['birth_date'] + '\';'
		playerId = 0
		result = engine.execute(t)
		for y in result:
			playerId = y[0]

	    #add player stats
		try:
			engine.execute(players_stats.insert(), player_id = playerId, match_id = matchId, team_id = homeTeamId, STLP = m['STL%'], FT = m['FT'], THR = m['3P'], TOV = m['TOV'], MP = m['MP'], STL_to_TOV = m['STL/TOV'], TSA = m['TSA'], TWOA = m['2PA'], FG = m['FG'], THRA = m['3PA'], DRB = m['DRB'], ORBP = m['ORB%'], BLKP = m['BLK%'], AST_to_TOV = m['AST/TOV'], AST = m['AST'], FTP = m['FT%'], THRAr = m['3PAr'], PF = m['PF'], PTS = m['PTS'], FGA = m['FGA'], DRBr = m['DRBr'], ORBr = m['ORBr'], TWO = m['2P'], STL = m['STL'], TRB = m['TRB'], TOVP = m['TOV%'], ASTP = m['AST%'], FTAr = m['FTAr'], FTA = m['FTA'], FIC = m['FIC'], EFGP = m['eFG%'], BLK = m['BLK'], FGP = m['FG%'], TWOAr = m['2PAr'], PLUS_MINUS = m['+/-'], USGP = m['USG%'], DRBP = m['DRB%'], TSP = m['TS%'], TWOP = m['2P%'], DRtg = m['DRtg'], ORtg = m['ORtg'], TRBP = m['TRB%'], FT_to_FGA = m['FT/FGA'], ORB = m['ORB'], THRP = m['3P%'], HOB = m['HOB'])
		except:
			x = 0


	#add home team stats
	m = jsondata['home']['totals']
	try:
		engine.execute(teams_stats.insert(), match_id = matchId, team_id = homeTeamId, STLP = m['STL%'], FT = m['FT'], THR = m['3P'], TOV = m['TOV'], STL_to_TOV = m['STL/TOV'], TSA = m['TSA'], TWOA = m['2PA'], FG = m['FG'], THRA = m['3PA'], DRB = m['DRB'], ORBP = m['ORB%'], BLKP = m['BLK%'], AST_to_TOV = m['AST/TOV'], AST = m['AST'], FTP = m['FT%'], THRAr = m['3PAr'], PF = m['PF'], PTS = m['PTS'], FGA = m['FGA'], DRBr = m['DRBr'], ORBr = m['ORBr'], TWO = m['2P'], STL = m['STL'], TRB = m['TRB'], TOVP = m['TOV%'], ASTP = m['AST%'], FTAr = m['FTAr'], FTA = m['FTA'], FIC = m['FIC'], EFGP = m['eFG%'], BLK = m['BLK'], FGP = m['FG%'], TWOAr = m['2PAr'], PLUS_MINUS = m['+/-'], USGP = m['USG%'], DRBP = m['DRB%'], TSP = m['TS%'], TWOP = m['2P%'], DRtg = m['DRtg'], ORtg = m['ORtg'], TRBP = m['TRB%'], FT_to_FGA = m['FT/FGA'], ORB = m['ORB'], THRP = m['3P%'], HOB = m['HOB'])
	except:
		x = 0

	#add away team stats
	m = jsondata['away']['totals']
	try:
		engine.execute(teams_stats.insert(), match_id = matchId, team_id = awayTeamId, STLP = m['STL%'], FT = m['FT'], THR = m['3P'], TOV = m['TOV'], STL_to_TOV = m['STL/TOV'], TSA = m['TSA'], TWOA = m['2PA'], FG = m['FG'], THRA = m['3PA'], DRB = m['DRB'], ORBP = m['ORB%'], BLKP = m['BLK%'], AST_to_TOV = m['AST/TOV'], AST = m['AST'], FTP = m['FT%'], THRAr = m['3PAr'], PF = m['PF'], PTS = m['PTS'], FGA = m['FGA'], DRBr = m['DRBr'], ORBr = m['ORBr'], TWO = m['2P'], STL = m['STL'], TRB = m['TRB'], TOVP = m['TOV%'], ASTP = m['AST%'], FTAr = m['FTAr'], FTA = m['FTA'], FIC = m['FIC'], EFGP = m['eFG%'], BLK = m['BLK'], FGP = m['FG%'], TWOAr = m['2PAr'], PLUS_MINUS = m['+/-'], USGP = m['USG%'], DRBP = m['DRB%'], TSP = m['TS%'], TWOP = m['2P%'], DRtg = m['DRtg'], ORtg = m['ORtg'], TRBP = m['TRB%'], FT_to_FGA = m['FT/FGA'], ORB = m['ORB'], THRP = m['3P%'], HOB = m['HOB'])
	except:
		x = 0



















