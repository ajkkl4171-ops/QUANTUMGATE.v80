import sqlite3
import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

# Configuración limpia para Render
# Buscamos 'templates' en la misma carpeta que este archivo
app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)

# Base de datos local
DB_NAME = 'quantum_users.db' 

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    try:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users 
                     (contact TEXT PRIMARY KEY, password TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"DB Error: {e}")

# Inicializamos la DB al arrancar
init_db()

# --- RUTAS DE NAVEGACIÓN ---

@app.route('/')
def serve_index():
    return render_template('index.html')

@app.route('/login.html')
def serve_login_page():
    return render_template('login.html')

@app.route('/checker.html')
def serve_checker():
    return render_template('checker.html')

# --- API ENDPOINTS ---

@app.route('/register', methods=['POST'])
def register_user():
    try:
        data = request.json
        contact = data.get('contact')
        password = data.get('password')

        if not contact or not password:
            return jsonify({"status": "error", "message": "Campos incompletos"}), 400

        conn = get_db_connection()
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (contact, password) VALUES (?, ?)", (contact, password))
            conn.commit()
            return jsonify({"status": "success", "redirect": "/checker.html"})
        except sqlite3.IntegrityError:
            return jsonify({"status": "error", "message": "El usuario ya existe"}), 409
        finally:
            conn.close()
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
        else:
            return jsonify({"status": "error", "message": "Credenciales inválidas"}), 401
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    # Render asigna el puerto mediante la variable de entorno PORT
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
