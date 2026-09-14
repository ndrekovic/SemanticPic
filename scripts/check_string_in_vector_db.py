import chromadb

client = chromadb.PersistentClient(path="../chroma_db")
collection = client.get_collection("search_images")
print("count", collection.count())

sixth_entry = collection.get(limit=1, offset=5)
print(sixth_entry)

folder_name = '2023'

results = collection.get(
    where={
        "$and": [
            {"folder": folder_name},
            {"extension": {"$in": ["jpeg", "png", "jpg", "gif", "webp"]}}
        ]
    }
)

print("results", results, len(results['documents']))

a = 0
saved_paths = []
for metadata, document in zip(
        results["metadatas"],
        results["documents"]
):
    print(metadata)
    saved_paths.append(metadata['path'])
    a += 1
#    print(metadata["path"])

print(a)
import os

forced_paths = []
for (root, _, files) in os.walk(os.path.join('~/Pictures/Fotoarchiv/Handyfotos', folder_name)):
    for file in files:
        forced_paths.append(os.path.join(root, file))

print("Length of actual files:", len(forced_paths))
print("Length of saved files:", len(saved_paths))

diff_paths = list(set(forced_paths) - set(saved_paths))
print("All files that are missing:", diff_paths)
