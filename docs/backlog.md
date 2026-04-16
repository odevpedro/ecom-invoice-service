# Backlog — ecom-invoice-service

> Registro vivo do progresso do projeto. Atualizado a cada mudanca de estado de uma funcionalidade.
> **Ultima atualizacao:** 2026-04-16

---

## Sobre o Projeto

Microsservico de emissao e gerenciamento de Notas Fiscais eletronicas (NF-e) para plataformas de e-commerce, com suporte a emissao, cancelamento e Carta de Correcao Eletronica.

**Versao atual:** `1.0.0`
**Repositorio:** [github.com/odevpedro/ecom-invoice-service](https://github.com/odevpedro/ecom-invoice-service)
**Stack principal:** Python 3.11 / FastAPI / SQLAlchemy / PostgreSQL

---

## Legenda

| Simbolo | Significado |
|---------|-------------|
| `[ ]`   | Pendente |
| `[~]`   | Em andamento |
| `[x]`   | Concluido |
| `P0`    | Critico — bloqueia outras features |
| `P1`    | Alta prioridade |
| `P2`    | Media prioridade |
| `P3`    | Melhoria / nice-to-have |
| `XS` `S` `M` `L` `XL` | Estimativa de complexidade |

---

## Em Andamento

> Features atualmente sendo desenvolvidas. Idealmente, maximo de 2-3 itens simultaneos.

_Nenhum item em andamento no momento._

---

## Pendentes

> Ordenadas por prioridade. Itens de P0 e P1 devem entrar em "Em Andamento" primeiro.

### Integracao SEFAZ (critico)

- [ ] `P0` `XL` — Implementar `SefazClient` real: geracao de XML NF-e conforme layout oficial, envio SOAP/REST a SEFAZ e tratamento de retorno
- [ ] `P0` `L` — Implementar `Signer` real: assinatura digital com certificado A1 (arquivo PFX) ou A3 (token USB) usando xmlsec ou PyKCS11
- [ ] `P0` `S` — Adicionar campo `protocolo_cce` ao modelo `NotaFiscalModel` (SQLAlchemy) e criar migration correspondente — campo e usado no mapper mas ausente no model

### Seguranca e Autorizacao

- [ ] `P1` `M` — Implementar autenticacao nos endpoints (atualmente todos publicos sem qualquer autenticacao)
- [ ] `P1` `S` — Adicionar validacao do digito verificador de CNPJ/CPF no value object `CnpjCpf` (TODO deixado no codigo)

### Mensageria

- [ ] `P2` `L` — Implementar `event_publisher.py` e `event_consumer.py` (arquivos criados mas vazios)
- [ ] `P2` `M` — Definir quais eventos de dominio serao publicados (ex: `NotaEmitida`, `NotaCancelada`)

### Infraestrutura e Qualidade

- [ ] `P1` `M` — Configurar CI/CD com GitHub Actions (lint, testes, build Docker)
- [ ] `P2` `M` — Adicionar testes unitarios de dominio (entidades e value objects isolados de infra)
- [ ] `P2` `S` — Paginacao na listagem `GET /invoices`
- [ ] `P3` `S` — Implementar `repository_impl.py` (arquivo criado mas vazio; logica esta em `nota_fiscal_sqlalchemy.py`)

### Melhorias

- [ ] `P3` `M` — Tratamento global de excecoes (atualmente cada rota tem try/except individual)
- [ ] `P3` `S` — Padronizar envelope de erro (`{"statusCode": ..., "error": "...", "message": "..."}`)

---

## Concluidas

> Features finalizadas com suas respectivas datas de conclusao.

- [x] `P0` `M` — Estrutura base (Clean Architecture: core / application / infrastructure / app) — *(2025-06-14)*
- [x] `P0` `S` — Configuracao Docker + PostgreSQL 15 (Dockerfile + docker-compose.yml) — *(2025-06-14)*
- [x] `P0` `S` — Migrations com Alembic (revisao `146d52710ce9`) — *(2025-06-14)*
- [x] `P0` `M` — Value Objects: `CnpjCpf`, `Endereco` (validacao de UF e CEP), `Imposto` (ICMS, IPI, PIS, COFINS) — *(2025-06-14)*
- [x] `P0` `S` — Entidade de dominio `NotaFiscal` com `ItemDaNota` e enum `StatusNota` — *(2025-06-14)*
- [x] `P0` `M` — Use case `EmitInvoiceUseCase`: emite NF-e via port e persiste resultado — *(2025-06-14)*
- [x] `P0` `M` — Use case `CancelInvoiceUseCase`: cancela NF-e autorizada via port e persiste resultado — *(2025-06-14)*
- [x] `P0` `M` — Use case `CorrectionInvoiceUseCase`: emite CC-e para nota autorizada via port e persiste protocolo — *(2025-06-14)*
- [x] `P1` `M` — API REST com 5 endpoints (POST emitir, GET listar, GET buscar, POST cancelar, POST corrigir) — *(2025-06-14)*
- [x] `P1` `M` — Testes de integracao com FastAPI `TestClient` cobrindo os 5 endpoints e cenarios de erro 404 — *(2025-06-14)*
- [x] `P1` `S` — Mapper `NotaFiscalMapper`: conversao bidirecional entre modelo SQLAlchemy e entidade de dominio — *(2025-06-14)*
- [x] `P0` `S` — Documentacao tecnica (README, backlog, system-feature-flows) — *(2026-04-16)*

---

## Bugs Conhecidos

> Problemas identificados que ainda nao foram corrigidos.

| ID | Descricao | Severidade | Reportado em |
|----|-----------|------------|--------------|
| #BUG-01 | Campo `protocolo_cce` usado no `NotaFiscalMapper` mas ausente em `NotaFiscalModel` — persistencia do protocolo da CC-e falha silenciosamente | Alta | 2026-04-16 |
| #BUG-02 | `NotaFiscalCancelamentoAdapter.cancelar()` cria uma `NotaFiscal` temporaria com `cnpj=None` e `endereco=None` para trafegar apenas status e protocolo — viola invariantes da entidade | Media | 2026-04-16 |
| #BUG-03 | `NotaFiscalModel` tem relacionamento mapeado como `items` mas o mapper acessa `itens` com fallback — inconsistencia de nomenclatura | Baixa | 2026-04-16 |

---

## Notas e Decisoes Pendentes

> Pontos em aberto que precisam de decisao antes de serem desenvolvidos.

- [ ] Definir certificado digital padrao (A1 arquivo vs A3 token) e como injetar via variavel de ambiente no `Signer`
- [ ] Decidir se o `SefazClient` apontara para o ambiente de homologacao (hom.nfe.fazenda.gov.br) ou producao por variavel de ambiente
- [ ] Avaliar se `event_publisher` usara RabbitMQ, Kafka ou outro broker — nenhuma dependencia de mensageria esta em `requirements.txt`
- [ ] Definir estrategia de autenticacao: JWT interno, API Key ou integracao com servico de identidade externo

---

## Historico de Versoes

| Versao | Data | Principais entregas |
|--------|------|---------------------|
| `1.0.0` | 2025-06-14 | Estrutura Clean Architecture, 3 use cases (emissao, cancelamento, CC-e), API REST, testes de integracao |
