import sqlite3
import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Base de Datos: En servidores como Render, /tmp se borra al reiniciar.
# Si quieres persistencia real, usa una base de datos externa.
DB_NAME = 'users.db'

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (contact TEXT PRIMARY KEY, password TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def serve_index():
    return render_template('index.html')

@app.route('/login.html')
def serve_login():
    return render_template('login.html')

@app.route('/checker.html')
def serve_checker():
    return render_template('checker.html')

@app.route('/register', methods=['POST'])
def register_user():
    try:
        data = request.json
        contact = data.get('contact')
        password = data.get('password')
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("INSERT INTO users (contact, password) VALUES (?, ?)", (contact, password))
        conn.commit()
        conn.close()
        return jsonify({"status": "success", "redirect": "/checker.html"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/login', methods=['POST'])
def login_user():
    try:
        data = request.json
        contact = data.get('contact')
        password = data.get('password')
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE contact=? AND password=?", (contact, password))
        user = c.fetchone()
        conn.close()
        if user:
            return jsonify({"status": "success", "redirect": "/checker.html"})
        return jsonify({"status": "error", "message": "Credenciales inválidas"}), 401
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    # El puerto lo asigna el servidor automáticamente
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)