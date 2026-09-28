# Segmentação de Clientes com Clusterização

Projeto de Machine Learning não supervisionado desenvolvido para identificar diferentes perfis de clientes a partir de características demográficas, comportamento de compra e padrões de consumo.

O projeto percorre todo o fluxo de uma solução de clusterização: preparação dos dados, construção e comparação de diferentes algoritmos, otimização, interpretação dos clusters e disponibilização dos resultados por meio de um dashboard interativo desenvolvido com Streamlit.

---

## 🎯 Objetivo do projeto

Uma empresa deseja abandonar campanhas de marketing genéricas e adotar estratégias mais personalizadas para diferentes perfis de consumidores.

O objetivo deste projeto é utilizar técnicas de **Clusterização** para identificar automaticamente grupos de clientes com características e comportamentos semelhantes.

Como requisito de negócio, a segmentação final deve possuir:

**3 perfis de clientes.**

Dessa forma, o projeto busca responder perguntas como:

- Quais perfis de clientes existem na base?
- Como esses grupos se diferenciam em renda, consumo e comportamento de compra?
- Quais canais são mais utilizados por cada segmento?
- Como os segmentos respondem às campanhas de marketing?
- Como essas informações podem apoiar estratégias de marketing mais personalizadas?

---

## 📂 Estrutura do projeto

```text
segmentacao-clientes/
│
├── dataset/
│   └── marketing_campaign.csv
│
├── notebook/
│   └── projeto_segmentacao_clientes.ipynb
│
├── projeto_dashboard/
│   ├── app.py
│   ├── customer_segmentation.csv
│   ├── requirements.txt
│   └── README.md
│
└── README.md
```

### `dataset/`

Contém o dataset original utilizado no projeto.

### `notebook/`

Contém todo o desenvolvimento do projeto de Ciência de Dados e Machine Learning, desde a análise inicial dos dados até a seleção e interpretação do modelo final.

### `projeto_dashboard/`

Contém a aplicação desenvolvida com **Streamlit** para exploração dos resultados da segmentação.

O dashboard utiliza o arquivo `customer_segmentation.csv`, gerado ao final do notebook.

---

## 📊 Dataset

O projeto utiliza o dataset **Customer Personality Analysis**, contendo informações sobre características dos clientes, comportamento de compra, produtos consumidos, canais utilizados e respostas às campanhas de marketing.

Entre as informações disponíveis estão:

- ano de nascimento;
- escolaridade;
- estado civil;
- renda;
- presença de crianças e adolescentes na residência;
- recência da última compra;
- gastos por categoria de produto;
- compras pela Web;
- compras por catálogo;
- compras em lojas físicas;
- compras realizadas com desconto;
- visitas ao site;
- respostas às campanhas de marketing.

---

## 🔎 Preparação dos dados

Antes da aplicação dos algoritmos de clusterização, os dados passam por etapas de preparação e análise.

Entre os principais procedimentos realizados estão:

- análise da estrutura do dataset;
- tratamento de valores ausentes;
- investigação de valores inconsistentes e outliers;
- remoção de atributos sem relevância para a modelagem;
- seleção das características utilizadas na clusterização;
- criação de novas características;
- padronização das variáveis.

Algumas das características construídas ao longo do projeto incluem:

- `Age`
- `Children`
- `Total_Spent`
- `Total_Purchases`
- `Customer_Tenure_Days`

Como os algoritmos utilizados são fortemente influenciados pelas distâncias entre as observações, as características utilizadas na modelagem são padronizadas antes da clusterização.

---

## 🤖 Algoritmos de Clusterização

São explorados três algoritmos de Machine Learning não supervisionado.

### K-Means

Algoritmo baseado em centroides que busca dividir as observações em grupos minimizando as distâncias internas de cada cluster.

Como o negócio exige três perfis de clientes, utilizamos:

```python
n_clusters = 3
```

### DBSCAN

Algoritmo baseado em densidade capaz de identificar regiões densas e também observações consideradas ruído.

Os principais hiperparâmetros explorados são:

- `eps`
- `min_samples`

Como o DBSCAN não recebe diretamente a quantidade de clusters desejada, são analisadas configurações capazes de produzir **3 clusters válidos**, respeitando o requisito de negócio.

### Clusterização Hierárquica

Algoritmo que constrói os agrupamentos progressivamente por meio da união de observações e clusters.

O projeto utiliza a abordagem hierárquica aglomerativa e explora diferentes critérios de ligação (*linkage*).

A quantidade final permanece:

```python
n_clusters = 3
```

---

## 📏 Avaliação dos modelos

Como não existem rótulos verdadeiros indicando previamente a qual segmento cada cliente pertence, a avaliação utiliza principalmente métricas internas de clusterização.

### Silhouette Score

Avalia simultaneamente a coesão dentro dos clusters e a separação entre diferentes clusters.

Quanto **maior**, melhor.

### Davies-Bouldin Index

Avalia a similaridade entre os clusters considerando sua dispersão interna e separação.

Quanto **menor**, melhor.

Além das métricas, também são analisados:

- quantidade de clientes por cluster;
- equilíbrio entre os grupos;
- presença de clusters muito pequenos;
- percentual de ruído no DBSCAN.

