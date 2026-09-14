import chromadb

client = chromadb.PersistentClient(path="../chroma_db")
collection = client.get_collection("search_images")
file_name = "IMG_2802.jpeg"

search_path = "/Users/nedimdrekovic/Pictures/Fotoarchiv/Handyfotos/2022/" + file_name

# Query for the exact path
exists = collection.get(
    where={"path": search_path}
)

# Check whether the ID list is not empty
if exists["ids"]:
    print(f"Yes, the file is in the database! ID: {exists['ids'][0]}")
else:
    print("No, this file does not exist in the database yet.")
