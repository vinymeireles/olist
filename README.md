## 🛍️ Projeto de Engenharia de Dados: Olist E-commerce Brasil

### Pipeline completo de ingestão, transformação, agregação e análise de dados utilizando arquitetura **Medallion (Bronze, Silver e Gold)** com base no dataset público do [Olist no Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce), incluindo visualizações de KPIs para tomada de decisão.

---

### 📁 Estrutura do Projeto

```bash
├── Notebook
│   ├── 01. Camada Bronze.py          # Ingestão e gravação dos dados brutos (camada Bronze)
│   ├── 02. Camada Silver.py          # Limpeza, transformação e enriquecimento dos dados (camada Silver)
│   ├── 03. Camada Gold.py            # Agregações e métricas para insights de negócio (camada Gold)
│   ├── 04. Gold re-invoiced.py       # Versão refatorada das agregações da camada Gold
├── /data
│   ├── /Raw                          # Arquivos originais .csv do Kaggle
│   ├── /Bronze                       # Dados convertidos para formato Delta, sem transformação
│   ├── /Silver                       # Dados tratados, enriquecidos e prontos para análise
│   ├── /Gold                         # Métricas consolidadas e indicadores de negócio (KPIs)
├── /image                            # Diagramas e imagens do projeto
└── README.md
```

⚙️ Tecnologias Utilizadas
- Apache Spark (PySpark)
- Delta Lake (armazenamento otimizado)
- Databricks Community Edition
- Power BI (visualização de dados)
- Python 3.13
- Kaggle API

### 🧱 Arquitetura Medallion
<img src="Image/Diagrama ETL Ifood.png">

```
O projeto segue a arquitetura em camadas da Medallion Architecture, com divisão clara entre ingestão, transformação e análise:

🔸 Bronze
 - Ingestão dos arquivos .csv originais do Kaggle.
 - Sem transformações.
 - Armazenamento em formato Delta.

🔹 Silver
 - Limpeza e padronização:
 - Conversão de tipos de dados
 - Remoção de valores nulos
 - Enriquecimento com novas colunas
 - Dataset consolidado por cliente/pedido.

🥇 Gold
 - Cálculo de métricas e KPIs:
 - Total de pedidos por estado
 - Tempo médio de entrega
 - Ticket médio por tipo de pagamento
 - Média de itens por pedido
 - Nota média de avaliação por estado
```

📊 Visualizações no Power BI

  O projeto pode ser integrado ao Power BI para visualização dos KPIs gerados:

  - Total de pedidos por estado
  - Tempo médio de entrega por estado
  - Valor médio por tipo de pagamento
  - Média de itens por pedido
  - Avaliação média por estado

```
▶️ Execução
  Clone o repositório:

 git clone https://github.com/seu-usuario/projeto-olist-etl.git

1. Importe os notebooks no Databricks

2. Execute-os na ordem:

  01. Camada Bronze.py  
  02. Camada Silver.py  
  04. Gold re-invoiced.py
   
3. Visualize os arquivos .parquet no Power BI

```
📈 Exemplos de KPIs Gerados
  
<table>
  <thead>
    <tr>
      <th>Métrica</th>
      <th>Descrição</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Pedidos por estado</td>
      <td>Total de pedidos agrupados por UF</td>
    </tr>
    <tr>
      <td>Tempo médio de entrega</td>
      <td>Diferença entre data de compra e entrega</td>
    </tr>
    <tr>
      <td>Valor médio por pagamento</td>
      <td>Ticket médio por tipo de pagamento (boleto, cartão...)</td>
    </tr>
    <tr>
      <td>Média de itens por pedido</td>
      <td>Quantidade média de produtos por pedido</td>
    </tr>
  </tbody>
</table>


```

✅ Status do Projeto

✔️ Pipeline Bronze → Silver → Gold funcional

✔️ Dados tratados e salvos em Delta

✔️ KPIs salvos na Gold prontos para visualização

❌ Visualização final no Power BI (em desenvolvimento)

❌ Deploy e automação (Databricks Jobs / Airflow)

📌 Futuras Melhorias
Integração com Power BI Service
  
 - Automação do pipeline (Jobs e triggers)
 - Testes unitários com pytest
 - Monitoramento do pipeline

```
📚 Fonte de Dados
Dataset: Brazilian E-Commerce Public Dataset by Olist

Fonte: Kaggle - Olist
Licença: CC BY-NC-SA 4.0

👨‍💻 Autor
Vinicius Meireles
Engenheiro de Dados | Especialista em Power BI

📎 LinkedIn: <a href= "https://www.linkedin.com/in/pviniciusmeireles/"> Linkedin </a>
📧 viniciusmeireles@gmail.com
```
<img src="Image/Logo Engenharia de Dados.png" width="150" height="150">   
