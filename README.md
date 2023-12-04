# [Cornell AppDev Hack Challenge Project: _Sportify_](https://github.com/3TTemi/sportify-backend)

#### By: [Chimdi](https://github.com/cejiogu) and [Temi Adebowale](https://github.com/3TTemi)

## Introduction
Welcome to _Sportify_, your go-to app for staying updated on upcoming and current sports matches hosted by Cornell University! Whether you're a passionate Cornell student hoping to support school spirit or just someone who loves the thrill of Cornell sports, this app is designed to keep you in the loop. 

## Description

_Sportify_ is an API that allows its clients to:
-  Access a database storing Cornell University's home games, in which the client can view all current and future games or modify their search by selecting qualities that specific games might have in common (referred to as _identifiers_)
- Register, Login, and Login into an account using an inputted email and password
- Edit the Configuration of the Account (Adding Funds, Changing Username)
- Purchase tickets for one or more games

Data Models:
- Game Model, representing a sports match betweeen two universities
- User Model, represening a user to login and view the available games
- Ticket Model, representing a ticket to that is bought by a user for a specific sports game 
- School Model, representing a university instituion that is participating in sports games 
- Player Model, representing students that are apart of univierites sports roster

Model Relationships:
- Many-to-Many Relationship of Users and Games (Attending Users)
- Many-to-Many Relationship ofGames and Players (Home Roster and Away Roster)
- One-to-Many Relationship ofUser and Tickets
- One-to-Many Relationship Game and Tickets
- One-to-Many Relationship School and Games (Home and Away Games)

## How to Use 
### GET: Get all games  `/games/`
#### Response:
```json
<HTTP STATUS CODE 200>

[
        {
            "id": <GAME ID>,
            "sport": <SPORT OF GAME>,
            "sex": <SEX OF GAME>,
            "date-time": <DATE-TIME OF GAME>,
            "location": <LOCATION OF GAME>,
            "away_team_logo": <LOGO OF AWAY TEAM OF GAME>,
            "away_team_name": <NAME OF AWAY TEAM OF GAME>,
            "num_tickets": <NUMBER OF TICKET REMAINING FOR GAME>,
            "tickets": [<SERIALIZED TICKET>, ...],
            "users_attending": [<SERIALIZED USER>, ...],
            "home_roster": [<SERIALIZED PLayer>, ...],
            "away_roster": [<SERIALIZED PLayer>, ...]
        },
        // Other Games Here 
        {},{},{}
]

```

### GET: Get all current games `/games/current/`
```json
<HTTP STATUS CODE 200>
[
        {
            "id": <GAME ID>,
            "sport": <SPORT OF GAME>,
            "sex": <SEX OF GAME>,
            "date-time": <DATE-TIME OF GAME>,
            "location": <LOCATION OF GAME>,
            "away_team_logo": <LOGO OF AWAY TEAM OF GAME>,
            "away_team_name": <NAME OF AWAY TEAM OF GAME>,
            "num_tickets": <NUMBER OF TICKET REMAINING FOR GAME>,
            "tickets": [<SERIALIZED TICKET>, ...],
            "users_attending": [<SERIALIZED USER>, ...],
            "home_roster": [<SERIALIZED PLayer>, ...],
            "away_roster": [<SERIALIZED PLayer>, ...]
        },
        // Other Games Here 
        {},{},{}
]
```

### GET: Get all future games `/games/future/`
```json
<HTTP STATUS CODE 200>
[
        {
            "id": <GAME ID>,
            "sport": <SPORT OF GAME>,
            "sex": <SEX OF GAME>,
            "date-time": <DATE-TIME OF GAME>,
            "location": <LOCATION OF GAME>,
            "away_team_logo": <LOGO OF AWAY TEAM OF GAME>,
            "away_team_name": <NAME OF AWAY TEAM OF GAME>,
            "num_tickets": <NUMBER OF TICKET REMAINING FOR GAME>,
            "tickets": [<SERIALIZED TICKET>, ...],
            "users_attending": [<SERIALIZED USER>, ...],
            "home_roster": [<SERIALIZED PLayer>, ...],
            "away_roster": [<SERIALIZED PLayer>, ...]
        },
        // Other Games Here 
        {},{},{}
]

```

