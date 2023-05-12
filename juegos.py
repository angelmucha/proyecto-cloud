from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
app = Flask(__name__)

CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:GHc8JaWh4oOrwwRuxJod@proyecto-db.cy5l082ix49i.us-east-1.rds.amazonaws.com:5432/tareas'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

class Juegos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String, unique=True, nullable=False)
    descripcion = db.Column(db.String)
    imagen = db.Column(db.String, nullable=False)

    def __repr__(self):
        return '<Juegos %r>' % self.nombre
    
    def serialize(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'imagen': self.imagen
        }

with app.app_context():
    db.create_all()

@app.route('/juegos', methods=['GET'])
def juegos():
    juegos = Juegos.query.all()
    juegos = list(map(lambda juegos: juegos.serialize(), juegos))
    return jsonify(juegos), 200

@app.route('/juegos/<int:id>', methods=['GET'])
def juego(id):
    juego = Juegos.query.get(id)
    if juego is None:
        return jsonify('Juego no existe'), 404
    else:
        return jsonify(juego.serialize()), 200
    
@app.route('/juegos', methods=['POST'])
def create_juego():
    nombre = request.json['nombre']
    descripcion = request.json['descripcion']
    imagen = request.json['imagen']

    juego = Juegos(nombre=nombre, descripcion=descripcion, imagen=imagen)
    db.session.add(juego)
    db.session.commit()

    return jsonify('Juego creado'), 201

@app.route('/juegos/<int:id>', methods=['PUT'])
def update_juego(id):
    juego = Juegos.query.get(id)
    if juego is None:
        return jsonify('Juego no existe'), 404
    else:
        nombre = request.json['nombre']
        descripcion = request.json['descripcion']
        imagen = request.json['imagen']

        juego.nombre = nombre
        juego.descripcion = descripcion
        juego.imagen = imagen

        db.session.commit()

        return jsonify('Juego actualizado'), 200

@app.route('/juegos/<int:id>', methods=['DELETE'])
def delete_juego(id):
    juego = Juegos.query.get(id)
    if juego is None:
        return jsonify('Juego no existe'), 404
    else:
        db.session.delete(juego)
        db.session.commit()
        return jsonify('Juego eliminado'), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001, debug=False)
