import pandas as pd
import streamlit as st
from datetime import timedelta
import numpy as np
import plotly.express as px


df = pd.read_csv('supermarket_sales.csv', encoding='unicode_escape')

# Inclusão de campos necessários ao dataframe
df['formatted_date'] = pd.to_datetime(df['date'])
df['total_amount'] = df['unit_cost'] * df['quantity']
df['week_number_month_year'] = pd.to_datetime(df['date']).dt.strftime('%V | %m/%Y')

# Exclusão de campos desnecessários
df.drop(columns=['invoice_id', 'date', 'time', '5pct_markup', 'revenue', 'cogs', 'gm_pct', 'gross_income'], inplace=True)

# Montagem de barra lateral (filtros) e configuração inicial da página
st.set_page_config(layout='wide', page_title='Dashboard - Supermercado')

st.sidebar.header('Dashboard - Supermercado')

unidade = st.sidebar.selectbox('Unidade', df['branch'].sort_values().unique())

dataInicial = st.sidebar.date_input(
    'Venda - data inicial', 
    value=df['formatted_date'].unique().min(), 
    min_value=df['formatted_date'].unique().min(), 
    max_value=df['formatted_date'].unique().max(),
    format='DD/MM/YYYY'
    )

dataFinal = st.sidebar.date_input(
    'Venda - data final', 
    value=df['formatted_date'].unique().min() + timedelta(days=1), 
    min_value=df['formatted_date'].unique().min() + timedelta(days=1), 
    max_value=df['formatted_date'].unique().max(),
    format='DD/MM/YYYY'
    )

# Atualização de dataframe conforme filtros aplicados
df = df.loc[(df['formatted_date'] >= np.datetime64(dataInicial)) & (df['formatted_date'] <= np.datetime64(dataFinal))]
df = df.loc[df['branch'] == unidade]

# Levantamento de dados variáveis
qtdRegistros = df.shape[0]
avaliacaoMedia = df['rating'].mean()

valorTotal = df['total_amount'].sum()
qtdTotal = df['quantity'].count()

ticketMedio = df['total_amount'].mean()
qtdMedia = df['quantity'].mean()
qtdCategoria = df.groupby('product_line')['product_line'].count()
vendasCategoria = df.groupby('product_line')['total_amount'].sum()

qtdSemana = df.groupby('week_number_month_year')['week_number_month_year'].count().reset_index(name='total')
qtdSemana['week_number'] = qtdSemana['week_number_month_year'].str[:2]
qtdSemana['month_year'] = qtdSemana['week_number_month_year'].str[5:]

vendasSemana = df.groupby('week_number_month_year')['total_amount'].sum().reset_index(name='total_amount')
vendasSemana['week_number'] = vendasSemana['week_number_month_year'].str[:2]
vendasSemana['month_year'] = vendasSemana['week_number_month_year'].str[5:]

#Exibição de dados variáveis
st.sidebar.write(f'{qtdRegistros} registros encontrados.')
st.sidebar.write(f'Avaliação média no período: {avaliacaoMedia:.2f}')

st.title(
    f'Detalhes da unidade {unidade} no período de {dataInicial.strftime("%d/%m/%Y")} a {dataFinal.strftime("%d/%m/%Y")}')

col1, col2 = st.columns(2)

with col1:
    st.header('Indicadores monetários')
    
    st.subheader('Valor total vendido no período')
    st.write('R$ ' + str(round(valorTotal, 2)))
    
    st.subheader('Ticket médio por cliente')
    st.write('R$ ' + str(round(ticketMedio, 2)))
    
    fig = px.bar(
        vendasCategoria, 
        title='Faturamento total por categoria',
        orientation='h', 
        text_auto='.2f'
        )
    fig.update_layout(
        xaxis = {'title': 'Valor (R$)'}, 
        yaxis = {'title': 'Categoria','categoryorder': 'total ascending'}, 
        showlegend=False
        )
    st.write(fig)
    
    fig = px.bar(
        vendasSemana, 
        x='week_number',
        y='total_amount',
        title='Faturamento total por semana',
        orientation='v', 
        text_auto='.2f',
        color='month_year'
        )
    
    fig.update_layout(
        xaxis = {'title': 'Semana', 'tickmode': 'linear'}, 
        yaxis = {'title': 'Valor (R$)'},
        showlegend=True
        )
    
    st.write(fig)
    
with col2:
    st.header('Indicadores quantitativos')
    
    st.subheader('Quantidade total vendida no período')
    st.write(str(round(qtdTotal, 0)) + ' unidades')
    
    st.subheader('Quantidade média por cliente')
    st.write(str(round(qtdMedia, 0)) + ' unidades')
    
    fig = px.bar(
        qtdCategoria, 
        title='Itens vendidos por categoria',
        orientation='h', 
        text_auto=True
        )
    
    fig.update_layout(
        xaxis = {'title': 'Quantidade'}, 
        yaxis = {'title': 'Categoria','categoryorder': 'total ascending'}, 
        showlegend=False
        )
    
    st.write(fig)
    
    fig = px.bar(
        qtdSemana, 
        x='week_number',
        y='total',
        title='Itens vendidos por semana',
        orientation='v', 
        text_auto='auto',
        color='month_year'
        )
    
    fig.update_layout(
        xaxis = {'title': 'Semana', 'tickmode': 'linear'}, 
        yaxis = {'title': 'Quantidade'},
        showlegend=True
        )
    
    st.write(fig)