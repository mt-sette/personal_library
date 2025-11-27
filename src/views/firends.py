import streamlit as st
from db import get_friends, get_friend_by_name, add_friend


def friends_catalog():
    st.header("Friends Catalog")

    # Create tabs for different operations
    tab1, tab2, tab3 = st.tabs(["View All Friends", "Search by Name", "Add Friend"])

    # Tab 1: View All Friends
    with tab1:
        st.subheader("All Friends")
        if st.button("Load All Friends", key="load_all_friends"):
            friends = get_friends()
            if friends:
                st.success(f"Found {len(friends)} friends!")
                for friend in friends:
                    col1, col2, col3 = st.columns([2, 2, 2])
                    with col1:
                        st.write(f"**{friend[1]}**")
                    with col2:
                        st.write(f"{friend[3]}")
                    with col3:
                        st.write(f"{friend[2]}")
            else:
                st.info("No friends in the catalog yet.")

    # Tab 2: Search by Name
    with tab2:
        st.subheader("Search Friends by Name")
        search_query = st.text_input(
            "Enter friend name (or part of it):", placeholder="e.g., 'Alice' or 'Smith'"
        )

        if st.button("Search", key="search_friends"):
            if search_query.strip():
                friends = get_friend_by_name(search_query)
                if friends:
                    st.success(f"Found {len(friends)} friend(s)!")
                    for friend in friends:
                        col1, col2, col3 = st.columns([2, 2, 2])
                        with col1:
                            st.write(f"**{friend[1]}**")
                        with col2:
                            st.write(f"{friend[3]}")
                        with col3:
                            st.write(f"{friend[2]}")
                else:
                    st.warning(f"No friends found matching '{search_query}'")
            else:
                st.warning("Please enter a search term")

    # Tab 3: Add New Friend
    with tab3:
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
