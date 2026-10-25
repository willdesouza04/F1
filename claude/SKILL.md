# SKILL.md — Padrões de Desenvolvimento Python

## Visão Geral

Este documento estabelece os padrões obrigatórios de engenharia de software para projetos Python, incluindo gerenciamento de dependências, isolamento do ambiente, qualidade de código, testes automatizados, cobertura mínima e documentação técnica.

A skill orienta a IA de desenvolvimento na criação, configuração, manutenção, validação e documentação de projetos de maneira autônoma, consistente e verificável.

---

## 1. Gerenciamento da Versão do Python com Pyenv

### Responsabilidades

O Pyenv é a ferramenta exclusivamente responsável pela seleção e controle da versão local do Python utilizada no projeto. Não substitui o Poetry no gerenciamento de dependências e ambientes virtuais.

### Requisitos Obrigatórios

#### 1.1 Verificação Prévia do Pyenv

Antes de configurar qualquer aspecto de versão Python, a IA deverá:

- Verificar se o Pyenv está instalado e funcionando corretamente no sistema.
- Listar as versões disponíveis localmente.
- Confirmar a capacidade de instalar novas versões quando necessário.
- Identificar qualquer problema na configuração do Pyenv que possa impedir seu uso.

Caso o Pyenv não esteja disponível, a IA deverá informar claramente que a configuração não pode prosseguir e orientar sobre a instalação.

#### 1.2 Seleção de Versão Estável

A IA deverá:

- Identificar uma versão estável do Python compatível com o projeto e suas dependências.
- Priorizar versões mantidas ativamente (não descontinuadas).
- Validar que a versão selecionada não possui limitações conhecidas para as ferramentas utilizadas no projeto.
- Documentar claramente qual versão foi selecionada e por quê.

#### 1.3 Instalação da Versão Selecionada

A IA deverá:

- Verificar se a versão selecionada está já instalada no Pyenv.
- Instalar a versão quando necessário, utilizando os mecanismos padrão do Pyenv.
- Confirmar que a instalação foi bem-sucedida antes de prosseguir.

#### 1.4 Definição da Versão Local

A IA deverá:

- Definir a versão local do Python por meio do Pyenv, afetando especificamente o diretório raiz do projeto e seus subdiretórios.
- Criar ou atualizar o arquivo `.python-version` na raiz do projeto.
- Garantir que o arquivo `.python-version` esteja versionado no Git.
- Validar que o interpretador Python utilizado corresponde à versão definida no Pyenv.

#### 1.5 Compatibilidade com pyproject.toml

A IA deverá:

- Verificar as restrições de versão declaradas no campo `python` do `pyproject.toml`.
- Garantir que a versão selecionada pelo Pyenv é compatível com essas restrições.
- Atualizar as restrições no `pyproject.toml` se necessário, sempre justificando a mudança.

#### 1.6 Validação Contínua

A IA deverá:

- Executar comandos Python críticos utilizando explicitamente o interpretador gerenciado pelo Pyenv.
- Verificar periodicamente que o interpretador utilizado corresponde à versão configurada.
- Avisar caso qualquer discrepância seja detectada.

#### 1.7 Prevenção de Inconsistências

A IA deverá:

- Evitar usar Python global ou versões não gerenciadas pelo Pyenv.
- Garantir que ambientes de desenvolvimento, testes e execução utilizem a mesma versão.
- Documentar claramente qualquer desvio necessário.

---

## 2. Gerenciamento de Dependências e Ambientes Virtuais com Poetry

### Responsabilidades

O Poetry é a ferramenta oficial e obrigatória para gerenciar dependências e ambientes virtuais. É a interface exclusiva para instalação, adição, remoção e atualização de pacotes.

### Requisitos Obrigatórios

#### 2.1 Arquivo pyproject.toml como Centro de Configuração

O `pyproject.toml` é o arquivo central de configuração. A IA deverá:

- Utilizar o `pyproject.toml` como fonte única de verdade para configuração do projeto.
- Manter nele as definições de metadados, dependências, versão do Python e configurações de ferramentas.
- Nunca editar manualmente o arquivo de lock; alterações devem ser feitas via Poetry.
- Garantir que o `pyproject.toml` segue a especificação PEP 518 / PEP 621.

#### 2.2 Arquivo poetry.lock e Reprodutibilidade

A IA deverá:

- Manter o `poetry.lock` atualizado após qualquer alteração de dependências.
- Versionar o `poetry.lock` no Git para garantir reprodutibilidade exata.
- Nunca editar manualmente o arquivo de lock.
- Executar `poetry lock` quando o `pyproject.toml` for alterado, garantindo que as alterações são refletidas no lock.

#### 2.3 Ambiente Virtual Dentro do Projeto

A IA deverá:

- Configurar o Poetry para criar o ambiente virtual preferencialmente no diretório do projeto.
- Utilizar a convenção `.venv` para o diretório do ambiente virtual.
- Validar que o ambiente virtual foi criado no local esperado.
- Garantir que o ambiente virtual funciona corretamente e que as ferramentas conseguem utilizá-lo.

#### 2.4 Instalação de Todas as Dependências no Ambiente Virtual

A IA deverá:

