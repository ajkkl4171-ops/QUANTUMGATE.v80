import time
import threading
from flask import Flask
from flask_cors import CORS
import webbrowser

app = Flask(__name__)
CORS(app) # Importante para que el navegador no bloquee la conexión local

@app.route('/heartbeat')
def heartbeat():
    return {"status": "secure_access_granted", "key": "quantum_v8_auth"}

if __name__ == '__main__':
    print(">>> QUANTUM AUTH v2.1 ACTIVO")
    print(">>> NO CIERRES ESTA VENTANA")
    try:
        # Se ejecuta localmente en el puerto 1337
        app.run(host='127.0.0.1', port=1337, debug=False)
    except:
        print("Error: Puerto 1337 ocupado.")
        input()