from flask import Flask, request, session, jsonify, redirect
from flask_cors import CORS
import pymysql.cursors
import hashlib

app = Flask(__name__)

app.secret_key = 'secret key'

app.config['SESSION_COOKIE_SAMESITE'] = 'None'
app.config['SESSION_COOKIE_SECURE'] = False

CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

conn = pymysql.connect(host='localhost',
                        port = 8889,
                        user='root',
                        password='root',
                        db='borderx',
                        charset='utf8mb4',
                        cursorclass=pymysql.cursors.DictCursor)

@app.route('/')
def home():
    return redirect("http://localhost:4173", code=200)

@app.route('/register', methods=["POST"]) 
def register():
    data = request.json
    print(data)
    
    if not data.get("username") or not data.get("email") or not data.get("password"):
        return jsonify({"error": "All fields are required"}), 400
    
    username = data.get("username")
    password = hash_password_md5(data.get("password"))
    email = data.get("email")
    
    cursor = conn.cursor()
    
    query = 'SELECT * FROM users WHERE email = %s'
    cursor.execute(query, (email,))
    
    ret_email = cursor.fetchone() 
    
    query = 'SELECT * FROM users WHERE username = %s'
    cursor.execute(query, (username,))
    
    ret_user = cursor.fetchone() 
    
    if ret_email:
        return jsonify({"error": "Email already registered"}), 400
    
    if ret_user:
        return jsonify({"error": "This username already exists"}), 400
    
    ins = 'INSERT INTO users (username, password_hash, email) VALUES(%s, %s, %s)'
    cursor.execute(ins, (username, password, email))
    
    conn.commit()
    cursor.close()
    
    return jsonify({"message": "User registered successfully"}), 201
    

@app.route('/login', methods=["POST"]) 
def login():
    data = request.json
    
    if not data.get("username") or not data.get("password"):
        return jsonify({"error": "All fields are required"}), 400
    
    username = data.get("username")
    password = hash_password_md5(data.get("password"))
    
    cursor = conn.cursor()
    
    query = 'SELECT * FROM users WHERE username = %s'
    cursor.execute(query, (username))
    
    ret_user = cursor.fetchone()
    
    if ret_user and ret_user['password_hash'] == password:
        session["username"] = username
        return jsonify({"message": "User logged in successfully"}), 201
    
    return jsonify({"error": "Username and password do not match"}), 400

@app.route('/appointments', methods=["POST"])
def add_appointment():    
    if "username" not in session:
        return jsonify({"error": "User not logged in"}), 401
    
    data = request.json
    
    username = session['username']
    
    name = data.get("name")
    email = data.get("email")
    phone = data.get("phone")
    date = data.get("date")
    time = data.get("time")
    notes = data.get("notes")
    
    cursor = conn.cursor() 
    
    ins = 'INSERT INTO appointments VALUES(%s, %s, %s, %s, %s, %s, %s)'
    cursor.execute(ins, (name, email, phone, date, time, notes, username))
    
    conn.commit()
    cursor.close()
    
    return jsonify({"message": "Appointment added successfully"}), 201

@app.route('/appointments', methods=["GET"])
def get_appointments():    
    session['username'] = 'b@gmail.com'
    if "username" not in session:
        return jsonify({"error": "User not logged in"}), 401
    
    username = session['username']
    
    cursor = conn.cursor()

    query = 'SELECT * FROM appointments WHERE user_id = %s'
    cursor.execute(query, (username,))
    
    appointments = cursor.fetchall()
    
    return jsonify({"data": appointments, "message": "appointments successfully retrieved"}), 200

@app.after_request
def after_request(response):
    response.headers.add("Access-Control-Allow-Origin", "http://localhost:4173/")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
    response.headers.add("Access-Control-Allow-Credentials", "true")
    return response

def hash_password_md5(password):
    md5 = hashlib.md5()
    md5.update(password.encode('utf-8'))
    return md5.hexdigest()

if __name__ == "__main__":
    app.run('localhost', 5000, debug = True)