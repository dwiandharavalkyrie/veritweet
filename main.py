from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import tensorflow as tf
import numpy as np
import json
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Tambahkan secret key untuk session

# Konfigurasi Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://dwiandharavalkyrie:Ra867293@localhost/skripsi'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Model User
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# Inisialisasi Database
with app.app_context():
    db.create_all()

# Route Halaman Utama
@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')  # Pastikan index.html ada di folder templates

# Route Sign Up - GET untuk menampilkan halaman signup
@app.route('/signup', methods=['GET'])
def signup_form():
    return render_template('signup.html')  # Pastikan signup.html ada di folder templates

# Route Home Setelah Login
@app.route('/home', methods=['GET'])
def home_page():
    if 'user_id' in session:  # Periksa apakah user sudah login
        return render_template('home.html')  # Merender file home.html
    return redirect(url_for('home'))  # Redirect ke index jika belum login

@app.route('/deteksi-hoaks', methods=['GET'])
def deteksi_hoaks():
    return render_template('deteksi-hoaks.html')  # Render file deteksi-hoaks.html

# Route Sign Up - POST untuk menerima data signup
@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'])
    new_user = User(username=data['username'], email=data['email'], password=hashed_password)
    
    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User created successfully!"}), 201
    except:
        return jsonify({"message": "Error: Username or email already exists!"}), 400

# Route Login - GET untuk menampilkan halaman login
@app.route('/login', methods=['GET'])
def login_form():
    return render_template('login.html')  # Pastikan login.html ada di folder templates

# Route Login - POST untuk memproses login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user and check_password_hash(user.password, data['password']):
        session['user_id'] = user.id  # Simpan user ID di session
        return jsonify({"message": "Login successful!", "redirect": url_for('home_page')}), 200
    return jsonify({"message": "Invalid email or password!"}), 401

# Route Logout
@app.route('/logout', methods=['GET'])
def logout():
    session.pop('user_id', None)  # Hapus sesi login
    return redirect(url_for('home'))  # Kembali ke halaman utama

if __name__ == '__main__':
    app.run(debug=True)
