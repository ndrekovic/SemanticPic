from pathlib import Path

# models
TEXT_MODEL = "sentence-transformers/clip-ViT-B-32-multilingual-v1"
IMAGE_MODEL = "clip-ViT-B-32"

# paths
IMAGE_FOLDER = Path("~/Pictures/Fotoarchiv/Handyfotos").expanduser()  # path to the folder containing images
DATABASE_PATH = "./chroma_db"

# chromadb
COLLECTION_NAME = "search_images"

# search
DEFAULT_N_RESULTS = 10
