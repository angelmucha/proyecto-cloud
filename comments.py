from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
app = Flask(__name__)

CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:GHc8JaWh4oOrwwRuxJod@proyecto-db.cy5l082ix49i.us-east-1.rds.amazonaws.com:5432/tareas'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    juegos_id = db.Column(db.Integer, db.ForeignKey('juegos.id'))

    def __repr__(self):
        return '<Comment %r>' % self.comment
    
    def serialize(self):
        return {
            'id': self.id,
            'comment': self.comment,
            'user_id': self.user_id,
            'juegos_id': self.juegos_id
        }


with app.app_context():
    db.create_all()


@app.route('/comments', methods=['GET'])
def comments():
    comments = Comments.query.all()
    comments = list(map(lambda comment: comment.serialize(), comments))

    return jsonify(comments), 200

@app.route('/juegos/<int:id>/comments', methods=['GET'])
def comments_by_juego(id):
    comments = Comments.query.filter_by(juego_id=id).all()
    comments = list(map(lambda comment: comment.serialize(), comments))

    return jsonify(comments), 200

@app.route('/juegos/<int:id>/comments', methods=['POST'])
def create_comment(id):
    comment = request.json['comment']
    user_id = request.json['user_id']

    comment = Comments(comment=comment, user_id=user_id, juegos_id=id)
    db.session.add(comment)
    db.session.commit()

    return jsonify('Comentario creado'), 201

@app.route('/juegos/<int:id>/comments', methods=['PUT'])
def update_comment(id):
    comment = Comments.query.get(id)
    if comment is None:
        return jsonify('Comentario no existe'), 404
    else:
        comment.comment = request.json['comment']
        db.session.commit()

        return jsonify('Comentario actualizado'), 200


@app.route('/juegos/<int:id>/comments', methods=['DELETE'])
def delete_comment(id):
    comment = Comments.query.get(id)
    if comment is None:
        return jsonify('Comentario no existe'), 404
    else:
        db.session.delete(comment)
        db.session.commit()

        return jsonify('Comentario eliminado'), 200

if __name__ == '__main__':  
    app.run(host='0.0.0.0', port=8001, debug=False)