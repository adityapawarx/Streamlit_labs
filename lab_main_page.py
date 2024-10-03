import streamlit as st

page = st.sidebar.selectbox("Choose a lab", ["Lab 1", "Lab 2", "Lab 3B","Lab 3C", "Lab 4"])

if page == "Lab 1":
    st.write("This is Lab 1")
    exec(open("Lab_1.py").read())

elif page == "Lab 2":
    st.write("This is Lab 2")
    exec(open("Lab_2.py").read())

elif page == "Lab 3B":
    st.write("This is Lab 3B")
    exec(open("Lab_3B.py").read())

elif page == "Lab 3C":
    st.write("This is Lab 3C")
    exec(open("Lab_3C.py").read())

elif page == "Lab 4":
    st.write("This is Lab 4")
    exec(open("Lab_4.py").read())