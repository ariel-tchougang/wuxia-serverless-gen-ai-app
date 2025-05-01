from templates.template_interface import TemplateGenerator
from templates.templates import AskQuestionTemplateGenerator, CodeTemplateGenerator, TranslateTemplateGenerator, AnalyzeCodeTemplateGenerator

class TemplateBuilder:
    @staticmethod
    def build(template_id: str) -> TemplateGenerator:
        if template_id == "ask_question":
            return AskQuestionTemplateGenerator(template_id)
        elif template_id == "generate_code":
            return CodeTemplateGenerator(template_id)
        elif template_id == "translate_code":
            return TranslateTemplateGenerator(template_id)
        elif template_id == "analyze_code":
            return AnalyzeCodeTemplateGenerator(template_id)
        else:
            raise ValueError(f"Unsupported template: {template_id}")