- Garantir que todas as dependências de produção são instaladas no ambiente virtual gerenciado pelo Poetry.
- Garantir que todas as ferramentas de desenvolvimento (lint, formatação, testes, documentação) são instaladas como dependências de desenvolvimento no ambiente virtual.
- Impedir absolutamente a instalação direta de dependências do projeto no ambiente global do Python.
- Utilizar `poetry install` para instalar o projeto no ambiente virtual durante o setup.

#### 2.5 Separação Clara de Dependências

A IA deverá:

- Manter dependências de produção explicitamente separadas das dependências de desenvolvimento.
- Documentar claramente qual ferramenta é dependência de desenvolvimento (Ruff, Pytest, MkDocs, etc.).
- Configurar o Poetry para instalar apenas dependências de produção quando o projeto for empacotado para distribuição.

#### 2.6 Utilização do Poetry para Gerenciamento de Dependências

Qualquer alteração em dependências deverá:

- Ser feita exclusivamente através dos comandos do Poetry (adicionar, remover, atualizar).
- Ser acompanhada de verificação de compatibilidade.
- Resultar em atualização automática do `poetry.lock`.
- Nunca envolver edição manual do `pyproject.toml` ou do `poetry.lock` sem explicação técnica clara.

#### 2.7 Compatibilidade Entre Ferramentas

A IA deverá:

- Verificar a compatibilidade entre a versão do Python selecionada, as versões das dependências e a versão do Poetry utilizada.
- Avisar caso incompatibilidades conhecidas sejam detectadas.
- Atualizar versões quando necessário para resolver conflitos.

#### 2.8 Reprodução do Ambiente

A IA deverá:

- Garantir que qualquer pessoa desenvolvedora consegue reproduzir o ambiente utilizando apenas o `pyproject.toml` e o `poetry.lock` versionados.
- Validar a reprodução criando um novo ambiente virtual e instalando dependências.
- Informar claramente as etapas necessárias para reprodução.

#### 2.9 Ignorância do Ambiente Virtual no Git

A IA deverá:

- Garantir que o diretório `.venv` (ou equivalente) é ignorado pelo Git.
- Manter no controle de versão os arquivos necessários à reprodução: `pyproject.toml`, `poetry.lock` e `.python-version`.

---

## 3. Estrutura e Organização do Projeto

### Responsabilidades

A estrutura de projeto deve ser organizada, modular e escalável, utilizando a abordagem `src/` para separação clara entre código de produção, testes e outros artefatos.

### Requisitos Obrigatórios

#### 3.1 Localização do Código de Produção

A IA deverá:

- Manter o código de produção em `src/projeto/`, onde `projeto` é o nome real do pacote Python.
- Garantir que o pacote é descoberto corretamente pelas ferramentas (pytest, pip, ferramentas de cobertura).
- Configurar o `pyproject.toml` para indicar corretamente a localização do código de produção.

#### 3.2 Localização dos Testes

A IA deverá:

- Manter testes automatizados em um diretório separado do código de produção.
- Organizar testes unitários e de integração de maneira coerente com a complexidade do projeto.
- Garantir que os testes são descobertos automaticamente pelo Pytest.

#### 3.3 Documentação Técnica

A IA deverá:

- Manter documentação técnica em `docs/`.
- Organizar páginas de documentação em Markdown dentro de `docs/`.
- Garantir que a estrutura de documentação é clara e hierarquizada.

#### 3.4 Configuração Centralizada

A IA deverá:

- Centralizar configurações de ferramentas no `pyproject.toml` quando houver suporte adequado.
- Manter arquivos de configuração específicos (ex: `mkdocs.yml`) em locais padronizados e documentados.

#### 3.5 Separação Clara de Responsabilidades

A IA deverá:

- Manter separados: código de produção, testes, documentação, configurações e artefatos gerados.
- Evitar diretórios, módulos e arquivos desnecessários.
- Documentar a função de cada diretório principal na raiz do projeto.

#### 3.6 Inspeção Prévia de Estrutura Existente

Antes de propor ou realizar alterações estruturais, a IA deverá:

- Inspecionar a estrutura atual do projeto.
- Avaliar a complexidade e o propósito de cada diretório.
- Propor mudanças apenas quando houver justificativa clara.
- Comunicar o impacto de eventual migração de estrutura.

#### 3.7 Avaliação de Impacto de Migrações

Quando uma migração de estrutura for necessária, a IA deverá:

- Identificar todas as importações que precisam ser atualizadas.
- Atualizar caminhos em configurações de ferramentas (pytest, coverage, mkdocs).
- Garantir que dependências internas continuam funcionando.
- Testar completa e rigorosamente após a migração.

#### 3.8 Coerência com o Sistema de Empacotamento

A IA deverá:

- Garantir que a estrutura é consistente com o sistema de empacotamento Python.
- Validar que o pacote pode ser instalado corretamente via Poetry.
- Garantir que ferramentas como Pytest e Coverage descobrem corretamente os módulos.

---

## 4. Lint e Formatação com Ruff

### Responsabilidades

O Ruff é a ferramenta oficial para análise estática, lint e formatação do código Python. Garante consistência, qualidade e conformidade com as práticas recomendadas.

### Requisitos Obrigatórios

