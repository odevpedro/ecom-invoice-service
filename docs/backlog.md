# Backlog — [Nome do Projeto]

> Registro vivo do progresso do projeto. Atualizado a cada mudança de estado de uma funcionalidade.
> **Última atualização:** YYYY-MM-DD

---

## Sobre o Projeto

Uma frase descrevendo o objetivo do produto e o problema que ele resolve.

**Versão atual:** `0.1.0`
**Repositório:** [github.com/odevpedro/REPO_NAME](https://github.com/odevpedro/REPO_NAME)
**Stack principal:** Node.js / NestJS / PostgreSQL *(substitua pelo seu)*

---

## Legenda

| Símbolo | Significado |
|---------|-------------|
| `[ ]`   | Pendente |
| `[~]`   | Em andamento |
| `[x]`   | Concluído |
| `P0`    | Crítico — bloqueia outras features |
| `P1`    | Alta prioridade |
| `P2`    | Média prioridade |
| `P3`    | Melhoria / nice-to-have |
| `XS` `S` `M` `L` `XL` | Estimativa de complexidade |

---

## Em Andamento

> Features atualmente sendo desenvolvidas. Idealmente, máximo de 2–3 itens simultâneos.

- [~] `P0` `M` — Autenticação com JWT + Refresh Token *(iniciado em: YYYY-MM-DD)*
- [~] `P1` `S` — Middleware de tratamento global de erros *(iniciado em: YYYY-MM-DD)*

---

## Pendentes

> Ordenadas por prioridade. Itens de P0 e P1 devem entrar em "Em Andamento" primeiro.

### Núcleo da Aplicação

- [ ] `P0` `L` — Módulo de pedidos (CRUD completo)
- [ ] `P0` `M` — Validação de endereço via ViaCEP
- [ ] `P1` `M` — Notificações por e-mail (SendGrid)
- [ ] `P1` `S` — Paginação nas listagens

### Infraestrutura & Qualidade

- [ ] `P1` `M` — Configuração de CI/CD com GitHub Actions
- [ ] `P1` `L` — Cobertura de testes unitários (meta: 80%)
- [ ] `P2` `S` — Dockerização completa (app + banco + redis)
- [ ] `P2` `M` — Documentação Swagger automática

### Melhorias & Evoluções

- [ ] `P2` `M` — Cache com Redis para consultas frequentes
- [ ] `P3` `L` — Módulo de relatórios exportáveis (PDF/CSV)
- [ ] `P3` `XL` — Integração com WhatsApp Business API

---

## Concluídas

> Features finalizadas com suas respectivas datas de conclusão e links de referência.

- [x] `P0` `S` — Estrutura inicial do projeto (Clean Architecture) — *(YYYY-MM-DD)* — [#PR-01](https://github.com/odevpedro/REPO_NAME/pull/1)
- [x] `P0` `S` — Configuração do banco de dados (TypeORM + PostgreSQL) — *(YYYY-MM-DD)* — [#PR-02](https://github.com/odevpedro/REPO_NAME/pull/2)
- [x] `P1` `M` — Módulo de usuários (cadastro, busca por ID) — *(YYYY-MM-DD)* — [#PR-03](https://github.com/odevpedro/REPO_NAME/pull/3)

---

## Bugs Conhecidos

> Problemas identificados que ainda não foram corrigidos.

| ID | Descrição | Severidade | Reportado em |
|----|-----------|------------|--------------|
| #BUG-01 | Token não é invalidado após logout | Alta | YYYY-MM-DD |
| #BUG-02 | Paginação retorna total incorreto quando há filtros | Média | YYYY-MM-DD |

---

## Notas & Decisões Pendentes

> Pontos em aberto que precisam de decisão antes de serem desenvolvidos.

- [ ] Definir estratégia de soft delete vs hard delete para entidade `Order`
- [ ] Avaliar uso de filas (BullMQ vs RabbitMQ) para processamento assíncrono de notificações
- [ ] Decidir se o módulo de relatórios será parte desta API ou um serviço separado

---

## Histórico de Versões

| Versão | Data | Principais entregas |
|--------|------|---------------------|
| `0.1.0` | YYYY-MM-DD | Estrutura inicial, autenticação, módulo de usuários |
| `0.2.0` | — | Módulo de pedidos, notificações (planejado) |
