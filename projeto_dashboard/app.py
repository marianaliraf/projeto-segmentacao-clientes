import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(
    page_title="Dashboard de Segmentação de Clientes",
    layout="wide",
)

TEMPLATE_GRAFICO = "plotly_white"
CORES_SEGMENTOS = ["#2563EB", "#10B981", "#F59E0B", "#8B5CF6"]
CORES_CANAIS = ["#2563EB", "#14B8A6", "#F97316"]

st.markdown(
    """
    <style>
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    h1 {
        color: #1F2937;
        letter-spacing: -0.03em;
    }

    h2, h3 {
        color: #374151;
    }

    div[data-testid="stMetric"] {
        background-color: #111827;
        border: 1px solid #1F2937;
        border-radius: 14px;
        padding: 18px 20px;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.18);
    }

    div[data-testid="stMetricLabel"],
    div[data-testid="stMetricLabel"] p,
    div[data-testid="stMetricLabel"] label {
        color: #E5E7EB !important;
    }

    div[data-testid="stMetricValue"],
    div[data-testid="stMetricValue"] div {
        color: #FFFFFF !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def carregar_dados(caminho_arquivo: str) -> pd.DataFrame:
    return pd.read_csv(caminho_arquivo)


try:
    df = carregar_dados("customer_segmentation.csv")
except FileNotFoundError:
    st.error(
        "Arquivo customer_segmentation.csv não encontrado. "
        "Coloque o CSV na mesma pasta do app.py."
    )
    st.stop()


st.title("Dashboard de Segmentação de Clientes")
st.write(
    "Explore os perfis de clientes identificados por meio de técnicas de "
    "clusterização e analise diferenças de comportamento entre os segmentos."
)


if "Segment_Name" not in df.columns:
    st.error("A coluna Segment_Name não foi encontrada no CSV.")
    st.stop()


st.sidebar.header("Filtros")

segmentos = sorted(df["Segment_Name"].dropna().unique())
segmento_selecionado = st.sidebar.selectbox(
    "Segmento",
    ["Todos"] + segmentos,
)

if segmento_selecionado == "Todos":
    df_filtrado = df.copy()
else:
    df_filtrado = df[df["Segment_Name"] == segmento_selecionado].copy()


col1, col2, col3, col4 = st.columns(4)

total_clientes = len(df_filtrado)
renda_media = df_filtrado["Income"].mean() if "Income" in df_filtrado.columns else None
gasto_medio = (
    df_filtrado["Total_Spent"].mean()
    if "Total_Spent" in df_filtrado.columns
    else None
)
compras_medias = (
    df_filtrado["Total_Purchases"].mean()
    if "Total_Purchases" in df_filtrado.columns
    else None
)

col1.metric("Total de Clientes", f"{total_clientes:,}".replace(",", "."))
col2.metric(
    "Renda Média",
    f"R$ {renda_media:,.2f}" if renda_media is not None else "Não disponível",
)
col3.metric(
    "Gasto Médio",
    f"R$ {gasto_medio:,.2f}" if gasto_medio is not None else "Não disponível",
)
col4.metric(
    "Compras Médias",
    f"{compras_medias:.1f}" if compras_medias is not None else "Não disponível",
)


grafico_col1, grafico_col2 = st.columns(2)

with grafico_col1:
    distribuicao_segmentos = (
        df_filtrado["Segment_Name"]
        .value_counts()
        .reset_index()
    )
    distribuicao_segmentos.columns = ["Segment_Name", "Quantidade"]

    fig_distribuicao = px.bar(
        distribuicao_segmentos,
        x="Segment_Name",
        y="Quantidade",
        text="Quantidade",
        title="Distribuição dos Clientes por Segmento",
        labels={
            "Segment_Name": "Segmento",
            "Quantidade": "Quantidade de clientes",
        },
        color="Segment_Name",
        color_discrete_sequence=CORES_SEGMENTOS,
        template=TEMPLATE_GRAFICO,
    )
    fig_distribuicao.update_traces(textposition="outside")
    fig_distribuicao.update_layout(
        showlegend=False,
        title_font_size=18,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=60, b=20),
    )
    st.plotly_chart(fig_distribuicao, use_container_width=True)

with grafico_col2:
    #st.subheader("Comportamento por Canal de Compra")

    canais_compra = {
        "NumWebPurchases": "Web",
        "NumCatalogPurchases": "Catálogo",
        "NumStorePurchases": "Loja Física",
    }

    colunas_canais = [
        coluna for coluna in canais_compra.keys() if coluna in df_filtrado.columns
    ]

    if colunas_canais:
        compras_por_canal = (
            df_filtrado.groupby("Segment_Name", as_index=False)[colunas_canais]
            .mean()
            .melt(
                id_vars="Segment_Name",
                value_vars=colunas_canais,
                var_name="Canal",
                value_name="Média de Compras",
            )
        )
        compras_por_canal["Canal"] = compras_por_canal["Canal"].map(canais_compra)

        fig_canais = px.bar(
            compras_por_canal,
            x="Segment_Name",
            y="Média de Compras",
            color="Canal",
            barmode="group",
            title="Compras Médias por Canal",
            labels={
                "Segment_Name": "Segmento",
                "Média de Compras": "Média de compras",
            },
            color_discrete_sequence=CORES_CANAIS,
            template=TEMPLATE_GRAFICO,
        )
        fig_canais.update_layout(
            title_font_size=18,
            legend_title_text="Canal",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=20, r=20, t=60, b=20),
        )
        st.plotly_chart(fig_canais, use_container_width=True)
    else:
        st.warning("Nenhuma coluna de canal de compra disponível.")


grafico_col3, grafico_col4 = st.columns(2)

with grafico_col3:
    #st.subheader("Resposta à Campanha de Marketing")

    if "Response" in df_filtrado.columns:
        resposta_campanha = (
            df_filtrado.groupby("Segment_Name", as_index=False)["Response"]
            .mean()
        )
        resposta_campanha["Taxa de Resposta (%)"] = (
            resposta_campanha["Response"] * 100
        )

        fig_resposta = px.bar(
            resposta_campanha,
            x="Segment_Name",
            y="Taxa de Resposta (%)",
            text="Taxa de Resposta (%)",
            title="Taxa de Resposta à Última Campanha",
            labels={
                "Segment_Name": "Segmento",
                "Taxa de Resposta (%)": "Taxa de resposta (%)",
            },
            color="Segment_Name",
            color_discrete_sequence=CORES_SEGMENTOS,
            template=TEMPLATE_GRAFICO,
        )
        fig_resposta.update_traces(
            texttemplate="%{text:.1f}%",
            textposition="outside",
        )
        fig_resposta.update_yaxes(ticksuffix="%")
        fig_resposta.update_layout(
            showlegend=False,
            title_font_size=18,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=20, r=20, t=60, b=20),
        )
        st.plotly_chart(fig_resposta, use_container_width=True)

        st.caption(
            "Esse indicador mostra a proporção de clientes de cada segmento "
            "que respondeu à última campanha. Essa relação não deve ser "
            "interpretada como causalidade."
        )
    else:
        st.warning("A coluna Response não está disponível no CSV.")

with grafico_col4:
    #st.subheader("Comparação do Perfil dos Segmentos")

    caracteristicas_disponiveis = [
        coluna
        for coluna in ["Income", "Age", "Total_Spent", "Total_Purchases", "Recency"]
        if coluna in df_filtrado.columns
    ]

    if caracteristicas_disponiveis:
        caracteristica = st.selectbox(
            "Característica",
            caracteristicas_disponiveis,
        )

        perfil_segmentos = (
            df_filtrado.groupby("Segment_Name", as_index=False)[caracteristica]
            .mean()
        )

        fig_perfil = px.bar(
            perfil_segmentos,
            x="Segment_Name",
            y=caracteristica,
            text=caracteristica,
            title=f"Média de {caracteristica} por Segmento",
            labels={
                "Segment_Name": "Segmento",
                caracteristica: f"Média de {caracteristica}",
            },
            color="Segment_Name",
            color_discrete_sequence=CORES_SEGMENTOS,
            template=TEMPLATE_GRAFICO,
        )
        fig_perfil.update_traces(
            texttemplate="%{text:.2f}",
            textposition="outside",
        )
        fig_perfil.update_layout(
            showlegend=False,
            title_font_size=18,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=20, r=20, t=60, b=20),
        )
        st.plotly_chart(fig_perfil, use_container_width=True)
    else:
        st.warning("Nenhuma coluna de perfil disponível para comparação.")
