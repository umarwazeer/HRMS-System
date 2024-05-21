from flask import jsonify
from app import app, db
from models.employee import Employee, Attendance, Leave, Payroll
from flask_jwt_extended import jwt_required, get_jwt_identity

def get_employee_basic_details(employee):
    return {
        'id': employee.id,
        'name': employee.name,
        'email': employee.email,
        'salary': employee.salary,
        'role': employee.role,
        'gender': employee.gender,
        'phone': employee.phone,
        'department': {
            'id': employee.department.id,
            'name': employee.department.name
        } if employee.department else None,
        

    }

def get_attendance_details(employee_id):
    attendance_records = Attendance.query.filter_by(emp_id=employee_id).all()
    return [{
        'date': record.date,
        'check_in_time': record.check_in_time,
        'check_out_time': record.check_out_time,
        'status': record.status
    } for record in attendance_records]

def get_leave_details(employee_id):
    leave_records = Leave.query.filter_by(emp_id=employee_id).all()
    return [{
        'leave_type': record.leave_type,
        'description': record.description,
        'on_date': record.on_date,
        'from_date': record.from_date,
        'to_date': record.to_date
    } for record in leave_records]

def get_payroll_details(employee_id):
    payroll_records = Payroll.query.filter_by(employee_id=employee_id).all()
    return [{
        'basic_salary': record.basic_salary,
        'total_salary': record.totalSalary,
        'payment_date': record.payment_date,
        'payment_method': record.payment_method,
        'deductions': record.deductions,
        'payroll_period': record.payroll_period
    } for record in payroll_records]

@app.route('/employees/<int:id>/details', methods=['GET'])
@jwt_required()
def get_employee_details(id):
    current_user_id = get_jwt_identity()
    employee = Employee.query.filter_by(id=id, created_by=current_user_id).first()
    if not employee:
        return jsonify({'message': 'Employee not found'}), 404

    employee_details = get_employee_basic_details(employee)
    employee_details['attendance'] = get_attendance_details(id)
    employee_details['leaves'] = get_leave_details(id)
    employee_details['payrolls'] = get_payroll_details(id)
    
    return jsonify(employee_details)