#### 4.1 Configuração no pyproject.toml

A IA deverá:

- Configurar o Ruff exclusivamente no `pyproject.toml` sob a seção `[tool.ruff]`.
- Definir explicitamente todas as opções de configuração necessárias.
- Manter a configuração versionada no Git.

#### 4.2 Largura de Linha Padronizada

A IA deverá:

- Definir a largura de linha padronizada em 88 caracteres (padrão amplamente adotado).
- Garantir coerência entre o formatador e a análise de lint.
- Documentar qualquer desvio da largura padrão com justificativa técnica.

#### 4.3 Seleção e Configuração de Regras

A IA deverá:

- Configurar regras de lint de acordo com as necessidades do projeto.
- Priorizar qualidade, legibilidade e práticas recomendadas do Python.
- Incluir regras que detectem: erros comuns, imports não utilizados, problemas de qualidade e violações de padrões.
- Documentar qualquer regra desabilitada com justificativa técnica.

#### 4.4 Compatibilidade com Versão de Python

A IA deverá:

- Garantir que a configuração do Ruff é compatível com a versão de Python selecionada.
- Validar que as regras selecionadas são apropriadas para a versão.

#### 4.5 Evitar Exceções Indiscriminadas

A IA deverá:

- Evitar exceções e supressões de regras sem justificativa técnica clara.
- Documentar explicitamente qualquer exceção, incluindo arquivo, linha e motivo.
- Corrigir problemas em vez de simplesmente desabilitar verificações.

#### 4.6 Correção Automática vs. Revisão Manual

A IA deverá:

- Distinguir problemas que Ruff pode corrigir automaticamente de forma segura daqueles que exigem análise técnica manual.
- Utilizar `ruff check --fix` apenas para correções seguras.
- Revisar manualmente correções potencialmente arriscadas.
- Validar qualidade do código após qualquer correção automática.

#### 4.7 Execução no Ambiente Virtual

A IA deverá:

- Executar todas as verificações de lint dentro do ambiente virtual gerenciado pelo Poetry.
- Garantir que o Ruff e suas dependências estão instaladas corretamente.
- Utilizar explicitamente o Ruff do ambiente virtual.

#### 4.8 Falha Obrigatória em Problemas de Qualidade

A IA deverá:

- Garantir que a validação final não é considerada concluída enquanto houver falhas no lint.
- Interromper processos de validação quando problemas de lint são detectados.
- Corrigir todos os problemas antes de considerar a tarefa concluída.

#### 4.9 Relatório de Resultados

A IA deverá:

- Informar claramente quais problemas foram detectados.
- Indicar quantos problemas de lint foram encontrados.
- Registrar se todos os problemas foram corrigidos.

---

## 5. Testes Automatizados com Pytest

### Responsabilidades

O Pytest é o framework padrão para testes automatizados. O pytest-cov é utilizado para medição da cobertura de código.

### Requisitos Obrigatórios

#### 5.1 Criação de Testes Unitários

A IA deverá:

- Criar testes unitários para módulos e componentes relevantes do projeto.
- Priorizar testes para funcionalidades críticas, regras de negócio e comportamentos complexos.
- Evitar testes artificiais que não adicionem valor.

#### 5.2 Separação de Testes do Código de Produção

A IA deverá:

- Manter testes em diretório separado do código de produção.
- Organizar estrutura de diretórios de testes de forma coerente com a organização do código.
- Garantir que testes não são instalados como parte do pacote de produção.

#### 5.3 Convenções de Descoberta do Pytest

A IA deverá:

- Seguir as convenções de descoberta de testes do Pytest (nomes de arquivos, classes e funções).
- Garantir que arquivos de teste começam com `test_` ou terminam com `_test.py`.
- Garantir que funções de teste começam com `test_`.
- Validar que o Pytest consegue descobrir automaticamente todos os testes.

#### 5.4 Utilização de Fixtures

A IA deverá:

- Utilizar fixtures do Pytest quando necessário para preparar e reutilizar dados e dependências de teste.
- Organizar fixtures em conftest.py quando apropriado.
- Documentar a responsabilidade e o escopo de cada fixture.

#### 5.5 Cobertura de Cenários

A IA deverá:

- Cobrir cenários de sucesso (happy path).
- Cobrir cenários de falha e exceções esperadas.
- Cobrir casos de borda e situações limite.
- Evitar testes redundantes que não agregam valor.

#### 5.6 Isolamento de Dependências Externas

A IA deverá:

- Isolar dependências externas quando apropriado, incluindo: APIs, bancos de dados, serviços remotos e sistemas de arquivos.
- Utilizar mocks, stubs ou fixtures para simular comportamentos externos.
- Garantir que testes não dependem de serviços reais sendo executados.
- Documentar explicitamente quando um teste depende de um recurso externo.

#### 5.7 Testes Robustos e Reproduzíveis

A IA deverá:

- Evitar testes frágeis que quebram facilmente com alterações menores.
- Evitar dependência da ordem de execução de testes.
- Garantir que testes são reproduzíveis e determinísticos.
- Executar testes múltiplas vezes para confirmar estabilidade.

#### 5.8 Execução no Ambiente Virtual

A IA deverá:

