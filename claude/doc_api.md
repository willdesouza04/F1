# Documentação da API OpenF1

## Visão Geral

A OpenF1 fornece acesso gratuito a dados históricos de Fórmula 1 a partir de 2023, com opções de assinatura paga para dados em tempo real. Todos os endpoints são consultados com requisições GET e retornam JSON por padrão (CSV disponível com `csv=true`).

### URL Base
```
https://api.openf1.org/v1/{endpoint}
```

### Autenticação
- **Dados históricos (2023+):** Gratuito, sem autenticação necessária
- **Dados em tempo real:** Requer assinatura paga (mecanismo não documentado)

### Formato de Resposta
- **Padrão:** Array JSON de objetos
- **Formato CSV:** Adicione `?csv=true` a qualquer URL do endpoint

---

## Parâmetros de Consulta & Filtragem

### Filtragem Básica
Adicione parâmetros de consulta para filtrar por qualquer atributo não-array:

```
/endpoint?parametro=valor&parametro2=valor2
```

### Operadores
Operadores de comparação suportados:
- `=` - Igual
- `>` - Maior que
- `<` - Menor que
- `>=` - Maior ou igual
- `<=` - Menor ou igual

### Múltiplos Valores
Repita um parâmetro para corresponder a múltiplos valores:
```
/drivers?driver_number=4&driver_number=81
```

### Valores Especiais
- `latest` - Para `meeting_key` e `session_key`, alvo o item atual ou mais recente

### Filtragem de Datas
Campos de data aceitam múltiplos formatos:
- ISO 8601: `2021-09-10`
- Legível: `Sep 10, 2021`
- ISO 8601 com hora: `2023-09-16T13:03:35.200`

---

## Endpoints da API

### 1. Dados do Carro — `/car_data`
**Descrição:** Telemetria do carro em aproximadamente 3,7 Hz

**Exemplo de Consulta:**
```
/car_data?driver_number=55&session_key=9159&speed>=315
```

**Filtros Disponíveis:**
- `driver_number`, `session_key`, `meeting_key`, `speed`, `date`, e outros campos

**Campos de Resposta:**
| Campo | Descrição |
|---|---|
| `brake` | `100` se o freio é pressionado, `0` caso contrário |
| `date` | Timestamp UTC (ISO 8601) |
| `driver_number` | Número de corrida do piloto |
| `drs` | Código de status do DRS |
| `n_gear` | Marcha (1-8), `0` para neutro |
| `rpm` | RPM do motor |
| `speed` | Velocidade em km/h |
| `throttle` | Porcentagem de potência (0-100) |
| `meeting_key` | Identificador da reunião |
| `session_key` | Identificador da sessão |

**Códigos de Status do DRS (interpretação da comunidade):**
- `0, 1` - DRS desligado
- `8` - Detectado, elegível uma vez na zona de ativação
- `10, 12, 14` - DRS ligado
- `2, 3, 9` - Desconhecido

---

### 2. Pilotos do Campeonato (beta) — `/championship_drivers`
**Descrição:** Classificação de pilotos (apenas sessões de corrida)

**Exemplo de Consulta:**
```
/championship_drivers?session_key=9839&driver_number=4&driver_number=81
```

**Filtros Disponíveis:**
- `session_key`, `driver_number`, `meeting_key`

**Campos de Resposta:**
- `driver_number` - Número de corrida do piloto
- `meeting_key` - Identificador da reunião
- `session_key` - Identificador da sessão
- `points_start` - Pontos antes da corrida
- `points_current` - Pontos no momento da requisição
- `position_start` - Posição antes da corrida
- `position_current` - Posição atual

---

### 3. Equipes do Campeonato (beta) — `/championship_teams`
**Descrição:** Classificação de equipes (apenas sessões de corrida)

**Exemplo de Consulta:**
```
/championship_teams?session_key=9839&team_name=McLaren
```

**Filtros Disponíveis:**
- `session_key`, `team_name`, `meeting_key`

**Campos de Resposta:**
- `team_name` - Nome da equipe
- `meeting_key` - Identificador da reunião
- `session_key` - Identificador da sessão
- `points_start` - Pontos antes da corrida
- `points_current` - Pontos no momento da requisição
- `position_start` - Posição antes da corrida
- `position_current` - Posição atual

---

### 4. Pilotos — `/drivers`
**Descrição:** Detalhes dos pilotos para uma sessão

