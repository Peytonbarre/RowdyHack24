from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_mongoengine import MongoEngine

###
### Configuration
###
app = Flask(__name__)
CORS(app)
app.config['MONGODB_SETTINGS'] = {
    'host': 'YOUR_MONGODB_URI'
}
db = MongoEngine(app)

###
### Classes
###
class Teacher(db.Document):
    username = db.StringField(required=True, unique=True)
    email = db.StringField(required=True)
    password = db.StringField(required=True)

class Students(db.Document):
    username = db.StringField(required=True, unique=True)
    email = db.StringField(required=True)
    password = db.StringField(required=True)
    teacher = db.StringField(required=True)

class Assignment(db.Document):
    id = db.StringField(required=True, unique=True)
    name = db.StringField(required=True)
    content = db.FileField(required=True)
    dueDate = db.DateTimeField(required=True)

class Itrack(db.Document):
    student = db.StringField(required=True)
    xpos = db.IntField(required=True)
    ypos = db.IntField(required=True)
    time = db.DateTimeField(required=True)

@app.route("/")
def helloWorld():
    return "<p>Hello World</p>"

###
### Teachers
###
@app.route("/teacher", method=["POST"])
def addTeacher():
    data = request.json()
    new_teacher = Teacher(
        username=data['username'],
        email=data['email'],
        password=data['password']
    )
    try:
        new_teacher.save()
        return jsonify({"message": "User created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

###
### Students
###
@app.route("/student", method=["POST"])
def addStudent():
    data = request.json()
    new_student = Teacher(
        username=data['username'],
        email=data['email'],
        password=data['password'],
        teacher=data['teacher']
    )
    teacher = Teacher.objects(username=data['teacher']).first()
    if teacher is not None:
        try:
            new_student.save()
            return jsonify({"message": "User created successfully"}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "Teacher not found"}), 500

###
### Assignments
###
@app.route("/assignment", method=["POST"])
def addAssignment():
    data = request.json()
    new_Assignment = Teacher(
        id=data['id'],
        name=data['name'],
        content=data['content'],
        dueDate = data['dueDate']
    )
    try:
        new_Assignment.save()
        return jsonify({"message": "User created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
###
### Itrack
###
@app.route("/itrack", method=["POST"])
def addtracker():
    data = request.json()
    new_tracker = Teacher(
        student=data['student'],
        position=data['position'],
        time=data['time'],
    )
    try:
        new_tracker.save()
        return jsonify({"message": "User created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

###
### Run app
###
if __name__ == "__main__":
    app.run()