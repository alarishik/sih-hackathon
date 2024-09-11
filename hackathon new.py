
from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory data storage (for demo purposes)
farmers = []
produce_list = []

@app.route('/farmers', methods=['POST'])
def register_farmer():
    data = request.get_json()
    farmer_id = len(farmers) + 1
    farmer = {"id": farmer_id, "name": data["name"], "email": data["email"]}
    farmers.append(farmer)
    return jsonify(farmer), 201

@app.route('/produce', methods=['POST'])
def add_produce():
    data = request.get_json()
    produce_id = len(produce_list) + 1
    produce = {
        "id": produce_id,
        "farmer_id": data["farmer_id"],
        "name": data["name"],
        "price": data["price"],
        "quantity": data["quantity"]
    }
    produce_list.append(produce)
    return jsonify(produce), 201

@app.route('/produce', methods=['GET'])
def get_produce():
    return jsonify(produce_list), 200

@app.route('/produce/<int:produce_id>', methods=['GET'])
def get_produce_by_id(produce_id):
    produce = next((p for p in produce_list if p["id"] == produce_id), None)
    if produce is None:
        return jsonify({"error": "Produce not found"}), 404
    return jsonify(produce)

@app.route('/purchase', methods=['POST'])
def purchase_produce():
    data = request.get_json()
    produce_id = data["produce_id"]
    quantity = data["quantity"]
    
    produce = next((p for p in produce_list if p["id"] == produce_id), None)
    if produce is None:
        return jsonify({"error": "Produce not found"}), 404
    
    if produce["quantity"] < quantity:
        return jsonify({"error": "Not enough quantity available"}), 400
    
    produce["quantity"] -= quantity
    return jsonify({"message": "Purchase successful"}), 200

if __name__ == '__main__':
    app.run(debug=True)
 