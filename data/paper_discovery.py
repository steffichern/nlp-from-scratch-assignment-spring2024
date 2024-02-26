import os
import requests
import PyPDF2
from io import BytesIO
from faculty_site_discovery import discover_faculty_pages

path_prefix = os.environ.get("DATA_PATH")+"faculty_papers/"


def read_author_ids():
    name_id_dict = {}
    filename = path_prefix+"author_ids.txt"
    # Open the file in read mode
    with open(filename, 'r') as file:
        # Read each line in the file
        for line in file:
            # Strip any leading/trailing whitespace from the line
            line = line.strip()
            # Split the line into name and id based on the colon
            name, id = line.split(':')
            # Add the name-id pair to the dictionary
            name_id_dict[name] = id
    
    return name_id_dict

def get_paper_ids(author_id, api_key):
    url = f"https://api.semanticscholar.org/graph/v1/author/{author_id}"
    # url += "?fields=papers.title,papers.abstract,papers.authors,papers.year,papers.venue,papers.tldr"
    url += "?fields=papers.year"
    headers = {"x-api-key": api_key}
    response = requests.get(url, headers=headers).json()
    # print(f"get_paper_ids response: {response}\n")
    # print(type(response))
    papers = []
    if 'papers' in response:
        for paper in response['papers']:
            # print(f"response: {paper}")
            if 'year' in paper and paper['year'] == 2023:
                print(f"appended paper: {paper['paperId']}")
                papers.append(paper['paperId'])
    return papers

# This does two things:
# 1. It writes the paper metadata to a file along with its full text if available.
# 2. It builds the paper_index dictionary which maps faculty names to their papers.
def record_paper(author_name, paperid,paper_index):
    url = f"https://api.semanticscholar.org/graph/v1/paper/{paperid}"
    url += "?fields=title,abstract,authors,year,venue,tldr,isOpenAccess,openAccessPdf"

    headers = {"x-api-key": api_key}
    response = requests.get(url, headers=headers).json()
    print(f"write_paper_to_file response: {response}")
    
    if 'paperId' in response:
        paper = response
        safe_name = author_name.replace(" ", "_")
        safe_title = paper['title'].replace(" ", "_")
        safe_title = safe_title.replace("/", "_")
        paper_index[author_name].append(safe_title)
        filename = f"{path_prefix}{safe_name}_{safe_title}.txt"
        filename = filename.replace("\'", "_")
        with open(filename, "w") as file:
            file.write(f"Title: {paper['title']}\n")
            file.write(f"Year: {paper['year']}\n")
            file.write("Authors: " + ", ".join([author['name'] for author in paper['authors']]) + "\n")
            file.write(f"Abstract: {paper.get('abstract', 'No abstract')}\n")
            file.write(f"Publication Venue: {paper.get('venue', 'No publicationVenue')}\n")
            file.write(f"TLDR: {paper['tldr']}\n")
            if paper['isOpenAccess'] == True and paper['openAccessPdf']:
                # Use the url field of openAccessPdf to download the paper and parse the paper by 
                #  calling download_write_pdf(url), then append the parsed paper to the file.
                url = paper['openAccessPdf']['url']
                print(f"Downloading and parsing {url}")
                pdf_text = download_write_pdf(url)  # PDF text is returned instead of saved
                if pdf_text:
                    file.write("\nFull paper text:\n")
                    file.write(pdf_text)
                else:
                    file.write("\nFailed to extract full paper text from PDF]\n")
                
def download_write_pdf(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to download {url} code : {response.status_code}")
        return None
    # response.raise_for_status()  # This will raise an exception for HTTP errors
    # Instead of saving the PDF directly, we first parse it
    with BytesIO(response.content) as f:
        reader = PyPDF2.PdfReader(f)
        text = ''
        for page_number in range(len(reader.pages)):
            text += reader.pages[page_number].extract_text() + "\n"
        text = text.encode('utf-8', 'ignore').decode('utf-8')
    return text


if __name__ == "__main__":
    api_key = os.environ.get("SEMANTIC_SCHOLAR_API")  # Replace with your Semantic Scholar API key
    
    faculty_id = read_author_ids()
    paper_index = {key: [] for key in faculty_id.keys()}
    for author_name, id in faculty_id.items():
        paperids = get_paper_ids(id, api_key)
        print(f"Papers by {author_name} in 2023:")
        for paperid in paperids:
            print(f"- {paperid}")
            record_paper(author_name, paperid,paper_index)
            
    # create an index file and write the paper_index to it
    with open(path_prefix+"paper_index.txt", "w") as file:
        for author, papers in paper_index.items():
            print(f"{author}: {papers}")
            file.write(f"{author}: {papers}\n")