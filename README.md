# AI Tutoring Bot

AI Tutoring Bot is a Telegram Bot designed to assist high-school students with their studies. It leverages Python 3.11, AWS Lambda, ChatGPT 3.5, DynamoDB, and langchain to create an intelligent study companion. This README will provide you with an overview of the bot, its functionality, and how to set it up for your own use.

## Features

AI Tutoring Bot offers the following key features:

- **Study Assistance:** AI Tutoring Bot can provide answers to questions related to various subjects, offer explanations, and suggest study resources.

- **Conversation History:** It saves parts of the conversation in a DynamoDB database to maintain context and provide better responses over time.

- **Langchain Integration:** AI Tutoring Bot utilizes langchain to build prompts for ChatGPT, ensuring relevant and accurate responses.

- **Serverless Architecture:** The bot is deployed using AWS SAM CLI, AWS Lambda, and CloudFormation, making it cost-effective and scalable.

- **API Gateway:** An API Gateway is used to connect the Telegram API with the Lambda function, enabling seamless communication.

## Demo

Try AI Tutoring Bot on Telegram!

- **Start a conversation** with [AI Tutoring Bot](https://t.me/AI_TutoringBot).
- **Scan the following QR Code**
![QR Code](https://github.com/maclenn77/ai-tutoring-bot/blob/main/assets/qr_code_ai_tutoring.jpg?raw=true)

## Architecture

![Serverless Architecture for Langchain Bot](https://github.com/maclenn77/ai-tutoring-bot/blob/main/assets/diagram.png?raw=true)

## Prerequisites

Before setting up AI Tutoring Bot, you'll need the following:

- Python 3.11 installed on your development environment.
- AWS SAM CLI installed: [AWS SAM CLI Installation Guide](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
- An AWS account with appropriate permissions to create and manage Lambda functions, DynamoDB tables, and API Gateway resources.
- A Telegram Bot token. You can create one by talking to the [BotFather](https://core.telegram.org/bots#botfather).
- A ChatGPT API key. You can obtain one from the OpenAI platform.

## Setup

Follow these steps to set up AI Tutoring Bot:

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/maclenn77/ai-tutoring-bot.git
   ```

2. Navigate to the project directory:

   ```bash
   cd ai-tutoring-bot
   ```

3. Create a virtual environment and activate it:

   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
4. Configure your AWS credentials using the AWS CLI:

   ```bash
   aws configure
   ```

5. Edit the `config.yaml` file to include your Telegram Bot token, ChatGPT API key, and other configuration options.

6. Deploy the Lambda function and API Gateway using SAM CLI:

The Serverless Application Model Command Line Interface (SAM CLI) is an extension of the AWS CLI that adds functionality for building and testing Lambda applications. It uses Docker to run your functions in an Amazon Linux environment that matches Lambda. It can also emulate your application's build environment and API.

To use the SAM CLI, you need the following tools.

* SAM CLI - [Install the SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
* [Python 3 installed](https://www.python.org/downloads/)
* Docker - [Install Docker community edition](https://hub.docker.com/search/?type=edition&offering=community)

To build and deploy your application for the first time, run the following in your shell:

```bash
sam build --use-container
sam deploy --guided
```

The first command will build the source of your application. The second command will package and deploy your application to AWS, with a series of prompts:

* **Stack Name**: The name of the stack to deploy to CloudFormation. This should be unique to your account and region, and a good starting point would be something matching your project name.
* **AWS Region**: The AWS region you want to deploy your app to.
* **Confirm changes before deploy**: If set to yes, any change sets will be shown to you before execution for manual review. If set to no, the AWS SAM CLI will automatically deploy application changes.
* **Allow SAM CLI IAM role creation**: Many AWS SAM templates, including this example, create AWS IAM roles required for the AWS Lambda function(s) included to access AWS services. By default, these are scoped down to minimum required permissions. To deploy an AWS CloudFormation stack which creates or modifies IAM roles, the `CAPABILITY_IAM` value for `capabilities` must be provided. If permission isn't provided through this prompt, to deploy this example you must explicitly pass `--capabilities CAPABILITY_IAM` to the `sam deploy` command.
* **Save arguments to samconfig.toml**: If set to yes, your choices will be saved to a configuration file inside the project, so that in the future you can just re-run `sam deploy` without parameters to deploy changes to your application.

You can find your API Gateway Endpoint URL in the output values displayed after deployment.

7. After the deployment is complete, note the API Gateway endpoint URL generated by SAM CLI.

8. Set up a webhook in your Telegram Bot. Here's an example:

```bash
# Replace 'YOUR_BOT_TOKEN' with your actual Telegram Bot token
BOT_TOKEN="YOUR_BOT_TOKEN"

# Replace 'YOUR_API_GATEWAY_URL' with the URL of your deployed API Gateway endpoint
API_GATEWAY_URL="https://YOUR_API_GATEWAY_URL/telegram/webhook"

# Set up the webhook using curl
curl -F "url=$API_GATEWAY_URL" "https://api.telegram.org/bot$BOT_TOKEN/setWebhook"
```

Execute this `curl` command in your terminal to set up the Telegram webhook. Once the webhook is successfully set up, your Telegram Bot will start receiving incoming messages and other updates at the specified endpoint.

9. Start a conversation with your Telegram Bot, and it will provide study assistance based on the messages you send.

### Use the SAM CLI to build and test locally

Build your application with the `sam build --use-container` command.

```bash
ai-tutoring-bot$ sam build --use-container
```

The SAM CLI installs dependencies defined in `hello_world/requirements.txt`, creates a deployment package, and saves it in the `.aws-sam/build` folder.

Test a single function by invoking it directly with a test event. An event is a JSON document that represents the input that the function receives from the event source. Test events are included in the `events` folder in this project.

Run functions locally and invoke them with the `sam local invoke` command.

```bash
ai-tutoring-bot$ sam local invoke HelloWorldFunction --event events/event.json
```

The SAM CLI can also emulate your application's API. Use the `sam local start-api` to run the API locally on port 3000.

```bash
ai-tutoring-bot$ sam local start-api
ai-tutoring-bot$ curl http://localhost:3000/
```

The SAM CLI reads the application template to determine the API's routes and the functions that they invoke. The `Events` property on each function's definition includes the route and method for each path.

```yaml
      Events:
        HelloWorld:
          Type: Api
          Properties:
            Path: /hello
            Method: get
```


### Fetch, tail, and filter Lambda function logs

To simplify troubleshooting, SAM CLI has a command called `sam logs`. `sam logs` lets you fetch logs generated by your deployed Lambda function from the command line. In addition to printing the logs on the terminal, this command has several nifty features to help you quickly find the bug.

`NOTE`: This command works for all AWS Lambda functions; not just the ones you deploy using SAM.

```bash
ai-tutoring-bot$ sam logs -n HelloWorldFunction --stack-name ai-tutoring-bot --tail
```

You can find more information and examples about filtering Lambda function logs in the [SAM CLI Documentation](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-logging.html).

### Tests

Tests are defined in the `tests` folder in this project. Use PIP to install the test dependencies and run tests.

```bash
ai-tutoring-bot$ pip install -r tests/requirements.txt --user
# unit test
ai-tutoring-bot$ python -m pytest tests/unit -v
# integration test, requiring deploying the stack first.
# Create the env variable AWS_SAM_STACK_NAME with the name of the stack we are testing
ai-tutoring-bot$ AWS_SAM_STACK_NAME="ai-tutoring-bot" python -m pytest tests/integration -v
```

### Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```bash
sam delete --stack-name "ai-tutoring-bot"
```
## Usage

AI Tutoring Bot operates as a Telegram Bot. Start a conversation with your bot and send it study-related questions or requests for assistance. The bot will respond with helpful information based on its integration with ChatGPT and langchain.

## Feedback and Contributions

If you have any feedback or would like to contribute to AI Tutoring Bot's development, please feel free to open issues or submit pull requests in the GitHub repository.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Enjoy using AI Tutoring Bot to enhance your high school studies! If you have any questions or encounter issues during the setup process, please don't hesitate to reach out for assistance.
