from pathlib import Path

import chromadb

# 1. Connect to the existing database
client = chromadb.PersistentClient(path="../chroma_db")
collection = client.get_collection("search_images")

print(f"Entries before update: {collection.count()}")

# 2. Retrieve all current entries
all_data = collection.get()

# Prepare lists for the update
updated_ids = []
updated_metadatas = []

# 3. Iterate through existing data and extend metadata
for img_id, metadata in zip(all_data["ids"], all_data["metadatas"]):
    # Read the old path from the metadata
    full_path = metadata.get("path")

    if full_path:
        p = Path(full_path)

        # Build the new structure (keep old data and add new fields)
        new_metadata = {
            "path": full_path,
            "folder": p.parent.name,  # e.g. "2022"
            "filename": p.name,  # e.g. "IMG_0035.jpeg"
            "extension": p.suffix[1:].lower()  # e.g. "jpeg" (without the dot)
        }

        updated_ids.append(img_id)
        updated_metadatas.append(new_metadata)

# 4. Write the new metadata back to the database
if updated_ids:
    collection.update(
        ids=updated_ids,
        metadatas=updated_metadatas
    )
    print(f"{len(updated_ids)} entries were successfully updated with new fields!")
else:
    print("No entries found to update.")
