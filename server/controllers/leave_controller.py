from flask import jsonify, request
from app import app, db
from models.employee import Employee, Leave, Department
from datetime import datetime


def format_date(date_obj):
    return date_obj.strftime('%A, %d %B %Y')


# API endpoint to get and post leave records
@app.route('/leave', methods=['GET', 'POST'])
def leave():
    if request.method == 'GET':
        leave_records = Leave.query.all()

        # Create a list to store leave records with additional details
        leave_details = []

        for record in leave_records:
            employee = Employee.query.get(record.emp_id) 

            if employee:
                leave_detail = {
                    'id': record.id,
                    'emp_id': employee.id,
                    'emp_name': employee.name,
                    'emp_gender': employee.gender,
                    'leave_type': record.leave_type,
                    'description': record.description,
                    'on_date': format_date(record.on_date),
                    'from_date': format_date(record.from_date),
                    'to_date': format_date(record.to_date),
                    'dep_name': employee.department.name if employee.department else None
                }
                leave_details.append(leave_detail)

        return jsonify(leave_details)

    elif request.method == 'POST':
        data = request.json
        try:
            new_leave = Leave(
                leave_type=data['leave_type'],
                description=data['description'],
                on_date=datetime.strptime(data['on_date'], '%Y-%m-%d'),  # Convert string to datetime
                from_date=datetime.strptime(data['from_date'], '%Y-%m-%d'),
                to_date=datetime.strptime(data['to_date'], '%Y-%m-%d'),
                emp_id=data['emp_id']
            )
            db.session.add(new_leave)
            db.session.commit()

            return jsonify({'message': 'Leave created successfully', 'leave_id': new_leave.id}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': 'Failed to create leave record', 'error': str(e)}), 500

# API endpoint to get leave record by ID
@app.route('/leave/<int:leave_id>', methods=['GET'])
def get_leave_by_id(leave_id):
    leave = Leave.query.get(leave_id)
    if not leave:
        return jsonify({'message': 'Leave record not found'}), 404

    employee = Employee.query.get(leave.emp_id)
    if not employee:
        return jsonify({'message': 'Employee not found for this leave record'}), 404

    leave_detail = {
        'id': leave.id,
        'emp_id': employee.id,
        'emp_name': employee.name,
        'emp_gender': employee.gender,
        'leave_type': leave.leave_type,
        'description': leave.description,
        'on_date': format_date(leave.on_date),
        'from_date': format_date(leave.from_date),
        'to_date': format_date(leave.to_date),
        'dep_name': employee.department.name if employee.department else None
    }
    return jsonify(leave_detail)

# API endpoint to update leave record by ID
@app.route('/leave/<int:leave_id>', methods=['PUT'])
def update_leave(leave_id):
    data = request.json
    leave = Leave.query.get(leave_id)
    if not leave:
        return jsonify({'message': 'Leave record not found'}), 404

    try:
        leave.leave_type = data.get('leave_type', leave.leave_type)
        leave.description = data.get('description', leave.description)
        leave.on_date = data.get('on_date', leave.on_date)
        leave.from_date = data.get('from_date', leave.from_date)
        leave.to_date = data.get('to_date', leave.to_date)
        leave.emp_id = data.get('emp_id', leave.emp_id)

        db.session.commit()
        return jsonify({'message': 'Leave record updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to update leave record', 'error': str(e)}), 500

# API endpoint to delete leave record by ID
@app.route('/leave/<int:leave_id>', methods=['DELETE'])
def delete_leave(leave_id):
    leave = Leave.query.get(leave_id)
    if not leave:
        return jsonify({'message': 'Leave record not found'}), 404

    db.session.delete(leave)
    db.session.commit()
    return jsonify({'message': 'Leave record deleted successfully'}), 200
