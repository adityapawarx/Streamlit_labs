import streamlit as st

page = st.sidebar.selectbox("Choose a lab", ["L1 Enter the Key", "L2 Ask Doc Questions", "lab3", "lab4", "lab5"])

if page == "L1 Enter the Key":
    st.write("L1 Enter the Key")
    exec(open("lab1.py").read())

elif page == "L2 Ask Doc Questions":
    st.write("L2 Ask Doc Questions")
    exec(open("lab2.py").read())

elif page == "lab3":
    st.write("This is lab3")
    exec(open("lab3.py").read())

elif page == "lab4":
    st.write("This is lab4")
    exec(open("lab4.py").read())

elif page == "lab5":
    st.write("This is lab5")
    exec(open("lab5.py").read())