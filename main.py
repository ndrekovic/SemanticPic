# app.py
import os

import streamlit as st

from config import DEFAULT_N_RESULTS
# import functions from search image file
from search_images import initialize_search, search_images

# page configuration
st.set_page_config(layout="wide")
st.html("""
    <style>
        /* Enlarges the text in the search field */
        .stTextInput input {
            font-size: 22px !important;
            height: 52px !important; /* Adjusts the field height to the font */
        }
        /* Enlarges the placeholder text */
        .stTextInput input::placeholder {
            font-size: 18px !important;
        }
    </style>
""")

st.title("📸 Local AI Image Search")
st.write("Search for images in your archive using natural language.")


# load model and collection from ChromaDB (cached to avoid reloading on every search)
@st.cache_resource
def load_backend():
    return initialize_search()


model, collection, device = load_backend()

# --- GUI layout ---
# 2 columns, for text field and button
col1, col2, col3 = st.columns([4, 2, 1], vertical_alignment="center")

with col1:
    search_query = st.text_input(
        "Enter search term",
        placeholder="e.g. A dog running on the beach...",
        label_visibility="collapsed",
    )

with col2:
    # Slider to choose how many results to display (between 1 and 20)
    num_results = st.slider(
        "Number of results",
        min_value=1,
        max_value=20,
        value=DEFAULT_N_RESULTS,
        step=1,
        label_visibility="collapsed"
    )

with col3:
    # Add some vertical spacing above so the button aligns with the rest (smaller spacer)
    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
    # let the button keep its natural (styled) width instead of stretching the column
    search_button = st.button("🔎 Search", use_container_width=True, type='primary')

# if user clicks on button or enters the search field
if search_query:
    with st.spinner("Loading images..."):
        # Call the strictly separated search method
        results = search_images(search_query, model, collection, device, n_results=num_results)

    if not results:
        st.warning("No images found in the database.")
    else:
        st.write("### Similar Results:")

        # Use the actual number of found documents to prevent IndexErrors
        actual_results_count = len(results["documents"][0]) if results.get("documents") else 0
        # shows results
        img_cols = st.columns(actual_results_count)

        for idx in range(actual_results_count):
            img_path = results["documents"][0][idx]
            distance = results["distances"][0][idx]
            # check if file exists locally
            with img_cols[idx]:
                if os.path.exists(img_path):
                    st.image(
                        img_path, use_container_width=True, caption=os.path.basename(img_path)
                    )

                    # calculate similarity score (cosine distance = 1 - similarity)
                    score = (1 - distance) * 100
                    st.metric(label="Similarity Score", value=f"{score:.1f} %")
                    st.caption(f"File path: `{img_path}`")
                else:
                    st.error(f"Image not found: {os.path.basename(img_path)}")
