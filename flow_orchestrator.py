from answer_generator import AskDeliveryAction
from flow_repository import FlowRepository


class FlowOrchestrator():
    flow_repository = FlowRepository()

    def __init__(self):
        self.current_path = []

    def persist_current_step(self, action):
        self.current_path.append(action)

    def get_possible_next_step(self, action):
        return self.flow_repository.get_all()[action]
    
    def get_last_step(self):
        return self.current_path[-1] if len(self.current_path) > 0 else AskDeliveryAction.greeting