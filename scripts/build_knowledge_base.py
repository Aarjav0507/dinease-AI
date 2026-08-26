from app.ai.vector_store import create_vector_store


if __name__ == "__main__":

    print("Building DineEase knowledge base...")

    create_vector_store()

    print("Knowledge base created successfully.")