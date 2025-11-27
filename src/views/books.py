import streamlit as st
import pandas as pd
from db import get_books, find_books_by_title, add_book


def books_catalog():
    st.header("Books Catalog")

    # Create tabs for different operations
    tab1, tab2, tab3 = st.tabs(["View All Books", "Search by Title", "Add Book"])

    # Tab 1: View All Books
    with tab1:
        st.subheader("All Books")
        if st.button("Load All Books", key="load_all_books"):
            books = get_books()
            if books:
                st.success(f"Found {len(books)} books!")
                df = pd.DataFrame(books, columns=["ID", "Title", "Author"])
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.info("No books available in the catalog yet.")

    # Tab 2: Search by Title
    with tab2:
        st.subheader("Search Books by Title")
        search_query = st.text_input(
            "Enter book title (or part of it):", placeholder="e.g., 'Great' or 'Gatsby'"
        )

        if st.button("Search", key="search_books"):
            if search_query.strip():
                books = find_books_by_title(search_query)
                if books:
                    st.success(f"Found {len(books)} book(s)!")
                    df = pd.DataFrame(books, columns=["ID", "Title", "Author"])
                    st.dataframe(df, use_container_width=True, hide_index=True)
                else:
                    st.warning(f"No books found matching '{search_query}'")
            else:
                st.warning("Please enter a search term")

    # Tab 3: Add New Book
    with tab3:
        st.subheader("Add a New Book")

        with st.form("add_book_form"):
            title = st.text_input("Book Title", placeholder="Enter the book title")
            author = st.text_input("Author", placeholder="Enter the author name")

            submitted = st.form_submit_button("Add Book")

            if submitted:
                if title.strip() and author.strip():
                    try:
                        rows_affected = add_book(title, author)
                        st.success(
                            f"Book added successfully! ({rows_affected} row(s) added)"
                        )
                    except Exception as e:
                        st.error(f"Error adding book: {str(e)}")
                else:
                    st.warning("Please fill in both Title and Author fields")
