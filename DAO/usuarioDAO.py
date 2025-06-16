import mysql.connector


class UsuarioDAO:
    def __init__(self):
        self.conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="merlin"
         )
        self.cursor = self.conexao.cursor()

    def criar(self, usuario):
        sql = "INSERT INTO usuario (nome, email, senha, permissao) VALUES (%s, %s, %s, %s)"
        self.cursor.execute(sql, (usuario.nome, usuario.email, usuario.senha, usuario.permissao))
        self.conexao.commit()

    def listar(self):
        self.cursor.execute("SELECT * FROM usuario")
        return self.cursor.fetchall()
    
    def atualizar(self, usuario):
        sql = " UPDATE usuario SET nome = %s, email = %s, senha = %s, permissao = %s WHERE id_usuario = %s "
        self.cursor.execute(sql, (usuario.nome, usuario.email, usuario.senha, usuario.permissao, usuario.id))
        self.conexao.commit()

    def deletar(self, id):
        sql = " DELETE FROM usuario WHERE id_usuario = %s "
        self.cursor.execute(sql, (id,))
        self.conexao.commit()

    def buscar_por_email_senha(self, email, senha):
        sql = "SELECT * FROM usuario WHERE email = %s AND senha = %s"
        self.cursor.execute(sql, (email, senha))
        return self.cursor.fetchone()
    
    def buscar_por_email(self, email):
        sql = "SELECT * FROM usuario WHERE email = %s"
        self.cursor.execute(sql, (email,))
        return self.cursor.fetchone()



        