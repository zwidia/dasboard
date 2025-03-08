import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
def load_data():
    data = pd.read_csv("data_day1.csv", parse_dates=['date'])
    return data

data_day = load_data()

data_day['year'] = data_day['date'].dt.year
data_day['month'] = data_day['date'].dt.month_name()
data_day['year_month'] = data_day['date'].dt.to_period('M')

# Sidebar navigation
st.sidebar.title("Dashboard Penyewaan Sepeda")
option = st.sidebar.radio("Pilih Visualisasi:", [
    "Jumlah Penyewaan per Bulan",
    "Penyewaan Casual & Registered",
    "Penyewaan Berdasarkan Musim",
    "Penyewaan Berdasarkan Hari",
    "Cluster Penyewaan"
])

if option == "Jumlah Penyewaan per Bulan":
    jumlah_per_bulan = data_day.groupby(['year_month']).agg({'total_user': 'sum'}).reset_index()
    jumlah_per_bulan['year_month'] = jumlah_per_bulan['year_month'].astype(str)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(jumlah_per_bulan['year_month'], jumlah_per_bulan['total_user'], marker='o', color='blue', linewidth=2)
    ax.set_title("Jumlah Penyewaan Sepeda per Bulan", fontsize=16)
    ax.set_xlabel("Bulan", fontsize=12)
    ax.set_ylabel("Jumlah Penyewaan Sepeda", fontsize=12)
    ax.grid(True)
    plt.xticks(rotation=45)
    st.pyplot(fig)

elif option == "Penyewaan Casual & Registered":
    jumlah_per_bulan = data_day.groupby(['year_month']).agg({'casual': 'sum', 'registered': 'sum'}).reset_index()
    jumlah_per_bulan['year_month'] = jumlah_per_bulan['year_month'].astype(str)
    
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.plot(jumlah_per_bulan['year_month'], jumlah_per_bulan['casual'], marker='o', label='Casual', color='blue')
    ax.plot(jumlah_per_bulan['year_month'], jumlah_per_bulan['registered'], marker='o', label='Registered', color='green')
    ax.set_title("Jumlah Penyewaan Sepeda per Bulan (Casual & Registered)", fontsize=16)
    ax.set_xlabel("Bulan", fontsize=12)
    ax.set_ylabel("Jumlah Penyewaan Sepeda", fontsize=12)
    ax.legend()
    ax.grid(True)
    plt.xticks(rotation=45)
    st.pyplot(fig)

elif option == "Penyewaan Berdasarkan Musim":
    jumlah_per_season = data_day.groupby('season').agg({'casual': 'sum', 'registered': 'sum', 'total_user': 'sum'}).reset_index()
    jumlah_per_season_melted = jumlah_per_season.melt(id_vars='season', value_vars=['casual', 'registered', 'total_user'], var_name='user_type', value_name='total_count')
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=jumlah_per_season_melted, x='season', y='total_count', hue='user_type', ax=ax)
    ax.set_title("Jumlah Penyewaan Sepeda Berdasarkan Musim", fontsize=16)
    ax.set_xlabel("Musim", fontsize=12)
    ax.set_ylabel("Jumlah Penyewaan Sepeda", fontsize=12)
    ax.grid(True)
    st.pyplot(fig)

elif option == "Penyewaan Berdasarkan Hari":
    jumlah_per_day = data_day.groupby('day').agg({'casual': 'sum', 'registered': 'sum', 'total_user': 'sum'}).reset_index()
    jumlah_per_day_melted = jumlah_per_day.melt(id_vars='day', value_vars=['casual', 'registered', 'total_user'], var_name='user_type', value_name='total_count')
    
    fig, ax = plt.subplots(figsize=(12, 7))
    sns.barplot(data=jumlah_per_day_melted, x='day', y='total_count', hue='user_type', ax=ax)
    ax.set_title("Jumlah Penyewaan Sepeda Berdasarkan Hari", fontsize=16)
    ax.set_xlabel("Hari", fontsize=12)
    ax.set_ylabel("Jumlah Penyewaan Sepeda", fontsize=12)
    ax.grid(True)
    plt.legend(title='User Type', bbox_to_anchor=(1.05, 1), loc='upper left')
    st.pyplot(fig)

elif option == "Cluster Penyewaan":
    st.subheader("Cluster Penyewaan Berdasarkan Season dan Workingday")
    
    # Mengelompokkan data berdasarkan season dan workingday untuk casual
    data_season_casual = data_day.groupby(["season", "workingday"])['casual'].sum().reset_index()
    
    # Mengelompokkan data berdasarkan season dan workingday untuk registered
    data_season_registered = data_day.groupby(["season", "workingday"])['registered'].sum().reset_index()
    
    # Visualisasi
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Plot Casual Users
    sns.barplot(data=data_season_casual, x="season", y="casual", hue="workingday", ax=axes[0])
    axes[0].set_title("Cluster 1: Penyewaan Casual Berdasarkan Season & Workingday")
    axes[0].set_xlabel("Season")
    axes[0].set_ylabel("Jumlah Penyewaan")
    axes[0].set_xticklabels(axes[0].get_xticklabels(), rotation=45)
    
    # Plot Registered Users
    sns.barplot(data=data_season_registered, x="season", y="registered", hue="workingday", ax=axes[1])
    axes[1].set_title("Cluster 2: Penyewaan Registered Berdasarkan Season & Workingday")
    axes[1].set_xlabel("Season")
    axes[1].set_ylabel("Jumlah Penyewaan")
    axes[1].set_xticklabels(axes[1].get_xticklabels(), rotation=45)
    
    # Menampilkan grafik
    st.pyplot(fig)

st.sidebar.info("Data diambil dari 'data_day1.csv'")
