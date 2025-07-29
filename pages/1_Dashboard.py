import streamlit as st
import sys
import os

# Adicionar o diretório pai ao path para importar auth_utils
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from auth_utils import require_permission, show_user_info

# Verificar permissões
require_permission("dashboard")

# Interface da página
st.set_page_config(page_title="Dashboard", page_icon="📊")
show_user_info()

st.title("📊 Dashboard")
st.write("Bem-vindo ao dashboard! Esta página é acessível para todos os usuários autenticados.")

# Métricas fictícias
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Usuários Ativos", "1,234", "12%")

with col2:
    st.metric("Vendas", "R$ 45,678", "5%")

with col3:
    st.metric("Produtos", "89", "-2%")

with col4:
    st.metric("Satisfação", "98%", "1%")

# Gráfico simples
st.subheader("Vendas por Mês")

import pandas as pd
import numpy as np

# Dados fictícios
data = pd.DataFrame({
    'Mês': ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun'],
    'Vendas': np.random.randint(10000, 50000, 6)
})

st.line_chart(data.set_index('Mês'))

st.info("ℹ️ Esta é uma página básica acessível a todos os usuários autenticados.")