import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Configurações iniciais
st.set_page_config(page_title="Análise Bolsa Família 2025", layout="wide")

# 👤 Cabeçalho personalizado
st.markdown("""
#Aline Spinosi
**RU:** 5045593
""")
st.title("Análise do Bolsa Família em 2025")

# 📄 Leitura dos dados
st.subheader("Carregando os dados...")

caminho_arquivo = "POP2024_20241230.xlsx"

df_bolsa = pd.read_excel(
    caminho_arquivo,
    sheet_name="BolsaFamilia"
)


# 🔄 Padronizar código do IBGE e filtrar o mês mais recente
df_bolsa["codigo_ibge"] = df_bolsa["codigo_ibge"].astype(str).str.zfill(6)
df_bolsa = df_bolsa[df_bolsa["anomes_s"] == df_bolsa["anomes_s"].max()]

# 🧮 Proporção de famílias beneficiadas
df_bolsa["proporcao_familias"] = (
    df_bolsa["qtd_familias_beneficiarias_bolsa_familia_s"] /
    df_bolsa["Populacao"]
)

st.success("✅ Dados processados com sucesso para o estado de São Paulo!")

# 📊 Gráfico 1


def formatar_valor(valor):
    if valor >= 1_000_000:
        return f"{valor/ 1_000_000:.1f} Mi"
    elif valor >= 1_000:
        return f"{valor /1_000:.0f} Mil"
    else:
        return f"{valor:.0f}"


col1, col2 = st.columns(2)

with col1:
    st.subheader("🔹 Top 10 municípios com maior valor repassado")
    top_valor = df_bolsa.nlargest(10, "valor_repassado_bolsa_familia_s")
    fig1, ax1 = plt.subplots(figsize=(10, 5))
    grafico = sns.barplot(data=top_valor, x="valor_repassado_bolsa_familia_s",
                          y="Municipio", palette="viridis", ax=ax1)
    ax1.set_title("Top 10 municípios - Valor Repassado")
    ax1.set_xlabel("Valor repassado (R$)")
    for p in grafico.patches:
        valor_formatado = formatar_valor(p.get_width())
        ax1.text(p.get_width() + top_valor["valor_repassado_bolsa_familia_s"].max() * 0.01,
                 p.get_y()+p.get_height()/2,
                 valor_formatado,
                 va='center')
    st.pyplot(fig1)


# 📊 Gráfico 2
def formatar_valor(valor):
    if valor >= 1_000_000:
        return f"{valor/ 1_000_000:.1f} Mi"
    elif valor >= 1_000:
        return f"{valor /1_000:.0f} Mil"
    else:
        return f"{valor:.0f}"


with col2:
    st.subheader(
        "🔹 Top 10 municípios com maior número de famílias beneficiadas")
    top_familias = df_bolsa.nlargest(
        10, "qtd_familias_beneficiarias_bolsa_familia_s")
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    grafico2 = sns.barplot(
        data=top_familias, x="qtd_familias_beneficiarias_bolsa_familia_s", y="Municipio", palette="magma", ax=ax2)
    ax2.set_title("Top 10 municípios - Famílias Beneficiadas")
    ax2.set_xlabel("Número de famílias")
    for p in grafico2.patches:
        valor_formatado = formatar_valor(p.get_width())
        ax2.text(p.get_width() + top_valor["qtd_familias_beneficiarias_bolsa_familia_s"].max() * 0.01,
                 p.get_y()+p.get_height()/2,
                 valor_formatado,
                 va='center')
    st.pyplot(fig2)

col3, col4 = st.columns(2)
# 📊 Gráfico 3
with col3:
    st.subheader("🔹 Maiores proporções de famílias beneficiadas")
    top_prop = df_bolsa.dropna(subset=["proporcao_familias"]).nlargest(
        10, "proporcao_familias")
    fig3, ax3 = plt.subplots(figsize=(10, 5))
    grafico3 = sns.barplot(data=top_prop, x="proporcao_familias",
                           y="Municipio", palette="coolwarm", ax=ax3)
    ax3.set_title("Top 10 - Proporção de famílias beneficiadas")
    ax3.set_xlabel("Proporção (famílias / população)")
    # ➕ Adiciona rótulos em formato percentual
    for p in grafico3.patches:
        valor_percentual = f"{p.get_width()*100:.1f}%"
        ax3.text(p.get_width() + top_prop["proporcao_familias"].max() * 0.01,
                 p.get_y()+p.get_height()/2,
                 valor_percentual,
                 va='center')
    st.pyplot(fig3)


# 📊 Gráfico 4

    def formatar_valor(valor):
        if valor >= 1_000_000:
            return f"R$ {valor/ 1_000_000:.1f} Mi"
        elif valor >= 1_000:
            return f"R$ {valor /1_000:.0f} Mil"
        else:
            return f"R$ {valor:.0f}"
with col4:
    st.subheader("🔹 Valor médio do benefício por Municipio")
    # Agrupar por município e calcular o valor médio
    municipio_mean = df_bolsa.groupby(
        "Municipio")["pbf_vlr_medio_benef_f"].mean().sort_values(ascending=False)
    # Selecionar os 10 municípios com maior valor médio
    top10_municipios = municipio_mean.head(10)
    # Criar o gráfico
    fig4, ax4 = plt.subplots(figsize=(10, 5))
    grafico4 = sns.barplot(x=top10_municipios.values,
                           y=top10_municipios.index, palette="cubehelix", ax=ax4)
    ax4.set_title("Valor médio do benefício - Top 10 Municipios")
    ax4.set_ylabel("R$ médio por família")
    for p in grafico4.patches:
        valor_formatado = formatar_valor(p.get_width())
        ax4.text(p.get_width() + top10_municipios.max() * 0.01,
                 p.get_y()+p.get_height()/2,
                 valor_formatado,
                 va='center')
    st.pyplot(fig4)
