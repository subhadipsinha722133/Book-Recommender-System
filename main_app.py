import streamlit as st
import pickle
import numpy as np
import gdown
import os
import requests
from pathlib import Path

# Set page configuration
st.set_page_config(
    page_title="Book Recommendation System",
    page_icon="📚",
    layout="wide"
)

# File URLs for Google Drive
FILE_URLS = {
    'popular.pkl': 'YOUR_POPULAR_PKL_DRIVE_LINK',
    'pt.pkl': 'YOUR_PT_PKL_DRIVE_LINK',
    'books.pkl': 'https://drive.google.com/uc?id=1-Yors5PsnMHJzsmnogt3ZBwQVPbbOsmQ',
    'similarity_scores.pkl': 'YOUR_SIMILARITY_SCORES_PKL_DRIVE_LINK'
}

# Download function for Google Drive files
@st.cache_data
def download_file(file_name, url):
    """Download file from Google Drive if it doesn't exist locally"""
    try:
        output_path = f"./{file_name}"
        
        # Check if file already exists locally
        if os.path.exists(output_path):
            return output_path
            
        st.info(f"📥 Downloading {file_name} from Google Drive...")
        
        # Download from Google Drive
        if 'drive.google.com' in url or 'uc?id=' in url:
            gdown.download(url, output_path, quiet=False)
        else:
            # For direct URLs (fallback)
            response = requests.get(url)
            with open(output_path, 'wb') as f:
                f.write(response.content)
                
        st.success(f"✅ {file_name} downloaded successfully!")
        return output_path
        
    except Exception as e:
        st.error(f"❌ Error downloading {file_name}: {e}")
        return None

# Load data with automatic download from Google Drive
@st.cache_data
def load_data():
    """Load data files, download from Google Drive if missing locally"""
    try:
        # Check and download missing files
        for file_name, url in FILE_URLS.items():
            if not os.path.exists(f"./{file_name}"):
                download_file(file_name, url)
        
        # Load all files
        popular_df = pickle.load(open("popular.pkl", "rb"))
        pt = pickle.load(open("pt.pkl", "rb"))
        books = pickle.load(open("books.pkl", "rb"))
        similarity_scores = pickle.load(open("similarity_scores.pkl", "rb"))
        
        return popular_df, pt, books, similarity_scores
        
    except FileNotFoundError as e:
        st.error(f"❌ Error loading data files: {e}")
        st.info("""
        📋 Please make sure all data files are available:
        - popular.pkl
        - pt.pkl  
        - books.pkl
        - similarity_scores.pkl
        
        🔗 Update the FILE_URLS dictionary with correct Google Drive links
        """)
        st.stop()
    except Exception as e:
        st.error(f"❌ Unexpected error: {e}")
        st.stop()

# Load data
popular_df, pt, books, similarity_scores = load_data()

# Sidebar header with your name
st.sidebar.header("Made By Subhadip 🔥")

# Display file status in sidebar
st.sidebar.subheader("📁 File Status")
file_status = {}
for file_name in FILE_URLS.keys():
    file_status[file_name] = "✅ Available" if os.path.exists(f"./{file_name}") else "❌ Missing"

for file_name, status in file_status.items():
    st.sidebar.write(f"{status} - {file_name}")

# Main app
def main():
    st.title("📚 Book Recommendation System")
    
    # Sidebar navigation
    page = st.sidebar.radio("🧭 Navigation", ["🏠 Home", "🔍 Recommend Books"])
    
    if page == "🏠 Home":
        show_home_page()
    else:
        show_recommend_page()

def show_home_page():
    st.header("🌟 Popular Books")
    
    # Display popular books in a grid
    cols = st.columns(4)
    
    for i in range(len(popular_df)):
        with cols[i % 4]:
            try:
                st.image(
                    popular_df["Image-URL-M"].values[i],
                    width=150,
                    use_container_width=True,
                    caption=popular_df["Book-Title"].values[i]
                )
                st.subheader(popular_df["Book-Title"].values[i])
                st.write(f"**Author:** {popular_df['Book-Author'].values[i]}")
                st.write(f"**Rating:** {popular_df['avg_rating'].values[i]:.2f} ⭐")
                st.write(f"**Votes:** {popular_df['num_ratings'].values[i]:,}")
                st.markdown("---")
            except Exception as e:
                st.warning(f"Could not display book {i+1}")

def show_recommend_page():
    st.header("🔍 Book Recommendations")
    
    # Book selection dropdown with search
    book_titles = list(pt.index)
    selected_book = st.selectbox(
        "📖 Select a book to get recommendations:",
        book_titles,
        index=0,
        help="Type to search through thousands of books"
    )
    
    if st.button("🎯 Get Recommendations", type="primary"):
        if selected_book:
            with st.spinner("🔍 Finding similar books..."):
                try:
                    # Get recommendations
                    index = np.where(pt.index == selected_book)[0][0]
                    similar_items = sorted(
                        list(enumerate(similarity_scores[index])),
                        key=lambda x: x[1],
                        reverse=True
                    )[1:5]
                    
                    # Display recommendations
                    st.subheader(f"📚 Books similar to '{selected_book}':")
                    
                    cols = st.columns(4)
                    
                    for i, (idx, score) in enumerate(similar_items):
                        temp_df = books[books["Book-Title"] == pt.index[idx]]
                        book_data = temp_df.drop_duplicates("Book-Title")
                        
                        if not book_data.empty:
                            with cols[i]:
                                try:
                                    st.image(
                                        book_data["Image-URL-M"].values[0],
                                        width=150,
                                        use_container_width=True,
                                        caption=book_data["Book-Title"].values[0]
                                    )
                                    st.subheader(book_data["Book-Title"].values[0])
                                    st.write(f"**Author:** {book_data['Book-Author'].values[0]}")
                                    st.write(f"**Similarity Score:** {score:.3f}")
                                    # Visual similarity indicator
                                    st.progress(float(score))
                                except (IndexError, KeyError):
                                    st.warning("Could not load complete book information")
                    
                except IndexError:
                    st.error("❌ Book not found in the database. Please select another book.")
                except Exception as e:
                    st.error(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    main()
