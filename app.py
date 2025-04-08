from flask import Flask, request, jsonify

app = Flask(__name__)

# Stockage temporaire (pour simplifier)
briefs = {}

@app.route('/nouveauBrief', methods=['POST'])
def nouveau_brief():
    data = request.json
    keyword = data.get('keyword')
    if keyword:
        # Pour le moment, on stocke juste le mot-clé
        briefs[keyword] = None  # Brief vide pour le moment
        return jsonify({"status": "success", "message": f"Mot-clé '{keyword}' reçu."}), 200
    return jsonify({"status": "error", "message": "Aucun mot-clé reçu."}), 400

@app.route('/recupererBrief', methods=['GET'])
def recuperer_brief():
    # Pour l'instant, renvoie simplement le premier mot-clé en attente
    for keyword, brief in briefs.items():
        if brief is None:
            return jsonify({"keyword": keyword}), 200
    return jsonify({"message": "Aucun mot-clé en attente."}), 200

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
    app.run(debug=True)
