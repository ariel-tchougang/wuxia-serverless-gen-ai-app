from abc import ABC, abstractmethod

class TemplateGenerator(ABC):
    def __init__(self, template_id):
        self.template_id = template_id

    @abstractmethod
    def generate_template(self, context):
        pass