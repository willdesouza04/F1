# Arquitetura

## Estrutura do Projeto

```
f1/
├── src/f1/                 # Pacote principal
│   ├── __init__.py         # Exportações do pacote
│   ├── client.py           # Cliente HTTP OpenF1Client
│   ├── cli.py              # Comandos CLI do Click
│   └── exceptions.py       # Exceções customizadas
├── tests/                  # Suite de testes
│   ├── conftest.py         # Fixtures do Pytest
│   ├── test_client.py      # Testes do cliente
│   └── test_cli.py         # Testes da CLI
├── docs/                   # Documentação (Markdown)
├── pyproject.toml          # Configuração do Poetry
├── mkdocs.yml              # Configuração do MkDocs
├── .python-version         # Versão Python do Pyenv
├── .gitignore              # Regras de ignore do Git
└── README.md               # Visão geral do projeto
```

## Módulos Principais

### `f1.client.OpenF1Client`

Cliente HTTP síncrono para a API OpenF1.

**Métodos Principais:**
- `get_meetings(year=None, **filters)` → `list[dict]`
- `get_drivers(session_key, **filters)` → `list[dict]`
- `get_laps(session_key, **filters)` → `list[dict]`
- `get_car_data(session_key, **filters)` → `list[dict]`
- `get_sessions(year=None, **filters)` → `list[dict]`

**Construtor:**
```python
OpenF1Client(base_url="https://api.openf1.org/v1", timeout=30)
```

### `f1.cli`

Interface de linha de comando baseada em Click.

**Comandos:**
- `f1 meetings [--year YEAR]`
- `f1 drivers --session SESSION_KEY [--limit N]`
- `f1 laps --session SESSION_KEY [--driver DRIVER_NUMBER] [--limit N]`
- `f1 car-data --session SESSION_KEY [--limit N]`
- `f1 sessions [--year YEAR] [--limit N]`

### `f1.exceptions`

Hierarquia de erros para erros de API e rede.

**Exceções:**
- `OpenF1Error` — Exceção base
- `NetworkError` — Problemas de conexão/timeout
- `APIError` — Erros HTTP 4xx/5xx
- `NotFoundError` — Respostas 404

## Modelo de Dados

Os dados são retornados como dicionários Python simples (JSON). Nenhum modelo Pydantic ou dataclass é usado inicialmente para manter a biblioteca leve.

**Resposta de Exemplo:**
```python
{
    "meeting_key": 1204,
    "year": 2024,
    "location": "Bahrain",
    "country_key": 84
}
```

## Decisões de Design

| Decisão | Justificativa |
|---------|---------------|
| HTTP Síncrono | Simples para v1, suficiente para a maioria dos casos de uso |
| Dicts/JSON brutos | Overhead mínimo, flexível para mudanças de esquema |
| Click para CLI | Maduro, bem documentado, amplamente utilizado |
| Biblioteca Requests | Estável, síncrono, padrão HTTP |
| Cobertura de testes 50%+ | Valida caminhos principais sem exaustividade |

## Fluxo de Dados

```
Comando CLI do Usuário
      ↓
Manipulador de Comando Click (cli.py)
      ↓
Método OpenF1Client (client.py)
      ↓
Solicitação HTTP (biblioteca requests)
      ↓
API OpenF1
      ↓
Resposta JSON
      ↓
Analisar e retornar dict
      ↓
Formatar e exibir (CLI) ou retornar (biblioteca)
```

## Melhorias Futuras

- **Suporte assíncrono** (httpx ou aiohttp)
- **Modelos Pydantic** para segurança de tipo
- **Cache de resposta**
- **Endpoints em lote**
