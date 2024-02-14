from flask import Flask, jsonify, request, abort
from flask_migrate import Migrate
from models import db, Hero, Power, HeroPower

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    return jsonify([hero.serialize() for hero in heroes])

@app.route('/heroes/<int:id>', methods=['GET'])
def get_hero(id):
    hero = Hero.query.get(id)
    if not hero:
        abort(404, description="Hero not found")
    return jsonify(hero.serialize())

@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    return jsonify([power.serialize() for power in powers])

@app.route('/powers/<int:id>', methods=['GET'])
def get_power(id):
    power = Power.query.get(id)
    if not power:
        abort(404, description="Power not found")
    return jsonify(power.serialize())

@app.route('/powers/<int:id>', methods=['PATCH'])
def update_power(id):
    power = Power.query.get(id)
    if not power:
        abort(404, description="Power not found")
    data = request.get_json()
    if 'description' not in data:
        abort(400, description="Missing 'description' in request")
    power.description = data['description']
    db.session.commit()
    return jsonify(power.serialize())

@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.get_json()
    if not all(key in data for key in ['strength', 'power_id', 'hero_id']):
        abort(400, description="Missing required fields in request")
    hero = Hero.query.get(data['hero_id'])
    power = Power.query.get(data['power_id'])
    if not hero or not power:
        abort(404, description="Hero or Power not found")
    hero_power = HeroPower(strength=data['strength'], hero=hero, power=power)
    db.session.add(hero_power)
    db.session.commit()
    return jsonify(hero.serialize())

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": error.description}), 404

@app.errorhandler(400)
def bad_request(error):
    return jsonify({"error": error.description}), 400

if __name__ == '__main__':
    app.run(port=5555)