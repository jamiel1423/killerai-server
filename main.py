from flask import Flask, request, jsonify
from openai import OpenAI
import os

# === SETUP ===
app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # Make sure you add your API key in Render!

# Memory for learning (simple version)
memory = []

@app.route('/')
def home():
    return "🤖 Killer AI server with learning is running!"

@app.route('/killerai', methods=['POST'])
def killer_ai():
    data = request.get_json(force=True)
    print("📡 Received from Roblox:", data)

    event = data.get("event")
    player = data.get("player", "Unknown Player")

    # Store what happens (so AI learns context)
    memory.append(f"{player} triggered event {event}")

    # Keep memory small (last 10 events)
    if len(memory) > 10:
        memory.pop(0)

    # Make the AI respond with memory awareness
    prompt = (
        "You are a learning killer AI inside a Roblox horror game.\n"
        "You remember past encounters and grow smarter.\n\n"
        f"Recent memories:\n{chr(10).join(memory)}\n\n"
        f"Current event: {event}\n"
        "Respond like a sinister, evolving killer NPC."
    )

    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a killer AI in a Roblox horror game."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=60
        )

        ai_text = completion.choices[0].message.content
        reply = {"action": "Say", "text": ai_text}

        print("🤖 Sending back:", reply)
        return jsonify(reply)

    except Exception as e:
        print("❌ Error talking to OpenAI:", e)
        return jsonify({"action": "Say", "text": "..."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=81)
