from flask import Flask, render_template, request, jsonify
import firebase_admin
from firebase_admin import credentials, firestore


app = Flask(__name__)

students = {}  # Dictionary to store student records

cred = credentials.Certificate("student-recored-management-firebase-adminsdk-fbsvc-30facad88f.json")  # Update path
firebase_admin.initialize_app(cred)

db = firestore.client()
students_ref = db.collection('students')

@app.route("/", methods=['GET'])
def index():
    return render_template("index.html")

@app.route('/add', methods=['POST'])
def add():
    data = request.get_json()
    stdid = str(data.get('id'))
    name = data.get('name')
    age = data.get('age')
    gender = data.get('gender')

    if not stdid:
        return jsonify({"error": "Student ID is required"}), 400

    students[stdid] = {'id': stdid, 'name': name, 'age': age, 'gender': gender}
    students_ref.document(stdid).set(data)

    return jsonify({"message": "Student added successfully!", "students": students})

@app.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    stdid = data.get('id')  # Convert to string to match dictionary keys

    if stdid in students:
        return jsonify({"message": "Student found!", "student": students[stdid]})
    else:
        return jsonify({"error": "Student not found"})


@app.route('/update', methods=['POST'])
def update():
    data = request.get_json()
    stdid = str(data.get('id'))

    if stdid in students:
        students[stdid] = {
            'id': stdid,
            'name': data.get('name'),
            'age': data.get('age'),
            'gender': data.get('gender')
        }
        return jsonify({"message": "Student updated successfully!", "students": students})
    else:
        return jsonify({"error": "Student not found"}), 404

@app.route('/delete', methods=['POST'])
def delete():
    data = request.get_json()
    stdid = str(data.get('id'))

    if stdid in students:
        del students[stdid]
        return jsonify({"message": "Student deleted successfully!", "students": students})
    else:
        return jsonify({"error": "Student not found"}), 404

if __name__ == "__main__":
    app.run(port=5000,host='0.0.0.0')
