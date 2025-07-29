# Sistema de Autenticação Azure AD com Streamlit

Um sistema completo de autenticação e autorização usando Azure Active Directory (AAD) integrado com Streamlit, permitindo controle de acesso baseado em grupos para diferentes páginas da aplicação.

## 📋 Características

- ✅ Autenticação via Azure Active Directory
- ✅ Autorização baseada em grupos do Azure AD
- ✅ Interface web responsiva com Streamlit
- ✅ Controle de acesso granular por páginas
- ✅ Gerenciamento de usuários e grupos
- ✅ Sistema de fallback para administradores
- ✅ Debug integrado para troubleshooting

## 🏗️ Arquitetura

```
streamlit_auth/
├── .streamlit/
│   └── secrets.toml          # Configurações do Azure AD
├── pages/
│   ├── 1_Dashboard.py        # Página acessível a todos
│   ├── 2_Reports.py          # Página para gerentes e admins
│   └── 3_Admin.py            # Página exclusiva para admins
├── app.py                    # Aplicação principal
├── auth_utils.py             # Utilitários de autenticação
├── requirements.txt          # Dependências Python
└── README.md                # Este arquivo
```

## 📦 Pré-requisitos

### Software Necessário
- Python 3.8 ou superior
- Conta Microsoft Azure com privilégios administrativos
- ngrok para exposição HTTPS local

### Conhecimentos Básicos
- Conceitos básicos de Azure Active Directory
- Python e Streamlit
- Autenticação OAuth 2.0

## 🚀 Configuração Completa

### Passo 1: Configuração no Azure Portal

#### 1.1. Registrar Aplicação no Azure AD