### GET: Get game by id number `/games/{game id}}/`
```json
<HTTP STATUS CODE 200>

{
    "id": <GAME ID>,
    "sport": <SPORT OF GAME>,
    "sex": <SEX OF GAME>,
    "date-time": <DATE-TIME OF GAME>,
    "location": <LOCATION OF GAME>,
    "away_team_logo": <LOGO OF AWAY TEAM OF GAME>,
    "away_team_name": <NAME OF AWAY TEAM OF GAME>,
    "num_tickets": <NUMBER OF TICKET REMAINING FOR GAME>,
    "tickets": [<SERIALIZED TICKET>, ...],
    "users_attending": [<SERIALIZED USER>, ...],
    "home_roster": [<SERIALIZED PLayer>, ...],
    "away_roster": [<SERIALIZED PLayer>, ...]
}
 
```

### GET: Get all games by identifier `/games/{identifier}/`
```json
<HTTP STATUS CODE 200>

[
        {
            "id": <GAME ID>,
            "sport": <SPORT OF GAME>,
            "sex": <SEX OF GAME>,
            "date-time": <DATE-TIME OF GAME>,
            "location": <LOCATION OF GAME>,
            "away_team_logo": <LOGO OF AWAY TEAM OF GAME>,
            "away_team_name": <NAME OF AWAY TEAM OF GAME>,
            "num_tickets": <NUMBER OF TICKET REMAINING FOR GAME>,
            "tickets": [<SERIALIZED TICKET>, ...],
            "users_attending": [<SERIALIZED USER>, ...]
        },
        // Other Games Here 
        {},{},{}
]
````

### POST: Insert game into database `/games/`
```json
<HTTP STATUS CODE 201>

{
    "id": <GAME ID>,
    "sport": <SPORT OF GAME>,
    "sex": <SEX OF GAME>,,
    "date_time": <DATE-TIME OF GAME>,
    "location": <LOCATION OF GAME>,
    "away_team_logo": <LOGO OF AWAY TEAM OF GAME>,
    "away_team_name": <NAME OF AWAY TEAM OF GAME>,
    "num_tickets": <NUMBER OF TICKET REMAINING FOR GAME>,
    "tickets": [<SERIALIZED TICKET>, ...],
    "users_attending": [<SERIALIZED USER>, ...],
    "home_roster": [<SERIALIZED PLayer>, ...],
    "away_roster": [<SERIALIZED PLayer>, ...]
}
    

```

### POST: Update a game's information with new variables `/games/{game id}/`
```json
<HTTP STATUS CODE 201>

{
    "id": <GAME ID>,
    "sport": <SPORT OF GAME>,
    "sex": <SEX OF GAME>,,
    "date_time": <DATE-TIME OF GAME>,
    "location": <LOCATION OF GAME>,
    "away_team_logo": <LOGO OF AWAY TEAM OF GAME>,
    "away_team_name": <NAME OF AWAY TEAM OF GAME>,
    "num_tickets": <NUMBER OF TICKET REMAINING FOR GAME>,
    "tickets": [<SERIALIZED TICKET>, ...],
    "users_attending": [<SERIALIZED USER>, ...],
    "home_roster": [<SERIALIZED PLayer>, ...],
    "away_roster": [<SERIALIZED PLayer>, ...]
}

```

### DELETE: Delete a specific game from database `/games/{game id}/`
```json
<HTTP STATUS CODE 200>

{
    "id": <GAME ID>,
    "sport": <SPORT OF GAME>,
    "sex": <SEX OF GAME>,,
    "date_time": <DATE-TIME OF GAME>,
    "location": <LOCATION OF GAME>,
    "away_team_logo": <LOGO OF AWAY TEAM OF GAME>,
    "away_team_name": <NAME OF AWAY TEAM OF GAME>,
    "num_tickets": <NUMBER OF TICKET REMAINING FOR GAME>,
    "tickets": [<SERIALIZED TICKET>, ...],
    "users_attending": [<SERIALIZED USER>, ...],
    "home_roster": [<SERIALIZED PLayer>, ...],
    "away_roster": [<SERIALIZED PLayer>, ...]
} 



