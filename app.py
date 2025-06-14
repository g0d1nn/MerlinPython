import streamlit as st
import hashlib
from usuario import Usuario
from usuarioDAO import UsuarioDAO
from video import Video
from videoDAO import VideoDAO
import pandas as pd

# Configuração da página
st.set_page_config(
    page_title="Sistema Merlin",
    page_icon="🧙‍♂️",
    layout="wide"
)

# Função para hash da senha
def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

# Função para verificar se o usuário está logado
def verificar_login():
    return 'usuario_logado' in st.session_state and st.session_state.usuario_logado is not None

# Função para fazer logout
def fazer_logout():
    st.session_state.usuario_logado = None
    st.rerun()

# Função de login
def tela_login():
    st.title("🔐 Login")
    
    with st.form("login_form"):
        email = st.text_input("Email")
        senha = st.text_input("Senha", type="password")
        submit = st.form_submit_button("Entrar")
        
        if submit:
            if email and senha:
                usuario_dao = UsuarioDAO()
                usuario = usuario_dao.buscar_por_email(email)
                
                if usuario and usuario.senha == hash_senha(senha):
                    st.session_state.usuario_logado = usuario
                    st.success("Login realizado com sucesso!")
                    st.rerun()
                else:
                    st.error("Email ou senha incorretos!")
            else:
                st.error("Preencha todos os campos!")

# Função de cadastro
def tela_cadastro():
    st.title("📝 Cadastro de Usuário")
    
    with st.form("cadastro_form"):
        nome = st.text_input("Nome completo")
        email = st.text_input("Email")
        senha = st.text_input("Senha", type="password")
        confirmar_senha = st.text_input("Confirmar senha", type="password")
        
        # Só permite escolher permissão se for admin
        if verificar_login() and st.session_state.usuario_logado.permissao == "admin":
            permissao = st.selectbox("Permissão", ["padrao", "admin"])
        else:
            permissao = "padrao"
        
        submit = st.form_submit_button("Cadastrar")
        
        if submit:
            if nome and email and senha and confirmar_senha:
                if senha == confirmar_senha:
                    usuario_dao = UsuarioDAO()
                    
                    # Verificar se email já existe
                    if usuario_dao.buscar_por_email(email):
                        st.error("Este email já está cadastrado!")
                    else:
                        novo_usuario = Usuario(
                            nome=nome,
                            email=email,
                            senha=hash_senha(senha),
                            permissao=permissao
                        )
                        
                        try:
                            usuario_dao.criar(novo_usuario)
                            st.success("Usuário cadastrado com sucesso!")
                        except Exception as e:
                            st.error(f"Erro ao cadastrar usuário: {str(e)}")
                else:
                    st.error("As senhas não coincidem!")
            else:
                st.error("Preencha todos os campos!")

