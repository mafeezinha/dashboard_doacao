import streamlit as st
import pandas as pd
import plotly.express as px
import os

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Dashboard de Doações - IDIS",
    page_icon="📊",
    layout="wide"
)

st.title("📊  Pesquisa de Doações IDIS")
st.markdown("Análise de demandas da população vulnerável e do volume de doações arrecadadas em São Paulo.")

# --- CARREGAMENTO DOS DADOS ---
# Encontra o caminho do ficheiro quer esteja a rodar da raiz ou de dentro da pasta 'Dados'
if os.path.exists('pesquisa_doacao_idis.xlsx'):
    excel_path = 'pesquisa_doacao_idis.xlsx'
elif os.path.exists('Dados/pesquisa_doacao_idis.xlsx'):
    excel_path = 'Dados/pesquisa_doacao_idis.xlsx'
else:
    excel_path = 'pesquisa_doacao_idis.xlsx'

@st.cache_data
def load_data(path):
    df_demanda = pd.read_excel(path, sheet_name='Demanda')
    df_doacoes = pd.read_excel(path, sheet_name='Doações arrecadadas')
    return df_demanda, df_doacoes

try:
    df_demanda, df_doacoes = load_data(excel_path)
except Exception as e:
    st.error(f"Erro ao carregar a planilha '{excel_path}': {e}")
    st.stop()

# --- BARRA LATERAL (NAVEGAÇÃO) ---
st.sidebar.header("🔍 Navegação e Filtros")
aba_selecionada = st.sidebar.selectbox(
    "Escolha a Seção do Dashboard:",
    ["Visão Geral", "Demanda (Público-Alvo)", "Doações Arrecadadas"]
)

st.sidebar.markdown("---")
st.sidebar.info("Dashboard desenvolvido com Streamlit e Plotly no VS Code.")

# --- SEÇÃO 1: VISÃO GERAL ---
if aba_selecionada == "Visão Geral":
    st.subheader("Visão Consolidada dos Dados")
    
    # Cálculo das Métricas (KPIs)
    total_pessoas = df_demanda['Pessoas (SP)'].sum()
    
    # Filtra para excluir a linha de total na agregação do gráfico/métrica
    df_doacoes_itens = df_doacoes[df_doacoes['Categoria do Item'] != 'TOTAL DE ROUPAS']
    total_doacoes = df_doacoes_itens['Volume Arrecadado (Peças)'].sum()
    
    col1, col2 = st.columns(2)
    col1.metric("👥 Total de Pessoas em Vulnerabilidade (SP)", f"{total_pessoas:,.0f}".replace(",", "."))
    col2.metric("📦 Total de Peças Arrecadadas", f"{total_doacoes:,.0f}".replace(",", "."))
    
    st.markdown("---")
    
    # Gráficos Principais
    col_g1, col_g2 = st.columns(2)
    
    with col_g1:
        st.markdown("#### Demanda por Público-Alvo")
        fig_demanda = px.bar(
            df_demanda, 
            x='Pessoas (SP)', 
            y='Público', 
            orientation='h',
            text='Pessoas (SP)',
            color='Público',
            title="População Atendida"
        )
        fig_demanda.update_layout(showlegend=False)
        st.plotly_chart(fig_demanda, use_container_width=True)
        
    with col_g2:
        st.markdown("#### Distribuição das Doações Arrecadadas")
        fig_doacoes = px.pie(
            df_doacoes_itens, 
            names='Categoria do Item', 
            values='Volume Arrecadado (Peças)',
            hole=0.4,
            title="Volume por Categoria"
        )
        st.plotly_chart(fig_doacoes, use_container_width=True)

# --- SEÇÃO 2: DEMANDA (PÚBLICO-ALVO) ---
elif aba_selecionada == "Demanda (Público-Alvo)":
    st.subheader("Análise Detalhada da Demanda")
    st.markdown("Detalhamento do público necessitado e das roupas de maior urgência.")
    
    st.dataframe(df_demanda, use_container_width=True)