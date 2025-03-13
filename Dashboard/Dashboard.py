import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
import numpy as np


hour_df = pd.read_csv('Data/day_cleaned.csv')

with st.sidebar:
    # Title
    st.title("Muhammad Naufal Nugroho")

    # Logo Image
    st.image("Dashboard/logo.png")

    # Date Range


table = hour_df.rename(columns={'yr' : 'Year', 'season' : 'Season', 'casual' : 'Pengguna Tidak Terdaftar', 'registered' : 'Pengguna Terdaftar', 'cnt' : 'Total', 'dteday' : 'Day', 'mnth' : 'Month' })

# Title
st.header("Bike Sharing Dashboard")

# Monthly Orders
st.subheader("Peminjaman Perbulan")


months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
hour_df['mnth'] = hour_df['mnth'].apply(
    lambda x: "Jan" if x == 1 else "Feb" if x == 2 else "Mar" if x == 3 
    else "Apr" if x == 4 else "May" if x == 5 else "Jun" if x == 6 
    else "Jul" if x == 7 else "Aug" if x == 8 else "Sep" if x == 9
    else "Oct" if x == 10 else "Nov" if x == 11 else "Dec")
hour_df['mnth'] = pd.Categorical(hour_df['mnth'], categories=months, ordered=True)
hour_df.sort_values(by="mnth",inplace=True)
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(20, 6))
colors = ["#FFB4C2", "#9DBDFF", "#a2c4c9","#72BCD4","#e06666","#9fc5e8", "#FF9874","#cfe2f3","#d9d2e9"]
years_2011 = table['Year'].values == 2011
total_2011 = table[years_2011]
total_2011 = total_2011.groupby(by="Month", observed=False).agg({"Total":  "sum"})
years_2012 = table['Year'].values == 2012
total_2012 = table[years_2012]
total_2012 = total_2012.groupby(by="Month", observed=False).agg({"Total":  "sum"})
sns.barplot(y="Total", x="Month", data=total_2011, hue="Total", palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("Bulan 2011", loc="center", fontsize=18)
ax[0].set_ylim(0, 700000)
ax[0].tick_params(axis ='x', labelsize=15)
sns.barplot(y="Total", x="Month", data=total_2012, hue="Total", palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].set_title("Bulan 2012", loc="center", fontsize=18)
ax[1].set_ylim(0, 700000)
ax[1].tick_params(axis ='x', labelsize=15)
plt.suptitle("Total Peminjaman Berdasarkan Bulan", fontsize=20)
st.pyplot(fig)

st.subheader("Peminjaman Permusim")
table.groupby(by=["Year", "Season"], observed=False).agg({"Total":  "sum"})
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(20, 6))
colors = ["#FFB4C2", "#9DBDFF", "#a2c4c9","#72BCD4"]
years_2011 = table['Year'].values == 2011
total_2011 = table[years_2011]
total_2011 = total_2011.groupby(by="Season", observed=False).agg({"Total":  "sum"})
years_2012 = table['Year'].values == 2012
total_2012 = table[years_2012]
total_2012 = total_2012.groupby(by="Season", observed=False).agg({"Total":  "sum"})
sns.barplot(y="Total", x="Season", data=total_2011, hue="Total", palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("By Season (2011)", loc="center", fontsize=18)
ax[0].set_ylim(0, 700000)
ax[0].tick_params(axis ='x', labelsize=15)
sns.barplot(y="Total", x="Season", data=total_2012, hue="Total", palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].set_title("By Season (2012)", loc="center", fontsize=18)
ax[1].set_ylim(0, 700000)
ax[1].tick_params(axis ='x', labelsize=15)
plt.suptitle("Total Peminjaman Berdasarkan Musim", fontsize=20)
st.pyplot(fig)

st.subheader("Perbandingan Antara Peminjam Sepeda dengan kategori Pengguna Terdaftar Diaplikasi dengan Pengguna Tidak Terdaftar Diaplikasi")
data_compare = table.groupby(by=["Year", "Month"], observed=False).agg({'Pengguna Tidak Terdaftar' : 'sum','Pengguna Terdaftar' : 'sum','Total':  'sum',})
data_compare["difference"] = data_compare["Pengguna Terdaftar"] - data_compare["Pengguna Tidak Terdaftar"]
data_compare["diff_percent"] = round(data_compare["difference"] / data_compare["Total"] * 100, 2)
years_2011 = table['Year'].values == 2011
user_2011 = table[years_2011]
user_2011 = user_2011.groupby(by="Month", observed=False).agg({'Pengguna Tidak Terdaftar' : 'sum','Pengguna Terdaftar' : 'sum','Total':  'sum',})
years_2012 = table['Year'].values == 2012
user_2012 = table[years_2012]
user_2012 = user_2012.groupby(by="Month", observed=False).agg({'Pengguna Tidak Terdaftar' : 'sum','Pengguna Terdaftar' : 'sum','Total':  'sum',})
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(20, 6))
ax[0].plot(months, user_2011['Pengguna Terdaftar'], label='Pengguna Terdaftar', marker="o", color='#72BCD4', figure=fig)
ax[0].plot(months, user_2011['Pengguna Tidak Terdaftar'], label='Pengguna Tidak Terdaftar', marker="*", color='#e06666', figure=fig)
ax[0].set_title("2011", loc="center", fontsize=20)
ax[0].set_ylim(0, 200000)
ax[0].legend()
ax[1].plot(months, user_2012['Pengguna Terdaftar'], label='Registered User', marker="o", color='#72BCD4', figure=fig)
ax[1].plot(months, user_2012['Pengguna Tidak Terdaftar'], label='Pengguna Tidak Terdaftar', marker="*", color='#e06666', figure=fig)
ax[1].set_title("2012", loc="center", fontsize=20)
ax[1].set_ylim(0, 200000)
ax[1].legend()
plt.suptitle("Rental Perbulan", fontsize=20)
st.pyplot(fig)
st.subheader("Perentalan Sepeda Pada Bulan Sep, Okt, Nov Tahun 2012")
years_2012 = table['Year'].values == 2012
data_2012 = table[years_2012]
month_sep = data_2012['Month'].values == 'Sep'
data_sep = data_2012[month_sep]
month_oct = data_2012['Month'].values == 'Oct'
data_oct = data_2012[month_oct]
month_nov = data_2012['Month'].values == 'Nov'
data_nov = data_2012[month_nov]
data_sep = data_sep.groupby(by="Day", observed=True).agg({'Day': 'unique','Total':  'sum'})
data_oct = data_oct.groupby(by="Day", observed=True).agg({'Day': 'unique','Total':  'sum'})
data_nov = data_nov.groupby(by="Day", observed=True).agg({'Day': 'unique','Total':  'sum'})
data_merge = data_oct
data_merge['Sep'] = data_sep['Total']
data_merge['Oct'] = data_oct['Total']
data_merge['Nov'] = data_nov['Total']
plt.figure(figsize=(12, 6))
plt.plot(data_sep['Day'], data_sep['Total'], marker="o", label='Sep', color='#FFB4C2')
plt.plot(data_oct['Day'], data_oct['Total'], marker="*", label='Oct', color='#9DBDFF')
plt.plot(data_nov['Day'], data_nov['Total'], marker="s", label='Nov', color='#a2c4c9')
plt.title('Perentalan Sepeda Pada Bulan Sep, Okt, Nov Tahun 2012', size=18)
plt.xlabel('Tanggal',size=15)
plt.ylabel('Perentalan',size=15)
plt.xticks(np.arange(1, 32, 1))
plt.yticks(np.arange(0, 10000, 1000))
plt.ylim(0, 10000)
plt.xlim(0, 31)
plt.legend()
st.pyplot(fig)