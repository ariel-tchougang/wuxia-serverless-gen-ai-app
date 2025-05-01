from models.model_interface import BedrockModel
from models.amazon_titan_text import AmazonTitanText
from models.mistral_generic import MistralGenericModel
from models.meta_llama3_generic import MetaLlama3GenericModel

class BedrockModelBuilder:
    @staticmethod
    def build(model_id: str) -> BedrockModel:
        if "mistral.mixtral-8x7b-instruct" in model_id or "mistral.mistral-7b-instruct" in model_id:
            return MistralGenericModel(model_id)
        elif model_id.startswith("amazon.titan-text"):
            return AmazonTitanText(model_id)
        elif "meta.llama3-70b-instruct" in model_id or "meta.llama3-8b-instruct" in model_id:
            return MetaLlama3GenericModel(model_id)
        else:
            raise ValueError(f"Unsupported model: {model_id}")