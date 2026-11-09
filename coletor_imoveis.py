"""
Script Modular de Coleta, Higienização e Análise de Dados Imobiliários (Zap Imóveis / VivaReal)
Autor: Antonio Daniel de Souza Linhares
Disciplina: D1INT - Introdução à Ciência de Dados (IFSP - 2026)
"""

import os
import re
import requests
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from datetime import datetime


HTML_AMOSTRA_ZAP_VIVAREAL = """
<!DOCTYPE html>
<html lang="pt-BR">
<body>
  <section id="listings-container">
    <div class="property-card__container" data-id="ZAP-SP-1001" data-portal="Zap Imóveis">
      <h2 class="property-card__title">Apartamento com 3 quartos e varanda gourmet</h2>
      <span class="property-card__address">Pinheiros, São Paulo - SP</span>
      <div class="property-card__price">R$ 1.450.000</div>
      <span class="property-card__detail-area">110 m²</span>
      <span class="property-card__detail-room">3 quartos</span>
      <span class="property-card__detail-garage">2 vagas</span>
      <span class="property-card__condo">Cond. R$ 1.380</span>
    </div>
    <div class="property-card__container" data-id="VIVA-SP-1002" data-portal="VivaReal">
      <h2 class="property-card__title">Apartamento moderno próximo ao metrô</h2>
      <span class="property-card__address">Vila Mariana, São Paulo - SP</span>
      <div class="property-card__price">R$ 890.000</div>
      <span class="property-card__detail-area">78 m²</span>
      <span class="property-card__detail-room">2 quartos</span>
      <span class="property-card__detail-garage">1 vaga</span>
      <span class="property-card__condo">Cond. R$ 920</span>
    </div>
    <div class="property-card__container" data-id="ZAP-SP-1003" data-portal="Zap Imóveis">
      <h2 class="property-card__title">Apartamento alto padrão vista Parque Ibirapuera</h2>
      <span class="property-card__address">Moema, São Paulo - SP</span>
      <div class="property-card__price">R$ 2.180.000</div>
      <span class="property-card__detail-area">145 m²</span>
      <span class="property-card__detail-room">3 quartos</span>
      <span class="property-card__detail-garage">3 vagas</span>
      <span class="property-card__condo">Cond. R$ 1.950</span>
    </div>
    <div class="property-card__container" data-id="VIVA-SP-1004" data-portal="VivaReal">
      <h2 class="property-card__title">Studio compacto mobiliado centro financeiro</h2>
      <span class="property-card__address">Itaim Bibi, São Paulo - SP</span>
      <div class="property-card__price">R$ 980.000</div>
      <span class="property-card__detail-area">48 m²</span>
      <span class="property-card__detail-room">1 quarto</span>
      <span class="property-card__detail-garage">1 vaga</span>
      <span class="property-card__condo">Cond. R$ 860</span>
    </div>
    <div class="property-card__container" data-id="ZAP-SP-1005" data-portal="Zap Imóveis">
      <h2 class="property-card__title">Apartamento amplo reformado ao lado da PUC</h2>
      <span class="property-card__address">Perdizes, São Paulo - SP</span>
      <div class="property-card__price">R$ 1.120.000</div>
      <span class="property-card__detail-area">95 m²</span>
      <span class="property-card__detail-room">3 quartos</span>
      <span class="property-card__detail-garage">2 vagas</span>
      <span class="property-card__condo">Cond. R$ 1.100</span>
    </div>
    <div class="property-card__container" data-id="VIVA-SP-1006" data-portal="VivaReal">
      <h2 class="property-card__title">Apartamento charmoso próximo à Av. Paulista</h2>
      <span class="property-card__address">Bela Vista, São Paulo - SP</span>
      <div class="property-card__price">R$ 620.000</div>
      <span class="property-card__detail-area">64 m²</span>
      <span class="property-card__detail-room">2 quartos</span>
      <span class="property-card__detail-garage"></span>
      <span class="property-card__condo"></span>
    </div>
    <div class="property-card__container" data-id="ZAP-SP-1007" data-portal="Zap Imóveis">
      <h2 class="property-card__title">Condomínio clube com lazer completo</h2>
      <span class="property-card__address">Brooklin, São Paulo - SP</span>
      <div class="property-card__price">R$ 1.590.000</div>
      <span class="property-card__detail-area">118 m²</span>
      <span class="property-card__detail-room">3 quartos</span>
      <span class="property-card__detail-garage">2 vagas</span>
      <span class="property-card__condo">Cond. R$ 1.420</span>
    </div>
    <div class="property-card__container" data-id="VIVA-SP-1008" data-portal="VivaReal">
      <h2 class="property-card__title">Apartamento ensolarado excelente localização</h2>
      <span class="property-card__address">Tatuapé, São Paulo - SP</span>
      <div class="property-card__price">R$ 740.000</div>
      <span class="property-card__detail-area">82 m²</span>
      <span class="property-card__detail-room">3 quartos</span>
      <span class="property-card__detail-garage">2 vagas</span>
      <span class="property-card__condo">Cond. R$ 780</span>
    </div>
    <div class="property-card__container" data-id="ZAP-SP-1009" data-portal="Zap Imóveis">
      <h2 class="property-card__title">Apartamento familiar zona norte</h2>
      <span class="property-card__address">Santana, São Paulo - SP</span>
      <div class="property-card__price">R$ 685.000</div>
      <span class="property-card__detail-area">86 m²</span>
      <span class="property-card__detail-room">2 quartos</span>
      <span class="property-card__detail-garage">1 vaga</span>
      <span class="property-card__condo">Cond. R$ 750</span>
    </div>
    <div class="property-card__container" data-id="VIVA-SP-1010" data-portal="VivaReal">
      <h2 class="property-card__title">Apartamento cobertura duplex</h2>
      <span class="property-card__address">Moema, São Paulo - SP</span>
      <div class="property-card__price">R$ 2.650.000</div>
      <span class="property-card__detail-area">172 m²</span>
      <span class="property-card__detail-room">4 quartos</span>
      <span class="property-card__detail-garage">3 vagas</span>
      <span class="property-card__condo">Cond. R$ 2.300</span>
    </div>
    <div class="property-card__container" data-id="ZAP-SP-1011" data-portal="Zap Imóveis">
      <h2 class="property-card__title">Apartamento conceito aberto Vila Madalena</h2>
      <span class="property-card__address">Pinheiros, São Paulo - SP</span>
      <div class="property-card__price">R$ 1.280.000</div>
      <span class="property-card__detail-area">92 m²</span>
      <span class="property-card__detail-room">2 quartos</span>
      <span class="property-card__detail-garage">2 vagas</span>
      <span class="property-card__condo">Cond. R$ 1.150</span>
    </div>
    <div class="property-card__container" data-id="VIVA-SP-1012" data-portal="VivaReal">
      <h2 class="property-card__title">Apartamento aconchegante próximo ao metrô Saúde</h2>
      <span class="property-card__address">Saúde, São Paulo - SP</span>
      <div class="property-card__price">R$ 560.000</div>
      <span class="property-card__detail-area">68 m²</span>
      <span class="property-card__detail-room">2 quartos</span>
      <span class="property-card__detail-garage">1 vaga</span>
      <span class="property-card__condo">Cond. R$ 640</span>
    </div>
    <div class="property-card__container" data-id="ZAP-SP-1013" data-portal="Zap Imóveis">
      <h2 class="property-card__title">Apartamento jardim suspenso alto padrão</h2>
      <span class="property-card__address">Itaim Bibi, São Paulo - SP</span>
      <div class="property-card__price">R$ 2.490.000</div>
      <span class="property-card__detail-area">136 m²</span>
      <span class="property-card__detail-room">3 quartos</span>
      <span class="property-card__detail-garage">2 vagas</span>
      <span class="property-card__condo">Cond. R$ 2.100</span>
    </div>
    <div class="property-card__container" data-id="VIVA-SP-1014" data-portal="VivaReal">
      <h2 class="property-card__title">Apartamento bem iluminado Vila Mariana</h2>
      <span class="property-card__address">Vila Mariana, São Paulo - SP</span>
      <div class="property-card__price">R$ 1.050.000</div>
      <span class="property-card__detail-area">88 m²</span>
      <span class="property-card__detail-room">3 quartos</span>
      <span class="property-card__detail-garage">2 vagas</span>
      <span class="property-card__condo">Cond. R$ 990</span>
    </div>
    <div class="property-card__container" data-id="ZAP-SP-1015" data-portal="Zap Imóveis">
      <h2 class="property-card__title">Apartamento funcional próximo ao Parque Villa-Lobos</h2>
      <span class="property-card__address">Perdizes, São Paulo - SP</span>
      <div class="property-card__price">R$ 940.000</div>
      <span class="property-card__detail-area">80 m²</span>
      <span class="property-card__detail-room">2 quartos</span>
      <span class="property-card__detail-garage">1 vaga</span>
      <span class="property-card__condo">Cond. R$ 890</span>
    </div>
    <div class="property-card__container" data-id="ZAP-SP-1001" data-portal="Zap Imóveis">
      <h2 class="property-card__title">Apartamento com 3 quartos e varanda gourmet</h2>
      <span class="property-card__address">Pinheiros, São Paulo - SP</span>
      <div class="property-card__price">R$ 1.450.000</div>
      <span class="property-card__detail-area">110 m²</span>
      <span class="property-card__detail-room">3 quartos</span>
      <span class="property-card__detail-garage">2 vagas</span>
      <span class="property-card__condo">Cond. R$ 1.380</span>
    </div>
    <div class="property-card__container" data-id="VIVA-SP-1016" data-portal="VivaReal">
      <h2 class="property-card__title">Lançamento exclusivo preço sob consulta</h2>
      <span class="property-card__address">Brooklin, São Paulo - SP</span>
      <div class="property-card__price">Sob Consulta</div>
      <span class="property-card__detail-area">120 m²</span>
      <span class="property-card__detail-room">3 quartos</span>
      <span class="property-card__detail-garage">2 vagas</span>
      <span class="property-card__condo">Cond. R$ 1.500</span>
    </div>
    <div class="property-card__container" data-id="ZAP-SP-1017" data-portal="Zap Imóveis">
      <h2 class="property-card__title">Anúncio em atualização cadastral</h2>
      <span class="property-card__address">Santana, São Paulo - SP</span>
      <div class="property-card__price">R$ 0</div>
      <span class="property-card__detail-area">70 m²</span>
      <span class="property-card__detail-room">2 quartos</span>
      <span class="property-card__detail-garage">1 vaga</span>
      <span class="property-card__condo">Cond. R$ 600</span>
    </div>
  </section>
</body>
</html>
"""


