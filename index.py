import sqlite3
import os
from flask import Flask, request, jsonify, render_template, send_file
from flask_cors import CORS

app = Flask(__name__, template_folder='.', static_folder='.')
CORS(app)

DB_NAME = 'quantum_users.db' 

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (contact TEXT PRIMARY KEY, password TEXT)''')
    conn.commit()
    conn.close()

init_db()

# --- RUTAS DE PÁGINAS ---
@app.route('/')
def page_register():
    return render_template('index.html')

@app.route('/login.html')
def page_login():
    return render_template('login.html')

@app.route('/checker.html')
def page_checker():
    return render_template('checker.html')

# --- RUTAS DE DESCARGA (LOS DOS ARCHIVOS) ---
@app.route('/download-key')
def download_key():
    try:
        # Descarga TU archivo original
        return send_file('QuantumAUTH.exe', as_attachment=True)
    except Exception as e:
        return f"Error: Falta QuantumAUTH.exe"

@app.route('/download-activator')
def download_activator():
    try:
        # Descarga el Activador del servidor
        return send_file('Activator.exe', as_attachment=True)
    except Exception as e:
        return f"Error: Falta Activator.exe"

# --- API REGISTRO/LOGIN ---
@app.route('/register', methods=['POST'])
def api_register():
    try:
        data = request.json
        contact = data.get('contact')
        password = data.get('password')
        if not contact or not password:
            return jsonify({"status": "error", "message": "Faltan datos"}), 400
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (contact, password) VALUES (?, ?)", (contact, password))
            conn.commit()
            return jsonify({"status": "success", "redirect": "/checker.html"})
        except:
            return jsonify({"status": "error", "message": "Usuario existe"}), 409
        finally:
            conn.close()
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/login', methods=['POST'])
def api_login():
    try:
        data = request.json
        contact = data.get('contact')
        password = data.get('password')
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE contact=? AND password=?", (contact, password))
        user = c.fetchone()
        conn.close()
        if user:
            return jsonify({"status": "success", "redirect": "/checker.html"})
        return jsonify({"status": "error", "message": "Datos incorrectos"}), 401
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
