import logging
import sys

import psycopg2
from llama_index.core import SimpleDirectoryReader, StorageContext
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.postgres import PGVectorStore
import textwrap

import os
import dotenv
from sqlalchemy import make_url


try:
    os.remove("data/test/generated_answers.txt")
    os.remove("generated_answers.txt")
except Exception as e:
    pass


# Uncomment to see debug logs
# logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, force=True)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings

Settings.embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-small-en-v1.5"
)

from llama_index.core import SimpleDirectoryReader
# reader = SimpleDirectoryReader(
#     input_files=["./data/faculty_websites/Bhiksharaj_lti_page.txt"]
# )
reader = SimpleDirectoryReader(input_dir="./data/faculty_papers/")
docs = reader.load_data()
reader = SimpleDirectoryReader(input_dir="./data/faculty_websites/")
docs += reader.load_data()
reader = SimpleDirectoryReader(input_dir="./data/Academics/")
docs += reader.load_data()
reader = SimpleDirectoryReader(input_dir="./data/Courses/")
docs += reader.load_data()
reader = SimpleDirectoryReader(input_dir="./data/events/")
docs += reader.load_data()
reader = SimpleDirectoryReader(input_dir="./data/history/")
docs += reader.load_data()
print(f"Loaded {len(docs)} docs")



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


storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(
    docs, storage_context=storage_context, show_progress=True
)


from llama_index.core import PromptTemplate
from llama_index.core import get_response_synthesizer
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine

from llama_index.llms.ollama import Ollama
from llama_index.core import Settings
# ollama
Settings.llm = Ollama(model="gemma", request_timeout=999999.0, context_window=60000)

# configure retriever
retriever = VectorIndexRetriever(
    index=index,
    similarity_top_k=3,
)

# configure response synthesizer
response_synthesizer =get_response_synthesizer(response_mode = "compact")

# assemble query engine with compact mode
query_engine = RetrieverQueryEngine(
    retriever=retriever,
    response_synthesizer=response_synthesizer,
)

# query_engine = index.as_query_engine()
prompts_dict = query_engine.get_prompts()
print(list(prompts_dict.keys()))
print(list(prompts_dict.values()))


# prompt engineering

qa_prompt_tmpl_str = (
    "You are a Q/A system that can answer questions based on the given context.\n"
    "Avoid verbose contents such as 'based on the context...' or 'Sure, here is the answer to the query'.\n"
    "Make the answer as short and concise as possible.\n"
    "Instructions for answering course-related questions:\n"
    "Return answer from a single course (do not add results together). "
    "If there are more than one answers, return a random one."
    "If asked about the time, please answer in the format of '08:00AM' and nothing else."
    "If asked about the course number, please answer in the format of '12345' and nothing else."
    "If asked about the name of the instructor or the course name, please answer only the name and nothing else."
    "If asked about the units/credit of a course, please answer in the format of '8.0' and nothing else."
    "If you cannot find the info, answer 'None' and nothing else."
    "\n"
    "Context information is below: \n"
    "---------------------\n"
    "{context_str}\n"
    "---------------------\n"
    "Given the context information and not prior knowledge, "
    "answer the query. If you can, directly reference the context.\n"
    "Query: {query_str}\n"
    "Answer: "
)

refine_prompt_tmpl_str = (
    "You are a Q/A system that can answer questions based on the given context.\n"
    "Avoid verbose contents such as 'based on the context...' or 'Sure, here is the answer to the query'.\n"
    "Make the answer as short and concise as possible.\n"
    "Instructions for answering course-related questions:\n"
    "Return answer from a single course (do not add results together). "
    "If there are more than one answers, return a random one."
    "If asked about the time, please answer in the format of '08:00AM' and nothing else."
    "If asked about the course number, please answer in the format of '12345' and nothing else."
    "If asked about the name of the instructor or the course name, please answer only the name and nothing else."
    "If asked about the units/credit of a course, please answer in the format of '8.0' and nothing else."
    "If you cannot find the info, answer 'None' and nothing else."
    "\n"
    "Context information is below: \n"
    "---------------------\n"
    "{context_str}\n"
    "---------------------\n"
    "Given the context information and not prior knowledge, "
    "answer the query. If you can, directly reference the context.\n"
    "If the context does not contain the answer, simply return the original answer.\n"
    "Query: {query_str}\n"
    "Answer: "
)

# # check_ctx_prompt = "print {context_str}"
qa_prompt_tmpl = PromptTemplate(qa_prompt_tmpl_str)
refine_prompt_tmpl = PromptTemplate(refine_prompt_tmpl_str)
query_engine.update_prompts(
    {"response_synthesizer:text_qa_template": qa_prompt_tmpl, "response_synthesizer:refine_template": refine_prompt_tmpl}
)


# Answering our questions
print("Answering our questions")
our_questions = 'data/train/questions.txt'
questions = []
with open(our_questions, 'r') as file:
    for line in file:
        # print(f"append question: {question} to list of questions")
        questions.append(line)

answers = []
for q in questions:
    response = query_engine.query(q)
    answer = textwrap.fill(str(response), 100)
    answer = answer.replace("\n", " ")

    with open('data/test/generated_answers.txt', 'a') as file:
        file.write(answer)
        file.write("\n")
    answers.append(answer)
    
    
# Answering released test questions
print("Answering released test questions")
our_questions = 'released_questions.txt'
questions = []
with open(our_questions, 'r') as file:
    for line in file:
        questions.append(line)

answers = []
for q in questions:
    response = query_engine.query(q)
    answer = textwrap.fill(str(response), 100)
    answer = answer.replace("\n", " ")
    with open('generated_answers.txt', 'a') as file:
        file.write(answer)
        file.write("\n")
    answers.append(answer)