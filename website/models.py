"""
Create SQLAlchemy database models
"""
from flask_login import UserMixin
from sqlalchemy import func
from .setup_db import db

match_team = db.Table('match_team',
    db.Column('match_id', db.Integer, db.ForeignKey('match.id'), primary_key=True),
    db.Column('team_id', db.Integer, db.ForeignKey('team.id'), primary_key=True)
)

competition_team = db.Table('competition_team',
    db.Column('competition_id', db.Integer, db.ForeignKey('competition.id'), primary_key=True),
    db.Column('team_id', db.Integer, db.ForeignKey('team.id'), primary_key=True)
)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True)
    password = db.Column(db.String(128))
    balance = db.Column(db.Float, default=0.0)

    bets = db.relationship('Bet', backref='user')
    transactions = db.relationship('Transaction', backref='user')
    user_numbers = db.relationship('UserNumbers', backref='user', cascade='all, delete-orphan') 

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    type = db.Column(db.String(10), nullable=False) 
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __init__(self, amount, type, user_id):
        self.amount = amount
        self.type = type
        self.user_id = user_id

class Bet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    money_placed = db.Column(db.Float)
    status = db.Column(db.String(16))
    odd = db.Column(db.Float, default=1.0)
    win_amount = db.Column(db.Float)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_won = db.Column(db.Boolean, default=None)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    bet_matches = db.relationship('BetMatch', backref='bet', cascade='all, delete-orphan')

class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    utc_date = db.Column(db.String(24), nullable=False)
    status = db.Column(db.String(20))
    stage = db.Column(db.String(50))
    group = db.Column(db.String(50))
    winner = db.Column(db.String(10))
    duration = db.Column(db.String(20))
    full_time_home = db.Column(db.Integer)
    full_time_away = db.Column(db.Integer)
    half_time_home = db.Column(db.Integer)
    half_time_away = db.Column(db.Integer)

    home_win_odd = db.Column(db.Float)
    away_win_odd = db.Column(db.Float)
    draw_odd = db.Column(db.Float)

    competition_id = db.Column(db.Integer, db.ForeignKey('competition.id'))
    teams = db.relationship('Team', secondary=match_team, backref='matches')
    bet_match = db.relationship('BetMatch', backref='match', uselist=False)

class BetMatch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bet_id = db.Column(db.Integer, db.ForeignKey('bet.id'))
    match_id = db.Column(db.Integer, db.ForeignKey('match.id'))
    home_team = db.Column(db.String(50))
    away_team = db.Column(db.String(50))
    winner = db.Column(db.String())
    odd = db.Column(db.Float, nullable=False)

class Area(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    code = db.Column(db.String(10))
    flag = db.Column(db.String(255))

    competitions = db.relationship('Competition', backref='area')

    def __init__(self, id: int, name: str, code: str, flag: str):
        self.id = id
        self.name = name
        self.code = code
        self.flag = flag

class Competition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    code = db.Column(db.String(10))
    type = db.Column(db.String(20))
    emblem = db.Column(db.String(255))

    area_id = db.Column(db.Integer, db.ForeignKey('area.id'))
    matches = db.relationship('Match', backref='competition')
    teams = db.relationship('Team', secondary=competition_team, backref='competitions')

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    short_name = db.Column(db.String(50))
    tla = db.Column(db.String(10))
    crest = db.Column(db.String(255))


class LotteryNumbers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numbers = db.Column(db.String, nullable=False) 

    def __init__(self, numbers):
        self.numbers = ','.join(map(str, numbers))

    def get_numbers(self):
        return list(map(int, self.numbers.split(',')))
    
class UserNumbers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numbers = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  

    def __init__(self, numbers, user_id):
        self.numbers = ','.join(map(str, numbers))
        self.user_id = user_id

    def get_numbers(self):
        return list(map(int, self.numbers.split(',')))
