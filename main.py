import time
import streamlit as st
from usuario import Usuario 
from DAO.usuarioDAO import UsuarioDAO
from video import Video
from DAO.videoDAO import VideoDAO


st.set_page_config(
    page_title="Merlin Learn to Code",
    page_icon="🧙‍♂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

if "usuario_logado" not in st.session_state:
    st.session_state.usuario_logado = None
if "permissao" not in st.session_state:
    st.session_state.permissao = None

st.sidebar.title("🧙‍♂️ Merlin Learn to code!")


opcoes_menu = []

if not st.session_state.usuario_logado:
    opcoes_menu = ["Entrar", "Cadastrar"]
else:
    opcoes_menu = ["Tela inicial"]
    if st.session_state.permissao == "admin":
        opcoes_menu += ["Gerenciar Usuários", "Gerenciar Videos"]
    opcoes_menu.append("Sair")

opcao = st.sidebar.selectbox(
    "Selecione uma opção",
    options=opcoes_menu
)

# tela de usuarios

if opcao == "Entrar":
    st.title("🔐 Entrar")
    with st.form("form_login"):
        input_email = st.text_input(label="Digite o seu email")
        input_senha = st.text_input(label="Digite a sua senha", type="password")
        input_button = st.form_submit_button(label="Entrar")

    if input_button:
        usuario_dao = UsuarioDAO()
        usuario = usuario_dao.buscar_por_email(input_email)

        if usuario and usuario[3] == input_senha:
            st.session_state.usuario_logado = usuario[1]
            st.session_state.permissao = usuario[4]
            st.success(f"Bem-vindo, {usuario[1]}!")
            time.sleep(2)
            st.rerun()
        else:
            st.error("Email ou senha incorretos!")

if opcao == "Sair":
    st.session_state.usuario_logado = None
    st.session_state.permissao = None
    st.success("Você saiu com sucesso!")
    st.rerun()

if opcao == "Cadastrar":
    st.title("📝 Cadastrar")
    with st.form("form_usuario"):
            input_nome = st.text_input(label="Digite o seu nome")
            input_email = st.text_input(label="Digite o seu email")
            input_senha = st.text_input(label="Digite a sua senha", type="password")
            input_confirmar_senha = st.text_input(label="Confirme a sua senha", type="password")
            input_button = st.form_submit_button(label="Cadastrar")

    if input_button:
        if input_senha != input_confirmar_senha:
            st.error("As senhas não coincidem!")
        else:
            usuario = Usuario(nome=input_nome, email=input_email, senha=input_senha)
            usuario_dao = UsuarioDAO()
            usuario_dao.criar(usuario)
            st.success("Usuário cadastrado com sucesso!")

if opcao == "Tela inicial":
    if st.session_state.usuario_logado:
        st.title(f"🏠 Home - Vídeos Disponíveis")
        video_dao = VideoDAO()
        categorias = video_dao.listar_categorias()
        opcoes_categoria = ["Todas"] + [categoria[1] for categoria in categorias]
        categoria_escolhida = st.selectbox("Filtrar por categoria", options=opcoes_categoria)
        videos_tuplas = video_dao.listar()
        videos = []
        for v in videos_tuplas:
            videos.append({
                "id": v[0],
                "titulo": v[1],
                "descricao": v[2],
                "id_categoria": v[3],
                "url": v[4],
            })
        
        if categoria_escolhida != "Todas":
            id_categoria_filtrada = next((categoria[0] for categoria in categorias if categoria[1] == categoria_escolhida), None)
            videos = [video for video in videos if video["id_categoria"] == id_categoria_filtrada]

        if videos:
            st.subheader("📚 Biblioteca de Vídeos")

            buscar_nome_categorias = {categoria[0]: categoria[1] for categoria in categorias}

            for video in videos:
                with st.expander(f"🎥 {video['titulo']}"):
                    st.write(f"**Descrição:** {video['descricao']}")
                    nome_categoria = buscar_nome_categorias.get(video['id_categoria'], "Categoria Desconhecida")
                    st.write(f"**Categoria:** {nome_categoria}")

                    if 'youtube.com/watch' in video['url'] or 'youtu.be/' in video['url']:
                        st.video(video['url'])
                    else:
                        st.write(f"**Link do vídeo:** {video['url']}")
                        st.markdown(f"[Assistir vídeo]({video['url']})")
        else:
            st.info("Nenhum vídeo disponível no momento.")

if opcao == "Gerenciar Usuários":
    st.title("👥 Gerenciar Usuários")
    aba1, aba2 = st.tabs(["Cadastrar Usuário", "Lista de Usuários"])

    with aba1:

        with st.form("form_usuario"):
            input_nome = st.text_input(label="Digite o nome")
            input_email = st.text_input(label="Digite o email")
            input_senha = st.text_input(label="Digite a senha", type="password")
            input_confirmar_senha = st.text_input(label="Confirme a senha", type="password")
            input_occupation = st.selectbox(
                "Selecione o tipo de usuário",
                options = ["padrao", "admin"],
                format_func=lambda x: "Administrador" if x == "admin" else "Padrão"
                )
            input_button = st.form_submit_button(label="Cadastrar")

        if input_button:
            if input_senha != input_confirmar_senha:
                st.error("As senhas não coincidem!")
            else:
                usuario = Usuario(nome=input_nome, email=input_email, senha=input_senha, permissao=input_occupation)
                usuario_dao = UsuarioDAO()
                usuario_dao.criar(usuario)
                st.success("Usuário cadastrado com sucesso!")

    with aba2:
        usuario_dao = UsuarioDAO()
        usuarios = usuario_dao.listar()
        if usuarios:
            for usuario in usuarios:
                id_usuario, nome, email, senha, permissao, assinatura = usuario

                with st.expander(f"👤 {nome} | 📧 {email}"):
                    novo_nome = st.text_input("Novo nome", value=nome, key=f"nome_{id_usuario}")
                    novo_email = st.text_input("Novo email", value=email, key=f"email_{id_usuario}")
                    novo_senha = st.text_input("Nova senha", type="password", key=f"senha_{id_usuario}")
                    nova_permissao = st.selectbox(
                        "Selecione o tipo de usuário",
                        options = ["padrao", "admin"],
                        format_func=lambda x: "Administrador" if x == "admin" else "Padrão",
                        key=f"permissao_{id_usuario}"
                    )

                    col1, col2 = st.columns(2)

                    with col1:
                        if st.button("Salvar", key=f"salvar_{id_usuario}"):
                            senha = novo_senha if novo_senha else senha  # Mantém a senha antiga se não for alterada
                            usuario_atualizado = Usuario(id=id_usuario, nome=novo_nome, email=novo_email, senha=senha, permissao=nova_permissao)
                            usuario_dao.atualizar(usuario_atualizado)
                            st.success("Usuário atualizado com sucesso!")
                            st.rerun()

                    with col2:
                        if st.button("Deletar", key=f"deletar_{id_usuario}"):
                            usuario_dao.deletar(id_usuario)
                            st.success("Usuário deletado com sucesso!")
                            st.rerun()
                                    
        else:
            st.warning("Nenhum usuário cadastrado.")

if opcao == "Gerenciar Videos":
    video_dao = VideoDAO()
    st.title("🎥 Gerenciar Videos")
    aba1, aba2 = st.tabs(["Cadastrar video", "Lista de videos"])

    with aba1:

        with st.form("form_video"):
            input_titulo = st.text_input(label="Digite o titulo do video")
            input_descricao = st.text_input(label="Digite a descrição do video")
            input_url = st.text_input(label="Digite a URL do video")

            categorias = video_dao.listar_categorias()
            nomes_categorias = [categoria[1] for categoria in categorias]
            nome_categoria_escolhida = st.selectbox(
                "Selecione a categoria do video",
                options=nomes_categorias,
                format_func=lambda x: x if x else "Nenhuma categoria"
            )
            input_button = st.form_submit_button(label="Cadastrar")

        if input_button:
                id_categoria_escolhida = next((categoria[0] for categoria in categorias if categoria[1] == nome_categoria_escolhida), None)
                video = Video(titulo=input_titulo, descricao=input_descricao, url=input_url, id_categoria=id_categoria_escolhida)
                video_dao = VideoDAO()
                video_dao.criar(video)
                st.success("Video cadastrado com sucesso!")

    with aba2:
        video_dao = VideoDAO()
        categorias = video_dao.listar_categorias()
        videos = video_dao.listar()
        if videos:
            for video in videos:
                id_videoaula, titulo, descricao, id_categoria, url_video = video

                with st.expander(f"🎬 {titulo} | 📝 {descricao}"):
                    novo_titulo = st.text_input("Novo titulo", value=titulo, key=f"titulo_{id_videoaula}")
                    novo_descricao = st.text_input("Nova descrição", value=descricao, key=f"descricao_{id_videoaula}")
                    novo_url = st.text_input("Nova url", value=url_video, key=f"url_video_{id_videoaula}")

                    nomes_categorias = [c[1] for c in categorias]
                    categoria_atual = next((categoria[1] for categoria in categorias if categoria[0] == id_categoria), None)
                    nome_categoria_nova = st.selectbox(
                        "Categoria do vídeo",
                        options=nomes_categorias,
                        index=nomes_categorias.index(categoria_atual) if categoria_atual in nomes_categorias else 0,
                        key=f"categoria_{id_videoaula}"
                    )
                    id_categoria_nova = next((categoria[0] for categoria in categorias if categoria[1] == nome_categoria_nova), None)
                   

                    col1, col2 = st.columns(2)

                    with col1:
                        if st.button("Salvar", key=f"salvar_{id_videoaula}"):
                            video_atualizado = Video(id=id_videoaula, titulo=novo_titulo, descricao=novo_descricao, url=novo_url, id_categoria=id_categoria_nova)
                            video_dao.atualizar(video_atualizado)
                            st.success("Video atualizado com sucesso!")
                            st.rerun()

                    with col2:
                        if st.button("Deletar", key=f"deletar_{id_videoaula}"):
                            video_dao.deletar(id_videoaula)
                            st.success("Video deletado com sucesso!")
                            st.rerun()
                                    
        else:
            st.warning("Nenhum video cadastrado.")   