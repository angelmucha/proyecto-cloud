from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash,generate_password_hash

db = SQLAlchemy()
app = Flask(__name__)

CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:GHc8JaWh4oOrwwRuxJod@proyecto-db.cy5l082ix49i.us-east-1.rds.amazonaws.com:5432/tareas'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String)
    password = db.Column(db.String, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username
    
    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email
        }

with app.app_context():
    db.create_all()

@app.route('/register', methods=['POST'])
def register():
    username = request.json['username']
    email = request.json['email']
    password = generate_password_hash(request.json['password'])

    user = User(username=username, email=email, password=password)
    db.session.add(user)
    db.session.commit()

    return jsonify('Usuario creado')

@app.route('/login', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']

    user = User.query.filter_by(username=username).first()
    if user is None:
        return jsonify('Usuario no existe')
    elif not check_password_hash(user.password, password):
        return jsonify('Contraseña incorrecta')
    else:
        return jsonify('Bienvenido')
    
@app.route('/users', methods=['GET'])
def users():
    users = User.query.all()
    users = list(map(lambda user: user.serialize(), users))
    return jsonify(users)

@app.route('/user/<id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify('Usuario eliminado')

@app.route('/user/<id>', methods=['PUT'])
def update_user(id):
    user = User.query.get(id)
    user.username = request.json['username']
    user.email = request.json['email']
    user.password = generate_password_hash(request.json['password'])
    db.session.commit()
    return jsonify('Usuario actualizado')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False)