# Função para gerenciar usuários (apenas admin)
def gerenciar_usuarios():
    st.title("👥 Gerenciar Usuários")
    
    if not verificar_login() or st.session_state.usuario_logado.permissao != "admin":
        st.error("Acesso negado! Apenas administradores podem acessar esta página.")
        return
    
    usuario_dao = UsuarioDAO()
    
    # Tabs para diferentes ações
    tab1, tab2, tab3 = st.tabs(["Listar Usuários", "Editar Usuário", "Excluir Usuário"])
    
    with tab1:
        st.subheader("Lista de Usuários")
        usuarios = usuario_dao.listar()
        
        if usuarios:
            df = pd.DataFrame(usuarios)
            if 'senha' in df.columns:
                df = df.drop('senha', axis=1)  # Não mostrar senhas
            st.dataframe(df, use_container_width=True)
        else:
            st.info("Nenhum usuário cadastrado.")
    
    with tab2:
        st.subheader("Editar Usuário")
        usuarios = usuario_dao.listar()
        
        if usuarios:
            # Selectbox para escolher usuário
            opcoes_usuarios = {f"{u['nome']} ({u['email']})": u['id'] for u in usuarios}
            usuario_selecionado = st.selectbox("Selecionar usuário", list(opcoes_usuarios.keys()))
            
            if usuario_selecionado:
                user_id = opcoes_usuarios[usuario_selecionado]
                usuario_atual = next(u for u in usuarios if u['id'] == user_id)
                
                with st.form("editar_usuario_form"):
                    novo_nome = st.text_input("Nome", value=usuario_atual['nome'])
                    novo_email = st.text_input("Email", value=usuario_atual['email'])
                    nova_permissao = st.selectbox("Permissão", ["padrao", "admin"], 
                                                index=0 if usuario_atual['permissao'] == "padrao" else 1)
                    
                    submit = st.form_submit_button("Atualizar")
                    
                    if submit:
                        usuario_editado = Usuario(
                            id=user_id,
                            nome=novo_nome,
                            email=novo_email,
                            senha=usuario_atual['senha'],  # Manter senha atual
                            permissao=nova_permissao
                        )
                        
                        try:
                            usuario_dao.atualizar(usuario_editado)
                            st.success("Usuário atualizado com sucesso!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Erro ao atualizar usuário: {str(e)}")
        else:
            st.info("Nenhum usuário cadastrado.")
    
    with tab3:
        st.subheader("Excluir Usuário")
        usuarios = usuario_dao.listar()
        
        if usuarios:
            opcoes_usuarios = {f"{u['nome']} ({u['email']})": u['id'] for u in usuarios}
            usuario_selecionado = st.selectbox("Selecionar usuário para excluir", list(opcoes_usuarios.keys()))
            
            if usuario_selecionado:
                st.warning("⚠️ Esta ação não pode ser desfeita!")
                
                if st.button("Confirmar Exclusão", type="primary"):
                    user_id = opcoes_usuarios[usuario_selecionado]
                    
                    try:
                        usuario_dao.deletar(user_id)
                        st.success("Usuário excluído com sucesso!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Erro ao excluir usuário: {str(e)}")
        else:
            st.info("Nenhum usuário cadastrado.")

# Função para home - visualizar vídeos (usuários padrão)
def home_videos():
    st.title("🏠 Home - Vídeos Disponíveis")
    
    if not verificar_login():
        st.error("Faça login para acessar esta página.")
        return
    
    video_dao = VideoDAO()
    videos = video_dao.listar()
    
    if videos:
        st.subheader("📚 Biblioteca de Vídeos")
        
        # Mostrar vídeos em cards
        for video in videos:
            with st.expander(f"🎥 {video['titulo']}"):
                st.write(f"**Descrição:** {video['descricao']}")
                
                # Se a URL for do YouTube, embed o vídeo
                if 'youtube.com/watch' in video['url'] or 'youtu.be/' in video['url']:
                    st.video(video['url'])
                else:
                    st.write(f"**Link do vídeo:** {video['url']}")
                    st.markdown(f"[Assistir vídeo]({video['url']})")
    else:
        st.info("Nenhum vídeo disponível no momento.")

