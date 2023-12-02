import json

from db import Game
from db import User
from db import Ticket
from db import School

from db import db

from flask import request
from flask import Flask

from datetime import datetime 

import users_dao
import os

app = Flask(__name__)
db_filename = "games.db" # Come back to

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_filename}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

db.init_app(app)
with app.app_context():
    db.create_all()

# Generalized response formats
def success_response(data, code=200):
    return json.dumps(data), code

def failure_response(message, code=404):
    return json.dumps({"error":message}), code

# Dictionary representing groups of possible identifiers client could use
options = {
    "sport": {"basketball", "baseball", "football", "soccer", "ice hockey", "tennis"},
    "sex": {"mens", "womens", "unisex"},
    "location": {"Schoellkopf Field, Jessup field"}
}

@app.route("/")
@app.route("/games/") # GET: Get all games
def base():
    """
    Endpoint that returns all the games stored in the database
    """
    games = [g.serialize() for g in Game.query.all()]

    # Filter by current time is greater than time of the object
    # current_games = [g.serialize() for g in Game.query.filter(datetime.datetime.now() > g.date_time).all()]
    # upcoming_games = [g.serialize() for g in Game.query.filter(datetime.datetime.now() < g.date_time).all()]

    return success_response({"games": games})
    # return success_response({"games": current_games})

@app.route("/games/<int:game_id>/") # GET: Get game by id number
def get_specific_game(game_id):
    """
    Endpoint that returns the game with game id 'game_id'
    """
    game = Game.query.filter_by(id=game_id).first()
    if game is None:
        return failure_response("Game not found!")
    return success_response(game.serialize())

@app.route("/games/<string:identifier>/")
def get_game(identifier): # GET: Get all games that share a given quality (mens, womens, basketball, etc.) 
    """
    Endpoint that returns all the games that can be identified by a given identifier
    """ 
    group = None # Early declaration (scope conscious) 
    for id in options:
         for x in options[id]:
            if identifier == x:
                group = id
                group = group.strip() # Removes the quotations of the key string
    
    # FIXME: Not efficient at all, there has to be a better way to do this
    if group == "sport":
        games = [g.serialize() for g in Game.query.filter_by(sport=identifier, sold_out=False).all()]
    if group == "location":
        games = [g.serialize() for g in Game.query.filter_by(location=identifier, sold_out=False).all()]
    if group == "sex":
        games = [g.serialize() for g in Game.query.filter_by(sex=identifier, sold_out=False).all()]
    
    # TODO: Implement games list for specific times/dates, for specific teams, and for those that still have remaining tickets 

    return success_response({f"{identifier} games":games})

# Be able to choose between mens and womens 

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


    home_team_id = body.get("home_team")
    if home_team_id is None:
        failure_response("You did not enter the away team!", 400)

    # Checks the request body for the away team of this game 
    away_team_id = body.get("away_team")
    if away_team_id is None:
        failure_response("You did not enter the away team!", 400)

    # Checks the request body for the number of tickets available for this game 
    num_tickets = body.get("num_tickets")
    if num_tickets is None:
        failure_response("You did not enter the amount of available tickets!", 400)

    ticket_price = body.get("ticket_price", 0)

    home_team = School.query.get(home_team_id)
    if home_team is None:
        failure_response("Teams inputted Incorrectly!", 400)
    away_team = School.query.get(away_team_id)
    if away_team_id is None:
        failure_response("Teams inputted Incorrectly!", 400)

    # Creates Game object
    new_game = Game(
        sport=sport,
        sex=sex,
        date_time = date_time,
        location=location,
        home_team=home_team,
        away_team=away_team,
        num_tickets=num_tickets # Note: Represents number of available tickets, not necessarily number of total tickets 
    )

    # for x in range(num_tickets):
    #     ticket = Ticket(
    #         cost=ticket_price,
    #         game_id=new_game.id
    #     )
    #     db.session.add(ticket)

    # Adds and fixes new Game object into database
    db.session.add(new_game)
    db.session.commit()
    return success_response(new_game.serialize(), 201)

@app.route("/games/<int:game_id>/", methods=["POST"]) # POST: Update a game's information
def update_game(game_id):
    """
    Endpoint that updates the information of an existing game with game id 'identifier'
    """
    game = Game.query.filter_by(id=game_id).first()
    if game is None:
        return failure_response("Game not found!")
    
    body = json.loads(request.data)

    # Checks the request body for the sport of this game 
    sport = body.get("sport")
    if sport is None:
        failure_response("You did not enter the game's sport!", 400)

    # Checks the request body for the competing sexes of this game 
    sex = body.get("sex")
    if sex is None:
        failure_response("You did not enter the relevant sexes!", 400)

    # Checks the request body for the location of this game 
    location = body.get("location")
    if location is None:
        failure_response("You did not enter a location!", 400)

    # Checks the request body for the competing teams of this game 
    away_team = body.get("away_team")
    if teams is None:
        failure_response("You did not enter the competing teams!", 400)

    # Checks the request body for the number of tickets available for this game 
    num_tickets = body.get("num_tickets")
    if num_tickets is None:
        failure_response("You did not enter the amount of available tickets!", 400)

    # Update the values of the object with the request data
    game.sport = sport
    game.sex = sex
    game.location = location
    game.away_team = away_team
    game.num_tickets = num_tickets

    db.session.commit()
    return json.dumps(game.serialize(), 201)

