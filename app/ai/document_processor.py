from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def load_documents():

    menu_path = DATA_DIR / "dinease_menu_knowledge.pdf"
    policy_path = DATA_DIR / "dinease_restaurant_policy.pdf"

    menu_documents = PyPDFLoader(
        str(menu_path)
    ).load()

    policy_documents = PyPDFLoader(
        str(policy_path)
    ).load()

    for document in menu_documents:
        document.metadata["source_type"] = "menu"

    for document in policy_documents:
        document.metadata["source_type"] = "policy"

    return menu_documents + policy_documents


def split_documents(documents):

    menu_documents = [
        document
        for document in documents
        if document.metadata.get("source_type") == "menu"
    ]

    policy_documents = [
        document
        for document in documents
        if document.metadata.get("source_type") == "policy"
    ]

    menu_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    policy_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )

    menu_chunks = menu_splitter.split_documents(
        menu_documents
    )

    policy_chunks = policy_splitter.split_documents(
        policy_documents
    )

    for chunk in menu_chunks:
        chunk.metadata["content_type"] = "menu"

    for chunk in policy_chunks:
        chunk.metadata["content_type"] = "policy"

    print(
        f"Created {len(menu_chunks)} menu chunks."
    )

    print(
        f"Created {len(policy_chunks)} policy chunks."
    )

    return menu_chunks + policy_chunks