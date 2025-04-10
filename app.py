from flask import Flask, request, jsonify

app = Flask(__name__)

# Mémoire en RAM
briefs = {}

@app.route('/nouveauBrief', methods=['POST'])
def nouveau_brief():
    data = request.json
    keyword = data.get('keyword')
    if keyword:
        if keyword not in briefs:
            briefs[keyword] = None
            return jsonify({"status": "success", "message": f"Mot-clé '{keyword}' reçu."}), 200
        else:
            return jsonify({"status": "already_exists", "message": "Mot-clé déjà enregistré."}), 200
    return jsonify({"status": "error", "message": "Aucun mot-clé reçu."}), 400

@app.route('/recupererBrief', methods=['GET'])
def recuperer_brief():
    # Trouver tous les briefs encore None
    pending_briefs = [(kw, ts) for kw, ts in briefs.items() if ts is None]

    if not pending_briefs:
        return jsonify({"message": "Aucun mot-clé en attente."}), 200

    # Récupérer le dernier ajouté (ordre d'insertion conservé en Python 3.7+)
    last_keyword = list(briefs.keys())[::-1]
    for kw in last_keyword:
        if briefs[kw] is None:
            return jsonify({"keyword": kw}), 200

    return jsonify({"message": "Aucun mot-clé en attente."}), 200

@app.route('/enregistrerBrief', methods=['POST'])
def enregistrer_brief():
    data = request.json
    keyword = data.get('keyword')
    brief = data.get('brief')
    if keyword and brief:
        if keyword in briefs:
            briefs[keyword] = brief
            return jsonify({"status": "success", "message": "Brief enregistré."}), 200
        else:
            return jsonify({"status": "error", "message": "Mot-clé introuvable."}), 404
    return jsonify({"status": "error", "message": "Mot-clé ou brief manquant."}), 400

@app.route('/reset', methods=['GET'])
def reset():
    briefs.clear()
    return jsonify({"status": "reset", "message": "Mémoire vidée."}), 200

@app.route('/')
def home():
    return "API GPT Bridge active.", 200

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)