# import flask
from flask import Flask, jsonify

# Setup flask
# define Flask app (Called "app")
app = Flask(__name__)

#Create Flask Routes
@app.route('/')
def welcome():
    return 'Welcome!'

@app.route('/about')
def about():
    return 'Damian in California'

@app.route('/contact')
def contact():
    return 'damian@gmail.com'