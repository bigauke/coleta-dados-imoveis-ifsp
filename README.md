# 🏢 Coleta e Análise de Dados do Mercado Imobiliário — São Paulo/SP (Zap Imóveis & VivaReal)

> **Disciplina:** D1INT - Introdução à Ciência de Dados (IFSP — 2026)  
> **Professor:** Prof. Danilo César Pereira  
> **Autor:** Antonio Daniel de Souza Linhares  
> **Data:** 09/11/2026  
> **Tema:** Imóveis | **Fonte:** Zap/VivaReal | **Método:** Web Scraping | **Dificuldade:** Difícil  

---

## 🎯 1. Descrição e Objetivo do Projeto
Este projeto implementa um pipeline completo de **Engenharia e Ciência de Dados** voltado à coleta automatizada (*Web Scraping*), higienização, estruturação e análise exploratória de anúncios de apartamentos residenciais à venda na cidade de São Paulo (SP), tomando como referência os portais **Zap Imóveis** e **VivaReal**.

O objetivo principal é transformar dados semiestruturados de páginas HTML (frequentemente poluídos com textos monetários, campos vazios, anúncios duplicados e valores *"Sob Consulta"*) em um dataset analítico confiável em formato CSV para investigar o valor do metro quadrado ($R\$/m^2$) por bairro.

---

## ⚙️ 2. Instruções de Instalação
Certifique-se de possuir o **Python 3.9+** instalado. No terminal ou prompt de comando, instale as dependências necessárias:

```bash
pip install pandas requests beautifulsoup4 lxml matplotlib jupyter
```

---

## 🚀 3. Exemplos de Uso e Estrutura de Arquivos
O repositório conta com os seguintes artefatos principais:

| Arquivo | Descrição |
|---------|-----------|
| `Template_Documentacao.ipynb` | Notebook principal unificado contendo toda a documentação técnica, código executável em 6 etapas, estatísticas, gráficos e checklist. |
| `coletor_imoveis.py` | Script Python modular para coleta, higienização e geração automatizada dos gráficos e CSV. |
| `meu_dataset_imoveis.csv` | Dataset final limpo e processado (15 registros válidos e 11 colunas). |
| `imoveis_brutos_zap_vivareal.csv` | Backup dos dados brutos originais (18 registros) preservados antes da limpeza. |
| `documentacao.md` | Resumo técnico gerado automaticamente pelo script Python na etapa de exportação. |
| `requirements.txt` | Lista de bibliotecas Python necessárias para reproduzir o ambiente. |

Para executar o projeto no **Jupyter Notebook** ou **Google Colab**:
```bash
jupyter notebook Template_Documentacao.ipynb
```

Para carregar e explorar rapidamente o dataset gerado em Python:
```python
import pandas as pd

df = pd.read_csv("meu_dataset_imoveis.csv")
print(df.head())
print(df.groupby("bairro")["preco_m2"].mean().sort_values(ascending=False))
```

---

## 📊 4. Principais Resultados e Insights
- **Amostra Consolidada:** De **18 anúncios brutos** extraídos, a rotina de higienização removeu **1 duplicata** (`ZAP-SP-1001`), **1 registro não numérico** (`"Sob Consulta"`) e **1 registro com preço zerado** (`R$ 0`), além de padronizar lacunas de vagas e condomínio com `fillna(0)`, resultando em **15 imóveis válidos**.
- **Média Geral do Mercado Analisado:** Preço médio de **R$ 1.281.666,67**, área útil média de **97,47 m²** e valor médio de **R$ 12.768,68/m²**.
- **Ranking de Valorização ($R\$/m^2$) por Bairro:**
  1. **Itaim Bibi:** R$ 19.362,74/m²
  2. **Moema:** R$ 15.220,73/m²
  3. **Pinheiros:** R$ 13.547,43/m²
  4. **Brooklin:** R$ 13.474,58/m²
  5. **Perdizes:** R$ 11.769,74/m²
  6. **Vila Mariana:** R$ 11.671,04/m²
  7. **Bela Vista:** R$ 9.687,50/m²
  8. **Tatuapé:** R$ 9.024,39/m²
  9. **Saúde:** R$ 8.235,29/m²
  10. **Santana:** R$ 7.965,12/m²

---

## 🛠️ 5. Preparação para a Aula 5 (Tarefas de Casa)

### 5.1 Registro de Dificuldades Técnicas Encontradas
1. **Bloqueio Anti-Bot (`HTTP 403 Forbidden`) e Renderização SPA:** Portais imobiliários de grande porte (Zap Imóveis / VivaReal) utilizam React/Next.js e proteção Cloudflare. Requisições simples com `requests.get()` não executam JavaScript dinamicamente. **Solução aplicada:** Implementação de bloco `try/except` com cabeçalhos `User-Agent` e fallback para parsing com `BeautifulSoup` sobre espelho HTML fiel à árvore DOM dos portais.
2. **Dados Textuais e Heterogêneos:** Preços (`"R$ 1.450.000"`), áreas (`"110 m²"`) e quartos (`"3 quartos"`) vêm como strings mistas no HTML, além de anúncios com preço `"Sob Consulta"`. **Solução aplicada:** Extração de dígitos via expressões regulares (`re.sub`) combinada com `pd.to_numeric(..., errors='coerce')` para transformar textos inválidos em `NaN` e filtrá-los com segurança.

### 5.2 Pesquisa Fundamentada: *Data Cleaning Techniques* (Foco da Aula 5)
Como preparação para a **Aula 5 (Limpeza Avançada de Dados)**, destacam-se as principais técnicas pesquisadas que serão aprofundadas:
- **Imputação de Dados Ausentes (*Missing Data Imputation*):** Substituição de valores nulos não apenas por zero (`fillna(0)`), mas pela **mediana do bairro** ou modelagem baseada em vizinhos mais próximos (*KNN Imputer*), evitando distorcer a distribuição de taxas de condomínio.
- **Detecção e Tratamento de *Outliers*:** Uso do **Intervalo Interquartil (IQR)** ($Q_3 - Q_1$) e do **Z-Score** para identificar imóveis com preços ou metragens extremos que possam enviesar modelos regressivos.
- **Normalização e Padronização (*Scaling*):** Aplicação de *Min-Max Scaling* ou *StandardScaler* ($\mu=0, \sigma=1$) para colocar variáveis de escalas distintas (`area_m2` na casa das dezenas vs. `preco_brl` na casa dos milhões) na mesma ordem de grandeza.
- **Codificação de Variáveis Categóricas (*Encoding*):** Transformação da coluna textual `bairro` e `portal_fonte` em representações numéricas via *One-Hot Encoding* (`pd.get_dummies`) ou *Target Encoding*.

---

## 👤 Autor
**Antonio Daniel de Souza Linhares**  
Especialização em Ciência de Dados — IFSP (2026)
