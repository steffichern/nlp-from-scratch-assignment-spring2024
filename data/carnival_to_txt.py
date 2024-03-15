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

    text_file_path = "./events/carnival.txt"
    with open(text_file_path, "w", encoding='utf-8') as file:
        for line in all_text:
            file.write(f"{line}")



fetch_and_parse('https://web.cvent.com/event/ab7f7aba-4e7c-4637-a1fc-dd1f608702c4/websitePage:645d57e4-75eb-4769-b2c0-f201a0bfc6ce?locale=en')