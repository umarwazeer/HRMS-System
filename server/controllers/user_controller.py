# from flask import Flask, jsonify, request
# from app import app, db
# from models.employee import Employee, User


# # Get all Users
# @app.route('/users', methods=['GET'])
# def get_users():
#     users = User.query.all()
#     return jsonify([{'id': user.id, 'name': user.name,
#                      'email': user.email,
#                      # 'depaprtment': user.dep.name,
#                      'dep': user.dep
#                      } for user in users]
#                    )


# # Get by is user
# @app.route('/users/<int:id>', methods=['GET'])
# def get_user_by(id):
#     user = User.query.get(id)
#     if not user:
#         return jsonify({'message': 'Employee not found'})
#     result = {'id': user.id, 'name': user.name,
#               'email': user.email, 'dep': user.dep}
#     return jsonify(result)


# # Post User
# @app.route('/users', methods=['POST'])
# def add_user():
#     data = request.get_json()
#     new_user = User(name=data['name'],  # dep_id=data['id'],
#                     email=data['email'],
#                     dep=data['dep'],
#                     )

#     db.session.add(new_user)
#     db.session.commit()
#     return jsonify({'id': new_user.id, 'name': new_user.name, 'email': new_user.email,
#                     #  'dep_id': new_user.dep_id,'department': new_user.dep
#                     }), 201


# # update user
# @app.route('/users/<int:id>', methods=['PUT'])
# def update_user(id):
#     user = User.query.get(id)
#     if not user:
#         return jsonify({'message': 'User not found'})
#     data = request.get_json()
#     user.name = data['name']
#     user.email = data['email']
#     user.salary = data['salary']
#     db.session.commit()
#     return jsonify({'message': 'User updated'})


# """ Delete user"""
# @app.route('/users/<int:id>', methods=['DELETE'])
# def delete_user(id):
#     user = User.query.get(id)
#     if not user:
#         return jsonify({'message': 'User not found'})
#     db.session.delete(user)
#     db.session.commit()
#     return jsonify({'message': 'User deleted'}, 200)
