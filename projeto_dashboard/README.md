# Dashboard de Segmentação de Clientes

Dashboard desenvolvido com Streamlit para explorar os segmentos de clientes identificados em uma etapa anterior de clusterização.

A aplicação não treina modelos, não recria clusters e não aplica pré-processamento. Ela apenas comunica os resultados já presentes no arquivo `customer_segmentation.csv`.

## Estrutura do projeto

```text
project/
├── app.py
├── customer_segmentation.csv
├── requirements.txt
└── README.md
```

## Instalação

Crie e ative um ambiente virtual, se desejar. Depois instale as dependências:

```bash
pip install -r requirements.txt
```

## Como executar

Na pasta do projeto, execute:

```bash
streamlit run app.py
```

O navegador abrirá automaticamente. Se isso não acontecer, acesse o endereço exibido no terminal.
