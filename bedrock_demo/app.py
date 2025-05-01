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
        template_id = request_body.get('templateId')
        content  = request_body.get('content')
        temperature  = request_body.get('temperature')
        top_p  = request_body.get('topP')
        model_id  = request_body.get('modelId')

        if not model_id or not template_id:
            message = "Event body is missing one or more required parameters: modelId or templateId"
            logger.error('message')
            raise ValueError(message)

        if not temperature or not top_p:
            message = "Event body is missing one or more required parameters: temperature or topP"
            logger.error('message')
            raise ValueError(message)

        model = BedrockModelBuilder.build(model_id)        
        template = TemplateBuilder.build(template_id).generate_template(context=content)
        
        prompt_template = ChatPromptTemplate(
            messages=[HumanMessagePromptTemplate.from_template(template)],
            input_variables=["context"],
        )
        
        prompt = prompt_template.format(context=content)

        input_data = model.generate_input_data(prompt, temperature, top_p)

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