**Exemplo de Consulta:**
```
/drivers?driver_number=1&session_key=9158
```

**Filtros Disponíveis:**
- `driver_number`, `session_key`, `meeting_key`

**Campos de Resposta:**
| Campo | Descrição |
|---|---|
| `broadcast_name` | Nome conforme mostrado na transmissão |
| `full_name` | Nome completo do piloto |
| `first_name` | Primeiro nome |
| `last_name` | Sobrenome |
| `name_acronym` | Código de três letras (ex: VER) |
| `headshot_url` | URL da foto do piloto |
| `team_name` | Nome da equipe |
| `team_colour` | Cor da equipe em hexadecimal RRGGBB |
| `country_code` | Código do país (descontinuado) |

---

### 5. Intervalos — `/intervals`
**Descrição:** Diferenças entre pilotos e para o líder (apenas corridas, atualizações a cada ~4 segundos)

**Exemplo de Consulta:**
```
/intervals?session_key=9165&interval>0&interval<0.005
```

**Filtros Disponíveis:**
- `session_key`, `driver_number`, `interval`, `gap_to_leader`, `date`

**Campos de Resposta:**
- `interval` - Diferença para o carro à frente (segundos) ou `+1 LAP` ou `null`
- `gap_to_leader` - Diferença para o líder (segundos) ou `+1 LAP` ou `null` (null para o líder)
- `date` - Timestamp
- `driver_number` - Número de corrida do piloto
- `meeting_key` - Identificador da reunião
- `session_key` - Identificador da sessão

---

### 6. Voltas — `/laps`
**Descrição:** Dados de cronometragem e velocidade por volta

**Exemplo de Consulta:**
```
/laps?session_key=9161&driver_number=63&lap_number=8
```

**Filtros Disponíveis:**
- `session_key`, `driver_number`, `lap_number`, `is_pit_out_lap`, `lap_duration`, `date_start`

**Campos de Resposta:**
| Campo | Descrição |
|---|---|
| `lap_number` | Índice da volta (começa em 1) |
| `lap_duration` | Tempo total da volta (segundos) |
| `duration_sector_1` | Tempo do setor 1 (segundos) |
| `duration_sector_2` | Tempo do setor 2 (segundos) |
| `duration_sector_3` | Tempo do setor 3 (segundos) |
| `i1_speed` | Velocidade no ponto intermediário 1 (km/h) |
| `i2_speed` | Velocidade no ponto intermediário 2 (km/h) |
| `st_speed` | Velocidade na armadilha de velocidade (km/h) |
| `is_pit_out_lap` | Booleano |
| `date_start` | Tempo aproximado de início da volta (UTC) |
| `segments_sector_1` | Códigos de cores dos mini-setores (array) |
| `segments_sector_2` | Códigos de cores dos mini-setores (array) |
| `segments_sector_3` | Códigos de cores dos mini-setores (array) |

**Códigos de Segmento:**
- `0` - Não disponível
- `2048` - Amarelo
- `2049` - Verde
- `2051` - Roxo
- `2064` - Pit lane
- `2050, 2052, 2068` - Desconhecido

**Nota:** Segmentos não estão disponíveis para corridas e podem não corresponder sempre às cores da transmissão.

---

### 7. Localização — `/location`
**Descrição:** Posição aproximada do carro na pista em ~3,7 Hz

**Exemplo de Consulta:**
```
/location?session_key=9161&driver_number=81&date>2023-09-16T13:03:35.200&date<2023-09-16T13:03:35.800
```

**Filtros Disponíveis:**
- `session_key`, `driver_number`, `date`

**Campos de Resposta:**
- `x` - Coordenada X (Cartesiana 3D)
- `y` - Coordenada Y (Cartesiana 3D)
- `z` - Coordenada Z (Cartesiana 3D)
- `date` - Timestamp
- `driver_number` - Número de corrida do piloto
- `meeting_key` - Identificador da reunião
- `session_key` - Identificador da sessão

**Nota:** Fornece progresso ao longo da pista mas não posição lateral. Origem (0, 0, 0) é arbitrária.

---

### 8. Reuniões — `/meetings`
**Descrição:** Grand Prix ou fins de semana de testes (atualizado diariamente à meia-noite UTC)

**Exemplo de Consulta:**
```
/meetings?year=2026&country_name=Singapore
```

**Filtros Disponíveis:**
- `year`, `country_name`, `meeting_key`, `circuit_key`, e outros

