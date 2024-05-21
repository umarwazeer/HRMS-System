from flask import Flask, jsonify, request
from app import app, db
from models.employee import Employee, Department


# Get all department
@app.route('/department', methods=['GET'])
def get_department():
    departments = Department.query.all()
    return jsonify([{'id': department.id, 'name': department.name,
                     } for department in departments]
                   )


# Get by is department
@app.route('/department/<int:id>', methods=['GET'])
def get_department_by(id):
    department = Department.query.get(id)
    if not department:
        return jsonify({'message': 'Employee not found'})
    result = {'id': department.id, 'name': department.name,
               }
    return jsonify(result)


# Post Department
@app.route('/department', methods=['POST'])
def add_department():
    data = request.get_json()
    new_dep = Department(id=data['id'],
                    name=data['name'],
                    )
    db.session.add(new_dep)
    db.session.commit()
    return jsonify({'id': new_dep.id, 'name': new_dep.name,
                    }), 201


# update Department
@app.route('/department/<int:id>', methods=['PUT'])
def update_department(id):
    department = Department.query.get(id)
    if not department:
        return jsonify({'message': 'Department not found'})
    data = request.get_json()
    department.name = data['name']
    department.id = data['id']
    db.session.commit()
    return jsonify({'message': 'Department updated'})


# /*  delete department by Id */
@app.route('/department/<int:id>', methods=['DELETE'])
def delete_department(id):
    dep = Department.query.get(id)
    if not dep:
        return jsonify({'message': 'Department not found'})
    db.session.delete(dep)
    db.session.commit()
    return jsonify({'message': 'Department deleted'}, 200)


#  Delete all Department
# @app.route('/department', methods=['DELETE'])
# def delete_departments():
#     try:
#         data = request.get_json()
#         if not data or 'ids' not in data:
#             return jsonify({'error': 'Invalid JSON data'}), 400

#         # Extract the list of department IDs to be deleted
#         ids_to_delete = data['ids']

#         # Delete the specified departments
#         db.session.query(Department).filter(Department.id.in_(ids_to_delete)).delete(synchronize_session=False)
#         db.session.commit()
#         return jsonify({'message': 'Departments deleted'}), 200
#     except Exception as e:
#         db.session.rollback()
#         return jsonify({'error': 'An error occurred while deleting departments'}), 500
