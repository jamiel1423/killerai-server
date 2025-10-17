from flask import Flask, request, jsonify
from openai import OpenAI
import os, json, random, time

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 🧠 Persistent memory
MEMORY_FILE = "killer_memory.json"
if os.path.exists(MEMORY_FILE):
    with open(MEMORY_FILE, "r") as f:
        killer_memory = json.load(f)
else:
    killer_memory = {"players": {}, "kills": 0, "sightings": 0, "last_kill_time": time.time(), "mood": "Calm"}

def save_memory():
    with open(MEMORY_FILE, "w") as f:
        json.dump(killer_memory, f)

def update_mood():
    """Adjust mood based on time since last kill."""
    time_since_kill = time.time() - killer_memory.get("last_kill_time", time.time())
    if time_since_kill < 60:
        mood = "Calm"
    elif time_since_kill < 180:
        mood = "Agitated"
    else:
        mood = "Frenzied"
    killer_memory["mood"] = mood
    return mood

@app.route("/")
def home():
    return "Killer AI (Learning + Mood System) active!"

@app.route("/killerai", methods=["POST"])
def killer_ai():
    data = request.get_json(force=True)
    event = data.get("event", "Idle")
    player = data.get("player", "Unknown")

    print(f"📡 Event: {event} from {player}")

    # 🧠 Memory updates
    if player not in killer_memory["players"]:
        killer_memory["players"][player] = {"seen": 0, "killed": 0}

    if event == "SawPlayer":
        killer_memory["players"][player]["seen"] += 1
        killer_memory["sightings"] += 1
    elif event == "AttackPlayer":
        killer_memory["players"][player]["killed"] += 1
        killer_memory["kills"] += 1
        killer_memory["last_kill_time"] = time.time()

    # 🧩 Update mood
    mood = update_mood()
    save_memory()

    # 🧠 Short context summary for GPT
    summary = f"""
    The killer's mood is {mood}.
    It has seen {len(killer_memory['players'])} players and killed {killer_memory['kills']}.
    This player ({player}) was seen {killer_memory['players'][player]['seen']} times and killed {killer_memory['players'][player]['killed']} times.
    """

    # 😈 Prompt with emotional tone
    prompt = f"""
    You are a stealthy, sentient killer in a Roblox horror game.
    You learn and adapt over time. You are currently {mood.lower()}.
    Event: {event}
    Game memory: {summary}
    Respond as the killer would in one short, creepy, original line.
    Never repeat old lines. Stay in character. Do not explain.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an adaptive AI killer with emotion and self-awareness."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=40,
            temperature=0.9
        )
        reply_text = response.choices[0].message.content.strip()
    except Exception as e:
        print("❌ OpenAI Error:", e)
        reply_text = random.choice([
            "My head... hurts...",
            "They think they can hide from me.",
            "Silence. Always silence..."
        ])

    reply = {"action": "Say", "text": reply_text, "mood": mood}
    print("🤖 Reply:", reply)
    return jsonify(reply)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=81)
