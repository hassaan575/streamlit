import streamlit as st
from PIL import Image


def app():
    st.title('Progress')

    st.write('This is the `progress page` of our stock prediction app.')

    st.write('In this page we will be documenting our progress in developing a stock predicting app.')

    image = Image.open('1.jpg')
    st.image(image)

    image = Image.open('2.jpg')
    st.image(image)

    image = Image.open('3.jpg')
    st.image(image)

    image = Image.open('4.jpg')
    st.image(image)

    image = Image.open('5.jpg')
    st.image(image)

    image = Image.open('6.jpg')
    st.image(image)

    image = Image.open('7.jpg')
    st.image(image)


