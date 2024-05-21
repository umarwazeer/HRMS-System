import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from flask_cors import CORS
from models.employee import MyUser
from app import app, db



# Initialize SQLAlchemy and JWTManager
jwt = JWTManager(app)
CORS(app)

# Your routes
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400
    existing_user = MyUser.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'message': 'Username already exists'}), 400
    new_user = MyUser(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400
    user = MyUser.query.filter_by(username=username).first()
    if not user or user.password != password:
        return jsonify({'message': 'Invalid username or password'}), 401
    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)
    return jsonify({'access_token': access_token, 'refresh_token': refresh_token}, (24)), 200

@app.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user)
    return jsonify({'access_token': new_access_token}), 200

# Protected route example
@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    user_id = get_jwt_identity()
    user = MyUser.query.get(user_id)
    return jsonify({'message': f'Hello, {user.username}! This is a protected route.'}), 200

if __name__ == '__main__':
    app.run(debug=True, port=2024)
