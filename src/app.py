"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
# from models import Person


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Create the jackson family object
jackson_family = FamilyStructure("Jackson")


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/members', methods=['GET'])
def handle_get_all_members():
    return jsonify(jackson_family.get_all_members()), 200


@app.route('/members/<int:id>', methods=['GET'])
def handle_get_member(id):
    member= jackson_family.get_member(id)
    if member:
        return jsonify(member), 200
    else:
        return jsonify({"error": "Miembro no encontrado"}), 404
    

@app.route('/members', methods=['POST'])
def handle_add_member():
    member_data= request.get_json()
    if not member_data or "first_name" not in member_data or "age" not in member_data or "lucky_numbers" not in member_data:
        return jsonify({"error": "Datos incompletos"}), 400
    jackson_family.add_member(member_data)
    return jsonify({"message": "Miembro agregado"}), 200


@app.route('/members/<int:id>', methods=['DELETE'])
def handle_delete_member(id):
    was_deleted = jackson_family.delete_member(id)
    if not was_deleted:
        return jsonify({"error": "Miembro no encontrado"}), 404
    return jsonify({"done": True}), 200



# This only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
