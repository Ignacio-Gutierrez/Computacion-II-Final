from flask import request, Blueprint, abort, jsonify
from .. import db
from main.models import UserModel
from flask_jwt_extended import create_access_token


auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data or not data.get("username") or not data.get("password"):
        abort(400, description="Missing input parameters.")

    user = db.session.query(UserModel).filter(UserModel.username == data.get("username")).first()

    if user and user.validate_pass(data.get("password")):
        access_token = create_access_token(identity=user.id)
        return jsonify({'access_token': access_token}), 200
    else:
        abort(401, description="Incorrect username or password.")
    
    
@auth.route('/register' , methods=['POST'])
def register():
    user = UserModel.from_json(request.get_json())
    exists = db.session.query(UserModel).filter(UserModel.username == user.username).scalar() is not None
    if exists:
        return 'Duplicated username', 409
    else:
        try:
            db.session.add(user)
            db.session.commit()
        except Exception as error:
            db.session.rollback()
            return str(error), 409
        return user.to_json(), 201