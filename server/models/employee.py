from app import  db, ma
from flask import  jsonify, request
from sqlalchemy import ForeignKey
from datetime import datetime
from marshmallow import Schema, fields


class MyUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)


# class User(db.Model):
#     id = db.Column(db.Integer,  primary_key=True)
#     name = db.Column(db.String(220), nullable=False)
#     email = db.Column(db.String(400), unique=True, nullable=False)
#     dep = db.Column(db.String(400), unique=False, nullable=False)
    # dep_id = db.Column(db.Integer, db.ForeignKey('department.id'))



class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(220), nullable=False)
    attan = db.relationship('Attendance', backref='department', lazy=True)
    emp = db.relationship('Employee', backref='department_emp', lazy=True)



class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(220), nullable=False)
    email = db.Column(db.String(400), unique=True, nullable=False)
    salary = db.Column(db.Integer, nullable=False)
    role = db.Column(db.String(400), nullable=False)
    gender = db.Column(db.String(400), nullable=False)
    phone = db.Column(db.Integer, unique=True, nullable=False)
    dep_id = db.Column(db.Integer, db.ForeignKey('department.id'))
    department = db.relationship('Department', backref='employees', lazy=True, overlaps="department_emp,emp")
    created_by = db.Column(db.Integer, db.ForeignKey('my_user.id'))
    updated_by = db.Column(db.Integer, db.ForeignKey('my_user.id'))
    attan = db.relationship('Attendance', backref='employee', lazy=True)



class Attendance(db.Model):
    __tablename__ = 'attendance'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    date = db.Column(db.Date, nullable=False)
    check_in_time = db.Column(db.DateTime, nullable=True)
    check_out_time = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(100), nullable=False)
    dep_id = db.Column(db.Integer, db.ForeignKey('department.id'))
    emp_id = db.Column(db.Integer, db.ForeignKey('employee.id'))

    
class Leave(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    leave_type = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    on_date = db.Column(db.Date, nullable=False)
    from_date = db.Column(db.Date, nullable=False)
    to_date = db.Column(db.Date, nullable=False)      
    dep_id = db.Column(db.Integer, db.ForeignKey('department.id'))
    emp_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    employee = db.relationship('Employee', backref='leaves', lazy=True)

class Payroll(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    # department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)
    employee = db.relationship('Employee', backref='payrolls', lazy=True)
    basic_salary = db.Column(db.Integer, nullable=False)
    totalSalary = db.Column(db.Integer, nullable=False)
    payment_date = db.Column(db.Date, nullable=False)
    payment_method = db.Column(db.String(100), nullable=True)  
    deductions = db.Column(db.Integer, nullable=True)  
    payroll_period = db.Column(db.String(50), nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey('my_user.id'))
    updated_by = db.Column(db.Integer, db.ForeignKey('my_user.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"Payroll(id={self.id}, employee_id={self.employee_id}, salary={self.salary}, payment_date={self.payment_date})"



# Define your Marshmallow schema in the same file
class DepartmentSchema(ma.Schema):
    class Meta:
        model = Department

class EmployeeSchema(ma.Schema):
    class Meta:
        model = Employee

class AttendanceSchema(ma.Schema):
    class Meta:
        model = Attendance

class LeaveSchema(ma.Schema):
    class Meta:
        model = Leave

class PayrollSchema(ma.Schema):
    class Meta:
        model = Payroll


# Initialize the schemas
department_schema = DepartmentSchema()
employee_schema = EmployeeSchema()
attendance_schema = AttendanceSchema(many=True)
leave_schema = LeaveSchema()
payroll_schema = PayrollSchema()



