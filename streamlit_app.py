import streamlit as st
from laba_ai1 import run as run_laba_ai_1
from laba_ai2 import run as run_laba_ai_2

def main():
    st.title("Выбор работы")

    option = st.selectbox("Выбери лабу", ("ИИ лаба 1", "ИИ лаба 2"))

    if option == "ИИ лаба 1":
        run_laba_ai_1()
    elif option == "ИИ лаба 2":
        run_laba_ai_2()

if __name__ == "__main__":
    main()
