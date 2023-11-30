import json

from db import Game
from db import User
from db import Ticket
from db import db

from flask import request
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

@app.route("/")
 # GET: Get all games
@app.route("/games/")
def base():
    """
    Endpoint that returns all the games stored in the database
    """
    games = [g.serialize() for g in Game.query.all()]
    return success_response({"games": games})


@app.route("/games/<int:game_id>/")
def get_game(game_id):
    """
    Endpoint that returns the game with game id 'game_id'
    """
    game = Game.query.filter_by(id=game_id).first()
    if game is None:
        return failure_response("Game not found!")
    return success_response(game.serialize())


@app.route("/games/", methods=["POST"])  
def create_game():
    """
    Endpoint for creating a new game
    """
    body = json.loads(request.data)
    sport = body.get('sport')
    gender = body.get('gender')
    # Converting String from JSON into python date time object 
    date_time = datetime.strptime(body.get('date_time'), '%Y-%m-%d %H:%M:%S')
    location = body.get('location')
    teams = body.get('teams')
    num_tickets = body.get('num_tickets')

    new_game = Game(
        sport=sport,
        gender=gender,
        date_time = date_time,
        location = location,
        teams = teams,
        num_tickets = num_tickets
    )

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