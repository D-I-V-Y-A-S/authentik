from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/", methods=["GET"])
def getServerStatus():
    print("Hiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii")
    return jsonify({"status": "ok","message" : "Server Running..."}), 200

@app.route("/authentik-webhook", methods=["POST"])
def handle_authentik_event():
    data = request.get_json(force=True, silent=True)  # parse JSON safely
    print("Received webhook payload:", data)
    return jsonify({"status": "ok"}), 200



if __name__ == "__main__":
    # Run Flask app in debug mode so you can see logs
    app.run(host="0.0.0.0", port=5000, debug=True)