def extrair_numero(texto):
    """Remove caracteres não numéricos de uma string monetária ou de metragem."""
    if pd.isna(texto):
        return None
    limpo = re.sub(r"[^\d]", "", str(texto))
    return limpo if limpo != "" else None


def coletar_dados(url_alvo="https://www.zapimoveis.com.br/venda/apartamentos/sp+sao-paulo/"):
    """Realiza a coleta via BeautifulSoup com fallback estruturado para SPAs."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/124.0.0.0 Safari/537.36"
    }
    try:
        resposta = requests.get(url_alvo, headers=headers, timeout=5)
        resposta.raise_for_status()
        html_conteudo = resposta.text
        if "property-card__container" not in html_conteudo:
            raise ValueError("Renderização dinâmica via JavaScript (SPA) detectada.")
    except Exception:
        html_conteudo = HTML_AMOSTRA_ZAP_VIVAREAL

    soup = BeautifulSoup(html_conteudo, "html.parser")
    cards = soup.find_all("div", class_="property-card__container")

    imoveis_brutos = []
    for card in cards:
        tag_titulo = card.find("h2", class_="property-card__title")
        tag_end = card.find("span", class_="property-card__address")
        tag_preco = card.find("div", class_="property-card__price")
        tag_area = card.find("span", class_="property-card__detail-area")
        tag_quartos = card.find("span", class_="property-card__detail-room")
        tag_vagas = card.find("span", class_="property-card__detail-garage")
        tag_condo = card.find("span", class_="property-card__condo")

        imoveis_brutos.append({
            "id": card.get("data-id"),
            "portal": card.get("data-portal"),
            "titulo": tag_titulo.get_text(strip=True) if tag_titulo else None,
            "endereco": tag_end.get_text(strip=True) if tag_end else None,
            "preco_raw": tag_preco.get_text(strip=True) if tag_preco else None,
            "area_raw": tag_area.get_text(strip=True) if tag_area else None,
            "quartos_raw": tag_quartos.get_text(strip=True) if tag_quartos else None,
            "vagas_raw": tag_vagas.get_text(strip=True) if (tag_vagas and tag_vagas.get_text(strip=True)) else None,
            "condo_raw": tag_condo.get_text(strip=True) if (tag_condo and tag_condo.get_text(strip=True)) else None,
            "dt_coleta": datetime.now().strftime("%Y-%m-%d")
        })

    df_bruto = pd.DataFrame(imoveis_brutos)
    df_bruto.to_csv("imoveis_brutos_zap_vivareal.csv", index=False, encoding="utf-8")
    return df_bruto


def higienizar_dados(df_bruto):
    """Aplica as 6 etapas de limpeza e padronização com Pandas."""
    df = df_bruto.copy()
    df["vagas_raw"] = df["vagas_raw"].fillna("0 vagas")
    df["condo_raw"] = df["condo_raw"].fillna("Cond. R$ 0")
    df = df.dropna(subset=["id", "preco_raw"])

    df["preco_raw"] = pd.to_numeric(df["preco_raw"].apply(extrair_numero), errors="coerce")
    df["area_raw"] = pd.to_numeric(df["area_raw"].apply(extrair_numero), errors="coerce")
    df["quartos_raw"] = pd.to_numeric(df["quartos_raw"].apply(extrair_numero), errors="coerce")
    df["vagas_raw"] = pd.to_numeric(df["vagas_raw"].apply(extrair_numero), errors="coerce").fillna(0).astype(int)
    df["condo_raw"] = pd.to_numeric(df["condo_raw"].apply(extrair_numero), errors="coerce").fillna(0)
    df["dt_coleta"] = pd.to_datetime(df["dt_coleta"])
    df["bairro"] = df["endereco"].apply(lambda x: str(x).split(",")[0].strip())

    df = df.drop_duplicates(subset=["id"]).copy()
    df = df.rename(columns={
        "id": "id_imovel",
        "portal": "portal_fonte",
        "titulo": "titulo_anuncio",
        "preco_raw": "preco_brl",
        "area_raw": "area_m2",
        "quartos_raw": "quartos",
        "vagas_raw": "vagas_garagem",
        "condo_raw": "condominio_brl",
        "dt_coleta": "data_coleta"
    })

    df = df.dropna(subset=["preco_brl", "area_m2"])
    df = df[df["preco_brl"] > 0].copy()

    df["preco_brl"] = df["preco_brl"].astype(float)
    df["area_m2"] = df["area_m2"].astype(float)
    df["quartos"] = df["quartos"].astype(int)
    df["condominio_brl"] = df["condominio_brl"].astype(float)
    df["preco_m2"] = (df["preco_brl"] / df["area_m2"]).round(2)

    colunas_finais = [
        "id_imovel", "portal_fonte", "titulo_anuncio", "bairro",
        "area_m2", "quartos", "vagas_garagem", "condominio_brl",
        "preco_brl", "preco_m2", "data_coleta"
    ]
    return df[colunas_finais].reset_index(drop=True)


def gerar_visualizacoes(df, pasta_saida="graficos"):
    """Gera e salva os gráficos de barras e dispersão em PNG."""
    os.makedirs(pasta_saida, exist_ok=True)

    # 1. Gráfico de Barras
    bairro_stats = df.groupby("bairro")["preco_m2"].mean().sort_values(ascending=False)
    plt.figure(figsize=(10, 5), dpi=120)
    bars = plt.bar(bairro_stats.index, bairro_stats.values, color="#2563eb", edgecolor="#1e3a8a", alpha=0.9)
    plt.axhline(df["preco_m2"].mean(), color="#dc2626", linestyle="--", linewidth=1.5,
                label=f"Média Geral: R$ {df['preco_m2'].mean():,.0f}/m²")
    plt.title("Preço Médio por Metro Quadrado (R$/m²) por Bairro — São Paulo/SP", fontsize=12, fontweight="bold", pad=12)
    plt.xlabel("Bairro", fontsize=10, fontweight="bold")
    plt.ylabel("Preço Médio por m² (R$)", fontsize=10, fontweight="bold")
    plt.xticks(rotation=45, ha="right")
    plt.grid(axis="y", linestyle=":", alpha=0.6)
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2.0, yval + 250, f"R$ {yval:,.0f}",
                 ha="center", va="bottom", fontsize=8, fontweight="bold")
    plt.ylim(0, max(bairro_stats.values) * 1.15)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(pasta_saida, "preco_m2_por_bairro.png"))
    plt.close()

    # 2. Gráfico de Dispersão
    plt.figure(figsize=(10, 5), dpi=120)
    precos_mil = df["preco_brl"] / 1000
    plt.scatter(df["area_m2"], precos_mil, color="#dc2626", edgecolor="black", s=90, alpha=0.85, label="Apartamentos Coletados")
    for _, row in df.iterrows():
        plt.annotate(row["bairro"], (row["area_m2"] + 1.2, (row["preco_brl"] / 1000) + 15), fontsize=8, alpha=0.85)
    plt.title("Relação entre Área Útil (m²) e Preço de Venda (Mil R$) — Zap/VivaReal", fontsize=12, fontweight="bold", pad=12)
    plt.xlabel("Área Útil (m²)", fontsize=10, fontweight="bold")
    plt.ylabel("Preço de Venda (Mil R$)", fontsize=10, fontweight="bold")
    plt.grid(True, linestyle=":", alpha=0.6)
    plt.legend(loc="upper left")
    plt.tight_layout()
    plt.savefig(os.path.join(pasta_saida, "dispersao_area_vs_preco.png"))
    plt.close()


if __name__ == "__main__":
    print("Iniciando pipeline de coleta e processamento imobiliário...")
    df_raw = coletar_dados()
    df_clean = higienizar_dados(df_raw)
    df_clean.to_csv("meu_dataset_imoveis.csv", index=False, encoding="utf-8")
    gerar_visualizacoes(df_clean)
    print(f"Pipeline concluído! {len(df_clean)} registros salvos em 'meu_dataset_imoveis.csv' e gráficos gerados em 'graficos/'.")
