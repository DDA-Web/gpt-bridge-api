import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

FICHIER_BRIEFS = "briefs.json"

def lire_brefs():
    if os.path.exists(FICHIER_BRIEFS):
        with open(FICHIER_BRIEFS, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def ecrire_brefs(data):
    with open(FICHIER_BRIEFS, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.route("/nouveauBrief", methods=["POST"])
def nouveau_brief():
    data = request.get_json()
    keyword = data.get("keyword")
    if not keyword:
        return jsonify({"error": "Champ 'keyword' requis"}), 400

    briefs = lire_brefs()
    briefs.append({"keyword": keyword, "status": "pending"})
    ecrire_brefs(briefs)
    return jsonify({"message": f"Mot-clé '{keyword}' reçu.", "status": "success"})

@app.route("/recupererBrief", methods=["GET"])
def recuperer_brief():
    briefs = lire_brefs()
    for i in reversed(range(len(briefs))):
        if briefs[i].get("status") == "done" and "brief" in briefs[i]:
            return jsonify({
                "keyword": briefs[i]["keyword"],
                "brief": briefs[i]["brief"],
                "status": "done"
            })

    return jsonify({"message": "Aucun brief disponible pour le moment."})

@app.route("/enregistrerBrief", methods=["POST"])
def enregistrer_brief():
    data = request.get_json()
    keyword = data.get("keyword")
    brief = data.get("brief")

    if not keyword or not brief:
        return jsonify({"error": "Champs 'keyword' et 'brief' requis"}), 400

    briefs = lire_brefs()
    for i in reversed(range(len(briefs))):
        if briefs[i]["keyword"] == keyword:
            briefs[i]["brief"] = brief
            briefs[i]["status"] = "done"
            ecrire_brefs(briefs)
            return jsonify({"message": "Brief enregistré.", "status": "success"})

    return jsonify({"error": "Mot-clé introuvable."}), 404

@app.route("/reset", methods=["GET"])
def reset():
    ecrire_brefs([])
    return jsonify({"message": "Mémoire vidée.", "status": "reset"})

# ✅ CORRECT POUR DEPLOIEMENT SUR RAILWAY
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
