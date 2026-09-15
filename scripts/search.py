import chromadb
import clip
import torch

device = 'cpu'
client = chromadb.PersistentClient(path="../chroma_db")

# Use the same CLIP model as during indexing
model, preprocess = clip.load(
    "ViT-B/32",
    device=device
)

collection = client.get_collection("search_images")
print("Count:", collection.count())
print(collection.peek(5))
query = input("Search: ")

# Convert text to a vector with CLIP
text = clip.tokenize([query]).to(device)

with torch.no_grad():
    text_features = model.encode_text(text)

# Normalize
text_features /= text_features.norm(
    dim=-1,
    keepdim=True
)

results = collection.query(
    query_embeddings=[
        text_features[0].cpu().tolist()
    ],
    n_results=10
)

print("Results:", results)

for image, distance in zip(
        results["documents"][0],
        results["distances"][0]
):
    print(f"{distance:.4f}  {image}")
