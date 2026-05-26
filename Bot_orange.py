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
    data = request.json
    if not data:
        return jsonify({"status": "error", "message": "Aucune donnée reçue"}), 400
        
    numero_expediteur = str(data.get("from", "")).lower()
    texte_sms = str(data.get("msg", ""))
    
    print(f"\n📩 [SMS REÇU de {numero_expediteur}] : {texte_sms}")
    
    # Vérification de l'expéditeur ou du contenu pour plus de flexibilité
    if "454" in numero_expediteur:
        donnees = extraire_donnees_orange(texte_sms)
        if donnees:
            print(f"🍊 [ORANGE MONEY] Dépôt valide détecté !")
            print(f"   - Montant   : {donnees['montant']} FCFA | Client : {donnees['client']} | Ref : {donnees['reference']}")
            
    # On vérifie si "wave" est dans l'expéditeur OU dans le texte de la notification
    elif "wave" in numero_expediteur.lower() or "wave" in texte_sms.lower():
        donnees = extraire_donnees_wave(texte_sms)
        if donnees:
            print(f"🌊 [WAVE] Transaction valide détectée !")
            print(f"   - Montant   : {donnees['montant']} FCFA | Client : {donnees['client']} | Ref : {donnees['reference']}")
            
    else:
        print(f"❓ SMS/Notif ignoré (Expéditeur: {numero_expediteur})")
            
    return jsonify({"status": "success"}), 200

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 LE ROBOT MULTI-RÉSEAUX (ORANGE & WAVE) EST PRÊT ET EN LIGNE !")
    print("👉 En attente des SMS de ton smartphone...")
    print("=" * 60)
    app.run(host='0.0.0.0', port=5000)