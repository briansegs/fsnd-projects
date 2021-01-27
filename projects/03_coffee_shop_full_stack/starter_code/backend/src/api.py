import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

db_drop_and_create_all()

# ROUTES


@app.route('/drinks')
def get_drinks():
    drink_list = Drink.query.all()
    if drink_list is None:
        abort(404)

    drinks = [drink.short() for drink in drink_list]

    return jsonify({
        "success": True,
        "drinks": drinks
    }), 200


@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_drinks_detail(jwt):
    drink_list = Drink.query.all()
    if drink_list is None:
        abort(404)
    drinks = [drink.long() for drink in drink_list]

    return jsonify({
        "success": True,
        "drinks": drinks
    }), 200


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drinks(jwt):
    body = request.get_json()

    new_title = body.get('title')
    new_recipe = body.get('recipe')

    drink = Drink(
            title=new_title,
            recipe=json.dumps([new_recipe])
        )
    try:
        drink.insert()
        return jsonify({
            'success': True,
            'drinks': drink.long()
        }), 200

    except Exception:
        abort(422)


@app.route('/drinks/<drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def patch_drinks(jwt, drink_id):
    body = request.get_json()

    try:
        drink = Drink.query.filter(Drink.id == drink_id).one_or_none()
        if drink is None:
            abort(404)

        new_title = body.get('title')
        new_recipe = body.get('recipe')

        patch_drink = Drink(
                title=new_title,
                recipe=json.dumps(new_recipe)
            )

        patch_drink.update()

        drink_list = Drink.query.all()
        if drink_list is None:
            abort(404)

        drinks = [drink.long() for drink in drink_list]

        return jsonify({
            "success": True,
            "drinks": drinks
        }), 200

    except Exception:
        abort(422)


@app.route('/drinks/<drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(jwt, drink_id):
    try:
        drink = (
            Drink.query.filter(Drink.id == drink_id).one_or_none()
        )

        if drink is None:
            abort(404)

        drink.delete()

        return jsonify({
            "success": True,
            "delete": drink_id
        }), 200

    except Exception:
        abort(422)


# Error Handling


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False,
                    "error": 422,
                    "message": "unprocessable"
                    }), 422


@app.errorhandler(404)
def resource_not_found(error):
    return jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404


@app.errorhandler(AuthError)
def handle_auth0_error(error):
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error['description']
    }), 401
