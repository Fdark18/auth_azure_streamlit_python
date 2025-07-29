import streamlit as st

def require_auth():
    """Verificar se o usuário está autenticado"""
    if not st.session_state.get("authenticated", False):
        st.error("🔒 Acesso negado. Faça login primeiro.")
        st.stop()

def require_permission(required_page):
    """Verificar se o usuário tem permissão para acessar a página"""
    require_auth()
    
    permissions = st.session_state.get("permissions", {})
    pages_access = permissions.get("pages_access", [])
    
    if required_page not in pages_access:
        st.error(f"⚠️ Acesso negado. Você não tem permissão para acessar a página '{required_page}'.")
        st.info("Páginas disponíveis para você:")
        for page in pages_access:
            st.write(f"✅ {page.title()}")
        st.stop()

def require_admin():
    """Verificar se o usuário é administrador"""
    require_auth()
    
    permissions = st.session_state.get("permissions", {})
    if not permissions.get("admin", False):
        st.error("🔴 Acesso restrito: Apenas administradores podem acessar esta página.")
        st.stop()

def require_manager_or_admin():
    """Verificar se o usuário é gerente ou administrador"""
    require_auth()
    
    permissions = st.session_state.get("permissions", {})
    if not (permissions.get("admin", False) or permissions.get("manager", False)):
        st.error("🟡 Acesso restrito: Apenas gerentes ou administradores podem acessar esta página.")
        st.stop()

def get_user_role():
    """Obter o papel do usuário"""
    permissions = st.session_state.get("permissions", {})
    
    if permissions.get("admin", False):
        return "admin"
    elif permissions.get("manager", False):
        return "manager"
    elif permissions.get("user", False):
        return "user"
    else:
        return "guest"

def show_user_info():
    """Mostrar informações básicas do usuário logado"""
    if st.session_state.get("authenticated", False):
        user_name = st.session_state.get("user_name", "Usuário")
        user_role = get_user_role()
        
        st.sidebar.success(f"👤 Logado como: {user_name}")
        st.sidebar.info(f"🏷️ Papel: {user_role.title()}")
        
        if st.sidebar.button("🚪 Logout"):
            st.session_state.clear()
            st.rerun()