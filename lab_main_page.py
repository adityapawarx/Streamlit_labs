import streamlit as st

page = st.sidebar.selectbox("Choose a lab", ["Enter the Key", "Ask Doc Questions", "lab3","lab4", "lab5"])

if page == "L1 Enter the Key":
    st.write("L1 Enter the Key")
    exec(open("lab1.py").read())

elif page == "L2 Ask Doc Questions":
    st.write("L2 Ask Doc Questions")
    exec(open("lab2.py").read())

elif page == "Lab 3B":
    st.write("This is Lab 3B")
    exec(open("lab3.py.py").read())

elif page == "Lab 3C":
    st.write("This is Lab 3C")
    exec(open("lab4.py.py").read())

elif page == "Lab 4":
    st.write("This is Lab 4")
    exec(open("lab5.py").read())