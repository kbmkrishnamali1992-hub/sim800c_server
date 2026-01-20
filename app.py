from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

LOG_FILE = "data.log"

@app.route("/api/logs", methods=["POST"])
def receive_logs():
    try:
        # Try JSON first
        data = request.get_json(silent=True)

        # If not JSON, try form data (SIM800C often sends this)
        if data is None:
            data = request.form.to_dict()

        if not data:
            return jsonify({"status": "error", "message": "No data received"}), 400

        # Add timestamp
        data["timestamp"] = datetime.utcnow().isoformat()

        # Store data
        with open(LOG_FILE, "a") as f:
            f.write(str(data) + "\n")

        return jsonify({"status": "success", "received": data}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/", methods=["GET"])
def health():
    return "SIM800C Server Running OK", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
