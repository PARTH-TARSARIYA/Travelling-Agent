from langchain.tools import tool

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

embeddings = HuggingFaceEmbeddings(
    model_name = 'sentence-transformers/all-MiniLM-L6-V2'
)

vectore_store = FAISS.load_local(
    'faiss_index',
    embeddings,
    allow_dangerous_deserialization = True
)

retriever = vectore_store.as_retriever(
    search_kwargs = {'k' : 3}
)

@tool
def search_places_rag(query : str) -> str:
    """
    Search tourist places using semantic similarity.
    Use this tool for travel recommendations,
    attractions, temples, beaches, nightlife,
    and tourist activities.
    """

    docs = retriever.invoke(query)

    if not docs:
        return 'no matching place found'
    
    result = []

    for doc in docs:
        result.append(doc.content)

    return '\n\n'.join(result)