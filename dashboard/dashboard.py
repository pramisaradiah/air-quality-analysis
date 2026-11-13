import os
import streamlit as st
import pandas as pd
import plotly.express as px

# ==================================================
# 1. KONFIGURASI DASHBOARD
# ==================================================

st.set_page_config(
    page_title="Air Quality Analysis Dashboard",
    page_icon="🌫️",
    layout="wide"
)

# ==================================================
# 2. MEMBACA DATASET
# ==================================================

@st.cache_data
def load_data():

    file_path = os.path.join(
        os.path.dirname(__file__),
        "main_data.csv"
    )

    data = pd.read_csv(file_path)

    # Membuat kolom tanggal
    data["date"] = pd.to_datetime(
        data[["year", "month", "day"]]
    )

    # Membuat kolom musim jika belum tersedia
    if "season" not in data.columns:

        def get_season(month):
            if month in [3, 4, 5]:
                return "Spring"
            elif month in [6, 7, 8]:
                return "Summer"
            elif month in [9, 10, 11]:
                return "Autumn"
            else:
                return "Winter"

        data["season"] = data["month"].apply(get_season)

    # Menyeragamkan nama musim
    # Menyeragamkan nama musim
    season_mapping = {
        "Spring": "Semi",
        "Spring (Semi)": "Semi",
        "Summer": "Panas",
        "Summer (Panas)": "Panas",
        "Autumn": "Gugur",
        "Autumn (Gugur)": "Gugur",
        "Fall": "Gugur",
        "Winter": "Dingin",
        "Winter (Dingin)": "Dingin",
        "Semi": "Semi",
        "Panas": "Panas",
        "Gugur": "Gugur",
        "Dingin": "Dingin"
    }

    data["season"] = (
        data["season"]
        .astype(str)
        .str.strip()
        .map(season_mapping)
    )

    return data


try:
    df = load_data()

except Exception as e:
    st.error(f"Gagal membaca dataset: {e}")
    st.stop()


# ==================================================
# 3. JUDUL DAN DESKRIPSI
# ==================================================

st.title("🌫️ Dashboard Analisis Kualitas Udara")

st.markdown("""
Dashboard ini menyajikan hasil analisis kualitas udara
berdasarkan konsentrasi PM2.5 di Beijing selama periode
Maret 2013 hingga Februari 2017.

Analisis meliputi tren bulanan, perbandingan antarstasiun,
hubungan dengan faktor meteorologi, serta perbandingan
berdasarkan empat musim.
""")

st.divider()



# ==================================================
# 4. FILTER DATA
# ==================================================

st.sidebar.header("Filter Data")

# Filter stasiun
station_options = ["Semua Stasiun"] + sorted(
    df["station"].dropna().unique().tolist()
)

selected_station = st.sidebar.selectbox(
    "Stasiun Pemantauan",
    options=station_options
)

# Filter periode
min_date = df["date"].min().date()
max_date = df["date"].max().date()

selected_dates = st.sidebar.date_input(
    "Periode Pengamatan",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Validasi tanggal
if not isinstance(selected_dates, (tuple, list)) or len(selected_dates) != 2:
    st.warning("Silakan pilih tanggal awal dan tanggal akhir.")
    st.stop()

start_date, end_date = selected_dates

if start_date > end_date:
    st.warning("Tanggal awal tidak boleh melebihi tanggal akhir.")
    st.stop()

# Menerapkan filter
data_filter = df[
    (df["date"].dt.date >= start_date) &
    (df["date"].dt.date <= end_date)
].copy()

if selected_station != "Semua Stasiun":
    data_filter = data_filter[
        data_filter["station"] == selected_station
    ]

if data_filter.empty:
    st.warning("Tidak ada data berdasarkan filter yang dipilih.")
    st.stop()


# ==================================================
# 5. RINGKASAN DATA
# ==================================================

st.header("Ringkasan Data")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Rata-rata PM2.5",
    f"{data_filter['PM2.5'].mean():.2f} µg/m³"
)

col2.metric(
    "PM2.5 Tertinggi",
    f"{data_filter['PM2.5'].max():.2f} µg/m³"
)

col3.metric(
    "PM2.5 Terendah",
    f"{data_filter['PM2.5'].min():.2f} µg/m³"
)

col4.metric(
    "Jumlah Data",
    f"{len(data_filter):,}"
)

