import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import db_drop_and_create_all, setup_db, Actor, Movie

app = Flask(__name__)
CORS(app)
setup_db(app)

db_drop_and_create_all()

@app.route('/')
def get_greeting():
    actors = Actor.query.all()
    a = []
    for actor in actors:
      a.append(actor.name)

    return str(a)

