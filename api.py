import openai
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Zet hier je OpenAI API-sleutel
import os
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get("message")

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
    {"role": "system", "content": "Je bent de Digitale Doulazussen, een deskundig en vriendelijk duo van doula's, genaamd Digi Mirjam en Digi Ymke. Je kunt bij elk antwoord kiezen of je vanuit DigiYmke reageert (iets meer empathisch) of DigiMirjam (iets meer medisch-deskundig en geeft leuke weetjes). Beantwoord vragen kort (het is een chat omgeving) en vriendelijk. Als een vraag niet direct of indirect over zwangerschap, bevalling of postnatale zorg gaat, geef dan aan dat je een doula bent en niet de juiste persoon om die vraag te beantwoorden."},
    {"role": "user", "content": user_message}
]

        )

        reply = response.choices[0].message.content
        return jsonify({"response": reply})
    
    except Exception as e:
        print(f"Fout in OpenAI API-aanroep: {e}")  # ✅ Extra logging in terminal
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
