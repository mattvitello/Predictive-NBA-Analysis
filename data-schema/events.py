import os
import sys
sys.path.append(os.path.abspath('.'))

import datetime
from collections import defaultdict
from sqlalchemy import Column, Integer, Numeric, String, ForeignKey, Date, Time, \
                       UniqueConstraint, create_engine, tuple_, or_, and_, func
from sqlalchemy.types import Boolean
from sqlalchemy.types import ARRAY
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry
import numpy as np 

from . import Session, Base, enums
from stats import TeamMatchStats, TeamSeasonStats, TeamSeasonHomeStats, TeamSeasonAwayStats


class GoalAttempt(Base):
	__tablename__ = 'goal_attempts'

	id = Column(Integer, primary_key=True)
	mins = Column(Integer)
	secs = Column(Integer)
	minsecs = Column(Integer)
	injurytime_play = Column(Boolean)
	start = Column(Geometry('POINT'))
	end = Column(Geometry('POINT'))
	player_id = Column(ForeignKey('players.id'), index=True)
	team_id = Column(ForeignKey('teams.id'), index=True)
	assisted_by = Column(ForeignKey('players.id'), index=True)
	pass_graph = Column(ARRAY(Integer))
	is_own = Column(Boolean)
	shot = Column(Boolean)
	headed = Column(Boolean)
	#action_type: type of pass. enum
	#coordinates: ??
	#middle: ??
	#swere: ??


class Pass(Base):
	__tablename__ = 'passes'

	id = Column(primary_key=True)
	mins = Column(Integer)
	secs = Column(Integer)
	minsecs = Column(Integer)
	injurytime_play = Column(Boolean)
	start = Column(Geometry('POINT'))
	end = Column(Geometry('POINT'))
	player_id = Column(ForeignKey('players.id'), index=True)
	team_id = Column(ForeignKey('teams.id'), index=True)
	assist = Column(Boolean)
	headed = Column(Boolean)
	key_pass = Column(Boolean)
	long_ball = Column(Boolean)
	through_ball = Column(Boolean)
	throw_ins = Column(Boolean)
	# action_type: type of pass. [Possession]
	# type = outcome enum


class Cross(Base):
	__tablename__ = 'crosses'

	id = Column(primary_key=True)
	mins = Column(Integer)
	secs = Column(Integer)
	minsecs = Column(Integer)
	injurytime_play = Column(Boolean)
	start = Column(Geometry('POINT'))
	end = Column(Geometry('POINT'))
	player_id = Column(ForeignKey('players.id'), index=True)
	team_id = Column(ForeignKey('teams.id'), index=True)
	key_pass = Column(Boolean)
	# type: outcome of the cross enum


class Corner(Base):
    __tablename__ = 'corners'

    id = Column(primary_key=True)
    mins = Column(Integer)
    secs = Column(Integer)
    minsecs = Column(Integer)
    injurytime_play = Column(Boolean)
    start = Column(Geometry('POINT'))
    end = Column(Geometry('POINT'))
    player_id = Column(ForeignKey('players.id'), index=True)
    team_id = Column(ForeignKey('teams.id'), index=True)
    # type enum


class Dribble(Base):
	__tablename__ = 'dribbles'

	id = Column(primary_key=True)
	mins = Column(Integer)
	secs = Column(Integer)
	minsecs = Column(Integer)
	injurytime_play = Column(Boolean)
	loc = Column(Geometry('POINT'))
	player_id = Column(ForeignKey('players.id'), index=True)
	team_id = Column(ForeignKey('teams.id'), index=True)
	other_player_id = Column(ForeignKey('players.id'), index=True)
	other_team_id = Column(ForeignKey('teams.id'), index=True)
	
	# type: outcome of dribble enum
	# action_type: type of action [Attack, Defense]


