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

from llama_index.core import PromptTemplate
from llama_index.core import get_response_synthesizer
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine

from llama_index.llms.ollama import Ollama
from llama_index.core import Settings
# ollama
llm = Ollama(model="mistral", request_timeout=999999.0, context_window=60000)

# Answering our questions
# print("Answering our questions")
# our_questions = 'data/train/questions.txt'
# questions = []
# with open(our_questions, 'r') as file:
#     for line in file:
#         # print(f"append question: {question} to list of questions")
#         questions.append(line)

# answers = []
# for q in questions:
#     response = llm.complete(q)
#     answer = textwrap.fill(str(response), 100)
#     answer = answer.replace("\n", " ")

#     with open('data/test/generated_answers.txt', 'a') as file:
#         file.write(answer)
#         file.write("\n")
#     answers.append(answer)


# Answering released test questions
print("Answering released test questions")
our_questions = 'released_questions.txt'
questions = []
with open(our_questions, 'r') as file:
    for line in file:
        questions.append(line)

answers = []
for q in questions:
    response = llm.complete(q)
    answer = textwrap.fill(str(response), 100)
    answer = answer.replace("\n", " ")
    with open('generated_answers.txt', 'a') as file:
        file.write(answer)
        file.write("\n")
    answers.append(answer)