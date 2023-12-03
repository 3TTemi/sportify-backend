from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.sql import func

db = SQLAlchemy()

game_user_association = db.Table("game_user_association", db.Model.metadata,
    db.Column("game_id", db.Integer, db.ForeignKey("game.id")),
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"))
    )

home_roster_association = db.Table('home_roster',
    db.Column('game_id', db.Integer, db.ForeignKey('game.id'), primary_key=True),
    db.Column('player_id', db.Integer, db.ForeignKey('player.id'), primary_key=True)
)

# Association table for away roster
away_roster_association = db.Table('away_roster',
    db.Column('game_id', db.Integer, db.ForeignKey('game.id'), primary_key=True),
    db.Column('player_id', db.Integer, db.ForeignKey('player.id'), primary_key=True)
)

class Game(db.Model):
    """
    Game Model 
    """
    _tablename__ = "game"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sport = db.Column(db.String, nullable=False)
    sex = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)
    date_time = db.Column(db.DateTime, nullable=False)

    home_team_id = db.Column(db.Integer, db.ForeignKey('school.id'), nullable=False)
    away_team_id = db.Column(db.Integer, db.ForeignKey('school.id'), nullable=False)

    home_team = db.relationship('School', foreign_keys=[home_team_id])
    away_team = db.relationship('School', foreign_keys=[away_team_id])

    num_tickets = db.Column(db.Integer, nullable=False) # Represents number of available tickets, not necessarily total tickets
    # ticket_price = db.Column(db.Integer, nullable = False)
    sold_out = db.Column(db.Boolean, nullable=False, default=False)
    tickets = db.relationship("Ticket", cascade="delete")

    home_roster = db.relationship('Player', secondary=home_roster_association)
    away_roster = db.relationship('Player', secondary=away_roster_association)

    # Link to the User table using association table 
    users_attending = db.relationship("User", secondary=game_user_association, back_populates="past_games")

    def __init__(self, **kwargs):
        """
        Initialize a Game Object 
        """
        self.sport = kwargs.get("sport")
        self.sex = kwargs.get("sex")
        self.date_time = kwargs.get("date_time")
        self.location =kwargs.get("location") # No need to include default value, throw error instead
        self.home_team = kwargs.get("home_team") # Leave Home Team Variable, just set default to cornell (Only Serialize away team)
        self.away_team = kwargs.get("away_team")
        self.num_tickets = kwargs.get("num_tickets") # When initializing a game, the amount of tickets remaining should never be 0 (there would be no attendees)


    def serialize(self):
        """
        Serialize Game Object
        """
        return {
            "id": self.id,
            "sport": self.sport,
            "sex": self.sex,
            # "date_time": self.date_time,
            # Converting date type object in database to stirng format to serialize 
            "date_time": self.date_time.strftime("%Y-%m-%dT%H:%M:%S") + 'Z',
            "location": self.location,
            # "home_team": self.home_team.serialize(),
            # "away_team": self.away_team.serialize(),
            "away_team_logo": self.away_team.logo_image,
            "away_team_name": self.away_team.name,
            "num_tickets": self.num_tickets,
            "tickets":  [t.serialize() for t in self.tickets],
            "users_attending":  [u.serialize() for u in self.users_attending],
            "home_roster": [h.serialize() for h in self.home_roster],
            "away_roster": [a.serialize() for a in self.away_roster]
        }

class User(db.Model):
    """
    User Model
    """
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    balance = db.Column(db.Integer, nullable=False)
    tickets = db.relationship("Ticket", cascade="delete")
    # Link to the Game table using assocaiton table 
    past_games = db.relationship("Game", secondary=game_user_association, back_populates="users_attending")

    def __init__(self, **kwargs):
        """
        Initialize a user object 
        """
        self.first_name = kwargs.get("first_name")
        self.last_name = kwargs.get("last_name")
        self.username = kwargs.get("username", "")
        self.password = kwargs.get("password")
        self.email = kwargs.get("email", "")
        self.balance = kwargs.get("balance", 0)

    def serialize(self):
        """
        Serliaze a user object without the courses field
        """
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "username": self.username,
            "email": self.email,
            # We do not return password for security purposes
            "balance": self.balance
        }


class Ticket(db.Model):
    """
    Ticket Model
    """
    __tablename__ = "ticket"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cost = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    game_id = db.Column(db.Integer, db.ForeignKey("game.id"), nullable=False)

    def __init__(self, **kwargs):
        """
        Initialize a Ticket object 
        """
        self.user_id = kwargs.get("user_id", None)
        self.game_id = kwargs.get("game_id")
        self.cost = kwargs.get("cost")

    def serialize(self):
        """
        Serliaze a ticket object (
        """
        return {
            "id": self.id,
            "cost": self.cost,
            "user_id": self.user_id,
            "game_id": self.game_id
        }

class Transactions(db.Model):
    """
    Transaction Model
    """
    __tablename__ = "ticket"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    timestamp = db.Column(db.DateTime(timezome=True), server_default=func.now())
    user_id = db.Column(db.Integer, nullable=False),
    game_id = db.Column(db.Integer, nullable=False),
    amount = db.Column(db.Integer, nullable=False)

    def __init__(self, **kwargs):
        """
        Initialize a Transaction object 
        """
        self.user_id = kwargs.get("user_id")
        self.game_id = kwargs.get("game_id")
        self.amount = kwargs.get("amount")

    def serialize(self):
        """
        Serialize a transaction object
        """
        user = User.query.filter_by(id=self.user_id).first()

        return {
            "id": self.id,
            "amount": self.amount,
            "user_id": self.user_id,
            "user_firstname": user.first_name,
            "user_lastname": user.last_name,
            "timestamp": self.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            "game_id": self.game_id
        }

class School(db.Model):
    __tablename__ = "school"
    # Id's of schools will be fixed in database, creation of game only needs ids
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    logo_image = db.Column(db.String, nullable=False)

    home_games = db.relationship('Game', foreign_keys='[Game.home_team_id]')
    away_games = db.relationship('Game', foreign_keys='[Game.away_team_id]')
    # home_games = db.relationship('Game', backref='home_team', foreign_keys='[Game.home_team_id]')


    def __init__(self, **kwargs):
        """
        Initialize a school object 
        """
        self.name = kwargs.get("name")
        self.logo_image = kwargs.get("logo_image")

    def serialize(self):
        """
        Serliaze a school object (
        """
        return {
            "id": self.id,
            "name": self.name,
            "logo_image": self.logo_image
        }


class Player(db.Model):
    __tablename__ = "player"
    # Id's of schools will be fixed in database, creation of game only needs ids
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.String, nullable=False)
    picture = db.Column(db.String, nullable=False)
    bio = db.Column(db.String, nullable=False)

    def __init__(self, **kwargs):
        """
        Initialize a school object 
        """
        self.name = kwargs.get("name")
        self.age = kwargs.get("age")
        self.picture = kwargs.get("picture")
        self.bio = kwargs.get("bio")


    def serialize(self):
        """
        Serliaze a school object (
        """
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "picture": self.picture,
            "bio": self.bio
        }