---

## ⚙️ Otimização

Após a construção e avaliação dos modelos iniciais, diferentes configurações de hiperparâmetros são exploradas.

O requisito de **3 clusters permanece fixo durante todo o processo** e não é tratado como um hiperparâmetro a ser otimizado.

São explorados:

**K-Means**
- `init`
- `n_init`

**Clusterização Hierárquica**
- `linkage`
- `metric`

As configurações são comparadas utilizando principalmente **Silhouette Score**, **Davies-Bouldin Index**, distribuição dos clientes e, quando aplicável, percentual de ruído.

---

## 📉 Visualização com PCA

Como os modelos trabalham com múltiplas características simultaneamente, é utilizado **Principal Component Analysis (PCA)** para reduzir os dados para duas dimensões e facilitar a visualização dos agrupamentos.

O PCA é utilizado exclusivamente como recurso de visualização.

Os algoritmos continuam sendo treinados utilizando o conjunto completo de características selecionadas para a modelagem.

---

## 🏆 Seleção do modelo final

A escolha do modelo final não considera apenas uma única métrica.

São analisados conjuntamente:

- Silhouette Score;
- Davies-Bouldin Index;
- distribuição dos clientes;
- presença de clusters muito pequenos;
- percentual de ruído;
- visualização com PCA;
- aderência ao requisito de negócio.

Essa abordagem permite selecionar uma segmentação que seja não apenas matematicamente adequada, mas também útil para o contexto do problema.

---

## 👥 Interpretação dos clusters

Após a seleção do modelo final, os clusters deixam de ser analisados apenas como identificadores numéricos e passam a ser interpretados sob a perspectiva do negócio.

São analisadas características como:

- idade;
- renda;
- recência;
- gasto total;
- quantidade de compras;
- presença de filhos;
- categorias de produtos consumidos;
- canais de compra;
- resposta às campanhas.

Variáveis que não participaram diretamente da formação dos clusters também podem ser utilizadas posteriormente para ajudar na caracterização dos segmentos.

A partir dessas análises, os três clusters são transformados em **perfis de clientes com significado para o negócio**, permitindo propor estratégias de marketing específicas para cada segmento.

---

## 📊 Dashboard com Streamlit

Depois da análise e interpretação dos clusters, o resultado da segmentação é exportado para:

```text
customer_segmentation.csv
```

Esse arquivo é utilizado como fonte de dados do dashboard desenvolvido com **Streamlit**.

O dashboard não realiza novamente o treinamento dos modelos.

Seu objetivo é transformar os resultados da análise em uma aplicação interativa que possa ser utilizada para explorar os segmentos encontrados.

O fluxo final do projeto pode ser representado por:

```text
Dataset
   ↓
Notebook
   ↓
Preparação dos dados
   ↓
Clusterização
   ↓
Avaliação e otimização
   ↓
Interpretação dos segmentos
   ↓
customer_segmentation.csv
   ↓
Dashboard Streamlit
```

---

## 📈 Funcionalidades do dashboard

A aplicação permite explorar os resultados da segmentação por meio de:

- filtro por segmento;
- total de clientes;
- renda média;
- gasto médio;
- média de compras;
- distribuição dos clientes por segmento;
- comparação das características dos segmentos;
- comportamento de compra por canal;
- taxa de resposta à última campanha.

Os gráficos são construídos utilizando **Plotly**, permitindo uma exploração interativa dos resultados.

---

## 🛠️ Tecnologias utilizadas

- Python
- Pandas
- NumPy
- Scikit-learn
- SciPy
- Matplotlib
- Plotly
- Streamlit
- Jupyter Notebook

---

## ▶️ Executando o dashboard

Acesse a pasta da aplicação:

```bash
cd projeto_dashboard
```

Crie um ambiente virtual:

```bash
python -m venv .venv
```

### Windows

Ative o ambiente:

```bash
.venv\Scripts\activate
```

### macOS / Linux

```bash
source .venv/bin/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Execute a aplicação:

```bash
streamlit run app.py
```

Após a inicialização, o Streamlit disponibilizará a aplicação no navegador.

Por padrão:

```text
http://localhost:8501
```

---

## 💡 Principais aprendizados

Este projeto demonstra que clusterização vai além de simplesmente executar um algoritmo.

Uma solução completa envolve:

1. compreender o problema de negócio;
2. preparar adequadamente os dados;
3. selecionar características relevantes;
4. construir diferentes algoritmos de clusterização;
5. avaliar a qualidade dos agrupamentos;
6. otimizar os hiperparâmetros;
7. comparar as soluções;
8. interpretar os clusters;
9. transformar os resultados em segmentos de negócio;
10. disponibilizar os insights por meio de uma aplicação interativa.

> **O melhor agrupamento não é necessariamente aquele que apresenta isoladamente a melhor métrica, mas aquele que produz segmentos coerentes com os dados e úteis para o objetivo do negócio.**

---

## 📌 Contexto

Projeto desenvolvido como parte de um estudo prático sobre **Clusterização e Segmentação de Clientes**, demonstrando a aplicação de técnicas de Machine Learning não supervisionado desde a preparação dos dados até a construção de um produto de dados com Streamlit.
