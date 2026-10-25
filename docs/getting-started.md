# Começando

## Requisitos

- **Python 3.13+** (verifique com `python --version`)
- `pip` ou `poetry` para gerenciamento de pacotes

## Instalação

### Usando pip

```bash
pip install f1
```

### Usando Poetry

```bash
poetry add f1
```

## Primeira Consulta

### Uso da Biblioteca

```python
from f1 import OpenF1Client

# Crie um cliente (usa https://api.openf1.org/v1 por padrão)
client = OpenF1Client()

# Obtenha todas as reuniões de um ano
meetings = client.get_meetings(year=2024)
print(f"Encontradas {len(meetings)} reuniões em 2024")

# Obtenha pilotos para uma sessão específica
drivers = client.get_drivers(session_key=9158)
for driver in drivers:
    print(f"  - {driver['first_name']} {driver['last_name']} (#{driver['driver_number']})")
```

### Uso da CLI

```bash
# Listar reuniões de 2024
f1 meetings --year 2024

# Listar pilotos em uma sessão
f1 drivers --session 9158

# Listar voltas para um piloto
f1 laps --session 9161 --driver 63 --limit 10

# Saída em JSON
f1 meetings --year 2024 --format json
```

## Próximos Passos

- Leia a [Referência da API](api-reference.md) para todos os endpoints disponíveis
- Verifique [Arquitetura](architecture.md) para entender a estrutura do código
- Veja [Desenvolvimento](development.md) para contribuir ou personalizar

## Solução de Problemas

### ModuleNotFoundError: No module named 'f1'

Certifique-se de que o pacote está instalado:
```bash
pip install f1
# ou
poetry add f1
```

### Erros de conexão

Verifique a conectividade com a internet e se [api.openf1.org](https://api.openf1.org) está acessível.

### session_key inválida

As chaves de sessão são números específicos para reuniões. Use `f1 meetings` para encontrar chaves de sessão válidas para um ano.
