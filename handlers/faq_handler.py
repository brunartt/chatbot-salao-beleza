from data.salao import FAQ
from services.state_service import set_estado

def get_menu_faq():
    opcoes = "\n".join([f"{key}️⃣ {valor[0]}" for key, valor in FAQ.items()])
    return f"""❓ *Dúvidas Frequentes*\n\n{opcoes}\n0️⃣ Voltar ao menu"""

def processar_faq(numero, msg):
    if msg == "0":
        set_estado(numero, {"etapa": "menu"})
        from handlers.menu_handler import get_menu_principal
        return get_menu_principal()
    
    elif msg in FAQ:
        _, resposta = FAQ[msg]
        return resposta + "\n\nDigite *menu* pra voltar ou *0* pra ver outras dúvidas."
    
    else:
        return get_menu_faq()