import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

# Create DynamoDB client
class DynamoDB:
    """Encapsulates DynamoDB table with user's last conversations data"""
    
    def __init__(self, table_name) -> None:
        client = boto3.resource('dynamodb')
        self.table = client.Table(table_name)

    def new_user(self, chat_info):
        """Add user to DynamoDB table"""

        try:
            response = self.table.put_item(
                Item={
                    'user_id': str(chat_info['id']),
                    'user_data': {
                        'first_name': chat_info.get('first_name', ""),
                        'last_name': chat_info.get('last_name', ""),
                        'username': chat_info.get('username', ""),
                    }
                }
            )
        except ClientError as err:
            return err.response['Error']['Message'] + " - " + err.response['Error']['Code']
        else:
            return response
        
    def update_subject(self, chat_id, subject):
        """Add subject to DynamoDB table"""

        try:
            response = self.table.update_item(
                Key={ 'user_id': str(chat_id) },
                UpdateExpression="SET subject = :subject",
                ExpressionAttributeValues={
                    ':subject': subject
                },
                ReturnValues="UPDATED_NEW"
            )
        except ClientError as err:
            return err.response['Error']['Message'] + " - " + err.response['Error']['Code']
        else:
            return response

    # def add_message(self, chat_id, message_info):
    #     """Add user to DynamoDB table"""

    #     try:
    #         response = self.table.update_item(
    #             Key={ 'user_id': str(chat_id) },
    #             UpdateExpression="SET messages = list_append(messages, :message)",
    #             ExpressionAttributeValues={
    #                 ':message': message_info
    #             },
    #             ReturnValues="UPDATED_NEW"
    #         )
    #     except ClientError as err:
    #         return err.response['Error']['Message'] + " - " + err.response['Error']['Code']
    #     else:
    #         return response

    def get_user(self, chat_id):
        """Get user from DynamoDB table"""
        try:
            response = self.table.get_item(Key={'user_id': str(chat_id)})
        except ClientError as err:
            return err.response['Error']['Message'] + " - " + err.response['Error']['Code']
        else:
            return response['Item']