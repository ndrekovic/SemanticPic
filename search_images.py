import chromadb
import torch
from sentence_transformers import SentenceTransformer

from config import TEXT_MODEL, DATABASE_PATH, COLLECTION_NAME, DEFAULT_N_RESULTS


def initialize_search():
    # load clip model for text search
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = SentenceTransformer(TEXT_MODEL)

    # establish connection to the existing ChromaDB
    chroma_client = chromadb.PersistentClient(path=DATABASE_PATH)
    collection = chroma_client.get_collection(name=COLLECTION_NAME)
    return model, collection, device


def search_images(search_query, model, collection, device,
                  n_results=DEFAULT_N_RESULTS):  # retrieve the search term from the user

    with torch.no_grad():
        text_embedding = model.encode(search_query, normalize_embeddings=True).tolist()

    # get the top 3 results from the database based on the text vector
    results = collection.query(
        query_embeddings=[text_embedding],
        n_results=n_results,
        include=["documents", "distances"]
    )

    # show results
    print("\n--- Best results ---")
    for doc, distance in zip(results['documents'][0], results['distances'][0]):
        # distance shows how similar the image is to the search term (lower distance = more similar)
        print(f"Image path: {doc} (distance: {distance:.4f})")
    print("Result:", results)
    return results
