from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask_cors import CORS
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)  # This will allow all origins

# Database configuration
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_DIALECT = os.getenv('DB_DIALECT')

DATABASE_URL = f"{DB_DIALECT}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Define Grade table model
class Grade(db.Model):
    __tablename__ = 'grade'
    __table_args__ = {'schema': 'school-schema'}
    row_id = db.Column(db.Integer, primary_key=True)
    grade_name = db.Column(db.String, unique=True, nullable=False)

# Define Student table model
class Student(db.Model):
    __tablename__ = 'student'
    __table_args__ = {'schema': 'school-schema'}
    row_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    grade = db.Column(db.Integer, db.ForeignKey('school-schema.grade.row_id'), nullable=False)

# Create the database tables
with app.app_context():
    db.create_all()

# Add sample data for grades
def add_sample_grades():
    grade_names = ['Kindergarten', 'First Grade', 'Second Grade', 'Third Grade', 'Fourth Grade', 
                   'Fifth Grade', 'Sixth Grade', 'Seventh Grade', 'Eighth Grade', 'Freshman', 
                   'Sophomore', 'Junior', 'Senior']
    for name in grade_names:
        grade = Grade(grade_name=name)
        db.session.add(grade)
    db.session.commit()

# Uncomment this line to add sample grades the first time you run the script
# with app.app_context():
#     add_sample_grades()

# Define a route to fetch all students
@app.route('/students', methods=['GET'])
def get_students():
    students = Student.query.all()
    result = [
        {'row_id': student.row_id, 'first_name': student.first_name, 
         'last_name': student.last_name, 'grade': student.grade} 
        for student in students
    ]
    print(students)
    print(result)
    return jsonify(result)

# Define a route to create a new student
@app.route('/students', methods=['POST'])
def create_student():
    data = request.json
    new_student = Student(
        first_name=data['first_name'],
        last_name=data['last_name'],
        grade=data['grade']
    )
    db.session.add(new_student)
    db.session.commit()
    return jsonify({'message': 'Student created successfully'}), 201

# Define a route to fetch all grades
@app.route('/grades', methods=['GET'])
def get_grades():
    grades = Grade.query.all()
    result = [{'row_id': grade.row_id, 'grade_name': grade.grade_name} for grade in grades]
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
