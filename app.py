from flask import Flask, request, jsonify
from twilio.twiml.messaging_response import MessagingResponse
import openai
import os

# Configuración de las claves API (reemplázalas con tus propias claves)
openai.api_key = 'TU_API_KEY_OPENAI'
twilio_phone_number = 'whatsapp:+14155238886'  # El número de WhatsApp de Twilio (esto te lo da Twilio)

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    # Obtener el mensaje del usuario
    incoming_msg = request.values.get("Body", "").strip()

    # Crear una respuesta con Twilio
    resp = MessagingResponse()

    # Generar respuesta con IA usando OpenAI
    if incoming_msg:
        response = openai.Completion.create(
            engine="text-davinci-003",  # O usa el modelo de tu preferencia
            prompt=incoming_msg,
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.9,
        )
        ai_response = response.choices[0].text.strip()

        # Enviar la respuesta generada por la IA
        resp.message(ai_response)
    else:
        resp.message("Lo siento, no entendí tu mensaje. ¿Puedes reformularlo?")

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
