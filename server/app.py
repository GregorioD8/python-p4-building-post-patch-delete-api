#!/usr/bin/env python3

# Import necessary modules and functions from Flask and Flask extensions
from flask import Flask, request, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Import the database models from a separate file called models
from models import db, User, Review, Game

# Create an instance of the Flask class
app = Flask(__name__)

# Configure the SQLAlchemy part of the app instance
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

# Set up the Flask-Migrate extension
migrate = Migrate(app, db)

# Initialize the app with the database
db.init_app(app)

# Define the route for the index page
@app.route('/')
def index():
    return "Index for Game/Review/User API"

# Define the route to get a list of all games
@app.route('/games')
def games():

    games = []
    # Query all games from the database and convert each to a dictionary
    for game in Game.query.all():
        game_dict = game.to_dict()
        games.append(game_dict)

    # Create a response with the list of games and a 200 OK status
    response = make_response(
        games,
        200
    )

    return response

# Define the route to get a specific game by its ID
@app.route('/games/<int:id>')
def game_by_id(id):

    # Query the game with the given ID from the database
    game = Game.query.filter(Game.id == id).first()

    # Convert the game to a dictionary
    game_dict = game.to_dict()

    # Create a response with the game dictionary and a 200 OK status
    response = make_response(
        game_dict,
        200
    )

    return response

## Handle requests with the POST HTTP verb to /reviews.
## Access the data in the body of the request.
## Use that data to create a new review in the database.
## Send a response with newly created review as JSON.
## create a new record using the attributes passed in the request.

# Define the route to handle GET and POST requests for reviews
@app.route('/reviews', methods=['GET', 'POST'])
def reviews():

    if request.method == 'GET':
         # Handle GET request: retrieve all reviews
        reviews = []
        for review in Review.query.all():
            review_dict = review.to_dict()
            reviews.append(review_dict)

        # Create a response with the list of reviews and a 200 OK status
        response = make_response(
            reviews,
            200
        )

        return response

    elif request.method == 'POST':

        # Handle POST request: create a new review
        new_review = Review(
            score=request.form.get("score"),
            comment=request.form.get("comment"),
            game_id=request.form.get("game_id"),
            user_id=request.form.get("user_id"),
        )

        # Add the new review to the database session and commit it
        db.session.add(new_review)
        db.session.commit()

        # Convert the new review to a dictionary
        review_dict = new_review.to_dict()

        # Create a response with the new review dictionary and a 201 Created status
        response = make_response(
            review_dict,
            201
        )

        return response




## First, we'll need to handle requests by adding a new route in the controller. We can write out a route for a DELETE request just like we would for a GET request, just by changing the method

# Define the route to handle GET, PATCH, and DELETE requests for a specific review by ID
@app.route('/reviews/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def review_by_id(id):

    # Query the review with the given ID from the database
    review = Review.query.filter(Review.id == id).first()

    if review == None:
        # Handle case where the review is not found
        response_body = {
            "message": "This record does not exist in our database. Please try again."
        }
        response = make_response(response_body, 404)

        return response

    else:
        if request.method == 'GET':
            # Handle GET request: retrieve the review
            review_dict = review.to_dict()

            response = make_response(
                review_dict,
                200
            )

            return response

        elif request.method == 'PATCH':
            # Handle PATCH request: update the review
            for attr in request.form:
                setattr(review, attr, request.form.get(attr))

            # Add the updated review to the database session and commit it
            db.session.add(review)
            db.session.commit()

            # Convert the updated review to a dictionary
            review_dict = review.to_dict()
            response = make_response(
                review_dict,
                200
            )

            return response

        elif request.method == 'DELETE':

            # Handle DELETE request: delete the review
            db.session.delete(review)
            db.session.commit()

            response_body = {
                "delete_successful": True,
                "message": "Review deleted."
            }

            response = make_response(
                response_body,
                200
            )

            return response

# Define the route to get a list of all users
@app.route('/users')
def users():

    # Initialize an empty list to store user dictionaries
    users = []

    # Query all users from the database and convert each to a dictionary
    for user in User.query.all():
        user_dict = user.to_dict()
        users.append(user_dict)

    # Create a response with the list of users and a 200 OK status
    response = make_response(
        users,
        200
    )

    return response


# If this script is run directly, start the Flask application
if __name__ == '__main__':
    app.run(port=5555, debug=True)