# Referência da API

## OpenF1Client

### Construtor

```python
OpenF1Client(base_url="https://api.openf1.org/v1", timeout=30)
```

**Parâmetros:**
- `base_url` (str): URL base para a API OpenF1. Padrão: `https://api.openf1.org/v1`
- `timeout` (int): Timeout da requisição em segundos. Padrão: `30`

**Retorna:** Instância de `OpenF1Client`

### Métodos

#### `get_meetings(year=None, **filters) -> list[dict]`

Obtenha reuniões de Fórmula 1 (corridas, testes, etc.).

**Parâmetros:**
- `year` (int, opcional): Filtrar por ano (ex: 2024)
- `**filters`: Parâmetros de consulta adicionais passados para a API

**Retorna:** Lista de dicionários de reunião

**Exemplo:**
```python
client = OpenF1Client()

# Todas as reuniões
all_meetings = client.get_meetings()

# Reuniões de 2024
meetings_2024 = client.get_meetings(year=2024)
```

**Exemplo de Resposta:**
```python
{
    "meeting_key": 1204,
    "year": 2024,
    "meeting_name": "Bahrain Grand Prix",
    "location": "Bahrain",
    "country_key": 84,
    "country_name": "Bahrain"
}
```

---

#### `get_sessions(year=None, **filters) -> list[dict]`

Obtenha sessões de Fórmula 1 (prática, qualificação, corrida).

**Parâmetros:**
- `year` (int, opcional): Filtrar por ano
- `**filters`: Parâmetros de consulta adicionais

**Retorna:** Lista de dicionários de sessão

**Exemplo:**
```python
# Sessões para 2024
sessions_2024 = client.get_sessions(year=2024)

# Sessões por chave de reunião
sessions = client.get_sessions(meeting_key=1204)
```

---

#### `get_drivers(session_key, **filters) -> list[dict]`

Obtenha pilotos participantes em uma sessão.

**Parâmetros:**
- `session_key` (int): Chave da sessão (obrigatório)
- `**filters`: Parâmetros de consulta adicionais

**Retorna:** Lista de dicionários de piloto

**Exemplo:**
```python
# Pilotos na sessão 9158
drivers = client.get_drivers(session_key=9158)

for driver in drivers:
    print(f"{driver['first_name']} {driver['last_name']}")
```

---

#### `get_laps(session_key, **filters) -> list[dict]`

Obtenha tempos de volta para uma sessão.

**Parâmetros:**
- `session_key` (int): Chave da sessão (obrigatório)
- `**filters`: Parâmetros de consulta adicionais (ex: `driver_number=63`)

**Retorna:** Lista de dicionários de volta

**Exemplo:**
```python
# Todas as voltas na sessão 9161
laps = client.get_laps(session_key=9161)

# Voltas do piloto #63
driver_laps = client.get_laps(session_key=9161, driver_number=63)

# Verificar tempos de volta
for lap in driver_laps[:5]:
    print(f"Volta {lap['lap_number']}: {lap['duration_seconds']}s")
```

---

#### `get_car_data(session_key, **filters) -> list[dict]`

Obtenha telemetria/dados do carro para uma sessão.

**Parâmetros:**
- `session_key` (int): Chave da sessão (obrigatório)
- `**filters`: Parâmetros de consulta adicionais

**Retorna:** Lista de dicionários de dados do carro

**Exemplo:**
```python
# Dados do carro para a sessão 9161
car_data = client.get_car_data(session_key=9161)

# Filtrar por piloto
driver_data = client.get_car_data(session_key=9161, driver_number=63)
```

---

## Exceções

### OpenF1Error

Exceção base para todos os erros da biblioteca F1.

```python
try:
    client.get_meetings()
except OpenF1Error as e:
    print(f"Erro: {e}")
```

### NetworkError

Levantada para erros de conexão/timeout.

```python
from f1.exceptions import NetworkError

try:
    client.get_meetings()
except NetworkError as e:
    print(f"Falha na conexão: {e}")
```

### APIError

Levantada para erros de API (4xx/5xx).

```python
from f1.exceptions import APIError

try:
    client.get_drivers(session_key=999999)
except APIError as e:
    print(f"Erro na API: {e}")
```

### NotFoundError

Levantada para respostas 404 Not Found.

```python
from f1.exceptions import NotFoundError

try:
    client.get_drivers(session_key=999999)
except NotFoundError as e:
    print(f"Recurso não encontrado: {e}")
```

---

## Filtros Comuns

Muitos métodos aceitam `**filters` para parâmetros de consulta:

```python
# Filtro de ano
client.get_meetings(year=2024)

# Filtro de piloto
client.get_laps(session_key=9158, driver_number=63)

# Limitar resultados (específico da API)
client.get_meetings(limit=5)
```

Consulte a [documentação da API OpenF1](https://www.openf1.org/) para todos os filtros disponíveis.

---

## Timeouts

Customize o timeout de requisição globalmente:

```python
client = OpenF1Client(timeout=60)  # Timeout de 60 segundos
```

O timeout padrão é 30 segundos. Aumente para conexões lentas ou respostas grandes.
