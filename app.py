from flask import Flask, request, jsonify

app = Flask(__name__)

briefs = []

@app.route("/nouveauBrief", methods=["POST"])
def nouveau_brief():
    data = request.json
    keyword = data.get("keyword")
    if not keyword:
        return jsonify({"message": "Mot-clé manquant."}), 400

    # Marquer tous les briefs comme terminés (sécurité si bug)
    for brief in briefs:
        if brief["status"] == "pending":
            brief["status"] = "skipped"

    briefs.append({
        "keyword": keyword,
        "status": "pending",
        "brief": ""
    })

    return jsonify({
        "message": f"Mot-clé '{keyword}' reçu.",
        "status": "success"
    }), 200

@app.route("/recupererBrief", methods=["GET"])
def recuperer_brief():
    for brief in briefs:
        if brief.get("status") == "pending":
            return jsonify({
                "keyword": brief["keyword"]
            }), 200

    return jsonify({"message": "Aucun brief disponible pour le moment."}), 200

@app.route("/enregistrerBrief", methods=["POST"])
def enregistrer_brief():
    data = request.json
    keyword = data.get("keyword")
    brief_content = data.get("brief")

    if not keyword or not brief_content:
        return jsonify({"message": "Champs manquants."}), 400

    for brief in briefs:
        if brief["keyword"] == keyword and brief["status"] == "pending":
            brief["brief"] = brief_content
            brief["status"] = "done"
            return jsonify({
                "message": "Brief enregistré.",
                "status": "success"
            }), 200

    return jsonify({"message": "Brief non trouvé."}), 404

@app.route("/reset", methods=["GET"])
def reset():
    briefs.clear()
    return jsonify({"message": "Mémoire vidée.", "status": "reset"}), 200
