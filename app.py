from flask import Flask, request, jsonify

app = Flask(__name__)

# Stockage temporaire (simulé en mémoire)
briefs = {}

@app.route('/nouveauBrief', methods=['POST'])
def nouveau_brief():
    data = request.json
    keyword = data.get('keyword')
    if keyword:
        briefs[keyword] = None  # Initialise le brief comme vide
        return jsonify({"status": "success", "message": f"Mot-clé '{keyword}' reçu."}), 200
    return jsonify({"status": "error", "message": "Aucun mot-clé reçu."}), 400

@app.route('/recupererBrief', methods=['GET'])
def recuperer_brief():
    for keyword, brief in briefs.items():
        if brief is not None:
            return jsonify({
                "keyword": keyword,
                "brief": brief,
                "status": "success"
            }), 200
    # S'il n'y a aucun brief rempli
    for keyword, brief in briefs.items():
        if brief is None:
            return jsonify({
                "keyword": keyword,
                "status": "pending"
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

@app.route('/reset', methods=['GET'])
def reset_briefs():
    global briefs
    briefs = {}
    return jsonify({"status": "reset", "message": "Mémoire vidée."}), 200

@app.route('/')
def home():
    return "API GPT Bridge active.", 200

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
