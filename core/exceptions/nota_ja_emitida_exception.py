from core.exceptions.domain_exceptions import DomainException


class NotaJaEmitidaException(DomainException):
    """
    Exceção lançada ao tentar alterar ou reemitir uma nota que já
    foi processada ou autorizada.
    """
    def __init__(self, message: str = "Nota já foi emitida ou está em estado inválido."):
        super().__init__(message)
