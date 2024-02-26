import random
from paper_discovery import read_author_ids

# Sample list of faculty names
faculty_names = read_author_ids().keys()
# Questions types
question_templates = [
    "Where is the office of {name}?",
    "What's the email address of {name}?",
    "What's the phone number of {name}?",
    "What are the research interests of {name}?",
    "What's the position of {name}?",
    "What paper did {name} publish?"
]

def generate_questions(names, templates):
    questions = []
    for i in range(len(templates)):
        # Select 5 random names for each question type
        qtemplate = templates[i]
        selected_names = random.sample(names, 5)
        for name in selected_names:
            # Format question with the selected name
            question = qtemplate.format(name=name)
            questions.append(question)
    # Shuffle the list of questions to mess up the order
    random.shuffle(questions)
    return questions

# Generate and print the questions
generated_questions = generate_questions(faculty_names, question_templates)
for question in generated_questions:
    print(question)
