import mysql.connector

class VideoDAO:
    def __init__(self):
        self.conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="merlin"
         )
        self.cursor = self.conexao.cursor()

    def criar(self, video):
        sql = "INSERT INTO videoaula (titulo, descricao, id_categoria, url_video) VALUES (%s, %s, %s, %s)"
        self.cursor.execute(sql, (video.titulo, video.descricao, video.id_categoria, video.url))
        self.conexao.commit()

    def listar(self):
        self.cursor.execute("SELECT * FROM videoaula")
        return self.cursor.fetchall()
        
    
    def atualizar(self, video):
        sql = " UPDATE videoaula SET titulo = %s, descricao = %s, url_video = %s, id_categoria = %s WHERE id_videoaula = %s "
        self.cursor.execute(sql, (video.titulo, video.descricao, video.url, video.id_categoria, video.id))
        self.conexao.commit()

    def deletar(self, id):
        sql = " DELETE FROM videoaula WHERE id_videoaula = %s "
        self.cursor.execute(sql, (id,))
        self.conexao.commit()

    def listar_categorias(self):
        self.cursor.execute("SELECT * FROM categoria")
        return self.cursor.fetchall()





        