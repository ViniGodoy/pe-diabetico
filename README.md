# Analisador de Desempenho (Pré e Pós-Intervenção)

Este script Python foi desenvolvido para analisar o impacto de uma intervenção educacional ou experimental com base nas respostas de questionários estruturados aplicados antes (pré) e depois (pós) do evento.

O script valida as respostas em relação a um gabarito pré-definido, calcula métricas estatísticas descritivas, executa testes de hipóteses não-paramétricos para avaliar o ganho de aprendizado e gera gráficos de dispersão para visualização dos resultados.

Projeto de pesquisa realizado para o curso de Especialização de Enfermagem em Estomaterapia, da PUCPR.

Pesquisadoras:
- Daiane Caetano Cano
- Natalia Aparecida Sokulski 
- Thais Adriane Leão de Mendonça
- Valéria Machado Ramalho

Orientação de:
- Rosenilda Rodrigues dos Santos
- Ana Rotilia Erzinger 

## Propósito e Funcionalidades

* **Processamento de Dados**: Lê respostas de um arquivo CSV, mapeando e comparando dinamicamente as colunas de sufixo `-a` (antes) e `-d` (depois) contra um gabarito estruturado.
* **Ordenação Inteligente**: Ordena chaves de questões alfanuméricas de forma natural (ex: `q1-1`, `q1-2`, `q10-1`).
* **Análise Estatística**:
* Métricas descritivas (Média, Mediana e Desvio Padrão) para os momentos pré e pós.
* Aplicação do **Teste de Wilcoxon (Matched-Pairs Signed-Rank Test)** para determinar a significância estatística das mudanças observadas no score geral e em uma questão específica de controle (Questão 8).


* **Visualização de Dados**: Gera gráficos de dispersão lado a lado salvos em formato PNG, destacando a média e a banda de desvio padrão das amostras.

## Bibliotecas Utilizadas

O script faz uso do ecossistema padrão de ciência de dados em Python:

* **`pandas`**: Utilizada para carregar a base de dados (`respostas.csv`) e iterar sobre as linhas para tabulação das respostas.
* **`statistics`**: Integrada nativamente no Python, é usada para calcular a média, mediana e desvio padrão amostral (`stdev`).
* **`scipy.stats` (`wilcoxon`)**: Fornece o teste estatístico não-paramétrico adequado para amostras pareadas/dependentes, avaliando se a diferença entre os momentos é estatisticamente significante.
* **`matplotlib.pyplot`**: Responsável pela renderização e exportação dos gráficos de dispersão lado a lado.
* **`numpy`**: Utilizada para manipulação de arrays (como a geração do índice de alunos via `arange`) e cálculo de médias e desvios padrão para a plotagem gráfica.

## Estrutura do Arquivo de Entrada

O script espera um arquivo chamado `respostas.csv` no mesmo diretório de execução. O arquivo deve conter obrigatoriamente:

1. Uma coluna identificadora chamada `numero` (numeração do participante/aluno).
2. Colunas pareadas com os sufixos `-a` (antes) e `-d` (depois) para cada chave presente no dicionário `gabarito`.

Exemplo de estrutura do `respostas.csv`:

```csv
numero,q1-1-a,q1-1-d,q1-2-a,q1-2-d,q1-3-a,q1-3-d
1,s,s,n,s,n,n
2,n,s,s,s,s,n
3,s,s,n,n,n,n

```

## Como Executar

### Pré-requisitos

Certifique-se de ter o Python 3 instalado juntamente com as dependências do projeto. Você pode instalar as bibliotecas necessárias via `pip`:

```bash
pip install pandas scipy matplotlib numpy

```

### Execução

Com o arquivo `respostas.csv` posicionado no mesmo diretório do script, execute o comando:

```bash
python nome_do_seu_script.py

```

## Artefatos Gerados

Ao finalizar a execução, além das saídas detalhadas no console contendo os logs de acertos por aluno, estatísticas descritivas e o *p-value* dos testes de Wilcoxon, o script salvará duas imagens no diretório corrente:

1. `dispersao_lado_a_lado.png`: Gráfico comparativo do total de acertos geral (Antes vs. Depois) com suas respectivas linhas de média e áreas de desvio padrão.
2. `dispersao_questao8.png`: Gráfico específico detalhando a performance dos alunos na Questão 8, isolando o comportamento pré e pós-intervenção para esta variável controlada.

