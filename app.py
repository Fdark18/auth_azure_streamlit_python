import streamlit as st
import msal
import requests
import os
from urllib.parse import urlencode

# Configuração do Azure AD
class MSALConfig:
    def __init__(self):
        self.CLIENT_ID = st.secrets["oauth"]["client_id"]
        self.CLIENT_SECRET = st.secrets["oauth"]["client_secret"]
        self.TENANT_ID = st.secrets["oauth"]["tenant_id"]
        self.AUTHORITY = f"https://login.microsoftonline.com/{self.TENANT_ID}"
        self.REDIRECT_URI ="https://5015d77f4d00.ngrok-free.app"
        self.SCOPE = ["User.Read", "Group.Read.All", "GroupMember.Read.All"]

def init_msal_app():
    config = MSALConfig()
    return msal.ConfidentialClientApplication(
        client_id=config.CLIENT_ID,
        client_credential=config.CLIENT_SECRET,
        authority=config.AUTHORITY
    )

def get_auth_url():
    config = MSALConfig()
    msal_app = init_msal_app()
    
    auth_url = msal_app.get_authorization_request_url(
        scopes=config.SCOPE,
        redirect_uri=config.REDIRECT_URI
    )
    return auth_url

def get_token_from_code(auth_code):
    config = MSALConfig()
    msal_app = init_msal_app()
    
    result = msal_app.acquire_token_by_authorization_code(
        code=auth_code,
        scopes=config.SCOPE,
        redirect_uri=config.REDIRECT_URI
    )
    return result

