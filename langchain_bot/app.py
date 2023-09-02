import json
# import langchain
# import openai
import requests
import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('LambdaDynamo')
def get_user(user_id):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('LambdaDynamo')

    try:
        response = table.get_item(Key={'user_id': user_id})
    except ClientError as err:
        return err.response['Error']['Message'] + " - " + err.response['Error']['Code']
    else:
        return response['Item']

def add_user():    
    try:
        table.put_item(
            Item={
                'user_id': '280852388',
                'first_name': 'Juan',
                'last_name': 'Paulo',
                'text': 'Hello World'
            }
        )
        message = "Added User"
    except ClientError as err:
        message = err.response['Error']['Message'] + " - " + err.response['Error']['Code']
    else:
        return message


# Write Telegram Bot Token
tgrm_token = "6631715010:AAFByiI3GWcJfr-gNxEruYSgrei4Xa0snXw"

url = "https://api.telegram.org/bot{}/".format(tgrm_token)

# Send Message to Telegram
def send_message(text, chat_id):
    text = text.replace("#", "%23")
    text = text.replace("&", "%26")
    text = text.replace(" ", "%20")
    url = "https://api.telegram.org/bot{}/sendMessage?text={}&chat_id={}".format(
        tgrm_token, text, chat_id
    )
    requests.get(url)


# @app.get("/")
# @tracer.capture_method
# def hello():
#     # adding custom metrics
#     # See: https://awslabs.github.io/aws-lambda-powertools-python/latest/core/metrics/
#     metrics.add_metric(name="HelloWorldInvocations", unit=MetricUnit.Count, value=1)

#     # structured log
#     # See: https://awslabs.github.io/aws-lambda-powertools-python/latest/core/logger/
#     logger.info("Hello world API - HTTP 200")
#     return {"message": "hello world"}

# Enrich logging with contextual information from Lambda
# @logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST)
# # Adding tracer
# # See: https://awslabs.github.io/aws-lambda-powertools-python/latest/core/tracer/
# @tracer.capture_lambda_handler
# # ensures metrics are flushed upon request completion/failure and capturing ColdStart metric
# @metrics.log_metrics(capture_cold_start_metric=True)
#def lambda_handler(event: dict, context: LambdaContext) -> dict:
def lambda_handler(event, context):
    # return app.resolve(event, context)
    send_message("Testing client", "280852388")
    response = get_user("280852388")
    message = response['text'] + " said " + response['first_name'] + " " + response['last_name']
    send_message(message, "280852388")
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Message sent to Telegram",
            # "location": ip.text.replace("\n", "")
        }),
    }
