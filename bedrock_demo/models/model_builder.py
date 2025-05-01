from models.model_interface import BedrockModel
from models.amazon_titan_text import AmazonTitanText
from models.mistral_generic import MistralGenericModel

class BedrockModelBuilder:
    @staticmethod
    def build(model_id: str) -> BedrockModel:
        if "mistral.mixtral" in model_id or "mistral.mistral" in model_id:
            return MistralGenericModel(model_id)
        elif model_id.startswith("amazon.titan-text"):
            return AmazonTitanText(model_id)
        else:
            raise ValueError(f"Unsupported model: {model_id}")