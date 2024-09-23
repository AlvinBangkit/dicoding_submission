import pandas as pd
import numpy as np
import seaborn as sns
import streamlit as st

df = pd.read_csv('Datas.csv', index_col=False)
print(df)

def gases (df):
    gas = df[['NO2','SO2','CO']]
    return gas
def hipotesis1_set (df):
    hipotesis1 = df.groupby(["year","hour"])[['NO2', 'SO2']].mean()
    return hipotesis1
def hipotesis2_set (df):
    hipotesis2 = df.groupby(["year", "hour"])[['CO']].mean()
    return hipotesis2
def hipotesis3_set (df):
    hipotesis3 = df.groupby(["year"])[['CO','O3']].mean().reset_index()
    return hipotesis3
def hipotesis4_set (df , gas):
    particle = df.groupby(['year', 'month'])[[gas, 'PM2.5', 'PM10']].mean().reset_index()
    particle = pd.melt(
        particle,
        id_vars=['year', 'month', gas],
        value_vars=('PM2.5', 'PM10'),
        var_name='Partikulat',
        value_name='Index',
        col_level=None
    )
    return particle
def pertanyaan_set (df, gas, direction):
    rank = df.groupby(["year", "station"])[[gas]].mean().sort_values(['year', gas], ascending=direction).reset_index()
    return rank

gas = gases(df)
hipo1 = hipotesis1_set(df)
hipo2 = hipotesis2_set(df)
hipo3 = hipotesis3_set(df)
hipo4 = hipotesis4_set(df, 'NO2')

#Streamlit Environment

##Title
gas_list=['NO2','SO2','CO']
year_list_hipo1=range(2013, 2018)

# You can use a column just like st.sidebar:

st.title("Analisis Air Quality")
st.write('Nama: Alvin Dzaki Pratama Darmawan')
st.write('Email: m299b4ky0427@bangkit.academy')
st.write('ID Dicoding: alvin_dzaki')
##Break
st.title('Hipotesis 1')
st.write('Hubungan variable NO2 dan SO2 terhadap Hour')
option_year_hipo1 = st.selectbox('Tahun Hipotesis 1', range(2013, 2018))
gas = st.selectbox('Polutan Hipotesis 1', ['NO2','SO2'])

gh1 = sns.FacetGrid(hipo1.filter(regex=str(option_year_hipo1), axis=0))
gh1.map_dataframe(sns.lineplot, x='hour', y=gas)
gh1.set(xticks=np.arange(0,23,2))
gh1.set_xticklabels(np.arange(0,23,2))
gh1.set_axis_labels('Jam', 'Kadar {}'.format(gas))
st.pyplot(gh1)
##Break
st.title('Hipotesis 2')
st.write('Hubungan variable CO terhadap Hour')
option_year_hipo2 = st.selectbox('Tahun Hipotesis 2', range(2013, 2018))
gh2 = sns.FacetGrid(hipo2.filter(regex=str(option_year_hipo2), axis=0))
gh2.map_dataframe(sns.lineplot, x='hour', y='CO')
gh2.set(xticks=np.arange(0,23,2))
gh2.set_xticklabels(np.arange(0,23,2))
gh2.set_axis_labels('Jam', 'Kadar CO')
st.pyplot(gh2)
##Break
st.title('Hipotesis 3')
st.write('Hubungan variable CO terhadap O3')
gas_hip3 = hipo3.groupby('year')[['CO','O3']].mean().reset_index()
gas_hip3 = pd.melt(
    gas_hip3,
    id_vars=['year'],
    value_vars=('CO','O3'),
    var_name='Gas',
    value_name='Kadar',
    col_level=None
)
gh3 = sns.catplot(x="year", y="Kadar", hue='Gas', data=gas_hip3, kind='point')
st.pyplot(gh3)
##Break
st.title('Hipotesis 4')
st.write('Hubungan variable NO2, SO2, dan CO terhadap PM2.5 dan PM10')
option_year_hipo4 = st.selectbox('Tahun Hipotesis 4', range(2013, 2018))
gas_hipo4 = st.selectbox('Polutan Hipotesis 4', ['NO2','SO2','CO'])
partikel = st.selectbox('Partikulat', ['PM2.5','PM10'])

partikulat = hipotesis4_set(df, gas_hipo4)

gh4 = sns.FacetGrid(partikulat.loc[hipo4['year'] == option_year_hipo4], hue='Partikulat')
gh4.map_dataframe(sns.scatterplot, x=gas_hipo4, y='Index')
gh4.set_axis_labels('Kadar {}'.format(gas_hipo4), 'Index')
gh4.add_legend()
st.pyplot(gh4)
##Break
st.title('Pertanyaan')
st.write('Urutan daerah penghasil polutan dari tahun ke tahun')
option_year_pert = st.selectbox('Tahun Pertanyaan', range(2013, 2018))
gas_pert = st.selectbox('Polutan Pertanyaan', ['NO2','SO2','CO'])
order = st.radio('Urutan', ['Tertinggi','Terendah'])

if order == 'Tertinggi':
    order = False
elif order == 'Terendah':
    order = True

rank = pertanyaan_set(df, gas_pert, order)

gp = sns.FacetGrid(rank.loc[rank['year'] == option_year_pert])
gp.map_dataframe(sns.barplot, x=gas_pert, y='station')
gp.set_axis_labels('Kadar {}'.format(gas_pert),'')
st.pyplot(gp)
