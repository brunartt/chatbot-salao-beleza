usuarios = {}

def get_estado(numero):
    """Retorna o estado atual do usuário. Se não existir, começa no menu."""
    return usuarios.get(numero, {"etapa": "menu"})

def set_estado(numero, novo_estado):
    """Atualiza o estado do usuário."""
    usuarios[numero] = novo_estado

def resetar_estado(numero):
    """Volta o usuário pro menu principal."""
    usuarios[numero] = {"etapa": "menu"}

def atualizar_estado(numero, **kwargs):
    """Atualiza campos específicos sem perder os dados anteriores."""
    estado_atual = get_estado(numero)
    usuarios[numero] = {**estado_atual, **kwargs}