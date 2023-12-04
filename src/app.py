import json

from db import Game
from db import User
from db import Ticket
from db import School
from db import Player
import users_dao  


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
    db.drop_all()
    db.create_all()

# Generalized response formats
def success_response(data, code=200):
    return json.dumps(data), code

def failure_response(message, code=404):
    return json.dumps({"error":message}), code

# Dictionary representing groups of possible identifiers client could use
options = {
    "sport": {"Basketball", "Baseball", "Football", "Soccer", "Hockey", "Tennis"},
    "sex": {"Mens", "Womens", "unisex"},
    "location": {"Schoellkopf Field, Jessup field"}
}

@app.route("/")
@app.route("/games/") # GET: Get all games
def base():
    """
    Endpoint that returns all the games stored in the database
    """
    games = [g.serialize() for g in Game.query.all()]

    return success_response(games)

@app.route("/games/current/")
def returnCurrent():
    """
    Endpoint that returns all the games currently being played 
    """
    current_games = [g.serialize() for g in Game.query.filter(datetime.now() > Game.date_time).all()]
    return success_response(current_games)

@app.route("/games/future/")
def returnFuture():
    """
    Endpoint that returns all the games to be played in the future
    """
    upcoming_games = [g.serialize() for g in Game.query.filter(datetime.now() < Game.date_time).all()]
    return success_response(upcoming_games)


@app.route("/games/<int:game_id>/") # GET: Get game by id number
def get_specific_game(game_id):
    """
    Endpoint that returns the game with game id 'game_id'
    """
    game = Game.query.filter_by(id=game_id).first()
    if game is None:
        return failure_response("Game not found!")
    return success_response(game.serialize())


@app.route("/games/<string:identifier>/<string:time_state>/")
def get_game(identifier,time_state): # GET: Get all games that share a given quality (mens, womens, basketball, etc.) 
    """
    Endpoint that returns all the games that can be identified by a given identifier
    """ 
    group = None # Early declaration (scope conscious) 
    for id in options:
         for x in options[id]:
            if identifier == x:
                group = id
                group = group.strip() # Removes the quotations of the key string
    
    if time_state == "current":
        time_condition = datetime.now() > Game.date_time

    if time_state == "future":
        time_condition = datetime.now() < Game.date_time

    games = []
        # FIXME: Not efficient at all, there has to be a better way to do this
    if group == "sport":
        games = [g.serialize() for g in Game.query.filter_by(sport=identifier, sold_out=False).filter(time_condition).all()]
    if group == "location":
        games = [g.serialize() for g in Game.query.filter_by(location=identifier, sold_out=False).filter(time_condition).all()]
    if group == "sex":
        games = [g.serialize() for g in Game.query.filter_by(sex=identifier, sold_out=False).filter(time_condition).all()]


    # TODO: Implement games list for specific times/dates, for specific teams, and for those that still have remaining tickets 

    return success_response(games)

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


@app.route("/games/", methods=["DELETE"]) # DELETE: Delete a specific game from database
def delete_all_games():
    """
    Endpoint for deleting all gmaes
    """
    db.session.query(Game).delete()
    db.session.commit()
    return success_response([])

@app.route("/user/register/", methods=["POST"]) # POST: Insert user into database
def register_account():
    """
    Endpoint that allows client to create a user account (register)
    """
    body = json.loads(request.data)

    username = body.get("username")
    if username is None:
        return failure_response("You did not enter your username!")

    password = body.get("password")
    if password is None:
        return failure_response("You did not enter your password!")

    email = body.get("email")
    if email is None:
        return failure_response("You did not enter your email!")

    balance = body.get("balance", 0)

    created, user = users_dao.create_user(username,email,password)
    if not created:
        return failure_response("User already exists")

    return success_response({
        "session_token": user.session_token,
        "session_expiration": str(user.session_expiration),
        "refresh_token": user.refresh_token 
    })



def extract_token(request):
    """
    Helper function that extracts the token from the header of a request
    """
    auth_header = request.headers.get("Authorization")
    if auth_header is None:
        return False, failure_response("Missing Authorization Number")

    #Bearer <token>
    bearer_token = auth_header.replace("Bearer", "").strip()
    if not bearer_token:
        return False, failure_response("Missing Authorization Number")
    return True, bearer_token

@app.route("/session/", methods=["POST"])
def refresh_session():
    """
    Endpoint for updating a user's session
    """
    success, response = extract_token(request)
    if not success:
        return response  
    refresh_token = response

    try:
        user = users_dao.renew_session(refresh_token)
    except Exception as e:
        failure_response("Invalid Refresh Token")

    return success_response({
        "session_token": user.session_token,
        "session_expiration": str(user.session_expiration),
        "refresh_token": user.refresh_token 
    })


@app.route("/secret/", methods=["GET"])
def secret_message():
    """
    Endpoint for verifying a session token and returning a secret message

    In your project, you will use the same logic for any endpoint that needs 
    authentication
    """
    success, response = extract_token(request)
    if not success:
        return response  
    session_token = response
    user = users_dao.get_user_by_session_token()
    if not user or not user.verify_session_token(session_token):
        return failure_response("Invalid session token")

    return success_response(user.username)

@app.route("/user/login/", methods=["POST"])
def login():

    body = json.loads(request.data)

    password = body.get("password")
    if password is None:
        failure_response("You did not enter your password!")

    email = body.get("email")
    if email is None:
        failure_response("You did not enter your email!")

    success, user = users_dao.verify_credentials(email, password)
    if not success:
        failure_response("Invalid credentials")
    
    user.renew_session()
    db.session.commit()

    return success_response({
        "session_token": user.session_token,
        "session_expiration": str(user.session_expiration),
        "refresh_token": user.refresh_token 
    })