st.caption(
    "Ringkasan ditampilkan berdasarkan stasiun dan periode "
    "yang dipilih pada filter."
)

st.divider()


# ==================================================
# 6. VISUALISASI 1: TREN BULANAN PM2.5
# ==================================================

st.header("1. Tren Rata-rata Konsentrasi PM2.5 Bulanan")

st.write(
    "Visualisasi ini menunjukkan perubahan rata-rata "
    "konsentrasi PM2.5 setiap bulan selama periode pengamatan."
)

monthly_pm25 = (
    data_filter
    .groupby(data_filter["date"].dt.to_period("M"))["PM2.5"]
    .mean()
    .reset_index()
)

monthly_pm25.columns = ["periode", "PM2.5"]
monthly_pm25["periode"] = monthly_pm25["periode"].dt.to_timestamp()

fig_monthly = px.line(
    monthly_pm25,
    x="periode",
    y="PM2.5",
    markers=True,
    labels={
        "periode": "Periode",
        "PM2.5": "Rata-rata PM2.5 (µg/m³)"
    },
    title="Perubahan Rata-rata PM2.5 Setiap Bulan"
)

fig_monthly.update_layout(
    height=450,
    hovermode="x unified"
)

st.plotly_chart(
    fig_monthly,
    use_container_width=True
)

if not monthly_pm25.empty:

    highest_month = monthly_pm25.loc[
        monthly_pm25["PM2.5"].idxmax()
    ]

    lowest_month = monthly_pm25.loc[
        monthly_pm25["PM2.5"].idxmin()
    ]

    st.info(
        f"**Insight:** Rata-rata PM2.5 tertinggi terjadi pada "
        f"{highest_month['periode'].strftime('%B %Y')} "
        f"sebesar {highest_month['PM2.5']:.2f} µg/m³. "
        f"Rata-rata terendah terjadi pada "
        f"{lowest_month['periode'].strftime('%B %Y')} "
        f"sebesar {lowest_month['PM2.5']:.2f} µg/m³."
    )

st.divider()


# ==================================================
# 7. VISUALISASI 2: PERBANDINGAN ANTARSTASIUN
# ==================================================

st.header("2. Perbandingan Rata-rata PM2.5 Antarstasiun")

st.write(
    "Visualisasi ini membandingkan rata-rata konsentrasi "
    "PM2.5 pada setiap stasiun pemantauan."
)

station_pm25 = (
    data_filter
    .groupby("station")["PM2.5"]
    .mean()
    .reset_index()
    .sort_values("PM2.5", ascending=True)
)

fig_station = px.bar(
    station_pm25,
    x="PM2.5",
    y="station",
    orientation="h",
    text="PM2.5",
    labels={
        "station": "Stasiun Pemantauan",
        "PM2.5": "Rata-rata PM2.5 (µg/m³)"
    },
    title="Rata-rata Konsentrasi PM2.5 Berdasarkan Stasiun"
)

fig_station.update_traces(
    texttemplate="%{text:.2f}",
    textposition="outside"
)

fig_station.update_layout(
    height=500
)

st.plotly_chart(
    fig_station,
    use_container_width=True
)

if not station_pm25.empty:

    highest_station = station_pm25.loc[
        station_pm25["PM2.5"].idxmax()
    ]

    lowest_station = station_pm25.loc[
        station_pm25["PM2.5"].idxmin()
    ]

    st.info(
        f"**Insight:** Stasiun dengan rata-rata PM2.5 tertinggi "
        f"adalah {highest_station['station']} "
        f"sebesar {highest_station['PM2.5']:.2f} µg/m³. "
        f"Stasiun dengan rata-rata terendah adalah "
        f"{lowest_station['station']} "
        f"sebesar {lowest_station['PM2.5']:.2f} µg/m³."
    )

st.divider()


# ==================================================
# 8. VISUALISASI 3: KORELASI FAKTOR METEOROLOGI
# ==================================================

st.header("3. Hubungan PM2.5 dengan Faktor Meteorologi")

st.write("""
Visualisasi ini menggunakan korelasi Pearson untuk
menunjukkan hubungan antara PM2.5 dengan suhu (TEMP),
tekanan udara (PRES), titik embun (DEWP), curah hujan
(RAIN), dan kecepatan angin (WSPM).
""")

meteorological_columns = [
    "TEMP",
    "PRES",
    "DEWP",
    "RAIN",
    "WSPM",
    "PM2.5"
]

