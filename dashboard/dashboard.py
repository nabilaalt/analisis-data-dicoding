import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FuncFormatter
import numpy as np
from datetime import datetime

def configure_page():
    st.set_page_config(
        page_title="Dashboard Penyewaan Sepeda",
        page_icon="🚲",
        layout="wide"
    )
    
    st.markdown("""
    <style>
    .stPlotlyChart, .stPlot {
        background-color: transparent !important;
    }
    .css-1kyxreq, .css-12oz5g7 {
        margin-top: -2rem;
    }
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)


@st.cache_data
def load_data():

    day_df = pd.read_csv("dashboard/cleaned_day_data.csv")
    hour_df = pd.read_csv("dashboard/cleaned_hour_data.csv")
    
    day_df['dteday'] = pd.to_datetime(day_df['dteday'])
    hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
    
    return day_df, hour_df

def plot_by_time_of_day(hour_df, start_date, end_date):
    filtered_hour_df = hour_df[(hour_df['dteday'] >= start_date) & (hour_df['dteday'] <= end_date)]
    
    time_group = filtered_hour_df.groupby("time_of_day")["total_rentals"].sum().reset_index()
    time_order = ["Morning", "Afternoon", "Evening", "Night"]
    time_group = time_group.set_index("time_of_day").reindex(time_order).reset_index()
    time_labels = ["Morning(6-12)", "Afternoon(12-18)", "Evening(18-0)", "Night(0-6)"]
    colors = ['#174e7d','#1f77b4','#1f77b4','#1f77b4']
    
    formatter = FuncFormatter(lambda x, _: f'{int(x):,}')
    
    fig, ax = plt.subplots(figsize=(10, 5))
    fig.patch.set_alpha(0.0)  
    ax.patch.set_alpha(0.0) 
    
    sns.barplot(data=time_group.sort_values(by="time_of_day"), x="time_of_day", y="total_rentals", palette=colors, ax=ax)
    
    plt.xticks(ticks=range(len(time_labels)), labels=time_labels, rotation=45)
    ax.yaxis.set_major_formatter(formatter)
    plt.title("Penyewaan Sepeda Berdasarkan Waktu dalam Sehari", color='white', fontsize=14)
    plt.xlabel("Periode Waktu", color='white')
    plt.ylabel("Jumlah Penyewaan", color='white')
    
    ax.grid(axis="y", linestyle="--", alpha=0.3, color='white')
    ax.tick_params(colors='white')
    for spine in ax.spines.values():
        spine.set_color('white')
        
    return fig

def plot_by_day_factors(day_df, start_date, end_date):
    filtered_day_df = day_df[(day_df['dteday'] >= start_date) & (day_df['dteday'] <= end_date)]
    
    colors = ["#1f77b4","#1f77b4","#1f77b4","#1f77b4","#1f77b4","#1f77b4","#1f77b4"]
    
    fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(12, 15))
    fig.patch.set_alpha(0.0)  
    
    for ax in axes:
        ax.patch.set_alpha(0.0)  
    
    sns.barplot(
        x='workingday',
        y='total_rentals',
        data=filtered_day_df,
        ax=axes[0],
        palette="Blues")
    axes[0].set_title('Jumlah Penyewaan Sepeda berdasarkan Hari Kerja', color='white', fontsize=14)
    axes[0].set_xlabel('Hari Kerja (0 = Libur, 1 = Kerja)', color='white', fontsize=12)
    axes[0].set_ylabel('Total Penyewaan', color='white', fontsize=12)
    axes[0].grid(axis='y', linestyle='--', alpha=0.3, color='white')
    
    sns.barplot(
        x='holiday',
        y='total_rentals',
        data=filtered_day_df,
        ax=axes[1],
        palette="Blues")
    axes[1].set_title('Jumlah Penyewaan Sepeda berdasarkan Hari Libur', color='white', fontsize=14)
    axes[1].set_xlabel('Hari Libur (0 = Tidak, 1 = Ya)', color='white', fontsize=12)
    axes[1].set_ylabel('Total Penyewaan', color='white', fontsize=12)
    axes[1].grid(axis='y', linestyle='--', alpha=0.3, color='white')
    
    sns.barplot(
        x='weekday',
        y='total_rentals',
        data=filtered_day_df,
        ax=axes[2],
        palette=colors)
    axes[2].set_title('Jumlah Penyewaan Sepeda berdasarkan Hari dalam Seminggu', color='white', fontsize=14)
    axes[2].set_xlabel('Hari dalam Seminggu (0 = Minggu, 6 = Sabtu)', color='white', fontsize=12)
    axes[2].set_ylabel('Total Penyewaan', color='white', fontsize=12)
    axes[2].grid(axis='y', linestyle='--', alpha=0.3, color='white')
    
    for ax in axes:
        ax.tick_params(colors='white')
        for spine in ax.spines.values():
            spine.set_color('white')
    
    plt.tight_layout()
    return fig

def plot_by_weather(day_df, start_date, end_date):
    filtered_day_df = day_df[(day_df['dteday'] >= start_date) & (day_df['dteday'] <= end_date)]
    
    sorted_day_df = filtered_day_df.sort_values(by='total_rentals', ascending=False)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_alpha(0.0) 
    ax.patch.set_alpha(0.0)  

    sns.barplot(
        x='weathersit',
        y='total_rentals',
        data=sorted_day_df,
        ax=ax)
    
    plt.title('Jumlah Pengguna Sepeda berdasarkan Kondisi Cuaca', color='white', fontsize=14)
    plt.xlabel('Kondisi Cuaca', color='white')
    plt.ylabel('Jumlah Pengguna Sepeda', color='white')
    
    ax.grid(axis="y", linestyle="--", alpha=0.3, color='white')
    ax.tick_params(colors='white')
    for spine in ax.spines.values():
        spine.set_color('white')
    
    return fig

def main():
    configure_page()
    
    st.title("📊 Dashboard Penyewaan Sepeda")
    st.markdown("---")
    
    try:
        day_df, hour_df = load_data()
    except Exception as e:
        st.error(f"Error loading data: {e}")
        st.warning("Gunakan placeholder data untuk demonstrasi")
        

    st.sidebar.header("Filter Data")
    
    min_date = day_df['dteday'].min().date()
    max_date = day_df['dteday'].max().date()
    
    start_date = st.sidebar.date_input(
        "Tanggal Mulai",
        min_date,
        min_value=min_date,
        max_value=max_date
    )
    
    end_date = st.sidebar.date_input(
        "Tanggal Akhir",
        max_date,
        min_value=start_date,
        max_value=max_date
    )
    
    start_date = pd.Timestamp(start_date)
    end_date = pd.Timestamp(end_date)
    
    st.header("Penyewaan Sepeda Berdasarkan Waktu dalam Sehari")
    time_fig = plot_by_time_of_day(hour_df, start_date, end_date)
    st.pyplot(time_fig,transparent=True)
    st.markdown("---")
    
    st.header("Penyewaan Sepeda Berdasarkan Faktor Hari")
    day_factors_fig = plot_by_day_factors(day_df, start_date, end_date)
    st.pyplot(day_factors_fig,transparent=True)
    st.markdown("---")
    
    st.header("Penyewaan Sepeda Berdasarkan Kondisi Cuaca")
    weather_fig = plot_by_weather(day_df, start_date, end_date)
    st.pyplot(weather_fig,transparent=True)

if __name__ == "__main__":
    main()