# Função para gerenciar vídeos (apenas admin)
def gerenciar_videos():
    st.title("🎥 Gerenciar Vídeos")
    
    if not verificar_login():
        st.error("Faça login para acessar esta página.")
        return
    
    if st.session_state.usuario_logado.permissao != "admin":
        st.error("Acesso negado! Apenas administradores podem gerenciar vídeos.")
        return
    
    video_dao = VideoDAO()
    
    # Tabs para diferentes ações
    tab1, tab2, tab3, tab4 = st.tabs(["Listar Vídeos", "Adicionar Vídeo", "Editar Vídeo", "Excluir Vídeo"])
    
    with tab1:
        st.subheader("Lista de Vídeos")
        videos = video_dao.listar()
        
        if videos:
            df = pd.DataFrame(videos)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("Nenhum vídeo cadastrado.")
    
    with tab2:
        st.subheader("Adicionar Novo Vídeo")
        
        with st.form("adicionar_video_form"):
            titulo = st.text_input("Título do vídeo")
            descricao = st.text_area("Descrição")
            url = st.text_input("URL do vídeo")
            
            submit = st.form_submit_button("Adicionar Vídeo")
            
            if submit:
                if titulo and descricao and url:
                    novo_video = Video(
                        titulo=titulo,
                        descricao=descricao,
                        url=url
                    )
                    
                    try:
                        video_dao.criar(novo_video)
                        st.success("Vídeo adicionado com sucesso!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Erro ao adicionar vídeo: {str(e)}")
                else:
                    st.error("Preencha todos os campos!")
    
    with tab3:
        st.subheader("Editar Vídeo")
        videos = video_dao.listar()
        
        if videos:
            opcoes_videos = {f"{v['titulo']}": v['id'] for v in videos}
            video_selecionado = st.selectbox("Selecionar vídeo", list(opcoes_videos.keys()))
            
            if video_selecionado:
                video_id = opcoes_videos[video_selecionado]
                video_atual = next(v for v in videos if v['id'] == video_id)
                
                with st.form("editar_video_form"):
                    novo_titulo = st.text_input("Título", value=video_atual['titulo'])
                    nova_descricao = st.text_area("Descrição", value=video_atual['descricao'])
                    nova_url = st.text_input("URL", value=video_atual['url'])
                    
                    submit = st.form_submit_button("Atualizar")
                    
                    if submit:
                        video_editado = Video(
                            id=video_id,
                            titulo=novo_titulo,
                            descricao=nova_descricao,
                            url=nova_url
                        )
                        
                        try:
                            video_dao.atualizar(video_editado)
                            st.success("Vídeo atualizado com sucesso!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Erro ao atualizar vídeo: {str(e)}")
        else:
            st.info("Nenhum vídeo cadastrado.")
    
    with tab4:
        st.subheader("Excluir Vídeo")
        videos = video_dao.listar()
        
        if videos:
            opcoes_videos = {f"{v['titulo']}": v['id'] for v in videos}
            video_selecionado = st.selectbox("Selecionar vídeo para excluir", list(opcoes_videos.keys()))
            
            if video_selecionado:
                st.warning("⚠️ Esta ação não pode ser desfeita!")
                
                if st.button("Confirmar Exclusão", type="primary"):
                    video_id = opcoes_videos[video_selecionado]
                    
                    try:
                        video_dao.deletar(video_id)
                        st.success("Vídeo excluído com sucesso!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Erro ao excluir vídeo: {str(e)}")
        else:
            st.info("Nenhum vídeo cadastrado.")

# Função principal
def main():
    # Inicializar session state
    if 'usuario_logado' not in st.session_state:
        st.session_state.usuario_logado = None
    
    # Sidebar para navegação
    with st.sidebar:
        st.title("🧙‍♂️ Sistema Merlin")
        
        if verificar_login():
            st.success(f"Bem-vindo, {st.session_state.usuario_logado.nome}!")
            st.write(f"Permissão: {st.session_state.usuario_logado.permissao}")
            
            # Menu de navegação baseado na permissão
            if st.session_state.usuario_logado.permissao == "admin":
                menu_options = ["Home", "Gerenciar Vídeos", "Gerenciar Usuários", "Cadastrar Usuário"]
            else:
                menu_options = ["Home"]
            
            menu_choice = st.selectbox("Navegar para:", menu_options)
            
            if st.button("Logout"):
                fazer_logout()
                
        else:
            menu_choice = st.selectbox("Escolha uma opção:", ["Login", "Cadastro"])
    
    # Renderizar a página escolhida
    if not verificar_login():
        if menu_choice == "Login":
            tela_login()
        elif menu_choice == "Cadastro":
            tela_cadastro()
    else:
        if menu_choice == "Home":
            home_videos()
        elif menu_choice == "Gerenciar Vídeos":
            gerenciar_videos()
        elif menu_choice == "Gerenciar Usuários":
            gerenciar_usuarios()
        elif menu_choice == "Cadastrar Usuário":
            tela_cadastro()

if __name__ == "__main__":
    main()