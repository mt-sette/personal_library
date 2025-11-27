import streamlit as st
import pandas as pd
from db import (
    get_books,
    get_friends,
    get_loans,
    books_on_loan,
    add_loan,
    update_book_return_date,
)
from datetime import datetime


def loans_management():
    st.header("Loan Management System")

    # Create tabs for different operations
    tab1, tab2, tab3, tab4 = st.tabs(
        ["Active Loans", "All Loans", "Create Loan", "Return Book"]
    )

    # Tab 1: View Active Loans
    with tab1:
        st.subheader("Books Currently on Loan")
        if st.button("Load Active Loans", key="load_active_loans"):
            loans = books_on_loan()
            if loans:
                st.success(f"Found {len(loans)} active loan(s)!")
                df = pd.DataFrame(
                    loans,
                    columns=[
                        "Book ID",
                        "Title",
                        "Author",
                        "Friend Name",
                        "Loan Date",
                        "Return Date",
                    ],
                )
                st.dataframe(
                    df[["Title", "Author", "Friend Name", "Loan Date"]],
                    use_container_width=True,
                    hide_index=True,
                )
            else:
                st.info("No books currently on loan.")

    # Tab 2: View All Loans
    with tab2:
        st.subheader("All Loans (Active and Returned)")
        if st.button("Load All Loans", key="load_all_loans"):
            loans = get_loans()
            if loans:
                st.success(f"Found {len(loans)} loan(s)!")
                df = pd.DataFrame(
                    loans,
                    columns=[
                        "ID",
                        "Book ID",
                        "Friend ID",
                        "Loan Date",
                        "Due Date",
                        "Return Date",
                    ],
                )
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.info("No loans in the system.")

    # Tab 3: Create New Loan
    with tab3:
        st.subheader("Create a New Loan")

        with st.form("add_loan_form"):
            col1, col2 = st.columns(2)

            with col1:
                books = get_books()
                book_options = {f"{b[1]} by {b[2]}": b[0] for b in books}
                selected_book = st.selectbox(
                    "Select Book", options=list(book_options.keys())
                )
                book_id = book_options[selected_book]

            with col2:
                friends = get_friends()
                friend_options = {f"{f[1]} ({f[3]})": f[0] for f in friends}
                selected_friend = st.selectbox(
                    "Select Friend", options=list(friend_options.keys())
                )
                friend_id = friend_options[selected_friend]

            submitted = st.form_submit_button("Create Loan")

            if submitted:
                try:
                    result = add_loan(book_id, friend_id)
                    if result:
                        st.success(
                            f"Loan created successfully! Book loaned to {selected_friend}"
                        )
                    else:
                        st.error("This book is already on loan to someone else.")
                except Exception as e:
                    st.error(f"Error creating loan: {str(e)}")

    # Tab 4: Return Book
    with tab4:
        st.subheader("Return a Book")

        active_loans = books_on_loan()
        if active_loans:
            with st.form("return_book_form"):
                loan_options = {
                    f"{loan[1]} loaned to {loan[3]} since {loan[4]}": loan[0]
                    for loan in active_loans
                }
                selected_loan = st.selectbox(
                    "Select Loan to Return", options=list(loan_options.keys())
                )
                loan_id = loan_options[selected_loan]

                return_date = st.date_input("Return Date", value=datetime.now().date())

                submitted = st.form_submit_button("Return Book")

                if submitted:
                    try:
                        rows_affected = update_book_return_date(
                            loan_id, return_date.isoformat()
                        )
                        st.success(
                            f"Book returned successfully! ({rows_affected} loan(s) updated)"
                        )
                    except Exception as e:
                        st.error(f"Error returning book: {str(e)}")
        else:
            st.info("No active loans to return.")
