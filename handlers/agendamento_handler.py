from data.salao import SERVICOS, HORARIOS_DISPONIVEIS
from services.state_service import get_estado, set_estado, atualizar_estado, resetar_estado

def processar_agendamento(numero, mensagem, etapa):
    
    if etapa == "agendamento_nome":
        atualizar_estado(numero, etapa="agendamento_servico", nome=mensagem)
        return f"Olá, *{mensagem}*! 😊\n\nQual serviço deseja?\n{SERVICOS}\nDigite o nome do serviço:"

    elif etapa == "agendamento_servico":
        atualizar_estado(numero, etapa="agendamento_data", servico=mensagem)
        return f"Ótimo! *{mensagem}* anotado ✅\n\nQual *data* você prefere?\n📅 Ex: 15/03"

    elif etapa == "agendamento_data":
        atualizar_estado(numero, etapa="agendamento_hora", data=mensagem)
        horarios = " | ".join(HORARIOS_DISPONIVEIS)
        return f"Data *{mensagem}* anotada ✅\n\nQual *horário* prefere?\n⏰ Disponíveis: {horarios}"

    elif etapa == "agendamento_hora":
        estado = get_estado(numero)
        nome = estado.get("nome")
        servico = estado.get("servico")
        data = estado.get("data")
        hora = mensagem

        resetar_estado(numero)

        return f"""✅ *Agendamento confirmado!*

👤 Nome: {nome}
✂️ Serviço: {servico}
📅 Data: {data}
⏰ Horário: {hora}

Te esperamos no *{data}* às *{hora}*! 💇‍♀️
Digite *menu* pra voltar ao início."""