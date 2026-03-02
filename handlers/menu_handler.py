from data.salao import NOME_SALAO, SERVICOS
from services.state_service import set_estado, resetar_estado

def get_menu_principal():
    return f"""Olá! 👋 Bem-vindo ao *{NOME_SALAO}*! 💇‍♀️

O que você deseja?

1️⃣ Ver serviços e preços
2️⃣ Agendar horário
3️⃣ Dúvidas frequentes
4️⃣ Falar com atendente"""

def processar_menu(numero, msg):
    if msg == "1":
        return SERVICOS + "\nDigite *menu* pra voltar."
    
    elif msg == "2":
        set_estado(numero, {"etapa": "agendamento_nome"})
        return "📅 Vamos agendar!\n\nPrimeiro, qual é o seu *nome completo*?"
    
    elif msg == "3":
        set_estado(numero, {"etapa": "faq"})
        from handlers.faq_handler import get_menu_faq
        return get_menu_faq()
    
    elif msg == "4":
        return "📞 Aguarde, em breve um atendente entrará em contato!\n\nDigite *menu* pra voltar."
    
    else:
        return get_menu_principal()