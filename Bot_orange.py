import sys
from flask import Flask, request

app = Flask(__name__)

@app.route('/sms', methods=['POST', 'GET'])
def recevoir_sms():
    # Récupération des données
    data = request.form.to_dict()
    brut = request.get_data(as_text=True)
    
    # Affichage forcé
    print("--- 📩 REQUÊTE REÇUE ---", flush=True)
    print(f"DONNÉES FORM: {data}", flush=True)
    print(f"DONNÉES BRUTES: {brut}", flush=True)
    
    return "OK - Recu", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
