
class UIMessages:

    def welcome_message(user_name):
        message = """Hello, {}. I'm a bot that can help you learn any High School subject.
        \nSelect a subject with /subject followed by the subject to study. Ex: /subject Math
        \nPlease type /help to see what I can do for you.
        """.format(user_name)
        return message
    
    help_message = """I can help you to learn any High School subject.
    \n- Write /subject Subject to start learning a subject or change subject. Ex: /subject Math
    \n- Write /help to see this message again.
    \n- Write /about to know more about this app
    \n\nOnce you select a subject, we can start to learn it."""
    
    about_message = """This bot was created by Juan Paulo Perez Tejada (2023).
        \nAI Tutoring Bot uses OpenAI's GPT-3 to generate responses to user's messages.
        \nVisit project repository: http://github.com/maclenn77/ai-tutoring-bot"""
    
    def subject_message(subject):
        message = "Okay! Let's study " + subject
        return message
    
    no_text_message = """"Sorry, I can only respond to text messages. Please try again. 
        \nIf you need help, type /help"""""
    
    no_subject_message = """Please specify a subject.
        \nExample: /subject Math"""
    
    no_subject_specified_message = """Please specify a subject.\nExample: /subject Math"""

    no_user_found_message = """Before starting a chat, type /start"""

    select_subject_message = """Before starting a chat conversation, select a subject with /subject followed by the subject to study. Ex: /subject Math"""