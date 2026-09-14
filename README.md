# ChromaLens – Semantic Image Search with ChromaDB

A local, AI-powered image search engine built with Python. This project utilizes a **CLIP (Vision Transformer) model**
to analyze images from local directories, convert them into mathematical vectors (embeddings), and store them in a
**ChromaDB vector database**. Once indexed, you can search through your images instantly using natural language text
descriptions (semantic search).

## 🚀 Features

- **Interactive UI (Streamlit):** A clean, web-based frontend to input search queries and view matching images instantly
  in a beautiful gallery grid.
- **Automated Indexing:** Traverses local directories (`os.walk`), converts images into embeddings, and saves them to
  the database.
- **Semantic Search:** Finds images based on descriptions (e.g., "A dog playing on the beach") instead of relying on
  filenames.
- **Local Database:** Powered by a persistent ChromaDB instance directly on your machine—ensuring 100% privacy and zero
  cloud costs.
- **Maintenance Tools:** Dedicated utility scripts to reset, update, and verify the vector database.

## 🛠️ Project Structure

```text
├── chroma_db/                  # Local vector database (In .gitignore)
├── scripts/                    # Maintenance & utility tools
│   ├── check_string_in_vector_db.py
│   ├── reset_chroma_vector_db.py
│   ├── search.py                   # Core search logic
│   ├── search_specific_image_path.py # Searches for a specific image path in the DB    
│   └── update_chroma_vector_db.py
├── index_images.py             # Indexes image directories into the DB
├── search_images.py            # CLI interface for searching images
├── main.py                     # Central entry point
├── .gitignore                  # Prevents DB and .venv from being uploaded
└── requirements.txt            # Python dependencies
```

## 📦 Installation & Setup

1. **Clone the Repository:**
   ```bash
   git clone git@github.com:ndrekovic/SemanticPic.git
   cd SemanticPic
   ```

2. **Set Up a Virtual Environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On macOS/Linux
   # Or on Windows: .venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## 🖥️ Usage

### 1. Indexing Images

Before searching, you need to process your local images. Configure the path to your photo archive in `index_images.py`
and run (only once):

```bash
python index_images.py
```

### 2. Searching Images

Query your database right from the terminal by entering a description of the image you are looking for:

```bash
python search_images.py
```

### 3. Resetting the Database

If you want to wipe the database clean and start over, use the maintenance script:

```bash
python scripts/reset_chroma_vector_db.py
```

## ⚙️ Technical Details

- **Database:** ChromaDB (Persistent SQLite backend)
- **Supported OS:** macOS, Linux, Windows

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for details.
