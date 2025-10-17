from flask import Flask, request, jsonify
from openai import OpenAI
import os, json, random

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 🧠 Memory file for long-term learning
MEMORY_FILE = "killer_memory.json"
if os.path.exists(MEMORY_FILE):
    with open(MEMORY_FILE, "r") as f:
        killer_memory = json.load(f)
else:
    killer_memory = {"players": {}, "kills": 0, "sightings": 0}

def save_memory():
    with open(MEMORY_FILE, "w") as f:
        json.dump(killer_memory, f)

@app.route("/")
def home():
    return "Killer AI (learning mode) active!"

@app.route("/killerai", methods=["POST"])
def killer_ai():
    data = request.get_json(force=True)
    event = data.get("event", "Idle")
    player = data.get("player", "Unknown")

    # 🧩 Update memory
    if player not in killer_memory["players"]:
        killer_memory["players"][player] = {"seen": 0, "killed": 0}
    
    if event == "SawPlayer":
        killer_memory["players"][player]["seen"] += 1
        killer_memory["sightings"] += 1
    elif event == "AttackPlayer":
        killer_memory["players"][player]["killed"] += 1
        killer_memory["kills"] += 1

    save_memory()

    # 🧠 Build a short description of what it knows
    summary = f"The killer has seen {len(killer_memory['players'])} players and made {killer_memory['kills']} kills."
    player_stats = killer_memory["players"].get(player, {})
    memory_line = f"This player ({player}) was seen {player_stats.get('seen', 0)} times and killed {player_stats.get('killed', 0)} times."

    # 🧩 Build prompt for OpenAI
    prompt = f"""
    You are a stealthy, intelligent killer in a Roblox horror game.
    You are trying not to get caught, but you like to toy with players before striking.
    Game memory: {summary}
    {memory_line}
    The current event is: {event}.
    Respond as the killer would — brief, eerie, human-like, no repetition.
    """

    # 🗣️ Ask OpenAI for a smart line
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a sinister killer AI with human-like intelligence."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=40,
            temperature=0.8
        )
        reply_text = response.choices[0].message.content.strip()
    except Exception as e:
        print("❌ OpenAI error:", e)
        reply_text = random.choice([
            "Something's wrong...",
            "Can't think... too quiet...",
            "They’re watching me..."
        ])

    reply = {"action": "Say", "text": reply_text}
    print("🤖 Reply:", reply)
    return jsonify(reply)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=81)