@app.route("/games/<int:game_id>/", methods=["DELETE"]) # DELETE: Delete a specific game from database
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

@app.route("/user/signup/", methods=["POST"]) # POST: Insert user into database
def create_user():
    """
    Endpoint that allows client to create a user account
    """
    body = json.loads(request.data)

    first_name = body.get("first_name")
    if first_name is None:
        failure_response("You did not enter your first name!")

    last_name = body.get("last_name")
    if last_name is None:
        failure_response("You did not enter your last name!")

    username = body.get("username")
    if username is None:
        failure_response("You did not enter your username!")

    password = body.get("password")
    if password is None:
        failure_response("You did not enter your password!")

    email = body.get("email")
    if email is None:
        failure_response("You did not enter your email!")

    balance = body.get("balance", 0)

    user = User(
        first_name=first_name,
        last_name=last_name,
        username=username,
        password=password,
        email=email,
        balance=balance
    )

    db.session.add(user)
    db.session.commit()

    return success_response(user.serialize(), 201)

@app.route("/user/login/", methods=["POST"])
def login():
    pass

@app.route("/user/logout/", methods=["POST"])
def logout():
    pass

@app.route("/user/<int:user_id>") # GET: Get specific user by user id
def get_user(user_id):
    """
    Endpoint that returns user with user id 'user_id'
    """
    user = User.query.filter_by(id=user_id).first()
    if user is None: # If the user is not in the database
        failure_response("User not found!")

    return success_response({"user":user.serialize()})

@app.route("/user/<int:user_id>/username/", methods=["POST"]) # POST: Update user username
def update_username(user_id):
    """
    Endpoint that changes an existing user's usersname and returns updated user information 
    """ 
    new_username = request.data.get("username")

    user = User.query.filter_by(id=user_id).first()
    if user is None: # If the user is not in the database
        failure_response("User not found!")

    user.username = new_username
    db.session.commit()
    return success_response(new_username, 201)

@app.route("/user/<int:user_id>/password/", methods=["POST"]) # POST: Update user password
def update_password(user_id):
    """
    Endpoint that changes an existing user's usersname and returns updated user information 
    """ 
    new_password = request.data.get("password")

    user = User.query.filter_by(id=user_id).first()
    if user is None: # If the user is not in the database
        failure_response("User not found!")

    user.password = new_password
    db.session.commit()
    return success_responses(new_password, 201)

@app.route("/user/<int:user_id>/funds/", methods=["POST"]) # POST: Update user funds
def update_funds(user_id):
    """
    Endpoint that increases or decreases the amount of funds a user client has on their account
    """
    update = request.data.get("balance")
    user = User.query.filter_by(id=user_id).first()
    if user is None: # If the user is not in the database
        failure_response("User not found!")

    new_balance = user.balance + update
    user.balance = new_balance
    db.session.commit()
    return success_response(new_balance, 201)

@app.route("/user/<int:user_id>/tickets/", methods=["POST"]) # POST: Purchase tickets
def purchase_tickets(user_id):
    """
    Endpoint that enables client to purchase tickets
    """
    body = request.data
    game_id = body.get("game_id")
    ticket = None
    
    game = Game.query.filter_by(game_id).first()
    if game is None:
        failure_response("User not found!")

    user = User.query.filter_by(user_id).first()
    if user is None: # Note: May not be necessary, as this endpoint would only be accessed from an existing user's page
        failure_response("User not found!")

    if game.num_tickets == 0:
        failure_response("Game Sold Out!")
    else:
        ticket = Ticket.query.filter_by(user_id = None).first()
        ticket_price = ticket.cost
        user_balance = user.balance

        if user_balance - ticket_price < 0:
            failure_response("You do not have the funds to purchase this ticket!")
        
        else:
            user.balance = user_balance - ticket_price
            ticket.user_id = user.id
            game.num_tickets -= 1
            
    db.session.commit()
    return success_response(ticket.serialize(), 201)

@app.route("/school/", methods=["POST"])
def create_school():
    """
    Endpoint that creates a inserts a school object into database
    """
    body = json.loads(request.data)

    name = body.get("name")
    if name is None:
        failure_response("You did not enter the name of the school!")

    logo_image = body.get("logo_image")
    if logo_image is None:
        failure_response("You did not neter a logo image for the school!")

    new_school = School(
        name=name,
        logo_image=logo_image,
    )

    db.session.add(new_school)
    db.session.commit()
    return success_response(new_school.serialize(), 201)


@app.route("/school/<int:school_id>/") # GET: Get school by id number
def get_school(school_id):
    """
    Endpoint that returns the school with school id 'school_id'
    """
    school = School.query.filter_by(id=school_id).first()
    if school is None:
        return failure_response("School not found!")
    return success_response(school.serialize())

@app.route("/school/<int:school_id>/", methods=["DELETE"]) 
def delete_school(school_id):
    """
    Endpoint for deleting a game by id
    """
    school = School.query.filter_by(id=school_id).first()
    if school is None:
        return failure_response("School not found!")
    db.session.delete(school)
    db.session.commit()
    return success_response(school.serialize())

@app.route("/school/") 
def return_schools():
    """
    Endpoint that returns all the schools stored in the database
    """
    schools = [s.serialize() for s in School.query.all()]

    return success_response({"schools": schools})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)