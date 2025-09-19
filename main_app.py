import streamlit as st
import pickle
import numpy as np

# Set page configuration
st.set_page_config(
    page_title="Book Recommendation System",
    page_icon="📚",
    layout="wide"
)

# Load the data
@st.cache_data
def load_data():
    try:
        popular_df = pickle.load(open("popular.pkl", "rb"))
        pt = pickle.load(open("pt.pkl", "rb"))
        books = pickle.load(open("books.pkl", "rb"))
        similarity_scores = pickle.load(open("similarity_scores.pkl", "rb"))
        return popular_df, pt, books, similarity_scores
    except FileNotFoundError as e:
        st.error(f"Error loading data files: {e}")
        st.stop()

# Load data
popular_df, pt, books, similarity_scores = load_data()
st.sidebar.header("Made By Subhadip 🔥")
# Main app
def main():
    st.title("📚 Book Recommendation System")
    
    # Sidebar navigation
    page = st.sidebar.radio("Navigation", ["Home", "Recommend Books"])
    
    if page == "Home":
        show_home_page()
    else:
        show_recommend_page()

def show_home_page():
    st.header("Popular Books")
    
    # Display popular books in a grid
    cols = st.columns(4)
    
    for i in range(len(popular_df)):
        with cols[i % 4]:
            st.image(
                popular_df["Image-URL-M"].values[i],
                width=150,
                use_container_width=True
            )
            st.subheader(popular_df["Book-Title"].values[i])
            st.write(f"**Author:** {popular_df['Book-Author'].values[i]}")
            st.write(f"**Rating:** {popular_df['avg_rating'].values[i]:.2f} ⭐")
            st.write(f"**Votes:** {popular_df['num_ratings'].values[i]}")
            st.markdown("---")

def show_recommend_page():
    st.header("Book Recommendations")
    
    # Book selection dropdown
    book_titles = list(pt.index)
    selected_book = st.selectbox(
        "Select a book to get recommendations:",
        book_titles,
        index=0
    )
    
    if st.button("Get Recommendations"):
        if selected_book:
            try:
                # Get recommendations
                index = np.where(pt.index == selected_book)[0][0]
                similar_items = sorted(
                    list(enumerate(similarity_scores[index])),
                    key=lambda x: x[1],
                    reverse=True
                )[1:5]
                
                # Display recommendations
                st.subheader(f"Books similar to '{selected_book}':")
                
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
                                    use_container_width=True
                                )
                                st.subheader(book_data["Book-Title"].values[0])
                                st.write(f"**Author:** {book_data['Book-Author'].values[0]}")
                                st.write(f"**Similarity Score:** {score:.3f}")
                            except (IndexError, KeyError):
                                st.warning("Could not load book information")
                
            except IndexError:
                st.error("Book not found in the database. Please select another book.")
            except Exception as e:
                st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
