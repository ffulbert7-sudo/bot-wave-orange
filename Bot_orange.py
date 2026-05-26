from flask import Flask, request, jsonify
import re

app = Flask(__name__)

@app.route('/sms', methods=['POST'])
def recevoir_sms():
    # --- DEBUG TOTAL ---
    print(f"--- REQUÊTE REÇUE ---")
    print(f"Données brutes (Form): {request.form}")
    print(f"Données brutes (JSON): {request.get_json(silent=True)}")
    
    # On force la lecture des données pour voir ce qu'il y a dedans
    data = request.get_json(silent=True) or request.form.to_dict()
    
    if not data:
        print("❌ Aucune donnée trouvée dans la requête")
        return jsonify({"status": "error"}), 400
    
    numero_expediteur = str(data.get("from", "vide")).lower()
    texte_sms = str(data.get("msg", "vide"))
    
    print(f"EXPEDITEUR: {numero_expediteur}")
    print(f"MESSAGE: {texte_sms}")
    
    # On retourne un succès pour que ton téléphone arrête de réessayer
    return jsonify({"status": "success"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
