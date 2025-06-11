from fastapi import FastAPI
from infrastructure.persistence.db import engine
from core.services.persistence.nota_fiscal_model import Base as NotaBase
from core.services.persistence.item_da_nota_model import Base as ItemBase


from app.interfaces.controllers.invoice_controller import router as invoice_router

NotaBase.metadata.create_all(bind=engine)
ItemBase.metadata.create_all(bind=engine)

app = FastAPI(
    title="Invoice Service",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Inclui seu controller de invoices
app.include_router(invoice_router)

# (Opcional) eventos de ciclo de vida
@app.on_event("startup")
async def on_startup():
    # aqui você poderia carregar configurações, conexões a filas, etc.
    pass

@app.on_event("shutdown")
async def on_shutdown():
    # fechar conexões, liberar recursos, etc.
    pass
