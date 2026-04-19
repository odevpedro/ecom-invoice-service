# ecom-invoice-service

> Microsservico de emissao e gerenciamento de Notas Fiscais eletronicas (NF-e) para plataformas de e-commerce — emite, consulta, cancela e corrige NF-es via API REST.

[![Build Status](https://img.shields.io/github/actions/workflow/status/odevpedro/ecom-invoice-service/ci.yml?branch=master&style=flat-square)](https://github.com/odevpedro/ecom-invoice-service/actions)
[![Coverage](https://img.shields.io/codecov/c/github/odevpedro/ecom-invoice-service?style=flat-square)](https://codecov.io/gh/odevpedro/ecom-invoice-service)
[![License](https://img.shields.io/github/license/odevpedro/ecom-invoice-service?style=flat-square)](./LICENSE)
[![Last Commit](https://img.shields.io/github/last-commit/odevpedro/ecom-invoice-service?style=flat-square)](https://github.com/odevpedro/ecom-invoice-service/commits/master)

---

## Sobre o Projeto

Servico responsavel pelo ciclo de vida completo de uma NF-e dentro de um ecossistema de e-commerce. Recebe os dados do emitente, destinatario e itens via HTTP, aplica as regras fiscais de dominio, aciona a integracao com a SEFAZ e persiste o resultado em PostgreSQL.

A integracao com a SEFAZ e a assinatura digital sao stubs — prontos para substituicao sem impacto nas camadas internas. Veja a secao de status para detalhes.

---

## Stack & Arquitetura

| Camada        | Tecnologia                    |
|---------------|-------------------------------|
| Runtime       | Python 3.11                   |
| Framework     | FastAPI 0.115                 |
| Servidor ASGI | Uvicorn                       |
| Banco de dados| PostgreSQL 15                 |
| ORM           | SQLAlchemy 2.0                |
| Driver DB     | psycopg (v3, binary)          |
| Validacao     | Pydantic v2                   |
| Migrations    | Alembic 1.16                  |
| Mensageria    | Nao implementado (estrutura criada) |
| Infra         | Docker + Docker Compose       |
| Testes        | pytest 8.4                    |

> Padrao arquitetural: **Clean Architecture** com separacao em camadas `core (domain) → application → infrastructure → app (presentation)`.

---

## Estrutura de Pastas

```
ecom-invoice-service/
├── app/
│   ├── main.py                              # Entrypoint: cria app FastAPI, inclui routers
│   └── interfaces/
│       └── controllers/
│           └── invoice_controller.py        # Rotas, schemas Pydantic e injecao de dependencias
├── application/
│   ├── use_cases/
│   │   ├── emit_invoice.py                  # Caso de uso: emissao de NF-e
│   │   ├── cancel_invoice.py                # Caso de uso: cancelamento
│   │   └── correct_invoice.py              # Caso de uso: Carta de Correcao (CC-e)
│   └── mappers/
│       └── nota_fiscal_mapper.py            # Conversao bidirecional Model <-> Entity
├── core/
│   ├── entities/nota_fiscal.py              # Entidade NotaFiscal e ItemDaNota
│   ├── enum/status_nota.py                 # StatusNota: EM_PROCESSAMENTO, AUTORIZADA, REJEITADA, CANCELADA
│   ├── value_objects/                       # CnpjCpf, Endereco, Imposto (imutaveis, auto-validados)
│   ├── exceptions/                          # DomainException, NotaJaEmitidaException, NotaNaoEncontradaException
│   └── services/
│       ├── ports/                           # Interfaces ABC: EmissaoNotaPort, CancelamentoNotaPort, CartaCorrecaoPort, NotaFiscalRepository
│       └── persistence/                     # Modelos SQLAlchemy: NotaFiscalModel, ItemDaNotaModel
├── infrastructure/
│   ├── adapters/                            # Implementacoes dos ports
│   ├── external_services/
│   │   ├── sefaz_client.py                 # Stub do cliente SEFAZ (TODO: implementar integracao real)
│   │   └── signer.py                       # Stub de assinatura digital (TODO: implementar com xmlsec/PyKCS11)
│   ├── messaging/                           # event_publisher.py e event_consumer.py (nao implementados)
│   └── persistence/
│       └── db.py                            # Engine SQLAlchemy e SessionLocal
├── alembic/                                 # Migrations do banco
├── tests/
│   └── test_invoice_api.py                 # Testes de integracao via FastAPI TestClient
├── docs/
│   ├── system-feature-flows.md
│   └── backlog.md
├── Dockerfile
├── docker-compose.yml
├── alembic.ini
└── requirements.txt
```

---

## Como Rodar Localmente

### Pre-requisitos

- Docker + Docker Compose

### Setup

```bash
# 1. Clone o repositorio
git clone https://github.com/odevpedro/ecom-invoice-service.git && cd ecom-invoice-service

# 2. Suba os servicos (banco + aplicacao)
docker compose up -d

# 3. Execute as migrations
docker compose exec app alembic upgrade head
```

A API estara disponivel em `http://localhost:8000`.

> A unica variavel de ambiente necessaria e `DATABASE_URL`. O valor padrao ja esta configurado no `docker-compose.yml`.

### Variaveis de Ambiente

| Variavel       | Descricao                       | Valor padrao (dev)                                           |
|----------------|---------------------------------|--------------------------------------------------------------|
| `DATABASE_URL` | URL de conexao com o PostgreSQL | `postgresql+psycopg://user:password@localhost:5432/invoice_db` |

---

## Testes

```bash
# Todos os testes
docker compose exec app pytest

# Com verbose
docker compose exec app pytest -v

# Com cobertura
docker compose exec app pytest --cov=. --cov-report=term-missing
```

---

## API — Endpoints Principais

Todos os endpoints sao prefixados com `/invoices`.

| Metodo | Rota                                  | Descricao                                      | Auth |
|--------|---------------------------------------|------------------------------------------------|------|
| POST   | `/invoices`                           | Emite uma nova NF-e                            | TODO |
| GET    | `/invoices`                           | Lista todas as NF-es persistidas               | TODO |
| GET    | `/invoices/{chave_acesso}`            | Busca NF-e pela chave de acesso (44 chars)     | TODO |
| POST   | `/invoices/{chave_acesso}/cancel`     | Cancela uma NF-e autorizada                    | TODO |
| POST   | `/invoices/{chave_acesso}/correction` | Emite Carta de Correcao Eletronica (CC-e)      | TODO |

> Documentacao completa: `http://localhost:8000/docs` (Swagger UI) apos subir o projeto.

---

## Documentacao Tecnica

| Documento | Descricao |
|-----------|-----------|
| [Fluxos de Funcionalidades](./docs/system-feature-flows.md) | Fluxo interno detalhado de cada feature, diagramas de sequencia e ADRs |
| [Backlog](./docs/backlog.md) | Status de desenvolvimento, bugs conhecidos e decisoes pendentes |

---

## Status do Projeto

```
[x] Estrutura base (Clean Architecture)
[x] Configuracao Docker + PostgreSQL 15
[x] Migrations com Alembic
[x] Emissao de NF-e (use case + adapter stub)
[x] Cancelamento de NF-e (use case + adapter stub)
[x] Carta de Correcao Eletronica (use case + adapter stub)
[x] Testes de integracao (TestClient — 7 cenarios)
[ ] Integracao real com SEFAZ (SefazClient e Signer sao stubs)
[ ] Assinatura digital de XML (certificado A1/A3)
[ ] Autenticacao/autorizacao nos endpoints
[ ] Mensageria (event_publisher e event_consumer nao implementados)
[ ] CI/CD com GitHub Actions
```

---

## Contribuindo

1. Fork o repositorio
2. Crie uma branch: `git checkout -b feature/minha-feature`
3. Commit suas mudancas: `git commit -m 'feat: adiciona minha feature'`
4. Push: `git push origin feature/minha-feature`
5. Abra um Pull Request descrevendo o que foi feito

> Siga o padrao [Conventional Commits](https://www.conventionalcommits.org/pt-br/).

---

## Licenca

Distribuido sob a licenca MIT. Veja [LICENSE](./LICENSE) para mais informacoes.

---

<p align="center">
  Feito com foco em qualidade por <a href="https://github.com/odevpedro">@odevpedro</a>
</p>
