import requests

def get_author_id(name, api_key):
    url = f"https://api.semanticscholar.org/graph/v1/author/search?query={name}&limit=1"
    headers = {"x-api-key": api_key}
    response = requests.get(url, headers=headers).json()
    # Assuming the first result is the correct author
    author_id = response['data'][0]['authorId'] if response['data'] else None
    return author_id

def get_papers_by_author_id(author_id, api_key):
    url = f"https://api.semanticscholar.org/graph/v1/author/{author_id}/papers?limit=5"  # Adjust limit as needed
    headers = {"x-api-key": api_key}
    response = requests.get(url, headers=headers).json()
    papers = response['data'] if 'data' in response else []
    return papers

api_key = "YOUR_API_KEY_HERE"  # Replace with your Semantic Scholar API key
faculty_names = ["Faculty Name 1", "Faculty Name 2"]  # Replace with actual faculty names

for name in faculty_names:
    author_id = get_author_id(name, api_key)
    if author_id:
        papers = get_papers_by_author_id(author_id, api_key)
        print(f"Papers by {name}:")
        for paper in papers:
            print(f"- {paper['title']}")
    else:
        print(f"Author ID not found for {name}")
