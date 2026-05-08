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
    judul()
    df = load_data()
    year = select_year()
    locations = select_location(df)  # Sekarang mengembalikan LIST
    df_filtered = filter_data(df, year, locations)
    
    # Tampilkan informasi filter yang aktif
    st.sidebar.info(f"📌 Filter aktif: Tahun = {'Semua' if not year else year} | Provinsi = {', '.join(locations)}")
    
    # Metric cards
    kolom(df_filtered)
    
    # Visualisasi
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Pie Chart", "📈 Bar Chart Kematian", "📈 Bar Chart Kesembuhan", "🗺️ Peta Sebaran"])
    
    with tab1:
        st.subheader("Perbandingan Kematian vs Kesembuhan")
        pie_chart1(df_filtered)
    
    with tab2:
        st.subheader("Top 5 Provinsi dengan Kematian Tertinggi")
        bar_chart1(df_filtered)
    
    with tab3:
        st.subheader("Top 5 Provinsi dengan Kesembuhan Tertinggi")
        bar_chart2(df_filtered)
    
    with tab4:
        st.subheader("Peta Sebaran Kasus COVID-19")
        map_chart(df_filtered, year if year else None)

elif menu == "Halaman Data":
    judul()
    year = select_year()
    locations = select_location(df)  # Untuk halaman data juga bisa multi select
    df = load_data()
    df_filtered = filter_data(df, year, locations)
    show_data(df_filtered)

footer()