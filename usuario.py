class Usuario:
    def __init__(self, id=None, nome="", email="", senha="", permissao="padrao"):
        self._id = id
        self._nome = nome
        self._email = email
        self._senha = senha
        self._permissao = permissao

    @property
    def id(self):
        return self._id

    @property
    def nome(self):
        return self._nome

    @property
    def email(self):
        return self._email

    @property
    def senha(self):
        return self._senha

    @property
    def permissao(self):
        return self._permissao
