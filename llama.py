from llama_index.core import SimpleDirectoryReader, StorageContext
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.postgres import PGVectorStore
import textwrap
import os
import sys
import dotenv
import logging

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, force=True)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings

Settings.embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-small-en-v1.5"
)

input_dir = "./data/Courses/"


def remove_nul_characters(input_dir):
    # Iterate through all files in the specified directory
    for filename in os.listdir(input_dir):
        if filename.endswith(".txt"):  # Check if the file is a .txt file
            file_path = os.path.join(input_dir, filename)
            # Open the file, read the contents and remove NUL characters
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                file_content = file.read()
                clean_content = file_content.replace('\x00', '')
                clean_content = os.linesep.join([line for line in clean_content.splitlines() if line.strip()])
            
            # Write the clean content back to the file
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(clean_content)
            print(f'Processed {filename}')

# Specify the directory containing your text files
remove_nul_characters(input_dir)


from llama_index.core import SimpleDirectoryReader
# reader = SimpleDirectoryReader(
#     input_files=["./data/faculty_websites/Bhiksharaj_lti_page.txt"]
# )
reader = SimpleDirectoryReader(input_dir=input_dir)
docs = reader.load_data()
# print(f"Loaded {len(docs)} docs")
print("Document ID:", docs[0].doc_id)

import psycopg2

# Reload the variables in your '.env' file (override the existing variables)
dotenv.load_dotenv("../.env", override=True)
pwd = os.environ['PG_PASSWORD_RAG']
user = "711-rag"
connection_string = f'dbname=postgres user={user} password={pwd}'
db_name = "711-rag"
conn = psycopg2.connect(connection_string)
conn.autocommit = True

with conn.cursor() as c:
    c.execute(f"DROP DATABASE IF EXISTS \"{db_name}\"")
    c.execute(f"CREATE DATABASE \"{db_name}\"")
    
from sqlalchemy import make_url

# url = make_url(connection_string)
vector_store = PGVectorStore.from_params(
    database=db_name,
    host="localhost",
    password=pwd,
    port=5432,
    user=user,
    table_name="all",
    embed_dim=384, 
)

from llama_index.llms.ollama import Ollama
from llama_index.core import Settings
# ollama
Settings.llm = Ollama(model="gemma", request_timeout=120.0, context_window=32768)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(
    docs, storage_context=storage_context, show_progress=True
)

query_engine = index.as_query_engine()
prompt_engineering = "Return answer from a single course (do not add results together). If there's more than one answers, return a random one. If asked about the time, please answer in the format of '08:00AM' and nothing else. If asked about the course number, please answer in the format of '12345' and nothing else. If asked about the name of the instructor or the course name, please answer only the name and nothing else. If asked about the units/credit of a course, please answer in the format of '8.0' and nothing else. If you cannot find the info, answer 'None' and nothing else."
question = "When does Presenting Performing Arts & Festivals start?"

response = query_engine.query(question + " " + prompt_engineering)

print("\n\n\nThe response is:\n\n\n")
print(textwrap.fill(str(response), 100))

