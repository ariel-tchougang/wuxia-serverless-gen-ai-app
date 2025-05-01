from abc import ABC, abstractmethod

class BedrockModel(ABC):
    def __init__(self, model_id):
        self.model_id = model_id

    @abstractmethod
    def generate_input_data(self, prompt, temperature, top_p):
        pass

    @abstractmethod
    def parse_output(self, result):
        pass