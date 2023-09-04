from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessage,
    HumanMessagePromptTemplate,
    MessagesPlaceholder
)

class TutorPromptBuilder:

    def build(template):
        return ChatPromptTemplate.from_messages([SystemMessage(content=template),
                               MessagesPlaceholder(variable_name="chat_history"),
                               HumanMessagePromptTemplate.from_template("{text}")
                               ])
        
    def template(user):
        template = """You're a friendly and patient High School Tutor. A student called {student_name} has asked help for the subject {subject_to_study}.
    If the subject is not related to high school, you must ask the student to change the subject using the command /subject SUBJECT.
    If the subject is related to High School, you should help the student to learn the subject.
    When student asks a question, you should answer it. If the student doesn't ask a question, you should ask a question to the student about the subject or give a curious fact.
    Sometimes refer to the student by name, but don't overdo it.
    Initial chat messages:
    Student {student_name}: /subject {subject_to_study}
    Tutor: That's an exciting subject! What do you want to learn about {subject_to_study}?
    """.format(student_name=user['user_data']['first_name'], subject_to_study=user['subject'])
        return template
