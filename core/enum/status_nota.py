from enum import Enum

class StatusNota(Enum):
    EM_PROCESSAMENTO = "EM_PROCESSAMENTO"
    AUTORIZADA       = "AUTORIZADA"
    REJEITADA        = "REJEITADA"
    CANCELADA        = "CANCELADA"
