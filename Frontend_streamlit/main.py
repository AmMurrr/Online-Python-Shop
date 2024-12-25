import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

def main():
    st.title("MagaZ")
    response = requests.get(f"{API_URL}/products/")
    products = response.json()
    st.write(products)


if __name__ == "__main__":
    main()