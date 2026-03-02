from flask import Blueprint, request
from twilio.twiml.messaging_response import MessagingResponse
from services.state_service import get_estado, resetar_estado
from handlers.menu_handler import get_menu_principal, processar_menu
from handlers.faq_handler import processar_faq
from handlers.agendamento_handler import processar_agendamento

webhook_bp = Blueprint("webhook", __name__)

ETAPAS_AGENDAMENTO = [
    "agendamento_nome",
    "agendamento_servico",
    "agendamento_data",
    "agendamento_hora"
]

@webhook_bp.route("/webhook", methods=["POST"])
def webhook():
    numero = request.form.get("From")
    mensagem = request.form.get("Body", "").strip()
    msg = mensagem.lower()

    estado = get_estado(numero)
    etapa = estado.get("etapa", "menu")

    # Sempre volta ao menu se digitar "menu"
    if msg == "menu":
        resetar_estado(numero)
        resposta = get_menu_principal()

    # Direciona pro handler correto dependendo da etapa
    elif etapa == "menu":
        resposta = processar_menu(numero, msg)

    elif etapa == "faq":
        resposta = processar_faq(numero, msg)

    elif etapa in ETAPAS_AGENDAMENTO:
        resposta = processar_agendamento(numero, mensagem, etapa)

    else:
        resetar_estado(numero)
        resposta = get_menu_principal()

    resp = MessagingResponse()
    resp.message(resposta)
    return str(resp)