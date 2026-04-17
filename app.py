import streamlit as st
from data import show_data, footer

# Judul dashboard
def judul():
    st.title("📊 Dashboard COVID-19")
    st.write("Selamat datang di dashboard interaktif untuk menganalisis data COVID di Indonesia")

# Navigasi Sidebar
st.sidebar.title("Navigasi")
menu = st.sidebar.radio("Pilih Halaman", ["Home", "Halaman Data"])

if menu == "Home":
    judul()
elif menu == "Halaman Data":
    judul()
    show_data()

# Memanggil footer di luar if-else agar muncul di seluruh halaman
footer()

#ini komenan baru