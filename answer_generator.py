from config import AppConfig
from dtos import UserInputUnderstandingDTO


class AskDeliveryAction:
    greeting = 'greeting' 
    pedir_entrega = 'pedir_entrega' 
    definir_endereco_de_coleta = 'definir_endereco_de_coleta' 
    definir_largura_do_pacote = 'definir_largura_do_pacote' 
    definir_altura_do_pacote = 'definir_altura_do_pacote' 
    definir_comprimento_do_pacote = 'definir_comprimento_do_pacote' 
    definir_peso_do_pacote = 'definir_peso_do_pacote' 
    definir_endereco_de_entrega = 'definir_endereco_de_entrega' 
    endereco_esta_correto = 'endereco_esta_correto'
    mostrar_opcoes_de_entrega = 'mostrar_opcoes_de_entrega' 
    escolher_opcao_de_entrega = 'escolher_opcao_de_entrega'
    thank_you = 'thank_you'
    confirm = 'confirmar' 


class DialogManager:
    answers = {
        AskDeliveryAction.greeting:'Olá. Como posso ajudá-lo?',
        AskDeliveryAction.pedir_entrega: 'Ok, vamos começar. Qual o endereço de coleta?',
        AskDeliveryAction.definir_endereco_de_coleta: 'Qual o endereço de coleta?',
        AskDeliveryAction.definir_largura_do_pacote: 'Qual o largura do pacote em centimetros?',
        AskDeliveryAction.definir_altura_do_pacote: 'Qual altura do pacote em centimetros?',
        AskDeliveryAction.definir_comprimento_do_pacote: 'Qual o comprimento do pacote em centimetros?',
        AskDeliveryAction.definir_peso_do_pacote: 'Qual o peso do pacote em gramas?',
        AskDeliveryAction.definir_endereco_de_entrega: 'Qual o endereço de entrega?',
        AskDeliveryAction.endereco_esta_correto: 'Por favor confira se seu endereço está correto',
        AskDeliveryAction.mostrar_opcoes_de_entrega: 'As opções de entrega para você são:',
        AskDeliveryAction.escolher_opcao_de_entrega: 'Escolha uma das opções de entrega acima:',
        AskDeliveryAction.confirm: 'Seu Pedido confirmado o motorista está indo ao seu ponto de coleta, para coletar o pacote!',
        AppConfig.default_intent:'Me desculpe, mas não entendi o que você disse. Você poderia reformular?',
    }

    def on_new_bot_answer(self, callback):
        self._on_new_message_callback = callback

    def generate_next_answer(self, msg: UserInputUnderstandingDTO):
        msg = self.answers[msg.intent]
        if msg:
            self._on_new_message_callback(msg)