**Campos de Resposta:**

**Identidade:**
- `meeting_key` - Identificador da reunião
- `meeting_name` - Nome da reunião
- `meeting_official_name` - Nome oficial
- `year` - Ano
- `is_cancelled` - Booleano

**Localização:**
- `location` - Nome da localização
- `circuit_key` - Identificador do circuito
- `circuit_short_name` - Nome abreviado do circuito
- `circuit_type` - Tipo (Permanente, Temporário - Rua, Temporário - Estrada)
- `country_key` - Identificador do país
- `country_code` - Código do país
- `country_name` - Nome do país
- `gmt_offset` - Fuso horário GMT

**Cronograma:**
- `date_start` - Data de início (UTC)
- `date_end` - Data de término (UTC)

**Mídia:**
- `circuit_image` - URL da imagem do circuito
- `country_flag` - URL da bandeira
- `circuit_info_url` - URL de dados do MultiViewer

---

### 9. Ultrapassagens — `/overtakes`
**Descrição:** Trocas de posição entre pilotos (apenas corridas, pode estar incompleto)

**Exemplo de Consulta:**
```
/overtakes?session_key=9636&overtaking_driver_number=63&overtaken_driver_number=4&position=1
```

**Filtros Disponíveis:**
- `session_key`, `overtaking_driver_number`, `overtaken_driver_number`, `position`, `date`

**Campos de Resposta:**
- `overtaking_driver_number` - Piloto que ultrapassou
- `overtaken_driver_number` - Piloto que foi ultrapassado
- `position` - Posição do ultrapassador após a ultrapassagem (começa em 1)
- `date` - Timestamp
- `session_key` - Identificador da sessão
- `meeting_key` - Identificador da reunião

**Nota:** Inclui mudanças de posição de pit stops e penalidades pós-corrida.

---

### 10. Pit — `/pit`
**Descrição:** Passagens pela pit lane

**Exemplo de Consulta:**
```
/pit?session_key=9877&stop_duration<2.3
```

**Filtros Disponíveis:**
- `session_key`, `driver_number`, `lap_number`, `stop_duration`, `lane_duration`, `date`

**Campos de Resposta:**
- `lane_duration` - Tempo na pit lane (segundos)
- `stop_duration` - Tempo parado (segundos, disponível a partir do GP EUA 2024)
- `pit_duration` - **Descontinuado**, idêntico a `lane_duration`
- `lap_number` - Número da volta
- `driver_number` - Número de corrida do piloto
- `date` - Timestamp
- `session_key` - Identificador da sessão
- `meeting_key` - Identificador da reunião

---

### 11. Posição — `/position`
**Descrição:** Posições de pilotos em execução ao longo do tempo

**Exemplo de Consulta:**
```
/position?meeting_key=1217&driver_number=40&position<=3
```

**Filtros Disponíveis:**
- `meeting_key`, `driver_number`, `position`, `session_key`, `date`

**Campos de Resposta:**
- `position` - Posição do piloto (começa em 1)
- `driver_number` - Número de corrida do piloto
- `date` - Timestamp
- `session_key` - Identificador da sessão
- `meeting_key` - Identificador da reunião

---

### 12. Controle de Corrida — `/race_control`
**Descrição:** Status da sessão, bandeiras, safety car, penalidades e eventos de controle da corrida

**Exemplo de Consulta:**
```
/race_control?flag=BLACK AND WHITE&driver_number=1&date>=2023-01-01&date<2023-09-01
```

**Filtros Disponíveis:**
- `flag`, `driver_number`, `date`, `session_key`, `lap_number`, `category`

**Campos de Resposta:**
| Campo | Descrição |
|---|---|
| `category` | Tipo de evento (SessionStatus, CarEvent, Drs, Flag, SafetyCar, etc.) |
| `flag` | Tipo de bandeira (GREEN, YELLOW, DOUBLE YELLOW, CHEQUERED, BLACK AND WHITE, etc.) |
| `scope` | Escopo (Track, Driver, Sector, etc.) |
| `sector` | Mini-setor onde o evento ocorreu (começa em 1) |
| `lap_number` | Volta da corrida |
| `qualifying_phase` | 1, 2, ou 3 em qualificação; null caso contrário |
| `message` | Descrição legível por humanos |
| `date` | Timestamp |
| `session_key` | Identificador da sessão |

---

