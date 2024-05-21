# Import necessary modules
from flask import jsonify, request
from app import app, db
from models.employee import Employee, Attendance, Department
from datetime import datetime

# API endpoint to get all attendance records or add a new attendance record
@app.route('/attendance', methods=['GET', 'POST'])
def attendance():
    if request.method == 'GET':
        # Retrieve all attendance records
        attendance = Attendance.query.all()

        # Create a list to store attendance records with additional details
        attendance_records = []

        for record in attendance:
            department = Department.query.get(record.dep_id)
            employee = Employee.query.get(record.emp_id)

            if department and employee:
                attendance_record = {
                    'id': record.id,
                    'dep_id': department.id,
                    'dep_name': department.name,
                    'emp_id': employee.id,
                    'emp_name': employee.name,
                    'emp_gender': employee.gender,
                    'status': record.status,
                    'date': record.date.strftime('%Y-%m-%d'),  # Format the date
                    'check_in_time': record.check_in_time.strftime('%Y-%m-%d %H:%M:%S') if record.check_in_time else None,
                    'check_out_time': record.check_out_time.strftime('%Y-%m-%d %H:%M:%S') if record.check_out_time else None
                }
                attendance_records.append(attendance_record)

        return jsonify(attendance_records), 200

    elif request.method == 'POST':
        try:
            data = request.get_json()
            if not isinstance(data, list):
                return jsonify({'message': 'Invalid JSON data: Expected a list of dictionaries'}), 400
        except Exception as e:
            return jsonify({'message': 'Error parsing JSON data: ' + str(e)}), 400

        attendance_records = []

        for item in data:
            employee_id = item.get('emp_id')
            # department_id = item.get('dep_id')
            status = item.get('status')
            date_str = item.get('date')  # Define date_str here
            check_in_time = item.get('check_in_time')
            check_out_time = item.get('check_out_time')

            employee = Employee.query.get(employee_id)
            # department = Department.query.get(department_id)

            if not employee:
                return jsonify({'message': 'Employee not found'}), 404

            # if not department:
            #     return jsonify({'message': 'Department not found'}), 404
            
            # Parse the date string into a datetime object
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')  
            check_in_time = datetime.strptime(check_in_time, '%Y-%m-%d %H:%M') if check_in_time else None
            check_out_time = datetime.strptime(check_out_time, '%Y-%m-%d %H:%M') if check_out_time else None


            new_attendance = Attendance(
                status=status,
                date=date_obj,
                check_in_time=check_in_time,
                check_out_time=check_out_time,
                emp_id=employee_id,
            )

            db.session.add(new_attendance)

            attendance_record = {
                'id': new_attendance.id,
                # 'dep_id': department.id,
                'dep_name': department.name if employee.department else None,
                'emp_id': employee.id,
                'gender': employee.gender,
                'emp_name': employee.name,
                'status': new_attendance.status,
                'date': new_attendance.date.strftime('%Y-%m-%d'),  # Format the date
                'check_in_time': new_attendance.check_in_time.strftime('%Y-%m-%d %H:%M:%S') if new_attendance.check_in_time else None,
                'check_out_time': new_attendance.check_out_time.strftime('%Y-%m-%d %H:%M:%S') if new_attendance.check_out_time else None
            }
        attendance_records.append(attendance_record)


        db.session.commit()

        return jsonify({'message': 'Attendance created successfully', 'attendance_records': attendance_records}), 201

# API endpoint to get attendance record by ID
@app.route('/attendance/<int:attendance_id>', methods=['GET'])
def get_attendance_by_id(attendance_id):
    attendance = Attendance.query.get(attendance_id)
    if not attendance:
        return jsonify({'message': 'Attendance not found'}), 404

    department = Department.query.get(attendance.dep_id)
    employee = Employee.query.get(attendance.emp_id)

    if not department or not employee:
        return jsonify({'message': 'Related department or employee not found for this attendance record'}), 404

    attendance_record = {
        'id': attendance.id,
        'dep_id': department.id,
        'dep_name': department.name,
        'emp_id': employee.id,
        'emp_name': employee.name,
        'emp_gender': employee.gender,
        'status': attendance.status,
        'check_in_time': attendance.check_in_time.strftime('%Y-%m-%d %H:%M:%S') if attendance.check_in_time else None,
        'check_out_time': attendance.check_out_time.strftime('%Y-%m-%d %H:%M:%S') if attendance.check_out_time else None
    }

    return jsonify(attendance_record), 200

# API endpoint to delete attendance record by ID
@app.route('/attendance/<int:attendance_id>', methods=['DELETE'])
def delete_attendance(attendance_id):
    attendance = Attendance.query.get(attendance_id)
    if not attendance:
        return jsonify({'message': 'Attendance not found'}), 404

    db.session.delete(attendance)
    db.session.commit()
    return jsonify({'message': 'Attendance deleted successfully'}), 200
