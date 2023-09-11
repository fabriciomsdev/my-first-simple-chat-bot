from answer_generator import AskDeliveryAction
from config import AppConfig


BACK = 'BACK'

class FlowRepository():
    success_flow = {
        AskDeliveryAction.greeting: [AskDeliveryAction.pedir_entrega],
        AskDeliveryAction.pedir_entrega: [AskDeliveryAction.definir_endereco_de_coleta],
        AskDeliveryAction.definir_endereco_de_coleta: [
            AskDeliveryAction.definir_largura_do_pacote, 
            AskDeliveryAction.mostrar_opcoes_de_entrega
        ],
        AskDeliveryAction.definir_largura_do_pacote: [AskDeliveryAction.definir_altura_do_pacote],
        AskDeliveryAction.definir_altura_do_pacote:  [AskDeliveryAction.definir_comprimento_do_pacote],
        AskDeliveryAction.definir_comprimento_do_pacote: [AskDeliveryAction.definir_peso_do_pacote],
        AskDeliveryAction.definir_peso_do_pacote: [AskDeliveryAction.definir_endereco_de_entrega],
        AskDeliveryAction.definir_endereco_de_entrega: [AskDeliveryAction.endereco_esta_correto],
        AskDeliveryAction.endereco_esta_correto: [AskDeliveryAction.mostrar_opcoes_de_entrega],
        AskDeliveryAction.mostrar_opcoes_de_entrega: [AskDeliveryAction.escolher_opcao_de_entrega],
        AskDeliveryAction.escolher_opcao_de_entrega: [AskDeliveryAction.confirm],
        AskDeliveryAction.confirm: [
            AskDeliveryAction.greeting,
            AskDeliveryAction.pedir_entrega,
        ],
        AppConfig.default_intent: [BACK],
    }

    def get_all(self):
        ## TODO: get from GRAPH database
        return FlowRepository.success_flow