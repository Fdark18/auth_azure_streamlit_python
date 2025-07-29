import streamlit as st
import sys
import os

# Adicionar o diretório pai ao path para importar auth_utils
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from auth_utils import require_admin, show_user_info

# Verificar permissões (apenas admins)
require_admin()

# Interface da página
st.set_page_config(page_title="Administração", page_icon="⚙️")
show_user_info()

st.title("⚙️ Painel de Administração")
st.write("Esta página é exclusiva para administradores do sistema.")

st.error("🔴 ÁREA RESTRITA - APENAS ADMINISTRADORES")

# Seções de administração
tab1, tab2, tab3, tab4 = st.tabs(["👥 Usuários", "🏢 Grupos", "🔧 Sistema", "📊 Logs"])

with tab1:
    st.subheader("Gerenciamento de Usuários")
    
    st.write("**Ações disponíveis:**")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("➕ Adicionar Usuário"):
            st.success("Funcionalidade: Adicionar novo usuário")
    
    with col2:
        if st.button("✏️ Editar Usuário"):
            st.success("Funcionalidade: Editar usuário existente")
    
    with col3:
        if st.button("🗑️ Remover Usuário"):
            st.error("Funcionalidade: Remover usuário")
    
    # Lista fictícia de usuários
    st.write("**Usuários Registrados:**")
    import pandas as pd
    
    users_data = pd.DataFrame({
        'Nome': ['João Silva', 'Maria Santos', 'Pedro Oliveira'],
        'Email': ['joao@empresa.com', 'maria@empresa.com', 'pedro@empresa.com'],
        'Grupo': ['Administradores', 'Gerentes', 'Usuários'],
        'Status': ['Ativo', 'Ativo', 'Inativo']
    })
    
    st.dataframe(users_data, use_container_width=True)

with tab2:
    st.subheader("Gerenciamento de Grupos")
    
    st.write("**Grupos do Azure AD:**")
    
    # Verificar se há dados de grupos na sessão
    if st.session_state.get("all_groups_data"):
        groups_data = st.session_state["all_groups_data"]
        st.dataframe(groups_data, use_container_width=True)
    else:
        st.info("Dados dos grupos serão carregados após login completo.")
    
    st.write("**Ações de Grupo:**")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 Sincronizar Grupos"):
            st.success("Grupos sincronizados com Azure AD")
    
    with col2:
        if st.button("📋 Exportar Lista"):
            st.success("Lista exportada com sucesso")

with tab3:
    st.subheader("Configurações do Sistema")
    
    st.write("**Configurações de Segurança:**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.checkbox("Autenticação obrigatória", value=True)
        st.checkbox("Log de auditoria", value=True)
        st.checkbox("Backup automático", value=False)
    
    with col2:
        st.selectbox("Nível de log", ["Básico", "Detalhado", "Debug"])
        st.number_input("Timeout de sessão (min)", min_value=5, max_value=120, value=30)
    
    if st.button("💾 Salvar Configurações"):
        st.success("Configurações salvas com sucesso!")

with tab4:
    st.subheader("Logs do Sistema")
    
    st.write("**Logs Recentes:**")
    
    # Logs fictícios
    import datetime
    
    logs_data = pd.DataFrame({
        'Timestamp': [
            datetime.datetime.now() - datetime.timedelta(minutes=5),
            datetime.datetime.now() - datetime.timedelta(minutes=15),
            datetime.datetime.now() - datetime.timedelta(hours=1),
        ],
        'Usuário': ['joao@empresa.com', 'maria@empresa.com', 'pedro@empresa.com'],
        'Ação': ['Login', 'Acesso Relatórios', 'Logout'],
        'Status': ['Sucesso', 'Sucesso', 'Sucesso']
    })
    
    st.dataframe(logs_data, use_container_width=True)
    
    if st.button("📥 Baixar Logs Completos"):
        st.success("Logs baixados com sucesso!")

st.divider()
st.warning("⚠️ Esta é uma área sensível do sistema. Todas as ações são registradas em log.")
st.info("ℹ️ Para funcionalidades completas, integre com APIs específicas do Azure AD e seu sistema de backend.")