1. **Acesse o Azure Portal:**
   - Vá para [portal.azure.com](https://portal.azure.com)
   - Faça login com sua conta administrativa

2. **Navegue para Azure Active Directory:**
   - No menu lateral, clique em "Azure Active Directory"
   - Ou pesquise por "Azure Active Directory" na barra de busca

3. **Registrar Nova Aplicação:**
   - Clique em "App registrations" no menu lateral
   - Clique em "+ New registration"
   - Preencha os campos:
     - **Name:** `Streamlit Auth App`
     - **Supported account types:** "Accounts in this organizational directory only"
     - **Redirect URI:** Deixe em branco por enquanto
   - Clique em "Register"

4. **Copiar Informações da Aplicação:**
   Após o registro, anote as seguintes informações:
   - **Application (client) ID:** ``
   - **Directory (tenant) ID:** ``
   - **Object ID:** ``

#### 1.2. Criar Client Secret

1. **Gerar Segredo:**
   - Na página da aplicação, clique em "Certificates & secrets"
   - Clique em "+ New client secret"
   - **Description:** `Streamlit App Secret`
   - **Expires:** Escolha o período desejado
   - Clique em "Add"

2. **Copiar o Valor do Segredo:**
   - **IMPORTANTE:** Copie o valor imediatamente, não será mostrado novamente
   - **Client Secret Value:** ``
   - **Secret ID:** ``

#### 1.3. Configurar Permissões da API

1. **Adicionar Permissões:**
   - Clique em "API permissions"
   - Clique em "+ Add a permission"
   - Selecione "Microsoft Graph"
   - Escolha "Delegated permissions"

2. **Selecionar Permissões Necessárias:**
   - `User.Read` (já incluída por padrão)
   - `Group.Read.All`
   - `GroupMember.Read.All`

3. **Conceder Consentimento:**
   - Clique em "Grant admin consent for [Sua Organização]"
   - Confirme clicando em "Yes"

### Passo 2: Configuração do Ambiente Local

#### 2.1. Clonar/Baixar o Projeto

```bash
# Criar diretório do projeto
mkdir streamlit_auth
cd streamlit_auth

# Ou clonar se estiver em um repositório
git clone <url-do-repositorio>
cd streamlit_auth
```

#### 2.2. Criar Ambiente Virtual

```bash
# instala as bibliotecas e ativa ambiente virtual com poetry
poetry install

pertry shell

# Criar ambiente virtual sem poetry
python -m venv .venv

# Ativar ambiente virtual
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate
```

#### 2.3. Instalar Dependências se não tiver usando poetry

```bash
# Instalar dependências
pip install -r requirements.txt
```

**Conteúdo do requirements.txt:**
```
streamlit==1.28.0
msal==1.24.0
requests==2.31.0
pandas==2.0.0
numpy==1.24.0
```

#### 2.4. Configurar ngrok

1. **Baixar ngrok:**
   - Vá para [ngrok.com](https://ngrok.com)
   - Crie uma conta gratuita
   - Baixe o ngrok para seu sistema operacional

2. **Configurar ngrok:**
   ```bash
   # Adicionar seu token de autenticação
   ngrok config add-authtoken YOUR_AUTHTOKEN
   
   # Expor porta 8501 (porta padrão do Streamlit)
   ngrok http 8501
   ```

3. **Copiar URL HTTPS:**
   - O ngrok irá gerar uma URL como: `https://abc123.ngrok-free.app`
   - **Anote esta URL** - você precisará dela

#### 2.5. Atualizar Redirect URI no Azure

1. **Voltar ao Azure Portal:**
   - Vá para sua aplicação registrada
   - Clique em "Authentication"
   - Clique em "+ Add a platform"
   - Selecione "Web"

2. **Configurar Redirect URI:**
   - **Redirect URI:** `https://sua-url-ngrok.ngrok-free.app`
   - Marque "ID tokens" se solicitado
   - Clique em "Configure"

### Passo 3: Configuração dos Arquivos

#### 3.1. Criar Arquivo de Secrets

Crie o diretório `.streamlit` e o arquivo `secrets.toml`:

```bash
mkdir .streamlit
```

**Arquivo: .streamlit/secrets.toml**
```toml
[oauth]
client_id = ""
client_secret = ""
tenant_id = ""
redirect_uri = "https://sua-url-ngrok.ngrok-free.app"
```

> ⚠️ **IMPORTANTE:** Substitua `sua-url-ngrok.ngrok-free.app` pela URL real do seu ngrok

#### 3.2. Configurar Administradores

No arquivo `app.py`, localize a função `check_user_permissions` e atualize a lista de emails de administradores:

```python
# Lista de emails de administradores (fallback)
admin_emails = [
    "seu.email@empresa.com",  # Substitua pelo seu email real
    "admin@empresa.com"
]
```

### Passo 4: Configurar Grupos no Azure AD (Opcional)

#### 4.1. Criar Grupos

1. **No Azure Portal:**
   - Vá para "Azure Active Directory" > "Groups"
   - Clique em "+ New group"

2. **Criar Grupos Sugeridos:**
   - **Administradores**
     - Group type: Security
     - Group name: Administradores
     - Description: Grupo de administradores do sistema
   
   - **Gerentes**
     - Group type: Security  
     - Group name: Gerentes
     - Description: Grupo de gerentes
   
   - **Usuários**
     - Group type: Security
     - Group name: Usuários
     - Description: Grupo de usuários padrão

#### 4.2. Adicionar Membros aos Grupos

1. **Para cada grupo criado:**
   - Clique no grupo
   - Vá em "Members"
   - Clique em "+ Add members"
   - Pesquise e adicione os usuários apropriados

## 🎯 Execução da Aplicação

### Passo 1: Iniciar ngrok

```bash
# Terminal 1 - Manter rodando
ngrok http 8501
```

### Passo 2: Executar Streamlit

```bash
# Terminal 2 - Na pasta do projeto
streamlit run app.py
```

### Passo 3: Acessar a Aplicação

1. **Abrir navegador:** `http://localhost:8501`
2. **Fazer login:** Clicar em "Entrar com Azure AD"
3. **Autenticar:** Usar suas credenciais do Azure AD
4. **Explorar:** Navegar pelas diferentes páginas baseado nas suas permissões

## 🔒 Sistema de Permissões

### Níveis de Acesso

| Papel | Páginas Acessíveis | Critério de Acesso |
|-------|-------------------|-------------------|
| **Usuário** | Dashboard | Qualquer usuário autenticado |
| **Gerente** | Dashboard, Relatórios | Membro de grupo com "gerente" no nome |
| **Admin** | Todas as páginas | Membro de grupo com "admin" no nome OU email na lista hardcoded |

### Estrutura das Páginas

1. **Dashboard (1_Dashboard.py)**
   - Acessível a todos os usuários autenticados
   - Métricas básicas e gráficos

2. **Relatórios (2_Reports.py)**
   - Restrito a gerentes e administradores
   - Relatórios financeiros e operacionais

3. **Administração (3_Admin.py)**
   - Exclusivo para administradores
   - Gerenciamento de usuários e sistema

## 🛠️ Troubleshooting

### Problemas Comuns

#### Erro: "StreamlitSecretNotFoundError"
```bash
# Solução: Verificar arquivo secrets.toml
# 1. Confirmar que o arquivo existe em .streamlit/secrets.toml
# 2. Verificar sintaxe TOML (aspas duplas, sem caracteres especiais)
# 3. Confirmar permissões de leitura do arquivo
```

#### Erro: "Acesso restrito: Apenas administradores"
```python
# Soluções:
# 1. Adicionar seu email na lista admin_emails em app.py
# 2. Criar grupo "Administradores" no Azure AD e se adicionar
# 3. Usar o botão "Conceder Acesso Admin (Temporário)" na aba Perfil
```

#### Erro: "Permissão insuficiente para acessar"
```bash
# Solução: Verificar permissões da API no Azure
# 1. Azure Portal > App registrations > Sua app
# 2. API permissions > Verificar se Group.Read.All está presente
# 3. Grant admin consent se necessário
```

#### ngrok URL mudou
```bash
# Solução: Atualizar URLs
# 1. Copiar nova URL do ngrok
# 2. Atualizar .streamlit/secrets.toml
# 3. Atualizar Redirect URI no Azure Portal
# 4. Reiniciar aplicação Streamlit
```

### Debug Integrado

A aplicação inclui seções de debug que ajudam a identificar problemas:

1. **Aba "Perfil" > "Debug - Permissões"**: Mostra permissões calculadas
2. **Aba "Meus Grupos" > "Debug - Dados do grupo"**: Estrutura dos grupos
3. **Aba "Meus Grupos" > "Debug - Resposta da API"**: Response completo da API

## 🔧 Personalização

### Adicionar Novos Níveis de Permissão

1. **Modificar `check_user_permissions()` em app.py:**
```python
# Adicionar novo papel
permissions = {
    'admin': False,
    'manager': False,
    'supervisor': False,  # Novo papel
    'user': False,
    'pages_access': []
}

# Adicionar lógica de detecção
elif 'supervisor' in group_name:
    permissions['supervisor'] = True
    permissions['pages_access'].extend(['dashboard', 'reports'])
```

2. **Atualizar `auth_utils.py`:**
```python
def require_supervisor_or_above():
    """Verificar se o usuário é supervisor ou superior"""
    require_auth()
    
    permissions = st.session_state.get("permissions", {})
    if not (permissions.get("admin", False) or 
            permissions.get("manager", False) or 
            permissions.get("supervisor", False)):
        st.error("🟡 Acesso restrito: Supervisores ou superiores apenas.")
        st.stop()
```

### Adicionar Nova Página

1. **Criar arquivo em `pages/`:**
```python
# pages/4_Nova_Pagina.py
import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from auth_utils import require_permission, show_user_info

require_permission("nova_pagina")  # Definir permissão necessária

st.set_page_config(page_title="Nova Página", page_icon="🆕")
show_user_info()

st.title("🆕 Nova Página")
# Seu conteúdo aqui
```

2. **Atualizar sistema de permissões:**
```python
# Em check_user_permissions(), adicionar nova página às permissões apropriadas
permissions['pages_access'].extend(['dashboard', 'nova_pagina'])
```

## 📚 Estrutura do Código

### Principais Arquivos

- **`app.py`**: Aplicação principal com login e interface
- **`auth_utils.py`**: Funções auxiliares de autenticação
- **`pages/`**: Páginas com controle de acesso individual

### Principais Funções

- **`MSALConfig`**: Configuração centralizada do Azure AD
- **`check_user_permissions()`**: Lógica de determinação de permissões
- **`make_graph_request()`**: Interface com Microsoft Graph API
- **`require_auth()`**: Middleware de autenticação para páginas

## 🛡️ Segurança

### Boas Práticas Implementadas

- ✅ Secrets em arquivo separado (não versionado)
- ✅ Tokens de acesso mantidos apenas na sessão
- ✅ Verificação de permissões em cada página
- ✅ Fallback de administradores por email
- ✅ Tratamento de erros da API
- ✅ Logs de debug para auditoria

### Recomendações Adicionais

- 🔒 Use HTTPS em produção (não apenas ngrok)
- 🔄 Implemente rotação de client secrets
- 📝 Configure logs de auditoria
- 🚫 Remova botões de debug em produção
- 🔐 Use Azure Key Vault para secrets em produção

## 🚀 Deploy em Produção

### Streamlit Cloud

1. **Preparar repositório:**
```bash
# Remover .streamlit/secrets.toml do git
echo ".streamlit/secrets.toml" >> .gitignore
git add .
git commit -m "Initial commit"
git push origin main
```

2. **Configurar no Streamlit Cloud:**
- Vá para [streamlit.io](https://streamlit.io)
- Conecte seu repositório GitHub
- Configure as secrets nas configurações da app
- Deploy automático

### Azure App Service

1. **Criar App Service no Azure**
2. **Configurar variáveis de ambiente**
3. **Deploy via GitHub Actions ou Azure DevOps**

## 📞 Suporte

### Recursos Úteis

- [Documentação Azure AD](https://docs.microsoft.com/azure/active-directory/)
- [Microsoft Graph API](https://docs.microsoft.com/graph/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [MSAL Python](https://msal-python.readthedocs.io/)

### Logs e Monitoring

Para troubleshooting avançado, monitore:
- Logs do Streamlit no terminal
- Network tab do navegador para requisições
- Azure AD sign-in logs no portal
- Seções de debug na aplicação

---

**Criado por:** Jhonatan Novais  
**Versão:** 1.0  
**Data:** Julho 2025  
