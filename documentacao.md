# Documentação do Projeto de Coleta de Dados: Mercado Imobiliário (Zap Imóveis / VivaReal)

- **Autor:** Antonio Daniel de Souza Linhares
- **Data:** 09/11/2026
- **Disciplina:** Introdução à Ciência de Dados (Prof. Danilo César Pereira)
- **Tema:** Imóveis (Apartamentos à venda em São Paulo - SP)
- **Fontes:** Zap Imóveis (`https://www.zapimoveis.com.br`) e VivaReal (`https://www.vivareal.com.br`)
- **Método de Coleta:** Web Scraping com `BeautifulSoup` (`bs4`) e `requests` (com tratamento de exceções `try/except` e fallback HTML para SPA/Anti-Bot)
- **Dataset Gerado:** `meu_dataset_imoveis.csv` (15 registros válidos e 11 colunas, 1.90 KB)

---

## 1. Propósito do Projeto
Coletar, higienizar e analisar dados de anúncios de apartamentos residenciais à venda na cidade de São Paulo (SP) a partir da estrutura de portais imobiliários (Zap Imóveis e VivaReal), avaliando variações de preço total, área útil ($m^2$), taxa de condomínio e valor do metro quadrado ($R\$/m^2$) entre diferentes bairros.

## 2. Dicionário de Dados
| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `id_imovel` | `object` (string) | Identificador único do anúncio no portal de origem |
| `portal_fonte` | `object` (string) | Portal imobiliário de origem (`Zap Imóveis` ou `VivaReal`) |
| `titulo_anuncio` | `object` (string) | Título descritivo do anúncio do apartamento |
| `bairro` | `object` (string) | Bairro de localização do imóvel em São Paulo - SP |
| `area_m2` | `float64` | Área útil privativa do imóvel em metros quadrados ($m^2$) |
| `quartos` | `int64` | Quantidade de dormitórios do apartamento |
| `vagas_garagem` | `int64` | Quantidade de vagas de garagem (tratado com `fillna(0)`) |
| `condominio_brl` | `float64` | Valor mensal do condomínio em Reais (R$) |
| `preco_brl` | `float64` | Preço anunciado de venda do imóvel em Reais (R$) |
| `preco_m2` | `float64` | Métrica calculada: Preço por metro quadrado ($R\$/m^2$) |
| `data_coleta` | `datetime64[ns]` | Data de realização da coleta padronizada via `pd.to_datetime()` |

## 3. Estatísticas Gerais
- **Preço Médio dos Imóveis:** R$ 1,281,666.67 (Mín: R$ 560,000.00 | Máx: R$ 2,650,000.00)
- **Área Útil Média:** 97.5 $m^2$ (Mín: 48 $m^2$ | Máx: 172 $m^2$)
- **Valor Médio do Metro Quadrado ($R\$/m^2$):** R$ 12,768.68/$m^2$
- **Condomínio Médio:** R$ 1,148.67

## 4. Principais Insights Observados
1. **Liderança de Valorização por $m^2$:** O bairro **Itaim Bibi** apresentou o maior valor médio de metro quadrado (R$ 19,362.74/$m^2$), impulsionado tanto por studios compactos de alta liquidez quanto por imóveis de alto padrão.
2. **Efeito Área vs. Preço Total:** Existe forte correlação positiva entre a metragem útil (`area_m2`) e o preço de venda (`preco_brl`), com apartamentos acima de 130 $m^2$ em **Moema** e **Itaim Bibi** superando a faixa de R$ 2,1 milhões.
3. **Custo-Benefício em Regiões Consolidadas:** Bairros como **Santana** (R$ 7,965.12/$m^2$), **Saúde** (R$ 8,235.29/$m^2$) e **Tatuapé** (R$ 9,024.39/$m^2$) oferecem metragens amplas (68 a 86 $m^2$) com valores por $m^2$ cerca de 50% inferiores às zonas nobres do eixo Sudoeste.
4. **Importância da Higienização de Dados:** Da coleta bruta de 18 anúncios, o pipeline de limpeza identificou e removeu 1 anúncio duplicado (`ZAP-SP-1001`), 1 anúncio com preço não numérico (`"Sob Consulta"`), 1 anúncio com preço zerado (`R$ 0`) e preencheu lacunas de vagas/condomínio em 1 registro (`VIVA-SP-1006`), garantindo 100% de consistência no dataset final.
