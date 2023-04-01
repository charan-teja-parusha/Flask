from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate
import psycopg2

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://charan:Momdad9244@localhost:5432/example_db'
app.config['SQLALCHEMY_SCHEMA'] = 'example_schema'
db = SQLAlchemy(app)

migrate = Migrate(app, db)

class Student(db.Model):
    __tablename__ = 'students'
    student_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    amount_due = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return '<Student %r>' % self.first_name

@app.route('/students', methods=['POST'])
def create_student():
    data = request.get_json()
    new_student = Student(student_id=data['student_id'],
                          first_name=data['first_name'],
                          last_name=data['last_name'],
                          dob=datetime.strptime(data['dob'], '%Y-%m-%d'),
                          amount_due=data['amount_due'])
    db.session.add(new_student)
    db.session.commit()
    return jsonify({'message': 'Student created successfully!'})

@app.route('/students', methods=['GET'])
def get_students():
    students = Student.query.all()
    return jsonify([{'student_id': student.student_id,
                     'first_name': student.first_name,
                     'last_name': student.last_name,
                     'dob': student.dob.strftime('%Y-%m-%d'),
                     'amount_due': student.amount_due} for student in students])

@app.route('/students/<int:id>', methods=['GET'])
def get_student(id):
    student = Student.query.get(id)
    if not student:
        return jsonify({'message': 'Student not found'}), 404
    return jsonify({'student_id': student.student_id,
                    'first_name': student.first_name,
                    'last_name': student.last_name,
                    'dob': student.dob.strftime('%Y-%m-%d'),
                    'amount_due': student.amount_due})

@app.route('/students/<int:id>', methods=['PUT'])
def update_student(id):
    student = Student.query.get(id)
    if not student:
        return jsonify({'message': 'Student not found'}), 404
    data = request.get_json()
    if 'student_id' in data:
        student.student_id = data['student_id']
    if 'first_name' in data:
        student.first_name = data['first_name']
    if 'last_name' in data:
        student.last_name = data['last_name']
    if 'dob' in data:
        student.dob = datetime.strptime(data['dob'], '%Y-%m-%d')
    if 'amount_due' in data:
        student.amount_due = data['amount_due']
    db.session.commit()
    return jsonify({'message': 'Student updated successfully!'})


@app.route('/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    student = Student.query.get(id)
    if not student:
        return jsonify({'message': 'Student not found'}), 404
    db.session.delete(student)
    db.session.commit()
    return jsonify({'message': 'Student deleted successfully!'})


if __name__ == "__main__":
    app.run(debug=True)