### 13. Sessões — `/sessions`
**Descrição:** Sessões dentro de uma reunião (treino livre, qualificação, sprint, corrida, etc., atualizado diariamente à meia-noite UTC)

**Exemplo de Consulta:**
```
/sessions?country_name=Belgium&session_name=Sprint%20Qualifying&year=2023
```

**Filtros Disponíveis:**
- `year`, `country_name`, `session_name`, `session_type`, `date_start`, `date_end`, e outros

**Campos de Resposta:**

**Identidade:**
- `session_key` - Identificador da sessão
- `session_name` - Nome da sessão
- `session_type` - Tipo de sessão
- `meeting_key` - Identificador da reunião
- `year` - Ano
- `is_cancelled` - Booleano

**Localização:**
- `circuit_key` - Identificador do circuito
- `circuit_short_name` - Nome abreviado do circuito
- `location` - Nome da localização
- `country_key` - Identificador do país
- `country_code` - Código do país
- `country_name` - Nome do país
- `gmt_offset` - Fuso horário GMT

**Cronograma:**
- `date_start` - Tempo de início da sessão (UTC)
- `date_end` - Tempo de término da sessão (UTC)

---

### 14. Resultado da Sessão — `/session_result`
**Descrição:** Classificação final de uma sessão (publicado alguns minutos após os resultados oficiais)

**Exemplo de Consulta:**
```
/session_result?session_key=7782&position<=3
```

**Filtros Disponíveis:**
- `session_key`, `position`, `driver_number`, `dnf`, `dns`, `dsq`

**Campos de Resposta:**
- `position` - Posição final
- `driver_number` - Número de corrida do piloto
- `meeting_key` - Identificador da reunião
- `session_key` - Identificador da sessão
- `duration` - Melhor volta (treino livre/qualificação) ou tempo total da corrida em segundos. Em qualificação, array de três valores [Q1, Q2, Q3]
- `gap_to_leader` - Diferença em segundos ou `+N LAP(S)`. Em qualificação, array [Q1, Q2, Q3]
- `number_of_laps` - Número de voltas completadas
- `dnf` - Booleano (Did Not Finish) - apenas qualificação e corrida
- `dns` - Booleano (Did Not Start) - apenas qualificação e corrida
- `dsq` - Booleano (Desqualificado)

---

### 15. Grade de Largada — `/starting_grid`
**Descrição:** Ordem de largada para a próxima corrida (publicado alguns minutos após os resultados oficiais)

**Exemplo de Consulta:**
```
/starting_grid?session_key=7783&position<=3
```

**Filtros Disponíveis:**
- `session_key`, `position`, `driver_number`

**Campos de Resposta:**
- `position` - Posição na grade
- `driver_number` - Número de corrida do piloto
- `lap_duration` - Tempo de volta de qualificação (segundos)
- `meeting_key` - Identificador da reunião
- `session_key` - Identificador da sessão

---

### 16. Stints — `/stints`
**Descrição:** Períodos de execução contínua com um jogo de pneus

**Exemplo de Consulta:**
```
/stints?session_key=9165&tyre_age_at_start>=3
```

**Filtros Disponíveis:**
- `session_key`, `driver_number`, `compound`, `tyre_age_at_start`, `stint_number`, `lap_start`, `lap_end`

**Campos de Resposta:**
- `compound` - Composto dos pneus (SOFT, MEDIUM, HARD, etc.)
- `stint_number` - Número do stint (começa em 1)
- `lap_start` - Primeira volta do stint
- `lap_end` - Última volta do stint
- `tyre_age_at_start` - Voltas já nos pneus no início do stint
- `driver_number` - Número de corrida do piloto
- `meeting_key` - Identificador da reunião
- `session_key` - Identificador da sessão

---

### 17. Rádio da Equipe — `/team_radio`
**Descrição:** Gravações selecionadas de rádio piloto-equipe

**Exemplo de Consulta:**
```
/team_radio?session_key=9158&driver_number=11
```

**Filtros Disponíveis:**
- `session_key`, `driver_number`, `date`

**Campos de Resposta:**
- `recording_url` - Link MP3 para gravação de rádio
- `date` - Timestamp
- `driver_number` - Número de corrida do piloto
- `meeting_key` - Identificador da reunião
- `session_key` - Identificador da sessão

**Nota:** Cobertura é limitada e controlada pela F1. A maioria dos eventos de 2026+ não possui dados disponíveis.

---

### 18. Clima — `/weather`
**Descrição:** Condições da pista e ar (atualizado a cada minuto)

