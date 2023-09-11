from time import sleep
from answer_generator import AskDeliveryAction
from dtos import UserInputUnderstandingDTO
from platform_service import Address, Delivery, Package, PlatformService
import spacy


class ActionsManager:
    flows_with_dialogs_controled_by_system = [
        AskDeliveryAction.endereco_esta_correto,
        AskDeliveryAction.mostrar_opcoes_de_entrega
    ]

    def __init__(self):
        self.delivery = None
        self.named_entity_interpreter = spacy.load("pt_core_news_sm")
        self.platform_service = PlatformService()

    def on_chat_bot_message(self, callback):
        self.send_chat_bot_message = callback

    def convert_intents_to_actions(self, user_input_understanding: UserInputUnderstandingDTO):
        switcher = {
            AskDeliveryAction.pedir_entrega: self.iniciar_registro_de_entrega,
            AskDeliveryAction.definir_endereco_de_coleta: self.definir_endereco_de_coleta,
            AskDeliveryAction.definir_largura_do_pacote: self.definir_largura_do_pacote,
            AskDeliveryAction.definir_altura_do_pacote: self.definir_altura_do_pacote,
            AskDeliveryAction.definir_comprimento_do_pacote: self.definir_comprimento_do_pacote,
            AskDeliveryAction.definir_peso_do_pacote: self.definir_peso_do_pacote,
            AskDeliveryAction.definir_endereco_de_entrega: self.definir_endereco_de_entrega,
            AskDeliveryAction.mostrar_opcoes_de_entrega: self.mostrar_opcoes_de_entrega,
            AskDeliveryAction.confirm: self.pedir_entrega,
            AskDeliveryAction.endereco_esta_correto: self.verificar_endereco_esta_correto,
            AskDeliveryAction.mostrar_opcoes_de_entrega: self.mostrar_opcoes_de_entrega,
            AskDeliveryAction.escolher_opcao_de_entrega: self.escolher_opcao_de_entrega,
        }

        return switcher.get(user_input_understanding.intent, None)

    def tokenize_message(self, message):
        tokens = self.named_entity_interpreter(message)
        return tokens

    def proccess_intent(self, user_input_understanding: UserInputUnderstandingDTO):
        action = self.convert_intents_to_actions(user_input_understanding)
        self.tokenize_message(user_input_understanding.message)

        if action:
            action(user_input_understanding.message)
            return True
        
        return False

    def iniciar_registro_de_entrega(self, message):
        self.delivery = Delivery()

        if (self.delivery.package == None):
            self.delivery.package = Package()

        if (self.delivery.delivery_address == None):
            self.delivery.delivery_address = Address()

        if (self.delivery.pickup_address == None):
            self.delivery.pickup_address = Address()

    def definir_largura_do_pacote(self, message):
        self.delivery.package.width = self._parse_mesure_using_NER(message)
        pass

    def definir_altura_do_pacote(self, message):
        self.delivery.package.height = self._parse_mesure_using_NER(message)
        pass

    def definir_comprimento_do_pacote(self, message):
        self.delivery.package.depth = self._parse_mesure_using_NER(message)
        pass

    def _parse_mesure_using_NER(self, message: str):
        tokens = self.tokenize_message(message)
        weight = None

        for token in tokens:
            if token.pos_ == 'NUM' and token.tag_ == 'NUM':
                weight = float(token.text)

        return weight

    def definir_peso_do_pacote(self, message):
        self.delivery.package.weight = self._parse_mesure_using_NER(message)
        pass

    def definir_endereco_de_entrega(self, message):
        self.delivery.delivery_address.address = message
        pass

    def definir_endereco_de_coleta(self, message):
        self.delivery.pickup_address.address = message
        pass

    def mostrar_opcoes_de_entrega(self, message):
        sleep(3)
        self.quotes_available = self.platform_service.get_quote(self.delivery)

        if self.send_chat_bot_message:
            for quote in self.quotes_available:
                self.send_chat_bot_message(str(quote))

    def pedir_entrega(self, message):
        self.platform_service.ask_delivery(self.quote_choosed, self.delivery)

    def verificar_endereco_esta_correto(self, message):
        sleep(3)
        self.send_chat_bot_message(f'Você confirma a entrega de {self.delivery.delivery_address.address} para {self.delivery.pickup_address.address}?')

    def escolher_opcao_de_entrega(self, message):
        if (self.quotes_available):
            quote_choosed_id = self._parse_mesure_using_NER(message)
            self.quote_choosed = list(filter(lambda q: q.id == quote_choosed_id, self.quotes_available))[0]

