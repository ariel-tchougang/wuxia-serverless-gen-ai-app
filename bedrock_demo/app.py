import json
import boto3
import os
import logging

from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from models.model_builder import BedrockModelBuilder
from templates.template_builder import TemplateBuilder

logger = logging.getLogger()
logger.setLevel(logging.INFO)

bedrock_client = boto3.client('bedrock-runtime')

def lambda_handler(event, context):
    logger.info('Event: %s', json.dumps(event))

    try:
        request_body = json.loads(event['body'])
        prefix = request_body.get('prefix')
        content  = request_body.get('content')
        temperature  = request_body.get('temperature')
        topP  = request_body.get('topP')

        model = BedrockModelBuilder.build(os.environ['BEDROCK_MODEL_ID'])        
        template = TemplateBuilder.build(prefix).generate_template(context=content)
        
        prompt_template = ChatPromptTemplate(
            messages=[HumanMessagePromptTemplate.from_template(template)],
            input_variables=["context"],
        )
        
        prompt = prompt_template.format(context=content)

        input_data = model.generate_input_data(prompt, temperature, topP)

        logger.info('Input data: %s', json.dumps(input_data))

        response = bedrock_client.invoke_model(
            modelId=model.model_id,
            body=json.dumps(input_data).encode("utf-8"),
            accept='application/json',
            contentType='application/json'
        )

        result = json.loads(response["body"].read().decode())

        logger.info('Response payload: %s', json.dumps(result))

        generated_text = model.parse_output(result)

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST'
            },
            'body': generated_text
        }
    except ValueError as e:
        logger.error('ValueError: %s', e)
        return {
            'statusCode': 400,
            'headers': {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST'
            },
            'body': str(e)
        }
    except Exception as e:
        logger.error('Error: %s', e)
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST'
            },
            'body': 'Internal Server Error'
        }