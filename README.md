# Análise Estatística de Homicídios Intencionais - UNODC

## Descrição do Projeto

Este projeto foi desenvolvido para a disciplina de Tópicos Especiais em Computação e tem como objetivo realizar uma análise estatística completa de um dataset da UNODC (United Nations Office on Drugs and Crime) relacionado a homicídios intencionais ao redor do mundo.

A análise foi realizada utilizando Python e bibliotecas voltadas para ciência de dados, estatística e visualização, buscando identificar padrões, tendências e informações relevantes sobre os índices de homicídios em diferentes países, regiões e sub-regiões.

Além da análise estatística, o projeto também conta com uma aplicação interativa desenvolvida com Streamlit para exploração de regressões e visualizações dos dados.

---

## Estrutura do Projeto

```bash
.
├── .gitignore
├── app.py
├── AP1_Analise_Estatistica.ipynb
└── README.md
```

### Arquivos principais

#### `AP1_Analise_Estatistica.ipynb`
Notebook principal contendo:

- Limpeza e tratamento dos dados
- Análises estatísticas descritivas
- Visualizações gráficas
- Regressões
- Respostas das perguntas propostas pelo professor
- Exploração dos padrões de homicídios no dataset

#### `app.py`
Aplicação desenvolvida com Streamlit para:

- Exploração interativa dos dados
- Visualização gráfica
- Análises de regressão
- Comparações entre países e regiões
- Interação dinâmica com o dataset

---

## Dataset

O dataset utilizado foi disponibilizado pela UNODC e contém informações sobre homicídios intencionais em diversos países ao longo dos anos.

Os dados incluem:

- Número de homicídios
- Homicídios femininos
- Regiões e sub-regiões
- Indicadores estatísticos
- Séries temporais

---

## Perguntas Respondidas

O notebook responde às seguintes questões propostas:

1. Quais países apresentam os 10 maiores índices de homicídios nos últimos 5 anos?
2. Quais países apresentam os 10 maiores índices de homicídios de mulheres em 2022?
3. Quais as regiões com mais homicídios?
4. Quais países possuem o menor número de homicídios em cada sub-região?
5. Quais países possuem o menor número de mortes de mulheres?
6. Quais as sub-regiões com maior número de homicídios?
7. Identifique o país com maior número de homicídios em cada continente em 2020
8. Qual o país mais violento para as mulheres em 2021?
9. Qual o país com maior valor do indicador `Victims of intentional homicide`?
10. Qual a média de homicídios no Brasil nos últimos 10 anos?

---

## Tecnologias Utilizadas

### Linguagem

- Python

### Bibliotecas principais

- Pandas
- NumPy
- Matplotlib
- Plotly
- Streamlit
- Scikit-learn
- SciPy

---

## Análises Realizadas

Durante o desenvolvimento do projeto foram realizadas:

- Limpeza e tratamento de dados
- Estatística descritiva
- Análise exploratória de dados (EDA)
- Correlação entre variáveis
- Regressão linear
- Visualização de tendências temporais
- Comparações entre países e regiões
- Análise de homicídios femininos

---

## Como Executar o Projeto

## 1. Clone o repositório

```bash
git clone https://github.com/devjuliolandim/trabalho-1-topicos.git
```

## 2. Acesse a pasta do projeto

```bash
cd trabalho-1-topicos
```

## 3. Instale as dependências

```bash
pip install -r requirements.txt
```

---

## Executando o Notebook

Para abrir o notebook:

```bash
jupyter notebook
```

Depois abra:

```bash
AP1_Analise_Estatistica.ipynb
```

---

## Executando a Aplicação Streamlit

Execute o comando:

```bash
streamlit run app.py
```

A aplicação será aberta automaticamente no navegador.

---

## Objetivo Acadêmico

O principal objetivo deste trabalho é aplicar conceitos de:

- Estatística
- Ciência de Dados
- Visualização de Dados
- Regressão
- Manipulação de datasets reais
- Desenvolvimento de aplicações interativas

Além disso, o projeto busca demonstrar como análises estatísticas podem ser utilizadas para compreender fenômenos sociais complexos, como a violência e os homicídios intencionais ao redor do mundo.

---

## Possíveis Melhorias Futuras

- Adicionar mais modelos de regressão
- Implementar previsões temporais
- Melhorar a interface do Streamlit
- Adicionar filtros mais avançados
- Criar dashboards interativos
- Incorporar novos datasets relacionados à violência

---

## Autores

Júlio César Saldanha Landim
Nathan Dias Cunha
Christian Ximenes Paiva
Messias Trajano Barbosa
Alex Ehrich Sousa de Menezes
Jefferson de Aguiar Sousa

Projeto desenvolvido para a disciplina de Tópicos Especiais em Computação.

