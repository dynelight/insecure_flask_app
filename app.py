from flask import Flask, request, render_template, redirect, make_response
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    # Vulnerable to SQL Injection
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    cursor.execute(query)
    user = cursor.fetchone()
    conn.close()

    if user:
        # Insecure cookie handling, no HttpOnly/secure flag
        resp = make_response(redirect('/dashboard'))
        resp.set_cookie('user', username)
        return resp
    else:
        return "Login Failed", 401

@app.route('/dashboard')
def dashboard():
    user = request.cookies.get('user')
    return f"Welcome, {user}!"
