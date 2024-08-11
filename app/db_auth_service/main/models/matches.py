from .. import db

class Matches(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    player1_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    player2_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    game_date = db.Column(db.DateTime, nullable=False)
    winner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    loser_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    def __repr__(self):
        return '<Matches: %r %r %r %r %r %r>' % (self.id, self.player1_id, self.player2_id, self.game_date, self.winner_id, self.loser_id)

    def to_json(self):
        return {
            'id': self.id,
            'player1_id': self.player1_id,
            'player2_id': self.player2_id,
            'game_date': self.game_date,
            'winner_id': self.winner_id,
            'loser_id': self.loser_id
        }

    @staticmethod
    def from_json(matches_json):
        player1_id = matches_json.get('player1_id')
        player2_id = matches_json.get('player2_id')
        game_date = matches_json.get('game_date')
        winner_id = matches_json.get('winner_id')
        loser_id = matches_json.get('loser_id')

        return Matches(
            player1_id=player1_id,
            player2_id=player2_id,
            game_date=game_date,
            winner_id=winner_id,
            loser_id=loser_id
        )