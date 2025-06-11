import enum

class StatusNotaModel(enum.Enum):
    EM_PROCESSAMENTO = "EM_PROCESSAMENTO"
    AUTORIZADA       = "AUTORIZADA"
    REJEITADA        = "REJEITADA"
    CANCELADA        = "CANCELADA"