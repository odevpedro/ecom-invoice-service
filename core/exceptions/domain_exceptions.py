class DomainException(Exception):

    pass

class NotaJaEmitidaException(DomainException):

    def __init__(self, message: str = "Nota já foi emitida ou está em estado inválido."):
        super().__init__(message)

class NotaNaoEncontradaException(DomainException):

    def __init__(self, message: str = "Recurso não encontrado no domínio."):
        super().__init__(message)
