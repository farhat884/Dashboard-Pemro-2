import streamlit as st
import pandas as pd

# Fungsi untuk memuat data
def load_data():
    # Menggunakan r"" untuk menghindari error path pada Windows
    df = pd.read_csv(r"dataset\covid_19_indonesia_time_series_all.csv")
    return df

def show_data():
    df = load_data()
    
    st.subheader("📊 Ringkasan Data COVID-19 Indonesia")
    
    # 1. Menampilkan Total Kasus Keseluruhan di halaman data
    total_cases = df['Total Cases'].sum()
    st.metric(label="Total Kasus Keseluruhan", value=f"{int(total_cases):,}")
    
    # 2. Menampilkan kolom Location, dan rentang New Cases sampai Total Recovered
    # Kita menggunakan .loc untuk mengambil kolom secara spesifik
    kolom_pilihan = ['Location'] + list(df.loc[:, 'New Cases':'Total Recovered'].columns)
    df_filtered = df[kolom_pilihan]
    
    st.write("Preview Data (Kolom Terfilter):")
    st.dataframe(df_filtered.head(10))
    
    st.subheader("Statistik Deskriptif Dataset")
    st.write(df_filtered.describe())

def footer():
    # Menambahkan Copyright nama dan NPM
    st.markdown("---")
    st.caption('© 2024 | Farhat Chandra Permana - 184240007')