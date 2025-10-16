from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

# 🧠 Simple “memory” to let the AI learn a bit over time
ai_memory = []

@app.route('/')
def home():
    return "Killer AI server is running and thinking..."

@app.route('/killerai', methods=['POST'])
def killer_ai():
    data = request.get_json(force=True)
    print("📡 Received from Roblox:", data)

    event = data.get("event", "Idle")
    player = data.get("player", "Unknown")

    # Add to memory
    ai_memory.append(f"{event} with {player}")
    ai_memory[:] = ai_memory[-20:]  # limit memory size

    # 🧠 Make AI reasoning prompt
    prompt = f"""
You are a stealthy killer NPC in a Roblox horror game.
You hunt players like a murderer in Murder Mystery — act calm when in groups, but strike when alone.
You remember recent events: {ai_memory}.
Current event: {event} involving {player}.

Decide what to say or do now. Respond in JSON with:
{{
  "action": "Say" | "Attack" | "Hide" | "Idle",
  "text": "what the killer says"
}}
"""

    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100,
            temperature=0.8
        )

        ai_text = response.choices[0].message.content.strip()
        print("🧠 AI decided:", ai_text)
        return ai_text

    except Exception as e:
        print("❌ Error:", e)
        return jsonify({"action": "Say", "text": "..."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=81)
