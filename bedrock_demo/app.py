import json
import boto3
import os
import re
import logging

from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from template import generate_code_template, generate_translate_template, generate_analyze_code_template, ask_question_template


# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)


# Create a Bedrock Runtime client
bedrock_client = boto3.client('bedrock-runtime')


# Define Lambda function
def lambda_handler(event, context):
    # Log the incoming event in JSON format
    logger.info('Event: %s', json.dumps(event))

    request_body = json.loads(event['body'])
    prefix = request_body.get('prefix')
    content  = request_body.get('content')
    temperature  = request_body.get('temperature')
    topP  = request_body.get('topP')
    model_id=os.environ['BEDROCK_MODEL_ID']
        
    # Generate the prompt based on the prefix
    if prefix == 'generate_code':
        template_generator = generate_code_template
    elif prefix == 'translate_code':
        template_generator = generate_translate_template
    elif prefix == 'analyze_code':
        template_generator = generate_analyze_code_template
    elif prefix == 'ask_question':
        template_generator = ask_question_template

    template = template_generator(context=content)
    
    prompt_template = ChatPromptTemplate(
        messages=[HumanMessagePromptTemplate.from_template(template)],
        input_variables=["context"],
    )
    
    prompt = prompt_template.format(context=content)
    
    # Prepare the input data for the model
    input_data = generate_input_data(model_id, prompt, temperature, topP)
    
    # Log the input data
    logger.info('Input data: %s', json.dumps(input_data))

    # Invoke the Bedrock Runtime with the cleaned body as payload
    response = bedrock_client.invoke_model(
        modelId=model_id,
        body=json.dumps(input_data).encode("utf-8"),
        accept='application/json',
        contentType='application/json'
    )

    # Load the response body and decode it
    result = json.loads(response["body"].read().decode())
    
    # Log the response payload
    logger.info('Response payload: %s', json.dumps(result))
    
    # Extract the generated text from the response
    generated_text = parse_output(result)
    
    # Return the result with status code 200 and the necessary headers
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST'
        },
        'body': generated_text
    }

def generate_input_data(model_id, prompt, temperature, topP):
    if "mistral.mixtral" in model_id or "mistral.mistral" in model_id:
        return {
            "prompt": f"<s>[INST] {prompt} [/INST]",
            "max_tokens": 1000,
            "temperature": temperature,
            "top_p": topP,
            "top_k": 50
        }
    else:
        # Default: assume amazon.titan-text or others
        return {
            "inputText": prompt,
            "textGenerationConfig": {
                "temperature": temperature,
                "topP": topP,
                "maxTokenCount": 1000,
                "stopSequences": []
            }
        }

def parse_output(result):
    generated_text = ""

    if "results" in result and result["results"]:
        generated_text = result["results"][0].get("outputText", "").replace("\\n", "\n")
    elif "outputs" in result and result["outputs"]:
        generated_text = result["outputs"][0].get("text", "")
    elif "generation" in result:
        generated_text = result["generation"]
    else:
        generated_text = json.dumps(result)
        logger.warning("Unknown response format: %s", generated_text)
    
    return generated_text
