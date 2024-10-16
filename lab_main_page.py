import streamlit as st

import lab1 as lab1
import lab2 as lab2
import lab3 as lab3
import lab4 as lab4
import lab5 as lab5

def main():
    st.sidebar.title("Labs")
    page = st.sidebar.selectbox("Choose a lab", ["lab1", "lab2", "lab3", "lab4", "lab5"])

    if page == "lab1":
        lab1.run()  

    elif page == "lab2":
        lab2.run()  

    elif page == "lab3":
        lab3.run()  

    elif page == "lab4":
        lab4.run()  

    elif page == "lab5":
        lab5.run()  

if __name__ == "__main__":
    main()

#dg