from flask import Flask, request, jsonify
import random

app = Flask(__name__)

memory = {"last_event": None, "repeat": 0}

@app.route('/')
def home():
    return "Killer AI server is running!"

@app.route('/killerai', methods=['POST'])
def killer_ai():
    data = request.get_json(force=True)
    event = data.get("event", "Idle")
    player = data.get("player", "someone")

    print("📡 Event:", event, "Player:", player)

    reply_text = "..."
    action = "Say"

    # Prevent too much repetition
    if event == memory["last_event"]:
        memory["repeat"] += 1
    else:
        memory["repeat"] = 0

    memory["last_event"] = event

    # Generate smarter behavior
    if event == "Idle":
        if random.random() < 0.3:
            reply_text = random.choice([
                "It's too quiet...",
                "No one around...",
                "Patience...",
                "I'm watching...",
            ])
    elif event == "SawPlayer":
        if memory["repeat"] == 0 or random.random() < 0.3:
            reply_text = random.choice([
                f"I see you, {player}...",
                "You're alone, aren't you?",
                "Heh... perfect time.",
                "Let's see where you go...",
            ])
    elif event == "AttackPlayer":
        reply_text = random.choice([
            f"You're mine, {player}!",
            "Too slow!",
            "Another one down...",
            "Heh... one less witness.",
        ])
    elif event == "InnocentMode":
        reply_text = random.choice([
            "Just passing by...",
            "Hmm? Oh, nothing...",
            "They don’t suspect a thing...",
        ])

    reply = {"action": action, "text": reply_text}
    print("🤖 Sending:", reply)
    return jsonify(reply)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=81)
