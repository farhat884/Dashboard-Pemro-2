import streamlit as st
from data import *

# Judul dashboard
def judul():
    st.title("📊 Dashboard COVID-19")
    st.write("Selamat datang di dashboard interaktif untuk menganalisis data COVID di Indonesia")

# Navigasi Sidebar
st.sidebar.title("Navigasi")
menu = st.sidebar.radio("Pilih Halaman", ["Home", "Halaman Data"])

if menu == "Home":
    judul( )
    # Pilih tahun
    year = select_year( )
    # Load & filter data
    df = load_data()
    df_filtered = filter_data(df, year)
    kolom(df_filtered)
    pie_chart1 (df_filtered)
elif menu == "Halaman Data":
    judul()
    year = select_year()
    # Load & filter data
    df = load_data()
    df_filtered = filter_data(df, year)
    show_data(df_filtered)

# Memanggil footer di luar if-else agar muncul di seluruh halaman
footer()

#ini komenan baru