from models.model_interface import BedrockModel

class MetaLlama3GenericModel(BedrockModel):
    def __init__(self, model_id):
        super().__init__(model_id)

    def generate_input_data(self, prompt, temperature, top_p):
        return {
            "prompt": prompt,
            "max_gen_len": 512,
            "temperature": temperature,
            "top_p": top_p
        }
    
    def parse_output(self, result):
        generated_text = result["generation"]
        return generated_text
