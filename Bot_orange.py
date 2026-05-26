from flask import Flask, request

app = Flask(__name__)

@app.route('/sms', methods=['POST', 'GET'])
def recevoir_sms():
    print("--- 📩 REQUÊTE REÇUE ---")
    print(f"Données: {request.values.to_dict()}")
    print(f"Corps brut: {request.get_data(as_text=True)}")
    return "OK", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
