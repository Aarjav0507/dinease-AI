from pathlib import Path

from langchain_mistralai import MistralAIEmbeddings
from langchain_community.vectorstores import FAISS

from app.core.config import settings


VECTOR_DB_DIR = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "faiss_db"
)


def get_vector_store():

    embeddings = MistralAIEmbeddings(
        model="mistral-embed",
        api_key=settings.MISTRAL_API_KEY
    )

    vector_store = FAISS.load_local(
        str(VECTOR_DB_DIR),
        embeddings,
        allow_dangerous_deserialization=True
    )

    return vector_store


def get_retriever():

    vector_store = get_vector_store()

    return vector_store.as_retriever(
        search_kwargs={
            "k": 8
        }
    )