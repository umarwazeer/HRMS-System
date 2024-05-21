from flask import jsonify, request
from app import app, db
from models.employee import Employee,  Attendance, Department
from models.employee import Employee
from flask_jwt_extended import (
    JWTManager,
    jwt_required,
    create_access_token,
    get_jwt_identity
)


# Get all Employee
@app.route('/employees', methods=['GET'])
@jwt_required()
def get_emp():
    current_user_id = get_jwt_identity()
    employees = Employee.query.filter_by(created_by=current_user_id).all()
    result = []
    for employee in employees:
          department_id = employee.dep_id
          department_name = employee.department.name if employee.department else None
          result.append({
              'id': employee.id,
              'name': employee.name,
              'email': employee.email,
              "dep_id": department_id,
              "dep_name": department_name ,
              'salary': employee.salary,
              'role': employee.role,
              #  'image': employee.image,
              'phone': employee.phone,
              'gender': employee.gender
                     })
    return jsonify(result)
    # return jsonify([{'id': employee.id,
    #                  'name': employee.name,
    #                  'email': employee.email,
    #                 #  'department': employee.department.name,
    #                  'salary': employee.salary,
    #                  'role': employee.role,
    #                  #  'image': employee.image,
    #                  'phone': employee.phone,
    #                  'gender': employee.gender} for employee in employees])



# Get by is employee
@app.route('/employees/<int:id>', methods=['GET'])
def get_employee(id):
    employee = Employee.query.get(id)
    if not employee:
        return jsonify({'message': 'Employee not found'})
    result = {
        'id': employee.id,
        'name': employee.name,
        'email': employee.email, 
        'salary': employee.salary
        }
    # print(result)
    return jsonify(result)


# Employee
@app.route('/employees', methods=['POST'])
@jwt_required()
def add_employee():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    # if not data['name']:
    #     return {'message': 'Name is required.'}, 400
   # Check if 'dep_id' exists in the JSON data
    if 'dep_id' not in data:
        return jsonify({'error': 'Missing dep_id parameter'}), 400

    department_id = data['dep_id']
    department = Department.query.get(department_id)
    print("employeeDAta", data)

    if department is None:
        return jsonify({'error': 'Department not found'}), 404

    try:
        # Create a new employee record
        new_employee = Employee(
            name=data.get('name'),
            email=data.get('email'),
            salary=data.get('salary'),
            role=data.get('role'),
            gender=data.get('gender'),
            phone=data.get('phone'),
            dep_id=department_id,
            created_by=current_user_id,
            updated_by=current_user_id
        )
        db.session.add(new_employee)
        db.session.commit()

        return jsonify({'message': 'Employee added successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Update Employee
@app.route('/employees/<int:id>', methods=['PUT'])
def update_employee(id):
    employee = Employee.query.get(id)
    if not employee:
        return jsonify({'message': 'Employee not found'})
    data = request.get_json()
    employee.name = data['name']
    employee.email = data['email']
    employee.salary = data['salary']
    db.session.commit()
    
    return jsonify({'message': 'Employee updated'})


# Delete Employee
@app.route('/employees/<int:id>', methods=['DELETE'])
def delete_employee(id):
    employee = Employee.query.get(id)
    if not employee:
        return jsonify({'message': 'Employee not found'})
    db.session.delete(employee)
    db.session.commit()
    return jsonify({'message': 'Employee deleted'})


# Delete all
# @app.route('/employees/<int:id>', methods=['DELETE'])
# def delete_employee(id):
#     employee = Employee.query.get(id)
#     if not employee:
#         return jsonify({'message': 'Employee not found'})
#     db.session.delete(employee)
#     db.session.commit()
#     return jsonify({'message': 'Employee deleted'})
