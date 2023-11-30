from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

game_user_association = db.Table("game_user_association", db.Model.metadata,
    db.Column("game_id", db.Integer, db.ForeignKey("game.id")),
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"))
    )

class Game(db.Model):
    """
    Game Model 
    """
    _tablename__ = "game"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sport = db.Column(db.String, nullable=False)
    sex = db.Column(db.String, nullable=False)
    #date_time = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.Stirng, nullable=False)
    """
    PickleType allows us to use tuple as dattpe (automatically serializes and deserializaes for databse) 
    """
    teams = db.Column(db.PickleType)
    num_tickets = db.Column(db.Integer, nullable=False)
    tickets = db.relationship("Ticket", cascade="delete")
    # Link to the User tbale using association table 
    users_attending = db.relationship("User", secondary=game_user_association, back_populates="past_games")


    def __init__(self, **kwargs):
        """
        Initialize a Game Object 
        """
        self.sport = kwargs.get("sport", "")
        self.sex = kwargs.get("sex", "")
        #self.date_time = kwargs.get("date_time", "")
        self.location =kwargs.get("location", "")
        self.teams =kwargs.get("date_time", ("",""))
        self.num_tickets = kwargs.get("num_tickets", 0)

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    balance = db.Column(db.Integer, nullable=False)
    tickets = db.relationship("Ticket", cascade="delete")
    # Link to the Game table using assocaiton table 
    past_games = db.relationship("Game", secondary=game_user_association, back_populates="users_attending")

    def __init__(self, **kwargs):
        """
        Initialize a user object 
        """
        self.username = kwargs.get("username", "")
        self.email = kwargs.get("email", "")
        self.balance = kwargs.get("balance", 0)


class Ticket(db.Model):
    __tablename__ = "ticket"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey("game.id"), nullable=False)

    def __init__(self, **kwargs):
        """
        Initialize a Ticket object 
        """
        self.user_id = kwargs.get("user_id")
        self.game_id = kwargs.get("game_id")

"""
Test code
"""