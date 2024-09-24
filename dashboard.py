import pandas as pd
import numpy as np
import seaborn as sns
import streamlit as st

df = pd.read_csv('Datas.csv', index_col=False)
print(df)

def gases (df):
    gas = df[['NO2','SO2','CO']]
    return gas
def pert1_set (df):
    hipotesis1 = df.groupby(["year","hour"])[['NO2', 'SO2']].mean()
    return hipotesis1
def pert2_set (df):
    hipotesis2 = df.groupby(["year", "hour"])[['CO']].mean()
    return hipotesis2
def pert3_set (df):
    hipotesis3 = df.groupby(["year"])[['CO','O3']].mean().reset_index()
    return hipotesis3
def pert4_set (df , gas):
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
def pert5_set (df, gas, direction):
    rank = df.groupby(["year", "station"])[[gas]].mean().sort_values(['year', gas], ascending=direction).reset_index()
    return rank

gas = gases(df)
pert1 = pert1_set(df)
pert2 = pert2_set(df)
pert3 = pert3_set(df)
pert4 = pert4_set(df, 'NO2')

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
st.title('Pertanyaan 1')
st.write('Hubungan variable NO2 dan SO2 terhadap Hour')
option_year_pert1 = st.selectbox('Tahun Pertanyaan 1', range(2013, 2018))
gas = st.selectbox('Polutan Pertanyaan 1', ['NO2','SO2'])

gh1 = sns.FacetGrid(pert1.filter(regex=str(option_year_pert1), axis=0))
gh1.map_dataframe(sns.lineplot, x='hour', y=gas)
gh1.set(xticks=np.arange(0,23,2))
gh1.set_xticklabels(np.arange(0,23,2))
gh1.set_axis_labels('Jam', 'Kadar {}'.format(gas))
st.pyplot(gh1)
##Break
st.title('Pertanyaan 2')
st.write('Hubungan variable CO terhadap Hour')
option_year_pert2 = st.selectbox('Tahun Pertanyaan 2', range(2013, 2018))
gh2 = sns.FacetGrid(pert2.filter(regex=str(option_year_pert2), axis=0))
gh2.map_dataframe(sns.lineplot, x='hour', y='CO')
gh2.set(xticks=np.arange(0,23,2))
gh2.set_xticklabels(np.arange(0,23,2))
gh2.set_axis_labels('Jam', 'Kadar CO')
st.pyplot(gh2)
##Break
st.title('Pertanyaan 3')
st.write('Hubungan variable CO terhadap O3')
gas_pert3 = pert3.groupby('year')[['CO','O3']].mean().reset_index()
gas_pert3 = pd.melt(
    gas_pert3,
    id_vars=['year'],
    value_vars=('CO','O3'),
    var_name='Gas',
    value_name='Kadar',
    col_level=None
)
gh3 = sns.catplot(x="year", y="Kadar", hue='Gas', data=gas_pert3, kind='point')
st.pyplot(gh3)
##Break
st.title('Pertanyaan 4')
st.write('Hubungan variable NO2, SO2, dan CO terhadap PM2.5 dan PM10')
option_year_pert4 = st.selectbox('Tahun Pertanyaan 4', range(2013, 2018))
gas_pert4 = st.selectbox('Polutan Pertanyaan 4', ['NO2','SO2','CO'])
partikel = st.selectbox('Partikulat', ['PM2.5','PM10'])

partikulat = pert4_set(df, gas_pert4)

gh4 = sns.FacetGrid(partikulat.loc[pert4['year'] == option_year_pert4], hue='Partikulat')
gh4.map_dataframe(sns.scatterplot, x=gas_pert4, y='Index')
gh4.set_axis_labels('Kadar {}'.format(gas_pert4), 'Index')
gh4.add_legend()
st.pyplot(gh4)
##Break
st.title('Pertanyaan 5')
st.write('Urutan daerah penghasil polutan dari tahun ke tahun')
option_year_pert = st.selectbox('Tahun Pertanyaan 5', range(2013, 2018))
gas_pert5 = st.selectbox('Polutan Pertanyaan 5', ['NO2','SO2','CO'])
order = st.radio('Urutan', ['Tertinggi','Terendah'])

if order == 'Tertinggi':
    order = False
elif order == 'Terendah':
    order = True

rank = pert5_set(df, gas_pert5, order)

gp = sns.FacetGrid(rank.loc[rank['year'] == option_year_pert])
gp.map_dataframe(sns.barplot, x=gas_pert5, y='station')
gp.set_axis_labels('Kadar {}'.format(gas_pert5),'')
st.pyplot(gp)
