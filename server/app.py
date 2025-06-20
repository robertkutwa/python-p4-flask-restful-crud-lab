# app.py

from flask import Flask, request, jsonify
from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db.init_app(app)

# GET /plants - Get all plants
@app.route('/plants', methods=['GET'])
def get_plants():
    plants = Plant.query.all()
    return jsonify([plant.to_dict() for plant in plants]), 200

# GET /plants/<id> - Get one plant
@app.route('/plants/<int:id>', methods=['GET'])
def get_plant(id):
    plant = Plant.query.get_or_404(id)
    return jsonify(plant.to_dict()), 200

# PATCH /plants/<id> - Update a plant's 'is_in_stock' status
@app.route('/plants/<int:id>', methods=['PATCH'])
def update_plant(id):
    plant = Plant.query.get_or_404(id)
    
    data = request.get_json()
    
    if 'is_in_stock' in data:
        plant.is_in_stock = data['is_in_stock']
    
    db.session.commit()
    
    return jsonify(plant.to_dict()), 200

# DELETE /plants/<id> - Delete a plant
@app.route('/plants/<int:id>', methods=['DELETE'])
def delete_plant(id):
    plant = Plant.query.get_or_404(id)
    
    db.session.delete(plant)
    db.session.commit()
    
    return '', 204

# Run the app
if __name__ == '__main__':
    app.run(port=5555, debug=True)