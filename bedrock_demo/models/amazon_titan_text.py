from models.model_interface import BedrockModel

class AmazonTitanText(BedrockModel):
    def __init__(self, model_id):
        super().__init__(model_id)

    def generate_input_data(self, prompt, temperature, topP):
        return {
            "inputText": prompt,
            "textGenerationConfig": {
                "temperature": temperature,
                "topP": topP,
                "maxTokenCount": 1000,
                "stopSequences": []
            }
        }
    
    def parse_output(self, result):
        generated_text = result["results"][0].get("outputText", "").replace("\\n", "\n")
        return generated_text