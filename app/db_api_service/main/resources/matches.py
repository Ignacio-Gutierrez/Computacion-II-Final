from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import MatchModel, UserModel
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime


class Match(Resource):
    def get(self, id):
        match = db.session.query(MatchModel).get_or_404(id)
        return match.to_json()
    
class Matches(Resource):
    def get(self):
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=15, type=int)
        winner_name = request.args.get('winner', type=str)
        loser_name = request.args.get('loser', type=str)
        player_name = request.args.get('player', type=str)

        user1 = db.aliased(UserModel)
        user2 = db.aliased(UserModel)
        winner = db.aliased(UserModel)
        loser = db.aliased(UserModel)

        query = db.session.query(
            MatchModel.id,
            user1.username.label('player1_name'),
            user2.username.label('player2_name'),
            winner.username.label('winner_name'),
            loser.username.label('loser_name'),
            MatchModel.game_date
        ).join(user1, MatchModel.player1_id == user1.id) \
         .join(user2, MatchModel.player2_id == user2.id) \
         .join(winner, MatchModel.winner_id == winner.id) \
         .join(loser, MatchModel.loser_id == loser.id)

        if winner_name:
            query = query.filter(winner.username.ilike(f"%{winner_name}%"))
        if loser_name:
            query = query.filter(loser.username.ilike(f"%{loser_name}%"))
        if player_name:
            query = query.filter(
                db.or_(
                    user1.username.ilike(f"%{player_name}%"),
                    user2.username.ilike(f"%{player_name}%")
                )
            )

        paginated_matches = query.paginate(page=page, per_page=per_page, error_out=False)

        matches = []
        for match in paginated_matches.items:
            matches.append({
                'id': match.id,
                'player1_name': match.player1_name,
                'player2_name': match.player2_name,
                'winner_name': match.winner_name,
                'loser_name': match.loser_name,
                'game_date': match.game_date.isoformat()
            })

        return jsonify({
            'matches': matches,
            'total': paginated_matches.total,
            'pages': paginated_matches.pages,
            'page': paginated_matches.page,
            'per_page': per_page
        })

    
    def post(self):
        data = request.get_json()
        if not data:
            return {'message': 'No input data provided'}, 400
        try:
            match = MatchModel.from_json(data)
            db.session.add(match)
            db.session.commit()
        except :
            db.session.rollback()
            return {'message': 'error'}, 500

        return match.to_json(), 201