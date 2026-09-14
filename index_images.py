import os
import ssl
import time
import uuid
from pathlib import Path

import chromadb
import clip
import torch
from PIL import Image

IMAGE_FOLDER = Path("~/Pictures/Fotoarchiv/Handyfotos").expanduser()  # path to the folder containing images
DATABASE_FILE = "./chroma_db"

device = "cpu"
model_name = "ViT-L/14"

# initialize the ChromaDB client
chroma_client = chromadb.PersistentClient(path=DATABASE_FILE)

# create collection for images if it doesn't exist, otherwise load it
collection = chroma_client.get_or_create_collection(name="search_images", metadata={"hnsw:space": "cosine"})


def get_image_paths(image_folder):
    # iterate over image folder and collect paths in list
    image_file_names = []
    for root, _, folder in os.walk(image_folder):
        for file in folder:
            if file.lower().endswith(('.jpeg', '.jpg', '.png', '.gif', '.webp')):
                image_file_names.append(os.path.join(root, file))
                print(os.path.join(root, file))
    return image_file_names


def print_progress(index, total_image_number, start_time):
    elapsed = time.time() - start_time
    avg = elapsed / (index + 1)
    remaining = avg * (total_image_number - index - 1)

    print(
        f"→ Progress: {index + 1}/{total_image_number} | "
        f"Average: {avg:.2f} s/image | "
        f"Approx. remaining: {remaining / 60:.1f} min"
    )


if __name__ == '__main__':
    # deactivate ssl verification for downloads in this script
    if not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context

    # iterate over image folder and collect paths in list
    image_file_names = get_image_paths(IMAGE_FOLDER)
    print(f"Images found: {len(image_file_names)}")

    # save in vector database
    print("Load Clip...")
    model, preprocess = clip.load(model_name, device=device)
    print("Clip loaded.")

    existing = collection.get(
        include=["metadatas"]
    )
    existing_paths = (
        metadata["path"]
        for metadata in existing["metadatas"]
        if metadata and "path" in metadata
    )

    success_count = 0
    start_time = time.time()

    for index, image_path in enumerate(image_file_names):
        if image_path in existing_paths:
            print(image_path, "already exists")
            continue
        # shows only the file name in the status for clarity
        file_name = os.path.basename(image_path)

        try:
            image = Image.open(image_path).convert("RGB")

            inputs = preprocess(image).unsqueeze(0).to(device)

            with torch.no_grad():
                image_features = model.encode_image(inputs)
            image_features /= image_features.norm(dim=-1, keepdim=True)

            # turn image in vector list for database storage
            # .cpu() is important to move the tensor back to CPU memory, especially if you're using a GPU or MPS device.
            # This ensures that the data can be serialized and stored in the database without issues.
            vector = image_features.cpu().flatten().tolist()

            unique_id = str(uuid.uuid4())
            p = Path(image_path)
            # save in vector database
            collection.add(
                embeddings=[vector],  # the vector representation of the image
                documents=[image_path],
                # path to the image in the database, can be used to retrieve the image later
                ids=[f"{unique_id}"],  # unique ID for the database
                metadatas=[
                    {"path": image_path,
                     "extension": p.suffix[1:],
                     "folder": p.parent.name,
                     "filename": p.name}]  # metadata for the image
            )
            success_count += 1
            if success_count % 100 == 0:
                print_progress(index, len(image_file_names), start_time)

        except Exception as e:
            print(f"Error for {image_path}: {e}")
            print(f"⚠️ Skipped (error for {image_path}): {e}")

    # summary: how many were successfully added and total in DB
    print(f"🎉 Successfully added: {success_count}")
    try:
        total = collection.count()
        print(f"🔢 Total count in DB: {total}")
    except Exception:
        # some Chroma versions may not support count(); fall back to a safe message
        print("🔢 Total count in DB: (not available in this Chroma version)")
