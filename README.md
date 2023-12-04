# [Cornell AppDev Hack Challenge Project: _Sportify_](https://github.com/3TTemi/sportify-backend)

#### By: [Chimdi](https://github.com/cejiogu) and [Temi Adebowale](https://github.com/3TTemi)

## Introduction
Welcome to _Sportify_, your go-to app for staying updated on upcoming and current sports matches hosted by Cornell University! Whether you're a passionate Cornell student hoping to support school spirit or just someone who loves the thrill of Cornell sports, this app is designed to keep you in the loop. 

## Description

_Sportify_ is an API that allows its clients to:
-  Access a database storing Cornell University's home games, in which the client can view all current and future games or modify their search by selecting qualities that specific games might have in common (referred to as _identifiers_)
- Create their own account or log into an existing account using an inputted username and password
- Add funds to their account
- Purchase tickets for one or more games

## How to Use 
### GET: Get all games  `/`, `/games/`
#### Response:
```json
<HTTP STATUS CODE 200>
{
    "games": [
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
    ]
}
```

### GET: Get all current games `/games/current/`
```json
<HTTP STATUS CODE 200>
{
    "games": [
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
    ]
}
```

### GET: Get all future games `/games/future/`
```json
<HTTP STATUS CODE 200>
{
    "games": [
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
    ]
}
```

### GET: Get game by id number `/games/{game id}}/`
```json
<HTTP STATUS CODE 200>
{
    "games": [
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
    ]
}
```

### GET: Get all games by identifier `/games/{identifier}/
```json
<HTTP STATUS CODE 200>
{
    "games": [
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
    ]
}
````

### POST: Insert game into database `/games/`
```json
<HTTP STATUS CODE 200>
{
    "games": [
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
    ]
}
```

### POST: Update a game's information `/games/{game id}/`
```json
<HTTP STATUS CODE 200>
{
    "games": [
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
    ]
}
```

### DELETE: Delete a specific game from database `/games/{game id}/`
```json
<HTTP STATUS CODE 200>
{
    "games": [
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
    ]
}
```

### DELETE: Delete all games from database `/games/`
```json
<HTTP STATUS CODE 200>
{
    "games": [
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
    ]
}
```

### POST: Insert user into database `/user/register/`
```json
<HTTP STATUS CODE 200>
{
    "games": [
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
    ]
}
```

### POST: Updates user's session token `/session/`
```json
<HTTP STATUS CODE 200>
{
    "games": [
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
    ]
}
```

### GET: Verify user's session token `/games/{game id}/`
```json
<HTTP STATUS CODE 200>
{
    "games": [
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
    ]
}
```


### POST: Login user `/user/login/`
```json
<HTTP STATUS CODE 200>
{
    "games": [
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
    ]
}
```


### POST: Logout user `/user/logout/`
```json
<HTTP STATUS CODE 200>
{
    "games": [
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
    ]
}
```

### GET: Get user by user id `/user/{user id}/`
```json
<HTTP STATUS CODE 200>
{
    "games": [
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
    ]
}
```

### POST: Update user username `user/{user id}/username/`
```json
<HTTP STATUS CODE 200>
{
    "games": [
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
    ]
}
```

### POST: Update funds on user's account `/user/{user id}/funds/`
```json
<HTTP STATUS CODE 200>
{
    "games": [
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
    ]
}
```

### POST: Update user funds `user/{user id}/funds/`
```json
<HTTP STATUS CODE 200>
{
    "games": [
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
    ]
}
```

### POST: Purchase tickets `/user/{user id}/tickets/`
```json
<HTTP STATUS CODE 200>
{
    "games": [
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
    ]
}
```

### POST: Add school to database `/schools/`
```json
<HTTP STATUS CODE 201>
{
    "games": [
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
    ]
}
```

### GET: Get school by school id `/school/{school id}`
```json
<HTTP STATUS CODE 200>
{
    "games": [
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
    ]
}
```

### DELETE: Remove school from database `/school/{school id}/`
```json
<HTTP STATUS CODE 200>
{
    "games": [
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
    ]
}
```

### GET: Get all schools `/school/`
```json
<HTTP STATUS CODE 200>
{
    "games": [
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
    ]
}
```


### POST: Add player to database `/players/`
```json
<HTTP STATUS CODE 201>
{
    "games": [
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
    ]
}
```


### GET: Insert school into database `/school/`
```json
<HTTP STATUS CODE 200>
{
    "games": [
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
    ]
}
```




## Feedback
Feel free to let us know if you would like us to include any other features to our app, or if there is something in our code that we could improve! Thank you for trying _Sportify_!