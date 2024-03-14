from bs4 import BeautifulSoup
import random
import pandas as pd

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
    
    
def parseEXCELtoQA(
    excel_path="2324-academic-calendar-list-view.xlsx", 
    questions_events_path_="questions_events_filtered.txt",
    answers_events_path="reference_answers_events_filtered.txt"):

    # Load the Excel file
    df = pd.read_excel(excel_path)
    df_cleaned = df.iloc[4:, [0, 4]].dropna()  # Skipping header rows and selecting only date and event columns
    df_cleaned.columns = ['Date', 'Event']  # Renaming columns for clarity
    
    # Attempt to convert 'Date' column to datetime, but ignore errors and keep original values for inspection
    df_cleaned['Date'] = pd.to_datetime(df_cleaned['Date'], errors='coerce')

    # Filter out rows where 'Date' conversion to datetime was unsuccessful (NaT values)
    df_filtered = df_cleaned.dropna(subset=['Date'])

    # Convert 'Date' back to date format (without time component) for the remaining valid rows
    df_filtered['Date'] = df_filtered['Date'].dt.date

    # Now, let's randomly select 50 events from the filtered dataframe
    selected_events_filtered = df_filtered.sample(n=min(50, len(df_filtered)), random_state=1)

    # Generate questions and answers for the filtered events
    questions_events_filtered = []
    answers_events_filtered = []

    for index, row in selected_events_filtered.iterrows():
        question_type = random.choice(["date", "event"])
        if question_type == "date":
            questions_events_filtered.append(f"When is {row['Event']}?")
            answers_events_filtered.append(row["Date"].strftime('%m/%d/%Y'))
        elif question_type == "event":
            questions_events_filtered.append(f"What is happening on {row['Date'].strftime('%m/%d/%Y')}?")
            answers_events_filtered.append(row["Event"])

    with open(questions_events_path_, "w+") as qef_file:
        qef_file.write("\n".join(questions_events_filtered))

    with open(answers_events_path, "w+") as aef_file:
        aef_file.write("\n".join(answers_events_filtered))
        
    print("Done! Files created successfully.")
    

def parseHTMLtoTXT():
    # Reformat the course information according to the specified format
    formatted_courses_v2 = []
    
    for row in rows[1:]:
        cells = row.find_all('td')
        cell_texts = [cell.get_text(strip=True) for cell in cells]
    
        if all(cell_texts[:10]) and "TBA" not in cell_texts[4:7]:  # Check for completeness excluding 'TBA' for time slots
            formatted_course_v2 = f"Course Architecture: {cell_texts[0]}, Title: {cell_texts[1]}, Units: {cell_texts[2]}, Lec/Sec: {cell_texts[3]}, Days: {cell_texts[4]}, Begin: {cell_texts[5]}, End: {cell_texts[6]}, Bldg/Room: {cell_texts[7]}, Location: {cell_texts[8]}, Instructor: {cell_texts[9]}"
            formatted_courses_v2.append(formatted_course_v2)
    
    # Save the reformatted courses to a new txt file
    output_path_v2 = 'Courses/spring.txt'
    with open(output_path_v2, 'w', encoding='utf-8') as output_file_v2:
        for course in formatted_courses_v2:
            output_file_v2.write(course + '\n')
    
    return output_path_v2

    
def parsePDFtoTXT():
    from PyPDF2 import PdfReader

    # Load and read the PDF file
    pdf_path = '/data/handbook_phd_2023-2024.pdf'
    reader = PdfReader(pdf_path)
    
    # Extract text from each page
    text_content = [page.extract_text() for page in reader.pages]
    
    # Combine text from all pages into a single string, stripping leading/trailing spaces on each line and removing empty lines
    cleaned_text = "\n".join([line.strip() for page in text_content for line in page.splitlines() if line.strip()])
    
    # Save the cleaned text to a new txt file
    output_path_pdf_to_text = '/data/handbook_phd_2023-2024_cleaned.txt'
    with open(output_path_pdf_to_text, 'w', encoding='utf-8') as output_file:
        output_file.write(cleaned_text)
    
    return output_path_pdf_to_text


from bs4 import BeautifulSoup
import os

def create_course_files_from_html(html_file, s="Spring"):
    # Open and read the HTML file
    with open(html_file, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract course rows - adjust the selector based on the actual structure
    course_rows = soup.find_all('tr')[1:]  # Assuming the first row is headers

    for row in course_rows[1:]:
        cells = row.find_all('td')
        cells = [cell.get_text(strip=True) for cell in cells]

        if all(cells[:10]):
            # Create a file name from course code and title
            file_name = f"{s} {cells[0]}: {cells[1]}.txt".replace('/', '')
            file_content = f"Course Number: {cells[0]}\nTitle: {cells[1]}\nUnits: {cells[2]}\nLec/Sec: {cells[3]}\nDays: {cells[4]}\nBegin: {cells[5]}\nEnd: {cells[6]}\nBldg/Room: {cells[7]}\nLocation: {cells[8]}\nInstructor: {cells[9]}"

            # Write course details to the file
            with open(file_name, 'w', encoding='utf-8') as course_file:
                course_file.write(file_content)

# Replace 'path/to/your/html_file.html' with the actual path of the HTML file
create_course_files_from_html('spring.html', s="Spring")
create_course_files_from_html('fall.html', s="Fall")


