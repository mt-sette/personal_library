import streamlit as st
import pandas as pd
from db import get_friends, add_friend


def friends_catalog():
    st.header("Friends Catalog")

    # Create tabs for different operations
    tab1, tab2 = st.tabs(["View All Friends", "Add Friend"])

    with tab1:
        st.subheader("All Friends")
        if st.button("Load All Friends", key="load_all_friends"):
            friends = get_friends()
            if friends:
                st.success(f"Found {len(friends)} friends!")
                df = pd.DataFrame(friends, columns=["ID", "Name", "Phone", "Email"])
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.info("No friends in the catalog yet.")


    with tab2:
        st.subheader("Add a New Friend")

        with st.form("add_friend_form"):
            name = st.text_input("Friend Name", placeholder="Enter the friend's name")
            email = st.text_input("Email", placeholder="Enter email address")
            phone = st.text_input("Phone", placeholder="Enter phone number")

            submitted = st.form_submit_button("Add Friend")

            if submitted:
                if name.strip() and email.strip() and phone.strip():
                    try:
                        rows_affected = add_friend(name, email, phone)
                        st.success(
                            f"Friend added successfully! ({rows_affected} row(s) added)"
                        )
                    except Exception as e:
                        st.error(f"Error adding friend: {str(e)}")
                else:
                    st.warning("Please fill in all fields (Name, Email, and Phone)")
