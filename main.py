from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/", methods=["GET"])
def getServerStatus():
    print("Hiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii")
    return jsonify({"status": "ok","message" : "Server Running..."}), 200

@app.route("/authentik-webhook", methods=["POST"])
def handle_authentik_event():
    data = request.get_json(force=True, silent=True)  
    
    body_str = data.get("body", "")
    
    # Convert the string to a Python dict safely
    try:
        # Strip the prefix "model_updated: " and parse the rest
        if body_str.startswith("model_updated: "):
            body_dict = ast.literal_eval(body_str.replace("model_updated: ", "", 1))
            name = body_dict.get("model", {}).get("name")
        else:
            name = None
    except Exception as e:
        print("Error parsing body:", e)
        name = None

    print("Extracted name:", name)
    return jsonify({"status": "ok", "name": name}), 200



if __name__ == "__main__":
    # Run Flask app in debug mode so you can see logs
    app.run(host="0.0.0.0", port=5000, debug=True)