**Exemplo de Consulta:**
```
/weather?meeting_key=1208&wind_direction>=130&track_temperature>=52
```

**Filtros Disponíveis:**
- `meeting_key`, `wind_direction`, `track_temperature`, `date`, e outros

**Campos de Resposta:**
| Campo | Unidade / Notas |
|---|---|
| `air_temperature` | °C |
| `track_temperature` | °C |
| `humidity` | % (porcentagem) |
| `pressure` | mbar |
| `rainfall` | Indicador de chuva |
| `wind_speed` | m/s (metros por segundo) |
| `wind_direction` | Graus (0-359) |
| `date` | Timestamp |
| `meeting_key` | Identificador da reunião |
| `session_key` | Identificador da sessão |

---

## Padrões de Uso Comum

### Encadeando Consultas
A maioria dos endpoints aceitam `meeting_key` e `session_key`. Fluxo típico:

1. Consulte `/meetings` para encontrar um `meeting_key`
2. Consulte `/sessions` para encontrar um `session_key`
3. Consulte endpoints de dados com o `session_key`

Exemplo:
```bash
# Obter GP de Singapura 2024
/meetings?year=2024&country_name=Singapore

# Obter sessão de corrida para essa reunião
/sessions?meeting_key=1234&session_type=Race

# Obter dados de posição para a corrida
/position?session_key=5678
```

### Consultas Baseadas em Tempo
Use `date` com operadores de comparação para filtrar por intervalo de tempo:

```
/car_data?session_key=9161&date>=2023-09-16T13:00:00&date<2023-09-16T14:00:00
```

### Exportar para CSV
Adicione `csv=true` a qualquer URL para receber CSV em vez de JSON:

```
/sessions?year=2023&csv=true
```

### Exemplo de Encadeamento de Dados
Fluxo típico para analisar uma corrida específica:

```
1. GET /meetings?year=2024&country_name=Monaco
   → Extrair meeting_key = 1205

2. GET /sessions?meeting_key=1205&session_type=Race
   → Extrair session_key = 5678

3. GET /drivers?session_key=5678
   → Obter todos os pilotos na sessão

4. GET /session_result?session_key=5678
   → Obter resultados finais da corrida

5. GET /laps?session_key=5678&driver_number=1
   → Obter dados de voltas de um piloto específico

6. GET /car_data?session_key=5678&driver_number=1
   → Obter dados de telemetria
```

---

## Exemplos de Clientes

A API OpenF1 fornece exemplos em múltiplas linguagens:

### cURL
```bash
curl "https://api.openf1.org/v1/drivers?session_key=9158"
```

### Python
```python
import urllib.request

url = "https://api.openf1.org/v1/drivers?session_key=9158"
with urllib.request.urlopen(url) as response:
    data = response.read()
```

Com pandas:
```python
import pandas as pd

url = "https://api.openf1.org/v1/drivers?session_key=9158"
df = pd.read_json(url)
```

### JavaScript
```javascript
fetch('https://api.openf1.org/v1/drivers?session_key=9158')
  .then(response => response.json())
  .then(data => console.log(data));
```

### R
```r
library(httr)
library(jsonlite)

url <- "https://api.openf1.org/v1/drivers?session_key=9158"
response <- GET(url)
data <- fromJSON(content(response, "text"))
```

---

## Notas Importantes

### Campos Descontinuados
Os seguintes campos estão marcados para remoção após a temporada de 2026:
- `country_code` em pilotos
- `pit_duration` em pit (use `lane_duration` em seu lugar)

### Limitações de Dados
- **Dados em tempo real:** Requer assinatura; a camada gratuita possui apenas dados históricos (2023+)
- **Rádio da Equipe:** Cobertura é limitada e controlada pela F1. A maioria dos eventos de 2026+ não possui dados.
- **Segmentos:** Cores de mini-setores não estão disponíveis para corridas e podem não corresponder às cores da transmissão
- **Ultrapassagens:** Pode estar incompleto

### Tratamento de Erros
A documentação da API não especifica códigos de erro ou formatos de resposta de erro. Monitore códigos de status HTTP e respostas com cuidado.

---

## Recursos Adicionais

- **Documentação Oficial:** https://openf1.org/docs/
- **URL Base:** `https://api.openf1.org/v1/`
- **Fonte de Dados:** Dados oficiais de Fórmula 1 a partir de 2023
