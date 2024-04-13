from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse, abort

app = Flask(__name__)
api = Api(app)

students = {}
next_student_id = 1

parser = reqparse.RequestParser()
parser.add_argument('name')
parser.add_argument('age')
parser.add_argument('grade')

class StudentList(Resource):
    def get(self):
        return students

    def post(self):
        args = parser.parse_args()
        student_id = generate_student_id()
        students[student_id] = {
            'name': args['name'],
            'age': args['age'],
            'grade': args['grade']
        }
        return students[student_id], 201

class Student(Resource):
    def get(self, student_id):
        if student_id not in students:
            abort(404, message="Student {} not found".format(student_id))
        return students[student_id]

    def put(self, student_id):
        if student_id not in students:
            abort(404, message="Student {} not found".format(student_id))
        args = parser.parse_args()
        students[student_id] = {
            'name': args['name'],
            'age': args['age'],
            'grade': args['grade']
        }
        return students[student_id], 200

    def delete(self, student_id):
        if student_id not in students:
            abort(404, message="Student {} not found".format(student_id))
        del students[student_id]
        return '', 204

api.add_resource(StudentList, '/students')
api.add_resource(Student, '/students/<int:student_id>')

def generate_student_id():
    global next_student_id
    current_id = next_student_id
    next_student_id += 1
    return current_id

@app.route('/')
def welcome():
    return "Welcome to Student Management Service!"

if __name__ == '__main__':
    app.run(debug=True, port=8000)
