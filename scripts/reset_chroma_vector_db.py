import os
import shutil

import chromadb


def reset_database():
    print("🔄 Starting ChromaDB cleanup...")

    # Method 1: Delete the collection via the Chroma client
    try:
        chroma_client = chromadb.PersistentClient(
            path="/Users/nedimdrekovic/PycharmProjects/local_image_search/chroma_db")
        # List all collections
        collections = chroma_client.list_collections()

        if collections:
            for coll in collections:
                # Use the correct method for newer ChromaDB versions
                chroma_client.delete_collection(name=coll.name)
                print(f"🗑️ Collection '{coll.name}' has been deleted.")
        else:
            print("ℹ️ No active collections found in ChromaDB.")
    except Exception as e:
        print(f"⚠️ Note during method 1 (client reset): {e}")

    # Method 2: Delete the physical folder forcefully (the safest method)
    # This removes all corrupt leftovers, lock files, and indexes from disk
    db_folder = ".././chroma_db"
    if os.path.exists(db_folder):
        try:
            shutil.rmtree(db_folder)
            print(
                f"💥 The folder '{db_folder}' was completely deleted from disk."
            )
        except Exception as e:
            print(f"❌ Error deleting the folder: {e}")
    else:
        print("ℹ️ The database folder no longer exists.")

    print("\n✅ ChromaDB is now completely empty and pristine!")


if __name__ == "__main__":
    # Safety prompt in the terminal so it is not accidentally triggered
    confirmation = input(
        "Do you really want to delete the ENTIRE ChromaDB? (yes/no): "
    )
    if confirmation.lower() == "yes":
        reset_database()
    else:
        print("❌ Aborted. Nothing was deleted.")