- Executar todos os testes dentro do ambiente virtual gerenciado pelo Poetry.
- Garantir que o Pytest e suas dependências estão instaladas corretamente.

#### 5.9 Testes com Funcionalidades

A IA deverá:

- Criar ou atualizar testes sempre que funcionalidades são adicionadas ou alteradas.
- Validar que testes existentes continuam passando após modificações.
- Refatorar testes quando sua manutenção se torna problemática.

#### 5.10 Evitar Alterações Artificiais

A IA deverá:

- Não alterar código de produção exclusivamente para aumentar cobertura de testes.
- Não criar testes que validam implementação em vez de comportamento.
- Focar em testes que adicionam valor real.

### 5.1 Cobertura Mínima Obrigatória de 50%

#### 5.1.1 Requisitos de Cobertura

A cobertura de testes deverá ser de, no mínimo, 50% do código de produção localizado em `src/projeto/`.

A IA deverá:

- Configurar a medição de cobertura por meio do pytest-cov e Coverage.py.
- Limitar a medição exclusivamente ao código de produção relevante do projeto (excluir testes, utilitários de desenvolvimento, etc.).
- Garantir que a configuração funciona corretamente com a estrutura `src/`.
- Definir um limite mínimo de cobertura que provoca falha automática na execução quando não é atingido.

#### 5.1.2 Relatório Detalhado de Cobertura

A IA deverá:

- Exibir os arquivos e as linhas não cobertos no relatório de execução.
- Gerar relatório em formato legível que identifica claramente as lacunas de cobertura.
- Incluir percentual total de cobertura no resultado.

#### 5.1.3 Definição de Métrica

A IA deverá:

- Definir explicitamente se a métrica utilizada considera linhas de código, branches ou ambas.
- Manter a métrica consistente ao longo do projeto.
- Documentar a definição utilizada.

#### 5.1.4 Sem Redução Arbitrária do Limite

A IA deverá:

- Nunca reduzir o limite mínimo para acomodar testes insuficientes.
- Aumentar a cobertura de testes quando necessário para atingir 50%.
- Justificar qualquer desvio do limite obrigatório.

#### 5.1.5 Sem Exclusão Arbitrária de Módulos

A IA deverá:

- Não excluir módulos relevantes da medição sem justificativa técnica clara.
- Documentar explicitamente qualquer exclusão.
- Considerar alternativas antes de excluir módulos.

#### 5.1.6 Apresentação de Resultados Reais

A IA deverá:

- Apresentar os resultados reais da cobertura ao concluir a validação.
- Indicar se a cobertura mínima de 50% foi atingida.
- Listar arquivos com baixa cobertura.

#### 5.1.7 Condição de Aprovação

A execução de testes é considerada aprovada somente quando:

- Todos os testes passam sem erros.
- A cobertura atinge ou supera 50%.
- Ambas as condições são validadas explicitamente.

---

## 6. Documentação com MkDocs Material

### Responsabilidades

O MkDocs Material é a solução padrão para criação e manutenção da documentação técnica do projeto. Garante documentação estruturada, acessível e mantida.

### Requisitos Obrigatórios

#### 6.1 Instalação de MkDocs e Material

A IA deverá:

- Instalar o MkDocs por meio do Poetry como dependência de desenvolvimento.
- Instalar o tema Material para MkDocs como dependência de desenvolvimento.
- Instalar todas as dependências necessárias para suportar recursos do Material.
- Validar que a instalação foi bem-sucedida verificando versão e funcionalidade.

#### 6.2 Configuração de MkDocs

A IA deverá:

- Manter a configuração principal da documentação em um arquivo de configuração na raiz do projeto.
- Configurar explicitamente: título do projeto, URL do site, estrutura de navegação, tema e extensões.
- Validar que a configuração segue o formato esperado pelo MkDocs.
- Manter a configuração versionada no Git.

#### 6.3 Armazenamento de Documentação

A IA deverá:

- Armazenar todas as páginas de documentação em formato Markdown dentro de `docs/`.
- Organizar páginas em subdiretórios quando apropriado para complexidade e estrutura.
- Manter nomes de arquivos descritivos e consistentes.

#### 6.4 Configuração do Tema Material

A IA deverá:

- Configurar o tema Material com navegação clara e organizada.
- Definir estrutura de navegação que reflita hierarquia lógica do projeto.
- Ativar recursos relevantes do Material (busca, ícones, etc.).
- Garantir que o tema funciona corretamente em modo claro e escuro.

#### 6.5 Página Inicial

A IA deverá:

- Criar página inicial (index.md) com visão geral do projeto.
- Incluir propósito, objetivos e funcionalidades principais.
- Fornecer links para seções relevantes de documentação.
- Garantir que a página inicial é atrativa e informativa.

#### 6.6 Documentação de Procedimentos

A IA deverá:

- Documentar procedimentos de instalação do projeto.
- Documentar procedimentos de configuração inicial.
- Documentar como executar o projeto.
- Documentar como contribuir ao desenvolvimento.

#### 6.7 Documentação de Validação

A IA deverá:

- Documentar como executar testes.
- Documentar como verificar qualidade do código.
- Documentar quais são os critérios de validação obrigatórios.
- Documentar como reproduzir o ambiente de desenvolvimento.

