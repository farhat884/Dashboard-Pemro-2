import streamlit as st
import pandas as pd
import plotly.express as px

# Fungsi untuk memuat data
def load_data():
    df = pd.read_csv("dataset/covid_19_indonesia_time_series_all.csv")
    df = df[df['Location'] != 'Indonesia']
    return df

# Filter data berdasarkan tahun (optional)
def filter_data(df, year=None, locations=None):
    """Filter data berdasarkan tahun dan multiple locations"""
    if year:
        df = df[df['Date'].astype(str).str.contains(str(year))]
    
    # Handle multiple locations
    if locations and "Semua Provinsi" not in locations:
        df = df[df['Location'].isin(locations)]  # .isin() untuk multiple values
    
    return df

def select_year():
    return st.sidebar.selectbox(
        "Pilih Tahun",
        options=[None, 2020, 2021, 2022],
        format_func=lambda x: "Semua Tahun" if x is None else str(x)
    )
def select_location(df):
    """Fungsi untuk memilih multiple provinsi"""
    locations = ["Semua Provinsi"] + sorted(df['Location'].unique())
    
    # Gunakan multiselect untuk memilih banyak provinsi
    selected_locations = st.sidebar.multiselect(
        "Pilih Provinsi (bisa lebih dari satu)",
        options=locations,
        default=["Semua Provinsi"]  # Default memilih Semua Provinsi
    )
    
    # Jika "Semua Provinsi" dipilih bersama provinsi lain, prioritaskan Semua Provinsi
    if "Semua Provinsi" in selected_locations:
        return ["Semua Provinsi"]  # Return list dengan Semua Provinsi saja
    
    # Return list provinsi yang dipilih (bisa kosong)
    return selected_locations if selected_locations else ["Semua Provinsi"]
    
    return selected_locations if selected_locations else locations

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
    total_kasus = df.sort_values('Date').groupby('Location', as_index=False).last()
    return total_kasus['Total Cases'].sum ()

def total_death(df) :
    total_kematian = df.sort_values('Date').groupby('Location', as_index=False).last()
    return total_kematian['Total Deaths'].sum()

def total_recovery(df) :
    total_sembuh = df.sort_values('Date').groupby('Location', as_index=False).last()
    return total_sembuh['Total Recovered'].sum() 

def kolom(df):
    kasus = total_case(df )
    kematian = total_death(df)
    sembuh = total_recovery(df )

    col1, col2, col3 = st.columns(3)

    col1.metric(label=" Total Kasus", value=f"{kasus/1000:.1f}K", border=True)
    col2.metric(label=" Total Kematian", value=f"{kematian/1000 :.1f}K", border=True)
    col3.metric(label=" Total Sembuh", value=f"{sembuh/1000 :.1f}K", border=True)
    

#piechart1
def pie_chart1(df) :
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

def bar_chart1(df):
    # Ambil data terakhir per provinsi (group by Location ambil baris terakhir)
    df_last = df.sort_values('Date').groupby('Location', as_index=False).last()

    # Ambil 5 provinsi dengan kematian terbanyak
    top5 = df_last.nlargest(5, 'Total Deaths')

    # Buat bar chart
    fig = px.bar(
        top5,
        x='Location',
        y='Total Deaths',
        color='Total Deaths',
        color_continuous_scale='Reds',
        title=' top 5 Provinsi dengan Kematian Tertinggi',
        labels={'Total Deaths': 'Total Kematian', 'Location' : 'Provinsi'}

    )

    fig.update_layout (xaxis_title='Provinsi', yaxis_title='Total Kematian', title_x=0.5)

    st.plotly_chart (fig, use_container_width=True)
    
def bar_chart2 (df) :
    # Ambil data terakhir per provinsi (group by Location ambil baris terakhir)
    df_last = df.sort_values ('Date') .groupby ('Location', as_index=False) .last ()

    # Ambil 5 provinsi dengan kematian terbanyak
    top5 = df_last.nlargest (5, 'Total Recovered')

    # Buat bar chart
    fig = px.bar(
        top5,
        x='Location',
        y='Total Recovered',
        color='Total Recovered',
        color_continuous_scale='greens',
        title=' 5 Provinsi dengan Kesembuhan Tertinggi',
        labels={'Total Recovered': 'Total Kesembuhan', 'Location' : 'Provinsi'}
    )

    fig.update_layout (xaxis_title='Provinsi', yaxis_title='Total Kesembuhan', title_x=0.5)

    st.plotly_chart (fig, use_container_width=True)

def map_chart (df, year=None) :
    # Konversi kolom Date
    df['Date'] = pd.to_datetime (df['Date'])

    # Filter data berdasarkan tahun
    if year:
        df = df[df['Date'].dt.year == year]

    # Agregasi data per lokasi
    df_agg = df.groupby(['Location', 'Latitude', 'Longitude'], as_index=False) ['New Cases' ] . sum ()
    df_map = df_agg.dropna (subset=['Latitude', 'Longitude', 'New Cases' ])

    # Validasi data
    if df_map.empty:
        st. info (" Tidak ada data yang ditampilkan")
        return

    # Buat scatter mapbox
    fig = px.scatter_mapbox (
        df_map,
        lat="Latitude",
        lon="Longitude",
        size="New Cases",
        color="New Cases",
        hover_name="Location",
        zoom=3,
        center={"lat": -2.5, "lon": 118}, # Fokus Indonesia
        size_max=20,
        opacity=0.7,
        color_continuous_scale="OrRd",
        title=f"Sebaran Kasus Baru Covid-19 di Indonesia ({year if year else 'Semua Tahun' } ) "
    )
    
    fig.update_layout (
        mapbox_style="carto-positron",
        height=600,
        margin={"r": 0, "t": 50, "l": 0, "b": 0}  # ✅ "l":0 (huruf L kecil)
    )

    # Tampilkan peta di Streamlit
    st.plotly_chart (fig, use_container_width=True)

def footer():
    # Menambahkan Copyright nama dan NPM
    st.markdown("---")
    st.caption('© 2024 | Farhat Chandra Permana - 184240007')
# ini komenan barunya