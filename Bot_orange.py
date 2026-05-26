import re
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/sms', methods=['POST'])
def recevoir_sms():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"status": "error"}), 400
    
    msg = data.get("msg", "")
    
    # Extraction du montant (recherche un nombre suivi de FCFA)
    montant_match = re.search(r'(\d+(?:\.\d+)?)\s*FCFA', msg)
    # Extraction du numéro de téléphone (recherche 8 ou 9 chiffres)
    num_match = re.search(r'(\d{8,9})', msg)
    
    montant = montant_match.group(1) if montant_match else "Non trouvé"
    numero = num_match.group(1) if num_match else "Non trouvé"
    
    print(f"--- ✅ TRANSACTION DÉTECTÉE ---")
    print(f"Montant : {montant} FCFA")
    print(f"Numéro client : {numero}")
    
    return jsonify({"status": "success"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
