import json

from db import Game
from db import User
from db import Ticket
from db import db

from flask import request
from flask import Flask
from flask import Flask
from datetime import datetime 


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


@app.route("/games/<int:game_id>/")
def get_specific_game(game_id):
    """
    Endpoint that returns the game with game id 'game_id'
    """
    game = Game.query.filter_by(id=game_id).first()
    if game is None:
        return failure_response("Game not found!")
    return success_response(game.serialize())


# # Specified Search Route
# @app.route("/games/<int:identifier>/") #TODO: Work on retrieving strings from urls
# def get_game(identifier): # GET: Get all games that share a given quality (mens, womens, basketball, etc.) 
#     """
#     Endpoint that returns all the games that can be indentified by a given identifier
#     """

#     # Dictionary representing groups of possible identifiers client could use
#     identities = {
#         "sports": {"basketball", "baseball", "football", "soccer", "ice hockey", "tennis"},
#         "sex": {"mens", "womens"}
#     }
    
#     group = None # Early declaration (scope conscious) 
#     for id in identities:
#         if id.get(identifier) is not None:
#            group = id
#            group = group.strip() # Removes the quotations of the key string
    
#     game = Game.query.filter_by(group=identifier).first()
#     if game is None:
#         return failure_response("Game not found!")
#     return success_response(game.serialize())

@app.route("/games/", methods=["POST"]) # POST: Insert game into database
def create_game():
    """
    Endpoint that inserts a new game into the database
    """
    body = json.loads(request.data)
    
    # Checks the request body for the sport of this game 
    sport = body.get("sport")
    if sport is None:
        failure_response("You did not enter the game's sport!", 400)

    # Checks the request body for the competing sexes of this game 
    sex = body.get("sex")
    if sex is None:
        failure_response("You did not enter the relevant sexes!", 400)

    date_time = datetime.strptime(body.get('date_time'), '%Y-%m-%d %H:%M:%S')
    if date_time is None: 
        failure_response("You did not enter a date for the game!", 400)


    # Checks the request body for the location of this game 
    location = body.get("location")
    if location is None:
        failure_response("You did not enter a location!", 400)

    # Checks the request body for the competing teams of this game 
    teams = body.get("teams")
    if teams is None:
        failure_response("You did not enter the competing teams!", 400)

    # Checks the request body for the number of tickets available for this game 
    num_tickets = body.get("num_tickets")
    if num_tickets is None:
        failure_response("You did not enter the amount of available tickets!", 400)

    # Creates Game object
    new_game = Game(
        sport=sport,
        sex=sex,
        date_time = date_time,
        location=location,
        teams=teams,
        num_tickets=num_tickets
    )

    # Adds and fixes new Game object into database
    db.session.add(new_game)
    db.session.commit()
    return success_response(new_game.serialize(), 201)

@app.route("/games/<int:game_id>/", methods=["DELETE"])
def delete_game(game_id):
    """
    Endpoint for deleting a game by id
    """
    game = Game.query.filter_by(id=game_id).first()
    if game is None:
        return failure_response("Game not found!")
    db.session.delete(game)
    db.session.commit()
    return success_response(game.serialize())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)