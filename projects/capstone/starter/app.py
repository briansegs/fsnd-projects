import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import db_drop_and_create_all, setup_db, Actor, Movie


def create_app(test_congig=None):
  app = Flask(__name__)
  CORS(app)
  setup_db(app)
  db_drop_and_create_all()

  @app.route('/')
  def health():
    return jsonify("Healthy")

  return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)




