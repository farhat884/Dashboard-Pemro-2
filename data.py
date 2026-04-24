import streamlit as st
import pandas as pd
import plotly.express as px

# Fungsi untuk memuat data
def load_data():
    df = pd.read_csv("dataset\covid_19_indonesia_time_series_all.csv")
    return df

# Filter data berdasarkan tahun (optional)
def filter_data(df, year=None):
    if year:
        df = df[df['Date'].astype(str).str.contains(str(year))]
    return df

def select_year():
    return st.sidebar.selectbox(
        "Pilih Tahun",
        options=[None, 2020, 2021, 2022],
        format_func=lambda x: "Semua Tahun" if x is None else str(x)
    )

def show_data(df):
    df = load_data()
    
    st.subheader("📊 Ringkasan Data COVID-19 Indonesia")
    
    # Menampilkan Total Kasus Keseluruhan di halaman data
    total_cases = df['Total Cases'].sum()
    st.metric(label="Total Kasus Keseluruhan", value=f"{int(total_cases):,}")
    
    # 2. Menampilkan kolom Location, dan rentang New Cases sampai Total Recovered
    # Kita menggunakan .loc untuk mengambil kolom secara spesifik
    kolom_pilihan = ['Location'] + list(df.loc[:, 'New Cases':'Total Recovered'].columns)
    df_filtered = df[kolom_pilihan]
    
    st.write("Preview Data (Kolom Terfilter):")
    st.dataframe(df_filtered.head(10))
    
    st.subheader("Preview Data awal")
    st.write(df.head(10))
    
    st.subheader("Statistik Deskriptif Dataset")
    st.write(df_filtered.describe())
    
def total_case(df) :
    df = load_data ()
    total_kasus= df ['New Cases' ] .sum ()
    return total_kasus

def total_death(df) :
    df=load_data ()
    total_kematian= df ['New Deaths' ] .sum ()
    return total_kematian

def total_recovery(df) :
    df=load_data()
    total_sembuh= df[ 'New Recovered' ].sum ()
    return total_sembuh

def kolom(df):
    kasus = total_case(df )
    kematian = total_death(df)
    sembuh = total_recovery(df )

    col1, col2, col3 = st.columns(3)

    col1.metric(label=" Total Kasus", value=f"{kasus/1000:.1f}K", border=True)
    col2.metric(label=" Total Kematian", value=f"{kematian/1000 :.1f}K", border=True)
    col3.metric(label=" Total Sembuh", value=f"{sembuh/1000 :.1f}K", border=True)
    

#piechart1
def pie_chart1 (df) :
    #pemanggilan data
    total_mati= total_death (df)
    total_sumbuh= total_recovery (df)

    #dataframe
    data={
        'Status' : ['Meninggal', 'Sembuh'],
        'Jumlah' : [total_mati, total_sumbuh]
    }

    fig=px.pie(
        data,
        names='Status',
        values='Jumlah',
        title='Perbandingan Total Kematian VS Total Kesembuhan',
        hole=0.5,
        color_discrete_sequence=['#4de89f','#ff6459']
    )

    st.plotly_chart(fig, use_container_width=True)

def footer():
    # Menambahkan Copyright nama dan NPM
    st.markdown("---")
    st.caption('© 2024 | Farhat Chandra Permana - 184240007')
# ini komenan barunya