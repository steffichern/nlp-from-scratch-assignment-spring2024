import requests
from bs4 import BeautifulSoup


def convert_tag_to_text(tag):
    text_parts = []

    # Iterate over each element within the given tag
    for element in tag.contents:
        if element.name == 'br':
            # Replace <br> tags with newlines
            text_parts.append('\n')
        elif element.name == 'span':
            # Directly append text from <span> tags and add a newline for separation
            text_parts.append(element.get_text() + '\n')
        elif element.string:
            # Append text directly if the element is a NavigableString
            text_parts.append(element.string.strip())
        else:
            # Recursively handle other tags
            text_parts.append(convert_tag_to_text(element))

    return ''.join(text_parts).strip()

def fetch_and_parse(url):
    response = requests.get(url)
    html_content = response.text


    soup = BeautifulSoup(html_content, 'html.parser')

    # Remove scripts, styles, and navigation bars
    for script_or_style in soup(["script", "style"]):
        script_or_style.decompose()

    # Initialize a list to store extracted texts
    extracted_texts = []

    # Extract and convert text from each <p> and <h2> tag
    for tag in soup.find_all(["p", "h2"]):
        extracted_texts.append(convert_tag_to_text(tag))


    text_file_path = "./events/commencement.txt"
    with open(text_file_path, "w", encoding='utf-8') as file:
        for text in extracted_texts:
            file.write(f"{text}\n")


fetch_and_parse('https://www.cmu.edu/commencement/schedule/index.html')