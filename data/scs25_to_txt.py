import requests
from bs4 import BeautifulSoup


def fetch_and_parse(url):
    response = requests.get(url)
    html_content = response.text

    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Remove scripts and styles
    for script_or_style in soup(["script", "style"]):
        script_or_style.decompose()

    selectors_to_remove = ['.menu', '#navigation', '.footer']  
    for selector in selectors_to_remove:
        for elem in soup.select(selector):
            elem.decompose()

    # Get the text and split into lines
    lines = (line.strip() for line in soup.get_text().splitlines())
    # Filter out blank lines
    text_lines = [line for line in lines if line]

    text_file_path = "./history/scs25.txt" 
    with open(text_file_path, "w", encoding='utf-8') as file:
        for line in text_lines:
            file.write(f"{line}\n")

fetch_and_parse('https://www.cs.cmu.edu/scs25/25things')

