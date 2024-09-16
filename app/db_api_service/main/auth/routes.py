from flask import request, Blueprint, abort, jsonify
from .. import db
from main.models import UserModel


auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data or not data.get("username") or not data.get("password"):
        return jsonify({'message': 'missing_parameters'}), 400

    user = db.session.query(UserModel).filter(UserModel.username == data.get("username")).first()

    if not user:
        return jsonify({'message': 'user_not_found'}), 404
    
    if not user.validate_pass(data.get("password")):
        return jsonify({'message': 'incorrect_password'}), 401
    
    if user and user.validate_pass(data.get("password")):
        return jsonify({'message': 'ok', 'user_id': user.id}), 200
    
    
@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    if not data or not data.get("username") or not data.get("password"):
        return jsonify({'message': 'missing_parameters'}), 400

    user = UserModel.from_json(data)
    exists = db.session.query(UserModel).filter(UserModel.username == user.username).scalar() is not None

    if exists:
        return jsonify({'message': 'duplicated_username'}), 409
    
    try:
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'registered', 'user_id': user.id}), 201
    except Exception as error:
        db.session.rollback()
        return jsonify({'message': str(error)}), 500