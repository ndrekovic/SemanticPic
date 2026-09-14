import chromadb
import clip
import torch

from index_images import model_name


def initialize_search():
    # load clip model for text search
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model, _ = clip.load(model_name, device=device)

    # establish connection to the existing ChromaDB
    chroma_client = chromadb.PersistentClient(path="./chroma_db")
    collection = chroma_client.get_collection(name="search_images")
    return model, collection, device


def search_images(search_query, model, collection, device, n_results=3):  # retrieve the search term from the user

    # turn the search query into a vector using CLIP
    text = clip.tokenize([search_query]).to(device)
    with torch.no_grad():
        text_features = model.encode_text(text)
        text_features /= text_features.norm(dim=-1, keepdim=True)
        text_vector = text_features.cpu().numpy().flatten().tolist()

    # get the top 3 results from the database based on the text vector
    results = collection.query(
        query_embeddings=[text_vector],
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
