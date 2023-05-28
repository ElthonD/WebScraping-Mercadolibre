### Librerías

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from PIL import Image
from dateutil.relativedelta import *
from joblib import dump, load
import streamlit.components.v1 as components        

# Title of the main page
pathLogo = 'Zebrands.png'
display = Image.open(pathLogo)
display = np.array(display)
col1, col2, col3 = st.columns([1,5,1])
col2.image(display, use_column_width=True)

st.write(""" ##### Bienvenido, está aplicación provee información histórica de precios e inventario disponible de los colchones Zebrands en Mercadolibre.""")

@st.cache_data(show_spinner='Cargando Datos... Espere...', persist=True)
def load_df():
    ruta = 'AmazonLuunaDataset.csv'
    data = pd.read_csv(ruta, encoding='latin-1')
    
    return data

#### Módulo Marco de Datos
st.markdown('#### Marco de Datos')

df = load_df()
st.write('Dimensión del Marco de Datos: ' + str(df.shape[0]) + ' filas y ' + str(df.shape[1]) + ' columnas.')
st.dataframe(df)

#### Módulo Gráfico
st.markdown(""" #### Gráfico Histórico de Precio e Inventario en Mercado Libre.""")

st.subheader('Seleccionar: ')

sorted_unique_product = sorted(df['Tipo'].unique())
selected_product = st.multiselect('Tipo:', sorted_unique_product)
df_selected_product = df[df['Tipo'].isin(selected_product)].astype(str)

fig = px.bar(df_selected_product, x="Fecha", y="Precio", color="Tipo")
st.plotly_chart(fig)