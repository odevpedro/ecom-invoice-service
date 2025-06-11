# infrastructure/persistence/db.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# TODO: ajustar a URL de conexão com seu banco de dados
DATABASE_URL = "postgresql://user:password@localhost:5432/invoice_db"

# Cria o engine SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

# Cria a fábrica de sessões
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Opcional: criar todas as tabelas definidas nos modelos
# from core.services.persistence.nota_fiscal_model import Base as NotaBase
# NotaBase.metadata.create_all(bind=engine)
