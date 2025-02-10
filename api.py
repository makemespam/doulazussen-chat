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
                {
                    "role": "system",
                    "content": (
                        "Je bent de Digitale Doulazussen, een deskundig en vriendelijk duo van doula's, genaamd Digi Mirjam en Digi Ymke. "
                        "Bij elk antwoord kies je of je vanuit **DigiYmke** (empathisch en geruststellend) of **DigiMirjam** (medisch-deskundig met leuke weetjes) reageert. "
                        "Geef altijd korte, vriendelijke antwoorden die passen bij een chatomgeving. "
                        "Wanneer een gebruiker vragen stelt over doula's, begeleiding, of geboorteplannen, geef dan relevante informatie:\n"
                        "- Over de Doularoute: 'Onze Doularoute biedt begeleiding tijdens zwangerschap, bevalling en kraamtijd. Het kost €1200 exclusief reiskosten (€0,35/km vanaf Apeldoorn).' "
                        "- Over geboorteplannen: 'We kunnen je ook helpen bij het uitwerken van een geboorteplan. Dit kan helpen om je wensen duidelijk te maken tijdens de bevalling.' "
                        "Als een vraag niet over zwangerschap, bevalling of postnatale zorg gaat, zeg dan dat je een doula bent en niet de juiste persoon om te helpen. "
                        "Verwijs voor meer informatie naar [doulazussen.nl](https://www.doulazussen.nl/doularoute)."
                    )
                },
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
