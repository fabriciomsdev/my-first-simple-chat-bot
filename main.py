


from answer_generator import AskDeliveryAction, DialogManager
from application_layer import TerminalApplicationLayer, WhatsappApplicationLayer
from actions_manager import ActionsManager
from config import AppConfig
from flow_orchestrator import FlowOrchestrator
from flow_repository import FlowRepository
from language_understanding import LanguageUnderstandingModel

class ChatBot():
    def __init__(self, application_layer: WhatsappApplicationLayer = None):
        self.language_model = LanguageUnderstandingModel()
        self.actions_manager = ActionsManager()
        self.dialog_manager = DialogManager()
        self.flow = FlowOrchestrator()

        if (application_layer):
            self.set_application_layer(application_layer);

    def set_application_layer(self, application_layer: WhatsappApplicationLayer):
        self.application_layer = application_layer
        self.application_layer.setup()
        return self

    def process_user_input(self, message):
        processed_message = self.language_model.undestand(message)
        success_action_executed_by_intent = self.actions_manager.proccess_intent(processed_message)
        flow_is_ok = processed_message.intent != AppConfig.default_intent

        if flow_is_ok:
            self.flow.persist_current_step(processed_message.intent)
        else:
            self.application_layer.send("Não entendi muito bem, vamos tentar novamente ...")
            previous_step = self.flow.get_last_step()
            processed_message.intent = previous_step

        if success_action_executed_by_intent:
            next_step = self.flow.get_possible_next_step(processed_message.intent)
            processed_message.intent = next_step[0] if len(next_step) == 1 else next_step[0]
            self.flow.persist_current_step(processed_message.intent)

            if (processed_message.intent in self.actions_manager.flows_with_dialogs_controled_by_system):
                action = self.actions_manager.convert_intents_to_actions(processed_message)
                if action: 
                    action(processed_message.message)

        self.dialog_manager.generate_next_answer(processed_message)
        

    def setup(self):
        self.language_model.setup()
        self.dialog_manager.on_new_bot_answer(self.application_layer.send)
        self.actions_manager.on_chat_bot_message(self.application_layer.send)
        self.application_layer.on_message(self.process_user_input)

        return self

    def run(self):
        self.application_layer.send('Ola! Em que posso te ajudar?')
        self.application_layer.listen()
        return self
    

if (AppConfig.ui_mode == 'terminal'):
    terminal_application_layer = TerminalApplicationLayer()
    agent = ChatBot(terminal_application_layer)
else:
    whatsapp_application_layer = WhatsappApplicationLayer()
    agent = ChatBot(whatsapp_application_layer)

agent.setup().run()