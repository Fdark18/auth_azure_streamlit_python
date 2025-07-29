import streamlit as st
import sys
import os

# Adicionar o diretório pai ao path para importar auth_utils
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from auth_utils import require_manager_or_admin, show_user_info, get_user_role

# Verificar permissões (apenas gerentes e admins)
require_manager_or_admin()

# Interface da página
st.set_page_config(page_title="Relatórios", page_icon="📈")
show_user_info()

st.title("📈 Relatórios Gerenciais")
st.write("Esta página é restrita a gerentes e administradores.")

user_role = get_user_role()

# Mostrar diferentes relatórios baseados no papel
if user_role == "admin":
    st.success("🔴 Acesso de Administrador - Todos os relatórios disponíveis")
    
    tab1, tab2, tab3 = st.tabs(["📊 Financeiro", "👥 RH", "🔧 Sistema"])
    
    with tab1:
        st.subheader("Relatório Financeiro")
        st.write("- Receitas e despesas")
        st.write("- Margem de lucro")
        st.write("- Fluxo de caixa")
    
    with tab2:
        st.subheader("Relatório de RH")
        st.write("- Funcionários ativos")
        st.write("- Folha de pagamento")
        st.write("- Performance")
    
    with tab3:
        st.subheader("Relatório do Sistema")
        st.write("- Logs de acesso")
        st.write("- Performance do sistema")
        st.write("- Usuários ativos")

elif user_role == "manager":
    st.warning("🟡 Acesso de Gerente - Relatórios limitados")
    
    tab1, tab2 = st.tabs(["📊 Financeiro", "👥 Equipe"])
    
    with tab1:
        st.subheader("Relatório Financeiro (Resumido)")
        st.write("- Receitas do departamento")
        st.write("- Orçamento disponível")
    
    with tab2:
        st.subheader("Relatório da Equipe")
        st.write("- Membros da equipe")
        st.write("- Metas e objetivos")
        st.write("- Performance da equipe")

# Tabela de dados fictícios
st.subheader("Dados de Vendas")

import pandas as pd
import numpy as np

# Gerar dados fictícios
np.random.seed(42)
data = pd.DataFrame({
    'Produto': ['Produto A', 'Produto B', 'Produto C', 'Produto D', 'Produto E'],
    'Vendas': np.random.randint(1000, 10000, 5),
    'Lucro': np.random.randint(100, 1000, 5),
    'Margem (%)': np.random.randint(10, 30, 5)
})

st.dataframe(data, use_container_width=True)

st.info(f"ℹ️ Você está visualizando como: {user_role.title()}")