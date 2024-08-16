import streamlit as st
import mc

st.title("Screen Feast")
genre = st.sidebar.selectbox("Genre", ("Adventure", "Romance", "Sci-Fi", "Horror"))

if genre:
    response = mc.generate_movie_details(genre)
    st.header(response['movie_title'].strip("."))

    st.write("**Plot**")
    st.write(response['plot'])

    cast_list = response['cast'].split(",")
    st.write("**Cast**")
    for actor in cast_list:
        st.write("-", actor)
