import re
import sys
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/sms', methods=['POST'])
def recevoir_sms():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"status": "error"}), 400
    
    msg = data.get("msg", "")
    print(f"DEBUG: Message reçu : {msg}", flush=True)
    
    # Correction : cherche soit "FCFA", soit "F" après un nombre
    montant_match = re.search(r'(\d+(?:\.\d+)?)\s*F', msg)
    num_match = re.search(r'(\d{8,9})', msg)
    
    montant = montant_match.group(1) if montant_match else "Non trouvé"
    numero = num_match.group(1) if num_match else "Non trouvé"
    
    print(f"--- ✅ TRANSACTION DÉTECTÉE ---", flush=True)
    print(f"Montant : {montant} F", flush=True)
    print(f"Numéro client : {numero}", flush=True)
    
    return jsonify({"status": "success"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
