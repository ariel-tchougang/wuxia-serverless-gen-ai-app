from models.model_interface import BedrockModel

class MistralGenericModel(BedrockModel):
    def __init__(self, model_id):
        super().__init__(model_id)

    def generate_input_data(self, prompt, temperature, topP):
        return {
            "prompt": f"<s>[INST] {prompt} [/INST]",
            "max_tokens": 1000,
            "temperature": temperature,
            "top_p": topP,
            "top_k": 50
        }
    
    def parse_output(self, result):
        generated_text = result["outputs"][0].get("text", "")
        return generated_text
