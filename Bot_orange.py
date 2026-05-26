from flask import Flask, request, jsonify
import re

app = Flask(__name__)

def extraire_donnees_orange(sms_texte):
    montant_match = re.search(r"transfert de ([\d.]+)\s*FCFA", sms_texte)
    client_match = re.search(r"du\s+(\d+)", sms_texte)
    ref_match = re.search(r"Reference\s+([A-Z0-9.]+)", sms_texte)
    
    if montant_match and client_match and ref_match:
        return {
            "montant": float(montant_match.group(1)),
            "client": client_match.group(1).strip(),
            "reference": ref_match.group(1).strip()
        }
    return None

def extraire_donnees_wave(sms_texte):
    # Cherche le montant (ex: 1000 FCFA)
    montant_match = re.search(r"([\d.,]+)\s*FCFA", sms_texte, re.IGNORECASE)
    client_match = re.search(r"\b(\d{10})\b", sms_texte)
    ref_match = re.search(r"(?:Id|Réf\.|Ref)[:\s]*([A-Z0-9_-]+)", sms_texte, re.IGNORECASE)
    
    if montant_match:
        montant_str = montant_match.group(1).replace('.', '').replace(',', '')
        montant = float(montant_str)
        client = client_match.group(1).strip() if client_match else "Inconnu"
        reference = ref_match.group(1).strip() if ref_match else "WAVE_REF_AUTO"
        return {"montant": montant, "client": client, "reference": reference}
    return None

@app.route('/sms', methods=['POST'])
def recevoir_sms():
    # 1. Tenter de lire les données (supporte JSON ou Form-Data)
    data = request.get_json(silent=True)
    if not data:
        data = request.form.to_dict()
        
    if not data:
        return jsonify({"status": "error", "message": "Aucune donnée"}), 400
        
    numero_expediteur = str(data.get("from", "")).lower()
    texte_sms = str(data.get("msg", ""))
    
    # 2. DEBUG : Affiche tout dans les logs pour comprendre pourquoi ça bloque
    print(f"\n--- RECEPTION ---")
    print(f"EXPEDITEUR: {numero_expediteur}")
    print(f"MESSAGE: {texte_sms}")
    
    # 3. Logique de détection
    if "454" in numero_expediteur:
        donnees = extraire_donnees_orange(texte_sms)
        if donnees:
            print(f"✅ [ORANGE MONEY] {donnees['montant']} FCFA reçu de {donnees['client']}")
        else:
            print("❌ Orange reçu mais données non extraites (vérifie le format du texte)")
            
    elif "wave" in numero_expediteur.lower() or "wave" in texte_sms.lower():
        donnees = extraire_donnees_wave(texte_sms)
        if donnees:
            print(f"✅ [WAVE] {donnees['montant']} FCFA reçu de {donnees['client']}")
        else:
            print("❌ Wave reçu mais données non extraites (vérifie le format du texte)")
    else:
        print(f"❓ Message ignoré (ne contient ni '454' ni 'wave')")
            
    return jsonify({"status": "success"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
