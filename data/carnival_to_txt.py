import requests
from bs4 import BeautifulSoup
from collections import OrderedDict

def fetch_and_parse(url):
    file_path = './carnival.html'

    # Read the HTML file
    with open(file_path, 'r', encoding='utf-8') as html_file:
        content = html_file.read()

    soup = BeautifulSoup(content, 'html.parser')
    text = [string.strip() for string in soup.stripped_strings]

    # Join the text elements into a single string
    all_text = '\n'.join(text)

    '''
    # Remove scripts and styles
    for script_or_style in soup(["script", "style"]):
        script_or_style.decompose()

    selectors_to_remove = ['.menu', '#navigation', '.footer']  
    for selector in selectors_to_remove:
        for elem in soup.select(selector):
            elem.decompose()

    text_lines = []

    # Handle <h2> and <p> specifically to insert newlines
    for elem in soup.find_all(['h2', 'p', 'span', 'div', 'title']):
        # Check if the tag is a div with a class attribute or any other specified condition
        if elem.name == 'div' and 'class' in elem.attrs:
            # Specific logic for div tags with a class, e.g., add a newline before the div content
            text_lines.append('\n')  # Adjust this line as needed for your requirements

        # Strip the text and add a newline before it if it's not empty
        text = elem.get_text().strip()
        if text:
            if text_lines: 
                text_lines.append('\n')  
            text_lines.append(text)

    # Remove duplicates while preserving order
    text_lines = list(OrderedDict.fromkeys(text_lines))
'''
    text_file_path = "./events/carnival.txt"
    with open(text_file_path, "w", encoding='utf-8') as file:
        for line in all_text:
            file.write(f"{line}")



fetch_and_parse('https://web.cvent.com/event/ab7f7aba-4e7c-4637-a1fc-dd1f608702c4/websitePage:645d57e4-75eb-4769-b2c0-f201a0bfc6ce?locale=en')