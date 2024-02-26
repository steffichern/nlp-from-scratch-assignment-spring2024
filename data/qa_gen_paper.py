import random
import os

path_prefix = os.environ.get("DATA_PATH")


def read_paper_titles():
    titles = []
    filename = path_prefix+"paper_index.txt"
    # The file is formatted as "author: [paper1,paper2,paper3]"
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            parsed_titles= line.split(':')[1].replace("[", "").replace("]", "").replace(" ","").replace("\'", "").split(',')
            # print(f"parsed_titles: {parsed_titles}")
            titles += parsed_titles
    return titles

def generate_questions(paper_titles):
    question_types = [
        "Who are the authors of {title}?",
        "What's the publication venue of {title}?",
        "Summarize the contents of {title}?",
        "Which year was {title} published?"
    ]

    questions = []
    for _ in range(5):  # Generate 5 questions for each type
        for question_template in question_types:
            title = random.choice(paper_titles)
            question = question_template.format(title=title)
            questions.append(question)

    random.shuffle(questions)  # Mess the order of questions
    return questions

if __name__ == "__main__":
    paper_titles = read_paper_titles()
    for t in paper_titles:
        if t is None or t == "" or len(t) == 0:
            paper_titles.remove(t)
    # print(f"paper_titles: {paper_titles}")
    questions = generate_questions(paper_titles)
    for question in questions:
        print(question)