#### 6.8 Documentação de Arquitetura

A IA deverá:

- Registrar arquitetura de alto nível do projeto.
- Documentar responsabilidades dos principais módulos.
- Descrever fluxo de dados e interações entre componentes quando relevante.
- Incluir diagramas quando adicionarem clareza.

#### 6.9 Alinhamento com Implementação

A IA deverá:

- Manter documentação sempre alinhada com implementação real.
- Atualizar documentação quando funcionalidades mudam.
- Revisar documentação periodicamente para verificar precisão.
- Remover ou corrigir documentação desatualizada.

#### 6.10 Qualidade de Documentação

A IA deverá:

- Evitar páginas vazias ou placeholders.
- Evitar links quebrados.
- Evitar informações desatualizadas ou contraditórias.
- Verificar ortografia e gramática.

#### 6.11 Idioma Padrão

A IA deverá:

- Adotar português do Brasil como idioma padrão para toda documentação.
- Utilizar outro idioma apenas quando houver necessidade específica documentada.

#### 6.12 Validação de Documentação em Modo Estrito

A IA deverá:

- Construir documentação em modo estrito do MkDocs.
- Tratar erros e avisos como falhas que impedem aprovação.
- Garantir que a documentação constrói sem erros ou avisos.
- Interromper processos de validação se a documentação falhar.

#### 6.13 Distinção Entre Geração Local e Publicação

A IA deverá:

- Separar procedimento de geração local da documentação de sua eventual publicação.
- Reconhecer que publicação depende de infraestrutura específica do projeto.
- Não presumir publicação automática a menos que explicitamente configurada.

---

## 7. Configuração Centralizada e Dependências de Desenvolvimento

### Responsabilidades

Todas as dependências e suas configurações devem ser organizadas de forma coerente e centralizada.

### Requisitos Obrigatórios

#### 7.1 Separação de Dependências

A IA deverá:

- Manter dependências de produção explicitamente separadas de dependências de desenvolvimento.
- Indicar claramente qual categoria cada dependência pertence.
- Garantir que dependências de desenvolvimento não são incluídas em distribuições de produção.

#### 7.2 Dependências de Desenvolvimento Obrigatórias

Toda dependência de desenvolvimento obrigatória deverá ser instalada. A IA deverá:

- Incluir Ruff para lint e formatação.
- Incluir Pytest para testes automatizados.
- Incluir pytest-cov para medição de cobertura.
- Incluir MkDocs para documentação.
- Incluir MkDocs Material para tema de documentação.

#### 7.3 Centralização de Configurações

A IA deverá:

- Centralizar configurações de ferramentas no `pyproject.toml` quando houver suporte adequado.
- Manter configurações de Ruff, Pytest, Coverage e outras ferramentas no `pyproject.toml`.
- Manter em arquivo separado apenas configurações que `pyproject.toml` não suporte (ex: `mkdocs.yml`).

#### 7.4 Compatibilidade de Versão

A IA deverá:

- Manter restrições de compatibilidade do Python explícitas no campo `python` do `pyproject.toml`.
- Garantir que configurações de ferramentas são compatíveis com as versões utilizadas.
- Validar compatibilidade entre versões de Poetry, dependências e Python.
- Documentar qualquer versão pinada com motivo técnico.

#### 7.5 Evitar Dependências Redundantes

A IA deverá:

- Evitar incluir dependências redundantes.
- Evitar ferramentas com funcionalidades sobrepostas.
- Manter apenas as ferramentas explicitamente necessárias.
- Documentar justificativa para cada dependência.

#### 7.6 Consistência de Lock File

A IA deverá:

- Garantir que `poetry.lock` corresponde exatamente às dependências declaradas.
- Executar `poetry lock` quando `pyproject.toml` é modificado.
- Nunca mergear código com `poetry.lock` desatualizado.

#### 7.7 Instalações Globais vs. Ambientes Virtuais

A IA deverá:

- Nunca utilizar instalações globais de Python como substituto de dependências no projeto.
- Garantir que todas as dependências são instaladas no ambiente virtual do Poetry.
- Verificar que ferramentas são executadas a partir do ambiente virtual.

#### 7.8 Adição Justificada de Dependências

A IA deverá:

- Adicionar dependências apenas quando houver necessidade técnica clara.
- Documentar o motivo da adição.
- Considerar alternativas antes de adicionar nova dependência.
- Avaliar trade-offs de complexidade vs. benefício.

#### 7.9 Coerência Entre Ferramentas

A IA deverá:

- Garantir coerência entre gerenciador de dependências, estrutura do pacote, ferramentas de qualidade, testes e documentação.
- Validar que todas as ferramentas trabalham em conjunto sem conflitos.
- Resolver incompatibilidades antes de considerar a configuração concluída.

---

## 8. Controle de Versão e Arquivos Ignorados

### Responsabilidades

Aplicar boas práticas de controle de versão específicas para projetos Python.

### Requisitos Obrigatórios

#### 8.1 Ignorar Ambiente Virtual

O `.gitignore` deverá:

- Ignorar o diretório `.venv` (ou qualquer outro diretório de ambiente virtual).
- Garantir que arquivos do ambiente virtual não sejam versionados.

