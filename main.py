from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "Killer AI server is running!"

@app.route('/killerai', methods=['POST'])
def killer_ai():
    data = request.get_json(force=True)
    print("📡 Received from Roblox:", data)

    event = data.get("event")
    if event == "SawPlayer":
        reply = {"action": "Say", "text": "hello..."}
    elif event == "AttackPlayer":
        reply = {"action": "Attack", "text": "You're mine!"}
    else:
        reply = {"action": "Say", "text": "..."}

    print("🤖 Sending back:", reply)
    return jsonify(reply)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=81)
