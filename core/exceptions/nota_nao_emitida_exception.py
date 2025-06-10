from core.exceptions.domain_exceptions import DomainException


class NotaNaoEncontradaException(DomainException):
    """
    Exceção lançada quando uma operação espera itens ou notas existentes
    no domínio, mas nenhum é encontrado.
    """
    def __init__(self, message: str = "Recurso não encontrado no domínio."):
        super().__init__(message)