#### 8.2 Ignorar Caches e Artefatos Temporários

O `.gitignore` deverá:

- Ignorar arquivos de cache do Python (`__pycache__/`, `*.pyc`, `.pytest_cache/`).
- Ignorar caches de ferramentas (`ruff_cache/`, `.ruff_cache/`).
- Ignorar diretórios temporários de testes e cobertura (`.coverage`, `htmlcov/`, `.pytest_cache/`).
- Ignorar diretórios gerados por empacotamento (`dist/`, `build/`, `*.egg-info/`).
- Ignorar site de documentação gerado (`site/`).

#### 8.3 Ignorar Credenciais e Segredos

O `.gitignore` deverá:

- Impedir versionamento acidental de credenciais.
- Ignorar arquivos de variáveis de ambiente locais (`.env`, `.env.local`).
- Ignorar arquivos de chaves privadas ou segredos.
- Documentar padrões ignorados relacionados a segurança.

#### 8.4 Preservar Arquivos de Configuração Necessários

A IA deverá:

- Versionar arquivos de configuração necessários à reprodução do projeto.
- Versionar `pyproject.toml`, `poetry.lock`, `.python-version`.
- Versionar `mkdocs.yml` ou equivalente.
- Versionar qualquer configuração compartilhada de ferramentas.

#### 8.5 Avaliação Específica do Projeto

A IA deverá:

- Avaliar necessidades específicas do projeto antes de adicionar regras de exclusão.
- Considerar se exclusões podem impedir reprodução ou desenvolvimento.
- Documentar exceções e justificativas.

#### 8.6 Evitar Exclusão de Arquivos Críticos

A IA deverá:

- Não excluir arquivos necessários à construção, testes ou instalação.
- Não excluir configurações essenciais.
- Revisar `.gitignore` antes de comprometer mudanças.

---

## 9. Processo Obrigatório de Validação

### Responsabilidades

Estabelecer sequência de validação que seja reproduzível localmente e adaptável à integração contínua.

### Requisitos Obrigatórios

#### 9.1 Sequência Obrigatória de Validação

A IA deverá executar validações nesta ordem:

1. Verificação da versão do Python selecionada pelo Pyenv.
2. Verificação da disponibilidade e configuração do ambiente virtual gerenciado pelo Poetry.
3. Instalação e validação das dependências declaradas.
4. Execução do lint com Ruff.
5. Verificação da formatação com Ruff.
6. Execução dos testes automatizados com Pytest.
7. Medição da cobertura com pytest-cov e validação do limite mínimo de 50%.
8. Construção e validação estrita da documentação com MkDocs Material.

#### 9.2 Execução no Ambiente Virtual

A IA deverá:

- Executar todas as ferramentas dentro do ambiente virtual do Poetry.
- Garantir que nenhuma ferramenta utiliza versão global.
- Verificar explicitamente que ferramentas são executadas corretamente.

#### 9.3 Unificação de Critérios

A IA deverá:

- Utilizar os mesmos critérios de qualidade no desenvolvimento local e na integração contínua.
- Garantir que um código que falha localmente também falhará na CI.
- Evitar discrepâncias de ambiente que causem diferenças de comportamento.

#### 9.4 Interrupção em Falhas Obrigatórias

A IA deverá:

- Interromper imediatamente a validação quando qualquer etapa obrigatória falhar.
- Não continuar com etapas subsequentes após falha.
- Registrar a etapa que falhou e o motivo.

#### 9.5 Correção Antes de Conclusão

A IA deverá:

- Corrigir todos os problemas identificados antes de considerar a tarefa concluída.
- Não declarar sucesso enquanto houver problemas pendentes.
- Re-executar validações após correções.

#### 9.6 Registro de Resultados

A IA deverá:

- Registrar explicitamente os resultados de cada etapa.
- Indicar quais etapas foram executadas com sucesso.
- Indicar quais etapas falharam e por quê.
- Apresentar dados quantitativos quando disponíveis (cobertura, número de problemas, etc.).

#### 9.7 Sem Validação Falsa

A IA deverá:

- Nunca declarar uma etapa como aprovada sem executá-la.
- Não simular execução de ferramentas.
- Não contar com resultados em cache quando revalidação é necessária.

#### 9.8 Transparência em Bloqueios

A IA deverá:

- Informar claramente as etapas que não puderam ser executadas.
- Explicar as razões de qualquer impossibilidade técnica.
- Sugerir ações corretivas quando possível.

#### 9.9 Reprodutibilidade de Validação

A IA deverá:

- Fornecer informações suficientes para que outra pessoa consiga reproduzir a validação.
- Documentar versões de ferramentas utilizadas.
- Descrever etapas executadas.
- Indicar quaisquer desvios do processo padrão.

---

## 10. Integração Contínua

### Responsabilidades

Preparar o projeto para integração contínua adaptada à infraestrutura disponível.

### Requisitos Obrigatórios

#### 10.1 Suporte a GitHub Actions

Quando o projeto utilizar GitHub Actions, a IA deverá:

- Criar ou atualizar workflows que executem automaticamente as verificações obrigatórias.
- Incluir todos os passos de validação descritos na seção 9.
- Garantir que o workflow segue a mesma sequência e critérios de desenvolvimento local.

