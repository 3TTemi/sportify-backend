import json

from db import Game
from db import User
from db import Ticket
from db import db

from flask import request
from flask import Flask

import os

app = Flask(__name__)
db_filename = "games.db" # Come back to

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_filename}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

db.init_app(app)
with app.app_context():
    db.drop_all()
    db.create_all()

# Generalized response formats
def success_response(data, code=200):
    return json.dumps(data), code

def failure_response(message, code=404):
    return json.dumps({"error":message}), code

# General Search Route
@app.route("/")
@app.route("/games/") # GET: Get all games
def base():
    """
    Endpoint that returns all the games stored in the database
    """
    games = [g.serialize() for g in Game.query.all()]
    return success_response({"games": games})

# Specified Search Route
@app.route("/games/<int:identifier>/") #TODO: Work on retrieving strings from urls
def get_game(identifier): # GET: Get all games that share a given quality (mens, womens, basketball, etc.) 
    """
    Endpoint that returns all the games that can be indentified by a given identifier
    """

    # Dictionary representing groups of possible identifiers client could use
    identities = {
        "sports": {"basketball", "baseball", "football", "soccer", "ice hockey", "tennis"},
        "sex": {"mens", "womens"}
    }
    
    group = None # Early declaration (scope conscious) 
    for id in identities:
        if id.get(identifier) is not None:
           group = id
           group = group.strip() # Removes the quotations of the key string
    
    game = Game.query.filter_by(group=identifier).first()
    if game is None:
        return failure_response("Game not found!")
    return success_response(game.serialize())