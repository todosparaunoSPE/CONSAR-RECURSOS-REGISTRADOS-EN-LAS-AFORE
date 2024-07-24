# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 14:01:39 2024

@author: jperezr
"""

import streamlit as st
import pandas as pd
import plotly.express as px

# Nombre del archivo
file_path = 'recursos_registrados_en_las_afores.xlsx'

# Datos de las hojas y sus descripciones
sheet_data = {
    "Hoja1": "Recursos Registrados en las Afores",
    "Hoja2": "Recursos Administrados por las Afores",
    "Hoja3": "Recursos de los trabajadores",
    "Hoja4": "RCV-IMSS",
    "Hoja5": "RCV ISSSTE",
    "Hoja6": "Ahorro Voluntario y Solidario",
    "Hoja7": "Ahorro Voluntario",
    "Hoja8": "Ahorro Solidario",
    "Hoja9": "Fondos de Previsión Social",
    "Hoja10": "Capital de las Afores",
    "Hoja11": "Bono de Pensión ISSSTE",
    "Hoja12": "Vivienda",
    "Hoja13": "INFONAVIT",
    "Hoja14": "FOVISSSTE",
    "Hoja15": "Recursos Depositados en Banco de México"
}

# Crear DataFrame de las hojas y sus descripciones
sheet_df = pd.DataFrame(list(sheet_data.items()), columns=["Hoja", "Descripción"])

# Función para leer el archivo Excel y devolver las hojas disponibles
def get_sheet_names(file):
    xls = pd.ExcelFile(file)
    return xls.sheet_names

# Función para leer la hoja seleccionada
def load_data(file, sheet_name):
    df = pd.read_excel(file, sheet_name=sheet_name)
    return df

# Interfaz de usuario en Streamlit
st.title("Recursos registrados en las AFORE")

# Sección de ayuda en la barra lateral
st.sidebar.title("Ayuda")
st.sidebar.write("""
Esta aplicación te permite explorar y visualizar los datos registrados en las AFOREs. A continuación, se detallan los pasos para utilizarla:

1. **Selecciona una hoja**: Utiliza el menú desplegable para seleccionar la hoja del archivo Excel que deseas visualizar.
2. **Visualiza los datos**: Los datos de la hoja seleccionada se mostrarán en una tabla.
3. **Filtra los datos**: Puedes filtrar los datos por "Descripción del Concepto" y "Fecha" utilizando los menús desplegables.
4. **Visualiza el gráfico**: Se mostrará un gráfico de barras basado en los datos filtrados.

Si tienes algún problema, asegúrate de que el archivo 'recursos_registrados_en_las_afores.xlsx' esté en el directorio correcto.
""")

# Pie de página en la barra lateral
#st.sidebar.write("© 2024 Todos los derechos reservados")
#st.sidebar.write("© 2024 jahoperi")

# Mostrar el DataFrame de las hojas y sus descripciones
st.write("Hojas disponibles y sus descripciones:")
st.dataframe(sheet_df)

# Cargar el archivo Excel automáticamente
try:
    sheet_names = get_sheet_names(file_path)
    
    # Combobox para seleccionar la hoja
    selected_sheet = st.selectbox("Elige una Hoja", sheet_names)
    
    # Cargar y mostrar los datos de la hoja seleccionada
    if selected_sheet:
        df = load_data(file_path, selected_sheet)
        st.write("Datos de la Hoja seleccionada:")
        st.dataframe(df)
        
        # Obtener valores únicos para cada columna
        unique_descriptions = df['Descripción del Concepto'].dropna().unique()
        unique_dates = df['Fecha'].dropna().unique()
        unique_data = df['Datos'].dropna().unique()

        # Filtrado de datos
        st.write("Filtrar Datos")
        description_filter = st.multiselect("Descripción del Concepto", unique_descriptions)
        date_filter = st.multiselect("Fecha", unique_dates)
        #data_filter = st.multiselect("Datos", unique_data)

        # Aplicar filtros
        filtered_df = df.copy()
        
        if description_filter:
            filtered_df = filtered_df[filtered_df['Descripción del Concepto'].isin(description_filter)]
        
        if date_filter:
            filtered_df = filtered_df[filtered_df['Fecha'].isin(date_filter)]
        
        #if data_filter:
        #    filtered_df = filtered_df[filtered_df['Datos'].isin(data_filter)]
        
        st.write("Datos filtrados:")
        st.dataframe(filtered_df)

        # Crear título dinámico
        graph_title = f"{sheet_data[selected_sheet]} vs Fecha"

        # Crear gráfico de barras no apiladas
        if not filtered_df.empty:
            fig = px.bar(
                filtered_df,
                x='Fecha',
                y='Datos',
                color='Descripción del Concepto',
                barmode='group',
                labels={'Fecha': 'Fecha', 'Datos': 'Datos', 'Descripción del Concepto': 'Descripción del Concepto'},
                title=graph_title
            )
            st.plotly_chart(fig)
except FileNotFoundError:
    st.error("El archivo 'recursos_registrados_en_las_afores.xlsx' no se encontró. Por favor, asegúrate de que el archivo esté en el directorio correcto.")



# Pie de página en la barra lateral
st.sidebar.write("© 2024 Todos los derechos reservados")
st.sidebar.write("© 2024 Creado por: Javier Horacio Pérez Ricárdez")
st.sidebar.write("PensionISSSTE: Analista UEAP B")
