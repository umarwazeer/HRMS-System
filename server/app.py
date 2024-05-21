from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import os
import mysql.connector
import random  # Add this line to import the random module
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_migrate import Migrate
from flask_cors import CORS
from flask_marshmallow import Marshmallow  # Import Flask-Marshmallowz
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)

def generate_secret_key(length):
    characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    secret_key = ''.join(random.choice(characters) for i in range(length))
    return secret_key

# mysql://username:password@server/db
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:mypassword@localhost:3306/HRM'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
engine = create_engine('mysql+mysqlconnector://root:mypassword@localhost:3306/HRM')
Session = sessionmaker(bind=engine)
migrate = Migrate(app, db)
ma = Marshmallow(app)
secret_key = os.urandom(24)
app.config['JWT_SECRET_KEY'] = generate_secret_key(32)
jwt = JWTManager(app)
CORS(app)


# import the controllers is Here                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    z
from controllers.emp_controller import *
from controllers.user_controller import *
from controllers.dep_controller import *
from controllers.attendance_controller import *
from controllers.Authentication import *
from controllers.leave_controller import *
from controllers.payroll_controller import *
from controllers.EmployeeReports.EmployeeDetails import *  # Import EmployeeDetails module




if __name__ == '__main__':
    app.run(debug=True, port=2024)
