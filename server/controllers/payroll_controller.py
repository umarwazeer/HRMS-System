from flask import jsonify, request
from app import app, db
from models.employee import Employee, Attendance, Department, Payroll
from datetime import datetime

# Helper function to serialize payroll record
def serialize_payroll(payroll_record):
    employee = Employee.query.get(payroll_record.employee_id)

    return {
        'id': payroll_record.id,
        'employee_id': employee.id,
        'employee_name': employee.name,
        'department_name': employee.department.name if employee.department else None,
        'basic_salary': payroll_record.basic_salary,
        'totalSalary': payroll_record.totalSalary,
        'payment_date': payroll_record.payment_date.strftime('%Y-%m-%d'),
        'deductions': payroll_record.deductions,
        'payment_method': payroll_record.payment_method,
        'payroll_period': payroll_record.payroll_period,
        'created_at': payroll_record.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        'updated_at': payroll_record.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
        'created_by': payroll_record.created_by,
        'updated_by': payroll_record.updated_by
    }

# API endpoint to get all payroll records or add a new payroll record
@app.route('/payroll', methods=['GET', 'POST'])
def payroll():
    if request.method == 'GET':
        # Retrieve all payroll records
        payroll_records = Payroll.query.all()
        payroll_data = [serialize_payroll(record) for record in payroll_records]
        return jsonify(payroll_data), 200

    elif request.method == 'POST':
        try:
            data = request.get_json()
            if not isinstance(data, dict):
                return jsonify({'message': 'Invalid JSON data: Expected a dictionary'}), 400
        except Exception as e:
            return jsonify({'message': 'Error parsing JSON data: ' + str(e)}), 400

        # Validate the request data
        required_fields = ['employee_id', 'totalSalary', 'basic_salary', 'payment_date']
        for field in required_fields:
            if field not in data:
                return jsonify({'message': f'Missing required field: {field}'}), 400

        # Get employee details
        employee = Employee.query.get(data['employee_id'])
        if not employee:
            return jsonify({'message': 'Employee not found'}), 404

        # Parse payment_date string into datetime object
        payment_date = datetime.strptime(data['payment_date'], '%Y-%m-%d')

        # Create a new payroll record
        new_payroll = Payroll(
            employee_id=data['employee_id'],
            basic_salary=data['basic_salary'],
            totalSalary=data['totalSalary'],
            payment_date=payment_date,
            deductions=data.get('deductions'),
            payroll_period=data.get('payroll_period'),
            payment_method=data.get('payment_method'),
        )

        db.session.add(new_payroll)
        db.session.commit()

        return jsonify({'message': 'Payroll created successfully', 'payroll_record': serialize_payroll(new_payroll)}), 201

# API endpoint to get payroll record by ID
@app.route('/payroll/<int:payroll_id>', methods=['GET'])
def get_payroll_by_id(payroll_id):
    payroll_record = Payroll.query.get(payroll_id)
    if not payroll_record:
        return jsonify({'message': 'Payroll record not found'}), 404
    return jsonify(serialize_payroll(payroll_record)), 200

# API endpoint to update payroll record by ID
@app.route('/payroll/<int:payroll_id>', methods=['PUT'])
def update_payroll(payroll_id):
    payroll_record = Payroll.query.get(payroll_id)
    if not payroll_record:
        return jsonify({'message': 'Payroll record not found'}), 404

    try:
        data = request.get_json()
        if not isinstance(data, dict):
            return jsonify({'message': 'Invalid JSON data: Expected a dictionary'}), 400
    except Exception as e:
        return jsonify({'message': 'Error parsing JSON data: ' + str(e)}), 400

    # Update the payroll record 
    if 'totalSalary' in data:
        payroll_record.totalSalary = data['totalSalary']
    if 'basic_salary' in data:
        payroll_record.basic_salary = data['basic_salary']    
    if 'payment_date' in data:
        payroll_record.payment_date = datetime.strptime(data['payment_date'], '%Y-%m-%d')
    if 'deductions' in data:
        payroll_record.deductions = data['deductions']
    if 'payroll_period' in data:
        payroll_record.payroll_period = data['payroll_period']
    if 'payment_method' in data:
        payroll_record.payment_method = data['payment_method']

    payroll_record.updated_at = datetime.utcnow()
    db.session.commit()

    return jsonify({'message': 'Payroll updated successfully', 'payroll_record': serialize_payroll(payroll_record)}), 200

# API endpoint to delete payroll record by ID
@app.route('/payroll/<int:payroll_id>', methods=['DELETE'])
def delete_payroll(payroll_id):
    payroll_record = Payroll.query.get(payroll_id)
    if not payroll_record:
        return jsonify({'message': 'Payroll record not found'}), 404

    db.session.delete(payroll_record)
    db.session.commit()

    return jsonify({'message': 'Payroll deleted successfully'}), 200
