# Guia de Desenvolvimento

## Configuração

### Pré-requisitos

- Python 3.13+
- Pyenv (para gerenciamento de versão)
- Poetry (para gerenciamento de dependências)

### Configuração Inicial

1. **Verifique a versão do Python:**
   ```bash
   python --version  # Deve ser Python 3.13.x
   ```

2. **Instale as dependências:**
   ```bash
   poetry install
   ```

3. **Ative o ambiente virtual:**
   ```bash
   poetry shell
   ```
   Ou execute comandos com prefixo `poetry run`.

## Fluxo de Desenvolvimento

### Estilo de Código e Linting

Este projeto usa **Ruff** para linting e formatação.

```bash
# Verificar código
poetry run ruff check src/ tests/

# Corrigir automaticamente problemas
poetry run ruff check --fix src/ tests/

# Formatar código
poetry run ruff format src/ tests/

# Verificar formatação sem fazer mudanças
poetry run ruff format --check src/ tests/
```

### Testes

Os testes são gerenciados com **Pytest** e **pytest-cov**.

```bash
# Executar todos os testes
poetry run pytest

# Executar com relatório de cobertura
poetry run pytest --cov=src/f1 --cov-report=term-missing

# Executar arquivo de teste específico
poetry run pytest tests/test_client.py

# Executar com saída detalhada
poetry run pytest -v

# Abrir relatório de cobertura em HTML
# Após executar os testes, abra htmlcov/index.html em um navegador
```

**Requisitos de Cobertura:**
- Mínimo: 50% do código em `src/f1/`
- Atualmente: Verificar a saída do `pytest` para a porcentagem exata

### Documentação

A documentação usa **MkDocs Material**.

```bash
# Compilar e servir localmente (modo observação)
poetry run task docs

# Compilar site estático
poetry run mkdocs build --strict

# Verificar erros/avisos
poetry run mkdocs build --strict
```

Os arquivos de documentação estão em `docs/` (formato Markdown).

## Checklist de Validação

Antes de fazer commit, execute esta sequência completa de validação:

```bash
# 1. Verifique a versão do Python
python --version

# 2. Verifique o ambiente do Poetry
poetry --version
poetry show

# 3. Lint e formatação
poetry run ruff check src/ tests/
poetry run ruff format --check src/ tests/

# 4. Execute os testes
poetry run pytest

# 5. Verifique a cobertura (deve ser >= 50%)
poetry run pytest --cov=src/f1 --cov-report=term-missing

# 6. Compile a documentação
poetry run mkdocs build --strict
```

Todas as etapas devem passar antes de fazer commit.

## Estrutura do Projeto

```
src/f1/                 # Pacote principal
├── __init__.py        # Inicialização do pacote
├── client.py          # OpenF1Client
├── cli.py             # Comandos da CLI
└── exceptions.py      # Exceções customizadas

tests/                 # Suite de testes
├── conftest.py        # Fixtures do Pytest
├── test_client.py     # Testes do cliente
└── test_cli.py        # Testes da CLI
```

## Adicionando um Novo Endpoint

1. **Adicione método ao `OpenF1Client`** em `src/f1/client.py`:
   ```python
   def get_my_data(self, key: int, **filters) -> list[dict]:
       """Obtenha meus dados da API."""
       endpoint = f"/my_data"
       params = {"key": key, **filters}
       return self._fetch(endpoint, params)
   ```

2. **Adicione comando CLI correspondente** em `src/f1/cli.py`:
   ```python
   @main.command()
   @click.option("--key", type=int, required=True)
   def my_data(key):
       """Busque meus dados."""
       client = OpenF1Client()
       data = client.get_my_data(key)
       click.echo(json.dumps(data, indent=2))
   ```

3. **Escreva testes** em `tests/test_client.py` e `tests/test_cli.py`

4. **Atualize a documentação** em `docs/`

5. **Garanta cobertura >= 50%**

## Fluxo de Git

1. Crie uma branch para seu trabalho
2. Faça as mudanças e passe em todas as verificações de validação
3. Faça commit com mensagens claras
4. Faça push e crie um PR
5. Garanta que CI/CD passe

## Comandos Comuns

| Comando | Propósito |
|---------|-----------|
| `poetry install` | Instalar todas as dependências |
| `poetry run pytest` | Executar testes |
| `poetry run ruff check src/ tests/` | Verificar estilo do código |
| `poetry run ruff format src/ tests/` | Formatar código |
| `poetry run task docs` | Visualizar documentação localmente |
| `poetry show` | Listar todas as dependências |
| `poetry lock` | Atualizar poetry.lock |

## Solução de Problemas

### Os testes falham com erros de importação

Certifique-se de que o ambiente Poetry está ativado:
```bash
poetry shell
# Então execute os testes
pytest
```

### Linting mostra erros que não consigo corrigir

Alguns erros podem precisar de revisão manual. Leia a documentação do Ruff:
```bash
poetry run ruff rule <RULE_CODE>
```

### A compilação do MkDocs falha

Verifique links quebrados ou Markdown inválido:
```bash
poetry run mkdocs build --strict -v
```

### Cobertura abaixo de 50%

Adicione mais testes cobrindo as linhas não cobertas. Verifique o relatório de cobertura:
```bash
poetry run pytest --cov=src/f1 --cov-report=term-missing
# Ou visualize o relatório em HTML:
# htmlcov/index.html
```

## Contribuindo

Todas as contribuições devem:
- Passar no linting (`ruff check`)
- Passar na formatação (`ruff format --check`)
- Passar nos testes (`pytest`)
- Manter >=50% de cobertura
- Atualizar a documentação

Veja o README principal para as diretrizes de contribuição.