#### 10.2 Seleção de Versão do Python

O workflow de CI deverá:

- Selecionar a versão do Python definida no `.python-version`.
- Utilizar a versão correta em todos os passos do pipeline.
- Falhar se a versão não estiver disponível.

#### 10.3 Instalação do Poetry

O workflow deverá:

- Instalar o Poetry de maneira controlada e compatível.
- Verificar que a instalação foi bem-sucedida.
- Utilizar versão estável do Poetry.

#### 10.4 Instalação de Dependências

O workflow deverá:

- Instalar dependências a partir dos arquivos versionados (`pyproject.toml` e `poetry.lock`).
- Garantir que ambiente virtual é criado e utilizado.
- Falhar se há divergências entre arquivo de lock e especificação.

#### 10.5 Execução de Validações

O workflow deverá:

- Executar lint com Ruff.
- Executar verificação de formatação com Ruff.
- Executar testes com Pytest.
- Executar medição de cobertura.
- Construir documentação em modo estrito.

#### 10.6 Falha em Etapas Obrigatórias

O workflow deverá:

- Interromper imediatamente quando qualquer etapa obrigatória falhar.
- Não continuar com etapas subsequentes.
- Reportar claramente qual etapa falhou.

#### 10.7 Unificação de Critérios com Desenvolvimento Local

A IA deverá:

- Garantir que critérios no workflow correspondem aos critérios de validação local.
- Evitar diferenças que causem código passar localmente mas falhar em CI.
- Revisar workflow periodicamente para manter sincronização.

#### 10.8 Não Presumir GitHub Actions

A IA deverá:

- Não introduzir infraestrutura de CI desnecessária em projetos que não a utilizam.
- Adaptar instruções à plataforma de CI específica do projeto.
- Documentar configuração de CI apropriada.

#### 10.9 Sem Infraestrutura CI Desnecessária

A IA deverá:

- Questionar necessidade de CI em projetos pequenos ou sem requisitos específicos.
- Não configurar CI automaticamente em todos os projetos.
- Documentar quando e por que CI é necessária.

---

## 11. Regras Operacionais da IA

### Responsabilidades

Orientar a IA a seguir regras claras durante execução de tarefas de desenvolvimento.

### Requisitos Obrigatórios

#### 11.1 Inspeção Prévia

A IA deverá:

- Inspecionar arquivos e configurações existentes antes de realizar alterações.
- Ler código, configurações e documentação relevantes.
- Entender estado atual do projeto antes de propor mudanças.

#### 11.2 Identificação de Tecnologias e Estrutura

A IA deverá:

- Identificar a versão do Python utilizada.
- Identificar o gerenciador de dependências e sua configuração.
- Identificar a estrutura atual do projeto.
- Documentar suas descobertas.

#### 11.3 Preservação de Validade

A IA deverá:

- Preservar funcionalidades válidas e existentes.
- Preservar configurações que funcionam.
- Não descartar trabalho já realizado sem motivo técnico.

#### 11.4 Evitar Sobrescrita Cega

A IA deverá:

- Nunca sobrescrever arquivos sem analisar seu conteúdo primeiro.
- Backup ou documentar alterações em arquivos críticos.
- Justificar qualquer modificação substancial.

#### 11.5 Verificação de Compatibilidade

A IA deverá:

- Verificar compatibilidade entre ferramentas, versões e configurações.
- Identificar incompatibilidades antes de implementar mudanças.
- Resolver conflitos de versão apropriadamente.

#### 11.6 Utilização de Poetry

A IA deverá:

- Utilizar Poetry para executar todos os comandos Python do projeto.
- Respeitar ambiente virtual gerenciado pelo Poetry.
- Evitar alterações globais ao Python sem autorização explícita.

#### 11.7 Correção de Causas Raiz

A IA deverá:

- Corrigir a causa dos problemas, não apenas ocultar os sintomas.
- Investigar por que um teste falha antes de desabilitá-lo.
- Resolver conflitos de dependência, não apenas ignorá-los.

#### 11.8 Sem Desabilitação de Verificações

A IA deverá:

- Não desabilitar verificações para fazer testes passarem.
- Não reduzir critérios de qualidade arbitrariamente.
- Não ignorar alertas de lint sem justificativa técnica.

#### 11.9 Sem Falsificação de Resultados

A IA deverá:

- Nunca falsificar ou simular resultados de validação.
- Não declarar sucesso sem executar verificações reais.
- Informar resultados genuínos, ainda que negativos.

#### 11.10 Comunicação Transparente

A IA deverá:

- Informar as alterações realizadas.
- Informar as validações executadas e seus resultados.
- Explicar eventuais bloqueios, incompatibilidades ou limitações.
- Fornecer recomendações de próximos passos.

#### 11.11 Propostas de Migração Segura

Quando a estrutura existente divergir dos padrões, a IA deverá:

- Propor migrações de forma segura.
- Comunicar impactos e riscos.
- Executar migrações passo a passo com validação.
- Validar completamente após migração.

#### 11.12 Adaptação à Complexidade

A IA deverá:

- Adaptar decisões à complexidade do projeto.
- Evitar abstrações desnecessárias.
- Evitar adicionar dependências sem valor.
- Manter simplicidade quando apropriado.

