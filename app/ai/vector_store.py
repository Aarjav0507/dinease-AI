from pathlib import Path

from langchain_mistralai import MistralAIEmbeddings
from langchain_community.vectorstores import FAISS

from app.core.config import settings

from app.ai.document_processor import (
    load_documents,
    split_documents
)


VECTOR_DB_DIR = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "faiss_db"
)


def create_vector_store():

    documents = load_documents()

    print(f"Loaded {len(documents)} PDF pages.")

    chunks = split_documents(documents)

    print(f"Created {len(chunks)} text chunks.")

    embeddings = MistralAIEmbeddings(
        model="mistral-embed",
        api_key=settings.MISTRAL_API_KEY
    )

    vector_store = FAISS.from_documents(
        documents=chunks,
        embedding=embeddings
    )

    VECTOR_DB_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    vector_store.save_local(
        str(VECTOR_DB_DIR)
    )

    print("FAISS vector store created successfully.")

    return vector_store