def make_graph_request(access_token, endpoint):
    """Fazer requisição para Microsoft Graph API com tratamento de erro"""
    try:
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.get(f'https://graph.microsoft.com/v1.0{endpoint}', headers=headers)
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 403:
            st.warning(f"⚠️ Permissão insuficiente para acessar: {endpoint}")
            return None
        else:
            st.error(f"Erro na API: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"Erro ao fazer requisição: {str(e)}")
        return None

def get_user_info(access_token):
    return make_graph_request(access_token, '/me')

def get_user_groups(access_token):
    """Obter grupos do usuário atual"""
    return make_graph_request(access_token, '/me/memberOf')

def get_all_groups(access_token):
    """Obter todos os grupos do Azure AD"""
    return make_graph_request(access_token, '/groups')

def get_group_members(access_token, group_id):
    """Obter membros de um grupo específico"""
    return make_graph_request(access_token, f'/groups/{group_id}/members')

def check_user_permissions(user_groups, user_info):
    """Definir permissões baseadas nos grupos do usuário"""
    permissions = {
        'admin': False,
        'manager': False,
        'user': False,
        'pages_access': []
    }
    
    # Lista de emails de administradores (fallback)
    admin_emails = [
        "@outlook.com",  # Substitua pelo seu email real
        "admin@example.com"
    ]
    
    # Verificar se é admin por email (fallback se não há grupos)
    user_email = user_info.get('userPrincipalName', '').lower()
    if user_email in [email.lower() for email in admin_emails]:
        permissions['admin'] = True
        permissions['pages_access'].extend(['dashboard', 'users', 'reports', 'settings'])
        st.info(f"🔴 Acesso de administrador concedido para: {user_email}")
    
    # Verificar se user_groups é válido
    if not user_groups or not user_groups.get('value'):
        # Se não há grupos mas é admin por email, manter as permissões de admin
        if not permissions['admin']:
            permissions['user'] = True
            permissions['pages_access'] = ['dashboard']
        return permissions
    
    for group in user_groups.get('value', []):
        # Verificar se o grupo tem displayName válido
        display_name = group.get('displayName')
        if not display_name:
            continue
            
        group_name = display_name.lower()
        
        # Definir permissões baseadas no nome do grupo
        if any(word in group_name for word in ['admin', 'administrador', 'administrator']):
            permissions['admin'] = True
            permissions['pages_access'].extend(['dashboard', 'users', 'reports', 'settings'])
        elif any(word in group_name for word in ['manager', 'gerente', 'gestor']):
            permissions['manager'] = True
            permissions['pages_access'].extend(['dashboard', 'reports'])
        elif any(word in group_name for word in ['user', 'usuario', 'usuário']):
            permissions['user'] = True
            permissions['pages_access'].extend(['dashboard'])
    
    # Se nenhuma permissão foi definida e não é admin por email, dar acesso básico
    if not any([permissions['admin'], permissions['manager'], permissions['user']]):
        permissions['user'] = True
        permissions['pages_access'] = ['dashboard']
    
    # Remover duplicatas
    permissions['pages_access'] = list(set(permissions['pages_access']))
    
    return permissions

# Interface Streamlit
def main():
    st.set_page_config(page_title="Login Azure AD", page_icon="🔐", layout="wide")
    
    st.title("🔐 Sistema de Login com Azure AD")
    
    # Verificar se há código de autorização na URL
    if "code" in st.query_params:
        auth_code = st.query_params["code"]
        
        with st.spinner("Autenticando..."):
            token_result = get_token_from_code(auth_code)
            
            if "access_token" in token_result:
                st.session_state["access_token"] = token_result["access_token"]
                st.session_state["authenticated"] = True
                st.rerun()
    
    # Verificar se usuário já está autenticado
    if st.session_state.get("authenticated", False):
        access_token = st.session_state.get("access_token")
        
        # Obter informações do usuário
        user_info = get_user_info(access_token)
        
        if not user_info:
            st.error("❌ Erro ao obter informações do usuário")
            st.session_state.clear()
            st.rerun()
            
        user_groups = get_user_groups(access_token)
        
        # user_groups pode ser None se não há permissão para ler grupos
        if user_groups is None:
            st.warning("⚠️ Não foi possível obter grupos do usuário. Aplicando permissões básicas.")
            user_groups = {'value': []}
        
        # Verificar permissões do usuário
        permissions = check_user_permissions(user_groups, user_info)
        st.session_state["permissions"] = permissions
        st.session_state["user_name"] = user_info.get("displayName", "Usuário")
            
            # Interface com abas
        tab1, tab2, tab3 = st.tabs(["👤 Perfil", "👥 Meus Grupos", "🏢 Gerenciar Grupos"])
            
        with tab1:
                st.subheader("Informações do Usuário")
                
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    st.write("**Nome:**")
                    st.write("**Email:**")
                    st.write("**ID:**")
                    st.write("**Permissões:**")
                
                with col2:
                    st.write(user_info.get("displayName", "N/A"))
                    st.write(user_info.get("userPrincipalName", "N/A"))
                    st.write(user_info.get("id", "N/A"))
                    
                    # Mostrar permissões
                    perm_text = []
                    if permissions['admin']:
                        perm_text.append("🔴 Administrador")
                    if permissions['manager']:
                        perm_text.append("🟡 Gerente")
                    if permissions['user']:
                        perm_text.append("🟢 Usuário")
                    
                    st.write(" | ".join(perm_text) if perm_text else "Sem permissões definidas")
                
                # Debug das permissões
                with st.expander("🔍 Debug - Permissões"):
                    st.json(permissions)
                    st.write(f"**Email do usuário:** {user_info.get('userPrincipalName', 'N/A')}")
                
                # Páginas acessíveis
                if permissions['pages_access']:
                    st.subheader("Páginas Acessíveis")
                    for page in permissions['pages_access']:
                        st.write(f"✅ {page.title()}")
                
                # Botão para forçar permissão de admin (temporário)
                if st.button("🔑 Conceder Acesso Admin (Temporário)"):
                    st.session_state["permissions"]['admin'] = True
                    st.session_state["permissions"]['pages_access'].extend(['dashboard', 'users', 'reports', 'settings'])
                    st.session_state["permissions"]['pages_access'] = list(set(st.session_state["permissions"]['pages_access']))
                    st.success("Permissões de admin concedidas!")
                    st.rerun()
            
        with tab2:
                st.subheader("Meus Grupos")
                
                if user_groups and user_groups.get('value'):
                    for group in user_groups['value']:
                        group_name = group.get('displayName', 'Nome não disponível')
                        with st.expander(f"📁 {group_name}"):
                            st.write(f"**ID:** {group.get('id', 'N/A')}")
                            st.write(f"**Descrição:** {group.get('description', 'Sem descrição')}")
                            st.write(f"**Tipo:** {group.get('@odata.type', 'N/A')}")
                            
                            # Debug - mostrar dados do grupo
                            with st.expander("🔍 Debug - Dados do grupo"):
                                st.json(group)
                else:
                    st.info("Você não pertence a nenhum grupo ou não há permissão para visualizá-los.")
                    
                    # Debug - mostrar resposta completa
                    if user_groups:
                        with st.expander("🔍 Debug - Resposta da API"):
                            st.json(user_groups)
            
        with tab3:
                st.subheader("Gerenciamento de Grupos")
                
                
                    # Obter todos os grupos
                all_groups = get_all_groups(access_token)
                
                if all_groups and all_groups.get('value'):
                    st.write(f"**Total de grupos:** {len(all_groups['value'])}")
                    
                    # Seletor de grupo
                    group_names = [f"{group.get('displayName', 'Sem nome')} ({group.get('id')})" 
                                    for group in all_groups['value']]
                    
                    selected_group = st.selectbox("Selecione um grupo para ver os membros:", 
                                                options=range(len(group_names)),
                                                format_func=lambda x: group_names[x])
                        
                    if st.button("📋 Listar Membros"):
                        group_id = all_groups['value'][selected_group].get('id')
                        group_name = all_groups['value'][selected_group].get('displayName')
                        
                        with st.spinner(f"Carregando membros do grupo {group_name}..."):
                            members = get_group_members(access_token, group_id)
                            
                            if members and members.get('value'):
                                st.write(f"**Membros do grupo '{group_name}':**")
                                
                                # Tabela de membros
                                member_data = []
                                for member in members['value']:
                                    member_data.append({
                                        'Nome': member.get('displayName', 'N/A'),
                                        'Email': member.get('userPrincipalName', 'N/A'),
                                        'Tipo': member.get('@odata.type', 'N/A').replace('#microsoft.graph.', '')
                                    })
                                
                                st.dataframe(member_data, use_container_width=True)
                            else:
                                st.info("Este grupo não possui membros ou você não tem permissão para visualizá-los.")
                    else:
                        st.warning("Não foi possível carregar os grupos.")
                else:
                    st.warning("⚠️ Acesso restrito: Apenas administradores podem visualizar esta seção.")
            
            # Botão de logout
        st.divider()
        if st.button("🚪 Logout", type="secondary"):
                st.session_state.clear()
                st.rerun()
    
    else:
        # Tela de login
        st.write("### Faça login com sua conta Microsoft")
        st.write("Clique no botão abaixo para se autenticar:")
        
        if st.button("🔑 Entrar com Azure AD", type="primary"):
            auth_url = get_auth_url()
            st.link_button("🔑 Clique aqui para fazer login", auth_url)

if __name__ == "__main__":
    main()