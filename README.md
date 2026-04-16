# ecom-invoice-service

> Microsserviço de geração e gerenciamento de faturas para plataformas de e-commerce, expondo uma API REST construída com FastAPI e persistência em PostgreSQL.

[![Python](https://img.shields.io/badge/python-3.11-blue?style=flat-square&logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?style=flat-square&logo=postgresql)](https://www.postgresql.org/)
[![License](https://img.shields.io/github/license/odevpedro/ecom-invoice-service?style=flat-square)](./LICENSE)
[![Last Commit](https://img.shields.io/github/last-commit/odevpedro/ecom-invoice-service?style=flat-square)](https://github.com/odevpedro/ecom-invoice-service/commits/master)

---

## Sobre o Projeto

Serviço responsável pela criação, consulta e gerenciamento do ciclo de vida de faturas em um contexto de e-commerce. Segue os princípios de Clean Architecture com separação clara entre domínio, casos de uso e infraestrutura, sendo executado de forma isolada via Docker e integrável com outros microsserviços via HTTP.

---

## Stack & Arquitetura

| Camada         | Tecnologia                        |
|----------------|-----------------------------------|
| Runtime        | Python 3.11                       |
| Framework      | FastAPI 0.115                     |
| Servidor ASGI  | Uvicorn                           |
| Banco de dados | PostgreSQL 15                     |
| ORM            | SQLAlchemy 2.0                    |
| Driver DB      | psycopg (v3, binary)              |
| Validação      | Pydantic v2                       |
| Migrations     | Alembic                           |
| Testes         | pytest                            |
| Infra          | Docker + Docker Compose           |

> **Padrão arquitetural:** Clean Architecture com 4 camadas — `core` (domínio), `application` (use cases), `infrastructure` (repositórios/ORM), `app` (rotas/controllers FastAPI).

---

## Estrutura de Pastas

```
ecom-invoice-service/
├── app/                  # Camada de apresentação (rotas FastAPI, schemas de I/O)
│   └── main.py           # Entrypoint da aplicação
├── application/          # Casos de uso — orquestração da lógica de negócio
├── core/                 # Domínio puro — entidades, regras de negócio, interfaces
├── infrastructure/       # Repositórios, modelos ORM, configuração do banco
├── alembic/              # Migrations do banco de dados
├── tests/                # Testes unitários e de integração
├── Dockerfile
├── docker-compose.yml
├── alembic.ini
└── requirements.txt
```

---

## Como Rodar Localmente

### Pré-requisitos

- Docker + Docker Compose instalados

### Setup

```bash
# 1. Clone o repositório
git clone https://github.com/odevpedro/ecom-invoice-service.git
cd ecom-invoice-service

# 2. Suba os containers (banco + aplicação)
docker compose up -d

# 3. Execute as migrations
docker compose exec app alembic upgrade head
```

A API estará disponível em `http://localhost:8000`.
Documentação interativa (Swagger): `http://localhost:8000/docs`

### Variáveis de Ambiente

| Variável       | Descrição                        | Valor padrão (dev)                              |
|----------------|----------------------------------|-------------------------------------------------|
| `DATABASE_URL` | URL de conexão com o PostgreSQL  | `postgresql://user:password@db:5432/invoice_db` |

---

## Testes

```bash
# Dentro do container
docker compose exec app pytest

# Com verbose
docker compose exec app pytest -v

# Com cobertura
docker compose exec app pytest --cov=. --cov-report=term-missing
```

---

## API — Endpoints Principais

| Método | Rota                    | Descrição                            |
|--------|-------------------------|--------------------------------------|
| POST   | `/invoices`             | Cria uma nova fatura                 |
| GET    | `/invoices`             | Lista faturas (com filtros/paginação) |
| GET    | `/invoices/{id}`        | Retorna fatura por ID                |
| PATCH  | `/invoices/{id}/status` | Atualiza status da fatura            |
| DELETE | `/invoices/{id}`        | Remove uma fatura                    |

> Documentação completa e interativa disponível em `http://localhost:8000/docs` após subir o projeto.

---

## Documentação Técnica

| Documento | Descrição |
|-----------|-----------|
| [Fluxos de Funcionalidades](./docs/system-feature-flows.md) | Fluxo interno detalhado de cada feature |
| [Backlog](./backlog.md) | Status de desenvolvimento do projeto |

---

## Status do Projeto

```
[x] Estrutura base (Clean Architecture)
[x] Configuração Docker + PostgreSQL
[x] Migrations com Alembic
[ ] CRUD de faturas (em andamento)
[ ] Testes de integração
[ ] CI/CD com GitHub Actions
```

---

## Contribuindo

1. Fork o repositório
2. Crie uma branch: `git checkout -b feature/minha-feature`
3. Commit: `git commit -m 'feat: descrição da mudança'`
4. Push: `git push origin feature/minha-feature`
5. Abra um Pull Request

> Siga o padrão [Conventional Commits](https://www.conventionalcommits.org/pt-br/).

---

<p align="center">
  Feito com foco em qualidade por <a href="https://github.com/odevpedro">@odevpedro</a>
</p>