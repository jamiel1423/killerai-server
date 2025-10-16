from flask import Flask, request, jsonify
import random

app = Flask(__name__)

# 🧠 Memory storage
memory = {}

@app.route('/')
def home():
    return "Killer AI with memory is online!"

@app.route('/killerai', methods=['POST'])
def killer_ai():
    data = request.get_json(force=True)
    print("📡 Received from Roblox:", data)

    event = data.get("event", "Idle")
    player = data.get("player", "Unknown")

    # Initialize memory for new players
    if player not in memory:
        memory[player] = {"seen": 0, "attacked": 0, "last_event": "none"}

    # Update memory based on event
    if event == "SawPlayer":
        memory[player]["seen"] += 1
        memory[player]["last_event"] = "saw"
        text = random.choice([
            f"I see you again, {player}...",
            f"You can’t hide from me, {player}.",
            f"Your scent is familiar, {player}..."
        ])
        action = "Say"

    elif event == "AttackPlayer":
        memory[player]["attacked"] += 1
        memory[player]["last_event"] = "attack"
        text = random.choice([
            f"That’s {memory[player]['attacked']} attacks now, {player}.",
            f"I’ll finish what I started, {player}.",
            f"You won’t survive this, {player}..."
        ])
        action = "Attack"

    else:
        memory[player]["last_event"] = "idle"
        text = random.choice([
            "It’s quiet… too quiet.",
            "Where did they go?",
            "Still searching..."
        ])
        action = "Say"

    # Log memory state
    print(f"🧠 Memory for {player}: {memory[player]}")

    reply = {"action": action, "text": text}
    print("🤖 Sending back:", reply)
    return jsonify(reply)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=81)
