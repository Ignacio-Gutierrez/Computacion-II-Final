from .. import db
from werkzeug.security import generate_password_hash, check_password_hash

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, index=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    # Relationships
    matches_as_player1 = db.relationship('Matches', foreign_keys='Matches.player1_id', backref='player1', lazy=True)
    matches_as_player2 = db.relationship('Matches', foreign_keys='Matches.player2_id', backref='player2', lazy=True)
    matches_as_winner = db.relationship('Matches', foreign_keys='Matches.winner_id', backref='winner', lazy=True)
    matches_as_loser = db.relationship('Matches', foreign_keys='Matches.loser_id', backref='loser', lazy=True)

    @property
    def plain_password(self):
        raise AttributeError('password cannot be read')

    @plain_password.setter
    def plain_password(self, password):
        self.password = generate_password_hash(password)

    def validate_pass(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<Users: %r %r>' % (self.id, self.username)

    def to_json(self):
        return {
            'id': self.id,
            'username': self.username,
        }

    @staticmethod
    def from_json(user_json):
        id = user_json.get('id')
        username = user_json.get('username')
        password = user_json.get('password')
        
        return Users(id=id,
                     username=username,
                     plain_password=password)
