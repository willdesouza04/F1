# Cliente de Dados F1

Bem-vindo à documentação do Cliente de Dados F1! Esta é uma biblioteca Python e ferramenta de linha de comando para acessar dados históricos da Fórmula 1 da [API OpenF1](https://www.openf1.org/).

## Funcionalidades

- **Cliente HTTP Síncrono**: Um wrapper simples e síncrono ao redor da API OpenF1
- **Ferramenta CLI**: Consulte dados de F1 diretamente do seu terminal
- **Dados JSON Brutos**: Trabalhe com dicionários e JSON diretamente — sem esquemas pesados
- **Python 3.13+**: Construído para a versão mais recente do Python
- **Totalmente Testado**: Cobertura de testes de 50%+

## Links Rápidos

- **[Começando](getting-started.md)** — Instale e execute sua primeira consulta
- **[Arquitetura](architecture.md)** — Entenda a estrutura do projeto
- **[Referência da API](api-reference.md)** — Documentação completa dos endpoints
- **[Guia de Desenvolvimento](development.md)** — Configure seu ambiente de desenvolvimento

## O que é OpenF1?

[OpenF1](https://www.openf1.org/) fornece dados históricos de Fórmula 1 incluindo:
- Reuniões (corridas e sessões)
- Pilotos e equipes
- Tempos de volta e telemetria
- Dados do carro e posicionamento

Os dados estão disponíveis a partir de 2023.

## Exemplo Rápido

=== "Biblioteca"

    ```python
    from f1 import OpenF1Client
    
    client = OpenF1Client()
    meetings = client.get_meetings(year=2024)
    for meeting in meetings:
        print(f"{meeting['meeting_name']}")
    ```

=== "CLI"

    ```bash
    f1 meetings --year 2024
    ```

---

**Python 3.13+** | **Licença MIT** | [GitHub](https://github.com)
