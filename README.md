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
### GET: Get all games `/games/`
### GET: Get all games by game id `/games/{game id}/`
### GET: Get all games by identifier `/games/{identifier}/`
### POST: Insert game into database `/games/`
### POST: Update a game's information `/games/{game id}/`
### DELETE: Delete a specific game from database `/games/{game id}/`
### POST: Insert user into database `/user/`
### GET: Get user by user id `/user/{user id}/`
### POST: Update user username `user/{user id}/username/`
### POST: Update user password `user/{user id}/password/`
### POST: Update user funds `user/{user id}/funds/`
### POST: Insert school into database `/school/`
### GET: Get school by school id `/school/{school id}`
### DELETE: Remove school from database `/school/{school id}/`
### GET: Get all schools `/school/`

## Feedback
