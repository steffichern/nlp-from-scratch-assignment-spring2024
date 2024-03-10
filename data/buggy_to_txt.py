import requests
from bs4 import BeautifulSoup


def fetch_and_parse(url):
    response = requests.get(url)
    html_content = response.text

    soup = BeautifulSoup(html_content, 'html.parser')

    # Remove scripts and styles
    for script_or_style in soup(["script", "style"]):
        script_or_style.decompose()

    selectors_to_remove = ['.menu', '#navigation', '.footer']  
    for selector in selectors_to_remove:
        for elem in soup.select(selector):
            elem.decompose()

    text_lines = []

    # Handle <h1>, <h2>, <p>, and <em> specifically to insert newlines
    for elem in soup.find_all(['h1', 'h2', 'p', 'em']):

        # Strip the text and add a newline before it if it's not empty
        text = elem.get_text().strip()
        if text:
            # Inserting a newline before each <h2> and <p> content except the first
            if text_lines: 
                text_lines.append('\n')  
            text_lines.append(text)

    text_file_path = "./history/buggy.txt"
    with open(text_file_path, "w", encoding='utf-8') as file:
        for line in text_lines:
            file.write(f"{line}")

fetch_and_parse('https://www.cmu.edu/news/stories/archives/2019/april/spring-carnival-buggy.html')
