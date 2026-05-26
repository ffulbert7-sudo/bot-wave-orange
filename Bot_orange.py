from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/sms', methods=['POST'])
def recevoir_sms():
    # Récupérer les données JSON envoyées par l'app
    data = request.get_json(silent=True)
    
    print("--- 📩 REQUÊTE REÇUE ---")
    print(f"Données reçues : {data}")
    
    if data:
        expediteur = data.get("from", "Inconnu")
        message = data.get("msg", "Vide")
        print(f"Expéditeur : {expediteur}")
        print(f"Message : {message}")
        return jsonify({"status": "success"}), 200
    else:
        print("❌ Aucune donnée JSON valide reçue")
        return jsonify({"status": "error", "message": "No JSON"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
