import os
import requests
from bs4 import BeautifulSoup
import re
from data.faculty_site_discovery import discover_faculty_pages

def fetch_and_parse(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        soup = BeautifulSoup(response.text, 'html.parser')

        # Define titles to be removed
        titles_to_remove = ["Academics", "Partnership", "News",
                            "Events", "LTI Intranet", "Contact Us", "Careers",
                            "navigation", "Apply", "People", "Search form", "Search",]

        # Remove script and style elements
        for script_or_style in soup(["script", "style"]):
            script_or_style.decompose()

        # Remove specific titles
        for title in titles_to_remove:
            for matching_element in soup.find_all(string=re.compile(r'\b' + re.escape(title) + r'\b', flags=re.IGNORECASE)):
                matching_element.extract()

        # Get text and filter out blanks and unnecessary spaces
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        return text, soup
    except Exception as e:
        print(f"Error fetching or parsing {url}: {e}")
        return None, None



websites = discover_faculty_pages()

for faculty, urls in websites.items():
    print(f"Processing faculty {faculty} pages...")
    path_prefix =  os.environ.get("DATA_PATH")+"faculty_websites/"
    text, soup = fetch_and_parse(urls[0])
    # Process and write the LTI page content
    lti_page_text, _ = fetch_and_parse(urls[0])  # Assuming the first URL is always present
    if lti_page_text:
        with open(f"{path_prefix}{faculty}_lti_page.txt", "w") as file:
            file.write(lti_page_text)
    
    # If there's a second URL, process and write the personal page content
    if len(urls) > 1 and urls[1] is not None:
        personal_page_text, _ = fetch_and_parse(urls[1])
        if personal_page_text:
            with open(f"{path_prefix}{faculty}_personal_page.txt", "w") as file:
                file.write(personal_page_text)
