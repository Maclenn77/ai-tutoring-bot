from lib.messenger import Messenger as msg
from lib.chat_model import ChatModel
from lib.tutor_chain import TutorChain
from langchain.memory.chat_message_histories import DynamoDBChatMessageHistory
import json
from aws_lambda_powertools import Logger
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessage,
    HumanMessagePromptTemplate,
    MessagesPlaceholder
)
from langchain.memory import ConversationBufferMemory

logger = Logger()

# Create a Menu class that will be used to create a menu for the bot
class Menu:
    def __init__(self, config, table):
        self.config = {
            "TELEGRAM_TOKEN": config['TELEGRAM_TOKEN'],
            "OPENAI_API_KEY": config['OPENAI_API_KEY']
        }
        self.msg = msg(self.config)
        self.table = table

    def start(self, chat_info):
        """Add user to DynamoDB table and send welcome message"""

        chat_id = chat_info['id']
        response = self.table.new_user(chat_info)
        logger.info(response)
        message = """Hello, {}. I'm a bot that can help you to learn any High School subject. \n
        Select a subject with */subject SUBJECT*. \n Please type */help* to see what I can do for you.
        """.format(chat_info['first_name'])
        response = self.msg.send_to_telegram(message, chat_id)
        logger.info(response.json())

    def help(self, chat_id):
        """Send help message"""

        message="""I can help you to learn any High School subject. \n
        - Write \*/subject Subject to start learning a subject or change subject. Ex: /subject Math\n
        - Write \*/evaluate\* to be evaluate about a subject\n
        - Write \*/history\* to see your last messages\n
        - Write \*/help\* to see this message again\n
        - Write \*/about\* to know more about this app\n"""
        self.msg.send_to_telegram(message, chat_id)
        pass

    def about():
        """Send about message"""
        pass

    def subject(self, chat_id, message):
        """Change subject or assign a new subject to user"""

        subject = message.split(' ')[1:]

        response = self.table.update_subject(chat_id, " ".join(subject))
        logger.info(response)
        self.msg.send_to_telegram("Okay! Let's study " + subject, chat_id)

    def evaluate():
        """Evaluate user about a subject"""
        pass

    def interaction(self, chat_id, message):
        """Send message to GPT-3 and save it to DynamoDB table"""

        user = self.table.get_user(chat_id)

        if 'subject' in user:
            # send chat_id, user_data to prepare prompt
            # prompt = prepare_prompt(chat_id, user_data)
            history = DynamoDBChatMessageHistory(table_name="SessionTable", session_id=str(chat_id))
            template = """You're a friendly and patient High School Tutor. A student called {student_name} has asked help for the subject {subject_to_study}.
    If the subject is not related to high school, you must ask the student to change the subject using the command /subject SUBJECT.
    If the subject is related to High School, you should help the student to learn the subject.
    When student asks a question, you should answer it. If the student doesn't ask a question, you should ask a question to the student about the subject or give a curious fact.
    Sometimes refer to the student by name, but don't overdo it.
    Previous messages:

    [Student {student_name}]: [/subject {subject_to_study}]
    [Tutor]: [Okay! Let's study {subject_to_study}]
    """.format(student_name=user['user_data']['first_name'], subject_to_study=user['subject'])
            logger.info(template)
            chat_prompt = ChatPromptTemplate.from_messages([SystemMessage(content=template),
                                                      MessagesPlaceholder(variable_name="chat_history"),
                                                      HumanMessagePromptTemplate.from_template("{text}")
                                                      ])
            memory = ConversationBufferMemory(memory_key="chat_history", chat_memory=history, return_messages=True)
            chat = ChatModel(openai_api_key=self.config['OPENAI_API_KEY'], temperature=1.2, model="gpt-3.5-turbo-0613")
            langchain = TutorChain(llm=chat,
                                   prompt=chat_prompt,
                                   memory=memory)
            response = langchain.run(message)
            logger.info(response)   
            self.msg.send_to_telegram(response, chat_id)
            history.add_user_message(message)
            history.add_ai_message(response)
        else:
            message = """"Before starting a chat, select a subject with the command /subject SUBJECT.\n
            Example: /subject Math"""
            self.msg.send_to_telegram(message, chat_id) 
        return

    def no_text(self, chat_id):
        """Respond to non-text messages"""

        message=""""Sorry, I can only respond to text messages. \n 
        Please try again. \n If you need help, type /help"""""
        self.msg.send_to_telegram(message, chat_id)
