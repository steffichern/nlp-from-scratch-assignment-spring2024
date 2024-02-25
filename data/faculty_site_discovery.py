import requests
from bs4 import BeautifulSoup
import re

def fetch_and_parse(url, base_url="https://lti.cs.cmu.edu"):
    """
    Fetch content from the given URL and parse it to extract links.
    Adjusted to handle relative links by prefixing with the base URL.
    """
    # Handle relative URLs
    if url.startswith('/'):
        url = base_url + url

    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup
    except Exception as e:
        print(f"Error fetching or parsing {url}: {e}")
        return None

def discover_faculty_pages():
    faculty_dict = {}
    visited = set()  # To track visited URLs
    base_urls = ["https://lti.cs.cmu.edu/directory/all/154/1", "https://lti.cs.cmu.edu/directory/all/154/1?page=1"]
    for base_url in base_urls:
        soup = fetch_and_parse(base_url)
        if soup:
            for link in soup.find_all('a', href=True):
                if link['href'].startswith('/people'):
                    faculty_url = "https://lti.cs.cmu.edu" + link['href']
                    if faculty_url not in visited:
                        visited.add(faculty_url)
                        faculty_soup = fetch_and_parse(faculty_url)
                        faculty_name = faculty_url.split('/')[-1].replace('-', ' ').title()  # Extracting name from URL
                        personal_website = None

                        if faculty_soup:
                            # Attempt to find a personal website link
                            for a_tag in faculty_soup.find_all('a', text=re.compile("website", re.IGNORECASE)):
                                if a_tag['href']:
                                    personal_website = a_tag['href']
                                    break
                        
                        if personal_website:
                            faculty_dict[faculty_name] = [faculty_url, personal_website]
                        else:
                            print(f"Cannot find personal website of faculty {faculty_name}")
                            faculty_dict[faculty_name] = [faculty_url, None]

    return faculty_dict

def is_subsequence(s1, s2):
    it = iter(s2)
    return all(char in it for char in s1)

if __name__ == "__main__":
    # Usage example
    faculty_websites = discover_faculty_pages()

    duplicate_faculty = []
    for f in faculty_websites.keys():
        if f in duplicate_faculty:
            continue
        for another_f in faculty_websites.keys():
            
            if f != another_f and is_subsequence(f, another_f):
                print(f"Duplicate: {f} and {another_f}")
                duplicate_faculty.append(f) if len(f) > len(another_f) else duplicate_faculty.append(another_f)
    for d in duplicate_faculty:
        del faculty_websites[d]


    print("--------------------\n\n")
    print(f"Num of faculty discovered: {len(faculty_websites)}")
    print("--------------------\n\n")

    print(sorted(faculty_websites.keys()))
    for faculty, urls in faculty_websites.items():
        print(f"{faculty}: {urls}")


