import json

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

with open('Data/places.json') as f:
    places = json.load(f)

documents = []

for place in places:
    doc = f"""
    Place name : {place['name']}

    City name : {place['city']}

    Type : {place['type']}

    Rating : {place['rating']}
    """

    documents.append(doc)

text_spliter = RecursiveCharacterTextSplitter(
    chunk_size = 300,
    chunk_overlap = 30
)

docs = text_spliter.create_documents(documents)

embeddings = HuggingFaceEmbeddings(
    model_name = 'sentence-transformers/all-MiniLM-L6-v2'
)

vectore_store = FAISS.from_documents(
    docs,
    embeddings
)

vectore_store.save_local('faiss_index')