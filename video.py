class Video:
    def __init__(self, id=None, titulo="", descricao="", id_categoria=None, url=""):
        self._id = id
        self._titulo = titulo
        self._descricao = descricao
        self._id_categoria = id_categoria
        self._url = url

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def titulo(self):
        return self._titulo

    @titulo.setter
    def titulo(self, value):
        self._titulo = value

    @property
    def descricao(self):
        return self._descricao

    @descricao.setter
    def descricao(self, value):
        self._descricao = value

    @property
    def id_categoria(self):
        return self._id_categoria

    @id_categoria.setter
    def id_categoria(self, value):
        self._id_categoria = value

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        self._url = value