@app.route("/user/logout/", methods=["POST"])
def logout():
    success, response = extract_token(request)
    if not success:
        return response  
    session_token = response 

    user = users_dao.get_user_by_session_token(session_token)
    if not user or not user.verify_session_token(session_token):
        return failure_response("Invalid session token")
    user.session_expiration = datetime.now()
    db.session.commit()
    return success_response("You have been logged out")



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
        return failure_response("User not found!")

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
        return failure_response("User not found!")

    user.password = new_password
    db.session.commit()
    return success_response(new_password, 201)

@app.route("/user/<int:user_id>/funds/", methods=["POST"]) # POST: Update user funds
def update_funds(user_id):
    """
    Endpoint that increases or decreases the amount of funds a user client has on their account
    """
    update = request.data.get("balance")
    user = User.query.filter_by(id=user_id).first()
    if user is None: # If the user is not in the database
        return failure_response("User not found!")

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

    success, response = extract_token(request)
    if not success:
        return response  
    session_token = response

    ticket = None
    
    game = Game.query.filter_by(game_id).first()
    if game is None:
        return failure_response("User not found!")

    user = User.query.filter_by(user_id).first()
    if user is None: # Note: May not be necessary, as this endpoint would only be accessed from an existing user's page
        return failure_response("User not found!")

    if game.num_tickets == 0:
        return failure_response("Game Sold Out!")
    else:
        ticket = Ticket.query.filter_by(user_id = None).first()
        ticket_price = ticket.cost
        user_balance = user.balance

        if user_balance - ticket_price < 0:
            return failure_response("You do not have the funds to purchase this ticket!")
        
        else:
            user.balance = user_balance - ticket_price
            ticket.user_id = user.id
            game.num_tickets -= 1


    success, response = extract_token(request)
    if not success:
        return response  
    session_token = response
    user = users_dao.get_user_by_session_token()
    if not user or not user.verify_session_token(session_token):
        return failure_response("Invalid session token")

    return success_response(user.username)
            
    db.session.commit()
    return success_response(ticket.serialize(), 201)

@app.route("/schools/", methods=["POST"])
def create_school():
    """
    Endpoint that creates a inserts a school object into database
    """
    body = json.loads(request.data)

    name = body.get("name")
    if name is None:
        return failure_response("You did not enter the name of the school!")

    logo_image = body.get("logo_image")
    if logo_image is None:
        return failure_response("You did not neter a logo image for the school!")

    new_school = School(
        name=name,
        logo_image=logo_image,
    )

    db.session.add(new_school)
    db.session.commit()
    return success_response(new_school.serialize(), 201)


@app.route("/schools/<int:school_id>/") # GET: Get school by id number
def get_school(school_id):
    """
    Endpoint that returns the school with school id 'school_id'
    """
    school = School.query.filter_by(id=school_id).first()
    if school is None:
        return failure_response("School not found!")
    return success_response(school.serialize())

@app.route("/schools/<int:school_id>/", methods=["DELETE"]) 
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

@app.route("/schools/") 
def return_schools():
    """
    Endpoint that returns all the schools stored in the database
    """
    schools = [s.serialize() for s in School.query.all()]

    return success_response(schools)

@app.route("/players/", methods=["POST"])  
def create_player():
    """
    Endpoint for creating a new course
    """
    body = json.loads(request.data)
    name = body.get('name')
    age = body.get('age')
    picture = body.get('picture')
    bio = body.get('bio')

    if name is None:
        return failure_response("Not all player inputs given", 400)
    if age is None:
        return failure_response("Not all player inputs given", 400)
    if picture is None:
        return failure_response("Not all player inputs given", 400)
    if bio is None:
        return failure_response("Not all player inputs given", 400)
   

    new_player = Player(
        name=name,
        age=age,
        picture=picture,
        bio=bio
    )

    db.session.add(new_player)
    db.session.commit()
    return success_response(new_player.serialize(), 201)

@app.route("/players/")  
def get_players():
    """
    Endpoint for returning all players in datapase
    """
    players = [p.serialize() for p in Player.query.all()]

    return success_response(players)

@app.route("/players/home/<int:player_id>/<int:game_id>/", methods=["POST"])  
def add_home_player(player_id,game_id):
    """
    Endpoint for adding a player to a team roster in a game
    """

    game = Game.query.filter_by(id=game_id).first()
    if game is None:
        return failure_response("Game not found!")

    player = Player.query.filter_by(id=player_id).first()
    if player is None:
        return failure_response("Plauer not found!")

    game.home_roster.append(player)

    db.session.commit()


    return success_response([h.serialize() for h in game.home_roster], 201)

@app.route("/players/away/<int:player_id>/<int:game_id>/", methods=["POST"])  
def add_away_player(player_id,game_id):
    """
    Endpoint for adding a player to a team roster in a game
    """

    game = Game.query.filter_by(id=game_id).first()
    if game is None:
        return failure_response("Game not found!")

    player = Player.query.filter_by(id=player_id).first()
    if player is None:
        return failure_response("Plauer not found!")

    game.away_roster.append(player)

    db.session.commit()

    return success_response([a.serialize() for a in game.away_roster], 201)

@app.route("/players/", methods=["DELETE"]) 
def delete_all_players():
    """
    Endpoint for deleting all games
    """
    db.session.query(Player).delete()
    db.session.commit()
    return success_response([])


@app.route("/reset/", methods=["DELETE"])
def reset_database():
    db.drop_all()
    db.create_all()

    return success_response([])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)