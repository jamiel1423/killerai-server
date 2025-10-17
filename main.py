from flask import Flask, request, jsonify
import random

app = Flask(__name__)

# 🧠 Basic memory of last event and player
memory = {"last_event": None, "last_player": None, "repeat": 0}

@app.route('/')
def home():
    return "Killer AI server is alive..."

@app.route('/killerai', methods=['POST'])
def killer_ai():
    data = request.get_json(force=True)
    event = data.get("event", "Idle")
    player = data.get("player", "someone")

    print(f"📡 Received event: {event} from {player}")

    # Track repetition
    if event == memory["last_event"]:
        memory["repeat"] += 1
    else:
        memory["repeat"] = 0

    memory["last_event"] = event
    memory["last_player"] = player

    # 🧩 Response logic — always something to say
    if event == "Idle":
        replies = [
            "So quiet... for now.",
            "They're hiding. I can feel it.",
            "No one around... yet.",
            "This place feels empty.",
            "Waiting... always waiting."
        ]
    elif event == "SawPlayer":
        replies = [
            f"I see you, {player}...",
            f"Don't run, {player}... I like the chase.",
            "You're all alone, aren't you?",
            "I’ve been waiting for you.",
            "Perfect time to strike."
        ]
    elif event == "AttackPlayer":
        replies = [
            f"You're mine now, {player}.",
            "Too slow.",
            "Another one falls.",
            "No one will find you.",
            "You never stood a chance."
        ]
    elif event == "InnocentMode":
        replies = [
            "Act natural...",
            "Just passing by...",
            "They don’t suspect a thing.",
            "Keep calm... blend in.",
            "Nothing to see here..."
        ]
    else:
        replies = [
            "I'm thinking...",
            "Hmm...",
            "Something’s not right.",
            "Where did they go?",
            "I can sense fear nearby..."
        ]

    # 🗣️ Always pick a reply, randomize it
    reply_text = random.choice(replies)
    reply = {"action": "Say", "text": reply_text}

    print("🤖 Replying with:", reply)
    return jsonify(reply)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=81)
