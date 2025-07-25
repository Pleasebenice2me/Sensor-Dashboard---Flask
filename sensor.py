from flask import Flask, render_template, request, jsonify
from collections import deque
from datetime import datetime

app = Flask(__name__)

# Historique des données (limité à 100 points)
history = deque(maxlen=100)

@app.route('/')
def dashboard():
    # Pour afficher la dernière donnée dans les cards (dashboard)
    latest_data = history[-1] if history else {
        "battery": None,
        "humidity": None,
        "nh3": None,
        "temperature": None
    }
    return render_template('index.html', data=latest_data)

@app.route('/update', methods=['POST'])
def update_data():
    content = request.json
    if content:
        # Ajouter un timestamp à chaque donnée reçue
        content['timestamp'] = datetime.now().strftime("%H:%M:%S")
        history.append(content)
        return jsonify({"message": "Données reçues"}), 200
    return jsonify({"error": "Aucune donnée reçue"}), 400

@app.route('/history', methods=['GET'])
def get_history():
    # Renvoie tout l'historique
    return jsonify(list(history))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


