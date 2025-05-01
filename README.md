# 🧠 Bedrock Wuxia Demo – Serverless GenAI Application

This project demonstrates the use of **Amazon Bedrock** with **AWS Lambda**, **API Gateway**, and **CloudFront** to power a generative AI backend, themed around the Wuxia universe. It showcases prompt engineering, code generation, translation, and analysis using foundation models such as **Titan** and **Mistral**.

![Alt text](/images/web-app-capture.png?raw=true "web-app-capture")

---

## 📦 Architecture Overview

- **AWS Lambda** – Python 3.11 function calling Bedrock models
- **IAM Role** – Fine-grained permission to invoke Bedrock
- **Lambda Layer** – Includes Langchain dependencies
- **Amazon Bedrock** – Titan and Mistral foundation models
- **API Gateway** – REST endpoint to expose the Lambda
- **Amazon S3** – Serves static web assets (optional)
- **CloudFront** – CDN to serve content securely via OAC

![Alt text](/images/architecture-white-back.png?raw=true "Architecture")

---

## 📂 Project Structure

```
.
├── bedrock_demo/                   # Lambda function code
│   └── models/
│       ├── amazon_titan_text.py
│       ├── mistral_generic.py
│       ├── model_builder.py
│       └── model_interface.py
│   └── templates/
│       ├── template_builder.py
│       ├── template_interface.py
│       └── templates.py
│   └── app.py
├── images/
│   └── ...
├── layers/
│   └── langchain_layer_python_311_310/
│       └── python/...
├── ui/                             # Project front-end ui files to upload to the created S3 bucket
│   ├── index.html
│   ├── wuxia.css 
│   └── wuxia.js 
├── samconfig.toml  
├── template.yaml                   # SAM infrastructure template
└── README.md
```

## 🚀 Deploying the Stack

> 📍 Note: This stack must be deployed in `us-east-1` due to CloudFront certificate requirements.

### ✅ Prerequisites
- AWS CLI configured
- SAM CLI installed
- Python 3.11+
- AWS account with Bedrock models access (Titan, Mistral)

### 🧰 Build and Deploy

```bash
# Make sure to configure the right aws profile in samconfig.toml
# profile = "<REPLACE_WITH_YOUR_AWS_PROFILE>"
sam build
sam deploy
```

## 🧪 Endpoints

| Route            | Method  | Description                         |
|------------------|---------|-------------------------------------|
| `/generate`      | POST    | Invokes the Bedrock Lambda function |
| `/`              | OPTIONS | CORS preflight                      |
| `CloudFront URL` | GET     | (Optional) static assets delivery   |

## 🛡 IAM & Permissions

- Lambda role: DemoBedrockLambdaRole

  + AWSLambdaBasicExecutionRole

  ```json
  {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "*"
        }
    ]
  }
  ```

  + Inline policy bedrock-lambda-AccessPolicy to invoke selected foundation models

  ```json
  {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": "bedrock:InvokeModel",
            "Resource": [
                "arn:aws:bedrock:us-east-1::foundation-model/amazon.titan-text-express-v1",
                "arn:aws:bedrock:us-east-1::foundation-model/amazon.titan-text-premier-v1:0",
                "arn:aws:bedrock:us-east-1::foundation-model/mistral.mixtral-8x7b-instruct-v0:1",
                "arn:aws:bedrock:us-east-1::foundation-model/mistral.mistral-7b-instruct-v0:2",
                "arn:aws:bedrock:us-east-1::foundation-model/meta.llama3-70b-instruct-v1:0",
                "arn:aws:bedrock:us-east-1::foundation-model/meta.llama3-8b-instruct-v1:0"
            ],
            "Effect": "Allow"
        }
    ]
  }
  ```

## 📌 Important

- You need to activate the models you want to use in Bedrock. The models currently accepted are:
  + amazon.titan-text-premier-v1:0
  + amazon.titan-text-express-v1
  + mistral.mixtral-8x7b-instruct-v0:1
  + mistral.mistral-7b-instruct-v0:2
  + meta.llama3-70b-instruct-v1:0
  + meta.llama3-8b-instruct-v1:0

- You need to upload the files in folder ui (index.html, wuxia.css and wuxia.js) to the S3 bucket created by the project so that it can get picked up by CloudFront.

- This project uses the latest OAC-based CloudFront–S3 setup (not legacy OAI).

- CORS is configured for development with permissive headers.

## 🙋‍♂️ Want to Extend?

Ideas for next steps:

- Add authentication with Cognito or JWT

- Log prompts and completions to DynamoDB

- Add support for more models (Claude, DeepSeek, etc.)

- Add X-Ray support for tracing

## Clean Up

- First empty the S3 bucket

- Then run:
``` bash
sam delete
```