#### 11.13 Criação e Manutenção de Testes

A IA deverá:

- Criar testes adequados para funcionalidades implementadas.
- Manter testes durante refatorações.
- Atualizar testes quando código muda.
- Garantir que cobertura se mantém acima de 50%.

---

## 12. Critérios de Aceitação

Todos os seguintes critérios são verificáveis e obrigatórios:

- [ ] Pyenv está instalado e utilizado para selecionar a versão local do Python.
- [ ] Arquivo `.python-version` foi criado e está versionado no Git.
- [ ] Poetry está configurado e é utilizado para gerenciar dependências.
- [ ] Ambiente virtual foi configurado preferencialmente dentro do projeto (`.venv`).
- [ ] Todas as dependências (produção e desenvolvimento) estão instaladas no ambiente virtual do Poetry.
- [ ] `pyproject.toml` está devidamente configurado e contém todas as dependências.
- [ ] `poetry.lock` existe, é consistente com `pyproject.toml` e está versionado.
- [ ] Estrutura de código utiliza abordagem `src/projeto/`.
- [ ] Código de produção está em `src/projeto/`.
- [ ] Testes estão em diretório separado e são descobertos pelo Pytest.
- [ ] Ruff está configurado para lint e formatação no `pyproject.toml`.
- [ ] Ruff executa sem erros e sem problemas de formatação.
- [ ] Pytest está configurado para executar testes.
- [ ] Todos os testes passam sem erros.
- [ ] pytest-cov está configurado para medir cobertura.
- [ ] Cobertura de testes atinge ou supera 50% do código em `src/projeto/`.
- [ ] Documentação existe em `docs/` em formato Markdown.
- [ ] MkDocs Material está instalado e configurado.
- [ ] Documentação constrói em modo estrito sem erros ou avisos.
- [ ] `.gitignore` ignora ambiente virtual, caches e artefatos temporários.
- [ ] Dependências de produção e desenvolvimento estão claramente separadas.
- [ ] Processo de validação está documentado e é reproduzível.
- [ ] Todos os passos de validação (Python, Poetry, lint, testes, cobertura, documentação) executam com sucesso.
- [ ] GitHub Actions (se aplicável) está configurado para executar as mesmas validações.
- [ ] Nenhuma validação foi falsificada ou simulada.
- [ ] Resultados reais de validação foram registrados e reportados.

---

## 13. Checklist de Implementação

Utilize esta checklist para verificar se todos os requisitos foram atendidos:

### Setup Inicial
- [ ] Versão do Python identificada e instalada via Pyenv
- [ ] Arquivo `.python-version` criado e versionado
- [ ] Poetry instalado e funcionando
- [ ] Ambiente virtual criado em `.venv`
- [ ] Dependências iniciais instaladas

### Estrutura de Projeto
- [ ] Código de produção em `src/projeto/`
- [ ] Testes em diretório apropriado
- [ ] Documentação em `docs/`
- [ ] `pyproject.toml` configurado e versionado
- [ ] `poetry.lock` criado e versionado

### Qualidade de Código
- [ ] Ruff configurado no `pyproject.toml`
- [ ] Lint passa sem problemas
- [ ] Formatação passa sem problemas
- [ ] Regras de Ruff documentadas

### Testes Automatizados
- [ ] Pytest configurado
- [ ] pytest-cov instalado e configurado
- [ ] Testes escritos e funcionando
- [ ] Cobertura medida e >= 50%
- [ ] Relatório de cobertura gerado

### Documentação
- [ ] MkDocs e Material instalados
- [ ] Configuração de MkDocs criada
- [ ] Páginas de documentação escritas
- [ ] Documentação constrói em modo estrito
- [ ] Sem erros ou avisos na documentação

### Controle de Versão
- [ ] `.gitignore` configurado apropriadamente
- [ ] Ambiente virtual ignorado
- [ ] Caches ignorados
- [ ] Credenciais ignoradas
- [ ] Arquivos críticos versionados

### Validação
- [ ] Processo de validação documentado
- [ ] Validação local executa com sucesso
- [ ] Todos os passos validados
- [ ] Resultados reportados

### Integração Contínua (se aplicável)
- [ ] Workflow de CI criado (se necessário)
- [ ] CI executa mesmas validações que local
- [ ] CI falha apropriadamente em problemas
- [ ] Documentação de CI mantida

### Documentação de Projeto
- [ ] SKILL.md mantido atualizado
- [ ] Instruções de desenvolvimento claras
- [ ] Instruções de validação claras
- [ ] Contribuições documentadas

---

## Notas Finais

Este documento estabelece um padrão consolidado para desenvolvimento Python. A IA deve:

- Consultar este documento quando dúvidas surgirem.
- Manter este documento atualizado conforme a evolução do projeto.
- Comunicar qualquer incompatibilidade entre requisitos e realidade do projeto.
- Propor ajustes fundamentados quando limitações técnicas forem identificadas.
- Sempre priorizar qualidade, reprodutibilidade e manutenibilidade.

O cumprimento destes requisitos garante projetos Python bem estruturados, testados, documentados e prontos para colaboração e evolução.
