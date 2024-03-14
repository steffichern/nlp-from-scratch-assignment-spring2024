from bs4 import BeautifulSoup
import os

def create_course_files_from_html(html_file):
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
            file_name = f"{cells[0]}: {cells[1]}.txt".replace('/', '')
            file_content = f"Course Number: {cells[0]}\nTitle: {cells[1]}\nUnits: {cells[2]}\nLec/Sec: {cells[3]}\nDays: {cells[4]}\nBegin: {cells[5]}\nEnd: {cells[6]}\nBldg/Room: {cells[7]}\nLocation: {cells[8]}\nInstructor: {cells[9]}"

            # Write course details to the file
            with open(file_name, 'w', encoding='utf-8') as course_file:
                course_file.write(file_content)

# Replace 'path/to/your/html_file.html' with the actual path of the HTML file
create_course_files_from_html('spring.html')
create_course_files_from_html('fall.html')
