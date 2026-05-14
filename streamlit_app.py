import streamlit as st
from laba_ai1 import run as run_laba_ai_1

def main():
    st.title("Выборо работы")

    option = st.selectbox("Выбери лабу", ("ИИ лаба 1"))

    if option == "ИИ лаба 1":
        run_laba_ai_1()

if __name__ == "__main__":
    main()