```

### DELETE: Delete all games from database `/games/`
```json
<HTTP STATUS CODE 200>
[
    {
        "id": <GAME ID>,
        "sport": <SPORT OF GAME>,
        "sex": <SEX OF GAME>,,
        "date_time": <DATE-TIME OF GAME>,
        "location": <LOCATION OF GAME>,
        "away_team_logo": <LOGO OF AWAY TEAM OF GAME>,
        "away_team_name": <NAME OF AWAY TEAM OF GAME>,
        "num_tickets": <NUMBER OF TICKET REMAINING FOR GAME>,
        "tickets": [<SERIALIZED TICKET>, ...],
        "users_attending": [<SERIALIZED USER>, ...],
        "home_roster": [<SERIALIZED PLayer>, ...],
        "away_roster": [<SERIALIZED PLayer>, ...]
    } 
    // Other Games Here 
     {},{},{}

]

```

### POST: Register user into database `/user/register/`
```json
<HTTP STATUS CODE 201>
{
    "session_token": <USER SESSION TOKEN>,
    "session_expiration": <DATE OF USER SESSION EXPIRATION>,
    "refresh_token": <USER REFRESH TOKEN> 
}
```

### POST: Refresh user's session token `/session/`
```json
<HTTP STATUS CODE 200>
{       
    "session_token": <USER SESSION TOKEN>,
    "session_expiration": <DATE OF USER SESSION EXPIRATION>,
    "refresh_token": <USER REFRESH TOKEN> 
}
```

### POST: Login user `/user/login/`
```json
<HTTP STATUS CODE 200>
{
    "session_token": <USER SESSION TOKEN>,
    "session_expiration": <DATE OF USER SESSION EXPIRATION>,
    "refresh_token": <USER REFRESH TOKEN> 
}
```


### POST: Logout user `/user/logout/`
```json
<HTTP STATUS CODE 200>
"You have been logged out"
```

### GET: Get user by user id `/user/{user id}/`
```json
<HTTP STATUS CODE 200>
{
    "id": <USER ID>,
    "username": <USER USERNAME>,
    "email": <USER EMAIL>,
    "balance": <USER BALANCE>
}
```

### POST: Update user username `user/{user id}/username/`
```json
<HTTP STATUS CODE 201>
<USER UPDATED USERNAME> 
```

### POST: Update funds on user's account `/user/{user id}/funds/`
```json
<HTTP STATUS CODE 201>
<USER UPDATED BALANCE>
```

### POST: Purchase tickets and add to respective tables `/user/{user id}/tickets/`
```json
<HTTP STATUS CODE 201>
{
    "id": <TICKKET ID>,
    "cost": <TICKET COST>,
    "user_id": <ID OF USER WHO PURCHASED TICKET>,
    "game_id": <ID OF GAME TICKET IS ASSOCIATED WITH>
}
```

### POST: Add school to database `/schools/`
```json
<HTTP STATUS CODE 201>
{
    "id": <SCHOOL ID>,
    "name": <SCHOOL NAME>,
    "logo_image": <SCHOOL SPORTS LOGO>
}
```

### GET: Get school by school id `/schools/{school id}`
```json
<HTTP STATUS CODE 200>
{
    "id": <SCHOOL ID>,
    "name": <SCHOOL NAME>,
    "logo_image": <SCHOOL SPORTS LOGO>
}
```

### DELETE: Remove school from database `/schools/{school id}/`
```json
<HTTP STATUS CODE 200>
{
    "id": <SCHOOL ID>,
    "name": <SCHOOL NAME>,
    "logo_image": <SCHOOL SPORTS LOGO>
}
```

### GET: Get all schools `/schools/`
```json
<HTTP STATUS CODE 200>

[
    {
    "id": <SCHOOL ID>,
    "name": <SCHOOL NAME>,
    "logo_image": <SCHOOL SPORTS LOGO>
    },
    // Other Schools
     {},{},{}
]

```


### POST: Add player to database `/players/`
```json
<HTTP STATUS CODE 201>
{
    "id": <PLAYER ID>,
    "name": <PLAYER NAME>,
    "age": <PLAYER AGE>,
    "picture": <PLAYER PROFILE PICTURE>,
    "bio": <PLAYER BIO>
}
```


### POST: Insert school into database `/schools/`
```json
<HTTP STATUS CODE 201>
{
    "id": <SCHOOL ID>,
    "name": <SCHOOL NAME>,
    "logo_image": <SCHOOL SPORTS LOGO>
}
```




## Feedback
Feel free to let us know if you would like us to include any other features to our app, or if there is something in our code that we could improve! Thank you for trying _Sportify_!
