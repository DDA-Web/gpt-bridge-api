from flask import Flask, request, jsonify

app = Flask(__name__)

# Stockage temporaire (en mémoire)
briefs = {}
last_keyword = None  # 🔧 nouvelle variable globale

@app.route('/nouveauBrief', methods=['POST'])
def nouveau_brief():
    global last_keyword
    data = request.json
    keyword = data.get('keyword')
    if keyword:
        briefs[keyword] = None
        last_keyword = keyword  # 🆕 on garde le dernier mot-clé reçu
        return jsonify({"status": "success", "message": f"Mot-clé '{keyword}' reçu."}), 200
    return jsonify({"status": "error", "message": "Aucun mot-clé reçu."}), 400

@app.route('/recupererBrief', methods=['GET'])
def recuperer_brief():
    if last_keyword and briefs.get(last_keyword):
        return jsonify({
            "keyword": last_keyword,
            "brief": briefs[last_keyword],
            "status": "success"
        }), 200
    return jsonify({"message": "Aucun brief disponible pour le moment."}), 200

@app.route('/enregistrerBrief', methods=['POST'])
def enregistrer_brief():
    data = request.json
    keyword = data.get('keyword')
    brief = data.get('brief')
    if keyword and brief:
        briefs[keyword] = brief
        return jsonify({"status": "success", "message": "Brief enregistré."}), 200
    return jsonify({"status": "error", "message": "Mot-clé ou brief manquant."}), 400

@app.route('/')
def home():
    return "API GPT Bridge active.", 200

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
