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

# File URLs
FILE_URLS = {
    'popular.pkl': 'YOUR_POPULAR_PKL_DRIVE_LINK',
    'pt.pkl': 'YOUR_PT_PKL_DRIVE_LINK',
    'books.pkl': 'https://drive.google.com/uc?id=1-Yors5PsnMHJzsmnogt3ZBwQVPbbOsmQ',
    'similarity_scores.pkl': 'YOUR_SIMILARITY_SCORES_PKL_DRIVE_LINK'
}

# Download function
@st.cache_data
def download_file(file_name, url):
    """Download file from Google Drive"""
    try:
        output_path = f"./{file_name}"
        
        # Check if file already exists
        if os.path.exists(output_path):
            return output_path
            
        st.info(f"📥 Downloading {file_name}...")
        
        # Google Drive direct download
        if 'drive.google.com' in url or 'uc?id=' in url:
            gdown.download(url, output_path, quiet=False)
        else:
            # For other URLs
            response = requests.get(url)
            with open(output_path, 'wb') as f:
                f.write(response.content)
                
        st.success(f"✅ {file_name} downloaded successfully!")
        return output_path
        
    except Exception as e:
        st.error(f"❌ Error downloading {file_name}: {e}")
        return None

# Load data with download fallback
@st.cache_data
def load_data():
    """Load data files, download if missing"""
    data_files = {}
    
    for file_name, url in FILE_URLS.items():
        file_path = download_file(file_name, url)
        if file_path and os.path.exists(file_path):
            try:
                with open(file_path, 'rb') as f:
                    data_files[file_name.split('.')[0]] = pickle.load(f)
                st.success(f"✅ {file_name} loaded successfully!")
            except Exception as e:
                st.error(f"❌ Error loading {file_name}: {e}")
        else:
            st.warning(f"⚠️ {file_name} not available")
    
    return data_files

# Check if files exist locally first
def check_local_files():
    """Check which files exist locally"""
    local_files = {}
    for file_name in FILE_URLS.keys():
        if os.path.exists(f"./{file_name}"):
            local_files[file_name] = True
        else:
            local_files[file_name] = False
    return local_files

# Main app
def main():
    st.title("📚 Book Recommendation System")
    
    # Display file status
    st.sidebar.header("📁 File Status")
    local_files = check_local_files()
    for file_name, exists in local_files.items():
        status = "✅" if exists else "❌"
        st.sidebar.write(f"{status} {file_name}")
    
    # Load data
    with st.spinner("🔄 Loading data..."):
        data = load_data()
    
    # Check if all data loaded successfully
    if not all(key in data for key in ['popular', 'pt', 'books', 'similarity_scores']):
        st.error("❌ Could not load all required data files. Please check the file links.")
        st.info("""
        📋 Required files:
        - popular.pkl
        - pt.pkl  
        - books.pkl
        - similarity_scores.pkl
        
        🔗 Update the FILE_URLS dictionary with your Google Drive links
        """)
        return
    
    popular_df = data['popular']
    pt = data['pt']
    books = data['books']
    similarity_scores = data['similarity_scores']
    
    # Sidebar navigation
    st.sidebar.header("🧭 Navigation")
    page = st.sidebar.radio("Go to", ["🏠 Home", "🔍 Recommend Books", "ℹ️ About"])
    
    if page == "🏠 Home":
        show_home_page(popular_df)
    elif page == "🔍 Recommend Books":
        show_recommend_page(pt, books, similarity_scores)
    else:
        show_about_page()

def show_home_page(popular_df):
    st.header("🌟 Popular Books")
    st.write("Discover the most popular books based on user ratings and reviews!")
    
    # Display popular books in a grid
    cols = st.columns(4)
    
    for i in range(min(20, len(popular_df))):  # Show first 20 books
        with cols[i % 4]:
            try:
                st.image(
                    popular_df["Image-URL-M"].values[i],
                    width=150,
                    use_container_width=True,
                    caption=popular_df["Book-Title"].values[i]
                )
                st.write(f"**Author:** {popular_df['Book-Author'].values[i]}")
                st.write(f"**Rating:** {popular_df['avg_rating'].values[i]:.2f} ⭐")
                st.write(f"**Votes:** {popular_df['num_ratings'].values[i]:,}")
                st.markdown("---")
            except Exception as e:
                st.warning(f"Could not display book {i}")

def show_recommend_page(pt, books, similarity_scores):
    st.header("🔍 Book Recommendations")
    st.write("Select a book you like and discover similar books!")
    
    # Book selection dropdown with search
    book_titles = list(pt.index)
    selected_book = st.selectbox(
        "📖 Select a book to get recommendations:",
        book_titles,
        index=0,
        help="Type to search through the book titles"
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
                    )[1:5]  # Top 4 similar books
                    
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
                                    st.write(f"**Author:** {book_data['Book-Author'].values[0]}")
                                    st.write(f"**Similarity:** {score:.3f}")
                                    st.progress(float(score))
                                except (IndexError, KeyError) as e:
                                    st.warning("Could not load book information")
                    
                except IndexError:
                    st.error("❌ Book not found in the database. Please select another book.")
                except Exception as e:
                    st.error(f"❌ An error occurred: {e}")

def show_about_page():
    st.header("ℹ️ About This App")
    st.write("""
    ## 📚 Book Recommendation System
    
    This application provides intelligent book recommendations using collaborative filtering.
    
    ### 🎯 Features:
    - Discover popular books with ratings
    - Get personalized book recommendations
    - Beautiful interface with book covers
    - Real-time results
    
    ### 🛠️ Built With:
    - Python 🐍
    - Streamlit 🎈
    - Scikit-learn 🤖
    - Pandas 📊
    
    ### 👨‍💻 Developer:
    **Subhadip Sinha**  
    GitHub: [@subhadipsinha722133](https://github.com/subhadipsinha722133)
    
    ---
    
    *Note: This app requires book data files to function properly.*
    """)

if __name__ == "__main__":
    main()
