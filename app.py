from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

briefs = []

@app.route("/nouveauBrief", methods=["POST"])
def nouveau_brief():
    data = request.json
    keyword = data.get("keyword")
    if not keyword:
        return jsonify({"error": "Le champ 'keyword' est requis."}), 400

    briefs.append({"keyword": keyword, "status": "pending", "brief": ""})
    return jsonify({"message": f"Mot-clé '{keyword}' reçu.", "status": "success"}), 200

@app.route("/enregistrerBrief", methods=["POST"])
def enregistrer_brief():
    data = request.json
    keyword = data.get("keyword")
    brief = data.get("brief")

    for b in reversed(briefs):
        if b["keyword"] == keyword:
            b["brief"] = brief
            b["status"] = "done"
            return jsonify({"message": "Brief enregistré.", "status": "success"}), 200

    return jsonify({"error": "Mot-clé introuvable."}), 404

@app.route("/recupererBrief", methods=["GET"])
def recuperer_brief():
    for b in reversed(briefs):
        if b["status"] == "done":
            return jsonify({
                "keyword": b["keyword"],
                "brief": b["brief"],
                "status": b["status"]
            }), 200

    return jsonify({"message": "Aucun brief disponible pour le moment."}), 200

@app.route("/reset", methods=["GET"])
def reset():
    briefs.clear()
    return jsonify({"message": "Mémoire vidée.", "status": "reset"}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)