from flask import Blueprint, request, jsonify
from services.state_service import get_estado, resetar_estado
from handlers.menu_handler import get_menu_principal, processar_menu
from handlers.faq_handler import processar_faq
from handlers.agendamento_handler import processar_agendamento
import requests
import os

webhook_bp = Blueprint("webhook", __name__)

ETAPAS_AGENDAMENTO = [
    "agendamento_nome",
    "agendamento_servico",
    "agendamento_data",
    "agendamento_hora"
]

EVOLUTION_URL = os.getenv("EVOLUTION_URL")
EVOLUTION_APIKEY = os.getenv("EVOLUTION_APIKEY")
EVOLUTION_INSTANCE = os.getenv("EVOLUTION_INSTANCE")

def enviar_mensagem(numero, texto):
    url = f"{EVOLUTION_URL}/message/sendText/{EVOLUTION_INSTANCE}"
    headers = {
        "apikey": EVOLUTION_APIKEY,
        "Content-Type": "application/json"
    }
    payload = {
        "number": numero,
        "text": texto
    }
    requests.post(url, json=payload, headers=headers)

@webhook_bp.route("/webhook", methods=["POST"])
def webhook():
    data = request.json

    # Ignora mensagens que não sejam de texto ou que sejam do próprio bot
    if not data or "data" not in data:
        return jsonify({"status": "ignored"}), 200

    msg_data = data.get("data", {})
    
    # Ignora mensagens enviadas pelo próprio bot
    if msg_data.get("key", {}).get("fromMe"):
        return jsonify({"status": "ignored"}), 200

    numero = msg_data.get("key", {}).get("remoteJid", "")
    mensagem = msg_data.get("message", {}).get("conversation", "") or \
               msg_data.get("message", {}).get("extendedTextMessage", {}).get("text", "")

    if not mensagem:
        return jsonify({"status": "ignored"}), 200

    msg = mensagem.strip().lower()
    estado = get_estado(numero)
    etapa = estado.get("etapa", "menu")

    if msg == "menu":
        resetar_estado(numero)
        resposta = get_menu_principal()
    elif etapa == "menu":
        resposta = processar_menu(numero, msg)
    elif etapa == "faq":
        resposta = processar_faq(numero, msg)
    elif etapa in ETAPAS_AGENDAMENTO:
        resposta = processar_agendamento(numero, mensagem, etapa)
    else:
        resetar_estado(numero)
        resposta = get_menu_principal()

    enviar_mensagem(numero, resposta)
    return jsonify({"status": "ok"}), 200