correlation = (
    data_filter[meteorological_columns]
    .corr(method="pearson")
)

fig_corr = px.imshow(
    correlation,
    text_auto=".2f",
    aspect="auto",
    color_continuous_scale="RdBu_r",
    zmin=-1,
    zmax=1,
    labels={
        "x": "Variabel",
        "y": "Variabel",
        "color": "Nilai Korelasi"
    },
    title="Heatmap Korelasi PM2.5 dan Faktor Meteorologi"
)

fig_corr.update_layout(
    height=550
)

st.plotly_chart(
    fig_corr,
    use_container_width=True
)

# Menampilkan nilai korelasi terhadap PM2.5
factor_correlation = (
    correlation["PM2.5"]
    .drop("PM2.5")
    .sort_values(key=abs, ascending=False)
    .reset_index()
)

factor_correlation.columns = [
    "Faktor Meteorologi",
    "Korelasi dengan PM2.5"
]

st.subheader("Nilai Korelasi Faktor Meteorologi")

st.dataframe(
    factor_correlation.style.format({
        "Korelasi dengan PM2.5": "{:.3f}"
    }),
    use_container_width=True,
    hide_index=True
)

st.info("""
**Insight:** Nilai korelasi positif menunjukkan hubungan
searah, sedangkan nilai negatif menunjukkan hubungan
berlawanan arah. Nilai yang mendekati nol menunjukkan
hubungan linear yang lemah. Korelasi tidak membuktikan
hubungan sebab-akibat.
""")

st.divider()


# ==================================================
# 9. VISUALISASI 4: PERBANDINGAN BERDASARKAN MUSIM
# ==================================================

st.header("4. Perbandingan Rata-rata PM2.5 Berdasarkan Musim")

st.write(
    "Visualisasi ini membandingkan rata-rata konsentrasi "
    "PM2.5 pada musim semi, panas, gugur, dan dingin."
)

season_order = [
    "Semi",
    "Panas",
    "Gugur",
    "Dingin"
]

season_pm25 = (
    data_filter
    .groupby("season")["PM2.5"]
    .mean()
    .reindex(season_order)
    .dropna()
    .reset_index()
)

fig_season = px.bar(
    season_pm25,
    x="season",
    y="PM2.5",
    text="PM2.5",
    category_orders={
        "season": season_order
    },
    labels={
        "season": "Musim",
        "PM2.5": "Rata-rata PM2.5 (µg/m³)"
    },
    title="Perbandingan Konsentrasi PM2.5 pada Empat Musim"
)

fig_season.update_traces(
    texttemplate="%{text:.2f}",
    textposition="outside"
)

fig_season.update_layout(
    height=450
)

st.plotly_chart(
    fig_season,
    use_container_width=True
)

if not season_pm25.empty:

    highest_season = season_pm25.loc[
        season_pm25["PM2.5"].idxmax()
    ]

    lowest_season = season_pm25.loc[
        season_pm25["PM2.5"].idxmin()
    ]

    st.info(
        f"**Insight:** Rata-rata PM2.5 tertinggi terdapat pada "
        f"musim {highest_season['season']} "
        f"sebesar {highest_season['PM2.5']:.2f} µg/m³, "
        f"sedangkan rata-rata terendah terdapat pada musim "
        f"{lowest_season['season']} "
        f"sebesar {lowest_season['PM2.5']:.2f} µg/m³."
    )

st.divider()


# ==================================================
# 10. TABEL DATA DAN DOWNLOAD
# ==================================================

st.header("Data yang Digunakan")

st.write(
    "Tabel berikut menampilkan dataset berdasarkan filter "
    "yang telah dipilih."
)

with st.expander("Tampilkan Dataset"):

    st.write(
        f"Jumlah baris: {len(data_filter):,}"
    )

    st.dataframe(
        data_filter.drop(columns=["date"], errors="ignore"),
        use_container_width=True,
        height=350
    )

    csv_data = data_filter.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="Download Data dalam Format CSV",
        data=csv_data,
        file_name="data_pm25_filtered.csv",
        mime="text/csv"
    )


# ==================================================
# 11. FOOTER
# ==================================================

st.divider()

st.markdown(
    """
    <div style="text-align: center;">
        <h4>Air Quality Analysis Dashboard</h4>
        <small>© 2026 | Diah Pramisara</small>
    </div>
    """,
    unsafe_allow_html=True
)
