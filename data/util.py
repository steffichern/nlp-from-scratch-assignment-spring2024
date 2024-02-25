from bs4 import BeautifulSoup
import random

def parseHTMLtoQA(
    html_content="Carnegie Mellon University - Full Schedule Of Classes.html", 
    questions_file_path="questions.txt", 
    answers_file_path="reference_answers.txt", 
    max_questions=100
    ):
    
    # Load the HTML content
    with open(html_content, "r", encoding="utf-8") as file:
        html_content = file.read()

    # Parse the HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # Define a function to check if a row is valid based on the required fields
    def is_valid_row(cells):
        # Required fields: course_number, title, units, begin, end, instructor
        # Checking if any of these fields are empty
        return all(cells[i].get_text(strip=True) for i in [0, 1, 2, 5, 6, 9])

    # Find all course rows
    course_rows = soup.find_all('tr')[2:]  # skipping header rows

    # Filter valid courses
    valid_courses = [row for row in course_rows if is_valid_row(row.find_all('td'))]

    # Select 100 random courses if there are enough, otherwise select as many as possible up to 100
    selected_courses = random.sample(valid_courses, max(max_questions, len(valid_courses)))

    # Extract information for the selected courses
    courses_info = []
    for course in selected_courses:
        cells = course.find_all('td')
        course_info = {
            "course_number": cells[0].get_text(strip=True),
            "title": cells[1].get_text(strip=True),
            "units": cells[2].get_text(strip=True),
            "begin": cells[5].get_text(strip=True),
            "end": cells[6].get_text(strip=True),
            "instructor": cells[9].get_text(strip=True)
        }
        courses_info.append(course_info)

    # Generate questions and answers
    questions = []
    answers = []
    for course in courses_info:
        question_type = random.choice([
            "course_number", "title", "instructor", "units", "begin", "end"
        ])
        if question_type == "course_number":
            questions.append(f"What is the course number of {course['title']}?")
            answers.append(course["course_number"])
        elif question_type == "title":
            questions.append(f"What is the name of course {course['course_number']}?")
            answers.append(course["title"])
        elif question_type == "instructor":
            questions.append(f"Who is the instructor of {course['title']}?")
            answers.append(course["instructor"])
        elif question_type == "units":
            questions.append(f"How many units does {course['title']} has?")
            answers.append(course["units"])
        elif question_type == "begin":
            questions.append(f"When does {course['title']} starts?")
            answers.append(course["begin"])
        elif question_type == "end":
            questions.append(f"When does {course['title']} ends?")
            answers.append(course["end"])

    with open(questions_file_path, "w+") as q_file:
        q_file.write("\n".join(questions))

    with open(answers_file_path, "w+") as a_file:
        a_file.write("\n".join(answers))

    print("Done! Files created successfully.")