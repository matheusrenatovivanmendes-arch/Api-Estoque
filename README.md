# API de Estoque

API REST de controle de estoque construída com Flask, com autenticação, autorização por cargo, testes automatizados e relatório de faturamento. O administrador pode criar, atualizar e deletar produtos, categorias e usuários, registrar movimentações de estoque (entrada/saída) com histórico completo, e gerar relatórios de faturamento em Excel.

## Funcionalidades

- **CRUD de Produtos** — criar, listar, buscar por nome, atualizar e deletar, com alerta de estoque baixo calculado automaticamente
- **CRUD de Categorias** — mesmo conjunto de operações, com proteção contra exclusão de categorias vinculadas a produtos
- **CRUD de Usuários** — dois cargos (`admin` e `operador`), senhas com hash (bcrypt)
- **Autenticação** — login via JWT armazenado em cookie `HttpOnly`, com proteção CSRF (double-submit token)
- **Autorização por cargo** — decorator customizado (`@requer_cargo`) restringe rotas por `admin`/`operador`
- **Movimentação de estoque** — entrada e saída, com validação de estoque disponível e transação atômica (histórico + quantidade atualizados juntos)
- **Relatório de faturamento** — gerado com Pandas, exportado como arquivo `.xlsx` (via Openpyxl), filtrável por período

## Tecnologias

Flask · SQLAlchemy · Pydantic · Flask-JWT-Extended · Flask-Migrate (Alembic) · Flask-Limiter · Pandas · Openpyxl · pytest

## Arquitetura

O projeto segue uma separação em camadas:

- **`models.py`** — classes SQLAlchemy, representando as tabelas e seus relacionamentos
- **`shemas/`** — schemas Pydantic, responsáveis por validar o formato dos dados de entrada
- **`services/`** — regras de negócio (a única camada que fala diretamente com o banco de dados)
- **`routes/`** — só sabem "HTTP": recebem a requisição, chamam o service, e traduzem o resultado em status code + JSON
- **`exceptions.py`** — exceções customizadas (`RecursoNaoEncontrado`, `ConflitoDeRecurso`) para diferenciar respostas `404` de `409`
- **`auth.py`** — decorator de autorização por cargo, usado nas rotas protegidas

```
app/
  models.py
  extensions.py
  exceptions.py
  auth.py
  shemas/
    schemas.py
  services/
    produtos.py
    categoria.py
    usuario.py
    movimentacao.py
    relatorio.py
    autentificar.py
  routes/
    produtos_rota.py
    categoria_rota.py
    usuario_rota.py
    movimentacao_rota.py
    relatorio_rota.py
    login.py
  tests/
run.py
seed_admin.py
```

## Como rodar

```bash
# 1. Cria e ativa o ambiente virtual
python3 -m venv .venv
source .venv/bin/activate

# 2. Instala as dependências
pip install -r requirements.txt

# 3. Configura as variáveis de ambiente
cp .env.example app/.env
# edite app/.env preenchendo SQLALCHEMY_DATABASE_URI, SECRET_KEY e JWT_SECRET_KEY

# 4. Roda as migrations
flask db upgrade

# 5. Cria o usuário admin inicial
python3 seed_admin.py

# 6. Sobe o servidor
python3 run.py
```
O servidor sobe em `http://127.0.0.1:5001`.

## Endpoints principais

Todas as rotas abaixo (exceto login) exigem autenticação via cookie JWT + cabeçalho `X-CSRF-TOKEN`.

| Método | Rota | Cargo | Descrição |
|---|---|---|---|
| POST | `/usuario/login` | — | Login, define cookies de sessão |
| POST | `/usuario/logout` | — | Encerra a sessão |
| POST | `/usuarios` | admin | Cria usuário |
| GET | `/usuarios` | admin | Lista usuários |
| GET | `/usuarios/buscar?username=` | admin | Busca usuário por username |
| PATCH | `/usuarios/<id>` | admin | Atualiza usuário (parcial) |
| DELETE | `/usuarios/<id>` | admin | Remove usuário |
| POST | `/categorias` | admin | Cria categoria |
| GET | `/categorias` | admin | Lista categorias |
| GET | `/categorias/buscar?nome=` | admin | Busca categoria por nome |
| PATCH | `/categorias/<id>` | admin | Atualiza categoria (parcial) |
| DELETE | `/categorias/<id>` | admin | Remove categoria (`409` se houver produto vinculado) |
| POST | `/produtos` | admin | Cria produto |
| GET | `/produtos` | admin | Lista produtos (com `estoque_baixo` calculado) |
| GET | `/produtos/buscar?nome=` | admin | Busca produto por nome |
| PATCH | `/produtos/<id>` | admin | Atualiza produto (parcial) |
| DELETE | `/produtos/<id>` | admin | Remove produto (`409` se houver movimentação vinculada) |
| POST | `/movimentacao` | admin, operador | Registra entrada/saída de estoque |
| GET | `/relatorio?data_inicio=&data_fim=` | admin | Gera relatório de faturamento em Excel |

## Testes

```bash
pytest app/tests -v
```
35 testes cobrindo os cenários principais de cada rota (sucesso, erro de validação, recurso não encontrado, conflito, autorização por cargo).

## Decisões técnicas

- **Autenticação via cookie + CSRF, em vez de token no header**: escolhi cookies `HttpOnly` pra evitar que o token JWT fosse acessível via JavaScript (proteção contra XSS), o que exigiu adicionar proteção CSRF, já que cookies são enviados automaticamente pelo navegador em qualquer requisição.
- **`quantidade_estoque` é um campo armazenado, não calculado**: decidi atualizar esse campo diretamente a cada movimentação (em vez de somar o histórico toda vez), priorizando performance de leitura — o painel administrativo consulta produtos com muito mais frequência do que movimentações são registradas.
- **`preco_unitario` só é salvo em movimentações de saída**: representa o preço de venda no momento da transação, usado no relatório de faturamento. Entradas de estoque não têm esse conceito (são custo, não receita).


## Autor

Matheus — [LinkedIn](#) · [GitHub](https://github.com/matheusrenatovivanmendes-arch)
