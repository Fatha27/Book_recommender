import pickle
import streamlit as st
custom_css = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: url('https://c1.wallpaperflare.com/preview/556/301/197/book-stack-books.jpg');
    background-size: cover;
    background-position:center;
    background-attachment: fixed;
}
</style>
"""

# Set the custom CSS
st.markdown(custom_css, unsafe_allow_html=True)

st.header("Book Recommendation App")
books=pickle.load(open('d:/bookrecmodel/df','rb'))
similarity=pickle.load(open('d:/bookrecmodel/sim','rb'))
book_list=books['bookTitle'].values
authordf=pickle.load(open('d:/bookrecmodel/dataframeog1','rb'))
selected_book=st.selectbox(
    'Type a book to get recommendations',
    book_list
)
def recommend(book):
    index = books[books['bookTitle'] == book].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    
    recommended_books = []
    author_names = []
    recommended_titles_set = set()  # To track unique recommended book titles
    recommendation_counter = 0  # To limit the recommendations to 5
    
    for i in distances[1:15]:
        title = books.iloc[i[0]].bookTitle
        if title not in recommended_titles_set and title!=book:
            recommended_books.append(title)
            author_names.append(authordf.iloc[i[0]].FirstAuthor)
            recommended_titles_set.add(title)
            recommendation_counter += 1
        
        if recommendation_counter == 5:
            break
    
    return recommended_books, author_names

if st.button('Show Recommendations', key='recommend_button'):
    recommended_books,author_names = recommend(selected_book)
    
    # Display the recommended books and their authors
    st.write("**Top 5 Recommended Books:**")
    for idx, (book, author) in enumerate(zip(recommended_books, author_names), start=1):
        st.write(f"{idx}. **{book}** -**{author}**")
   