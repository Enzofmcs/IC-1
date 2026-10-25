# IC-1 · Análise de sinais e curvas de calibração

**Python · Pandas · tratamento de sinais · automação de planilhas · regressão linear**

Repositório de iniciação científica de **Enzo Souza**, com ferramentas para organizar medições experimentais, extrair máximos de corrente e ajustar relações entre concentração e resposta instrumental.

O relatório identifica a pesquisa como **Otimização da coleta de dados de métodos analíticos desenvolvidos para a detecção do antitumoral metotrexato**, sob orientação de **Prof. Dr. Augusto Etchegaray Júnior**, na PUC-Campinas. Seu foco é automatizar a organização, análise e visualização de dados de HPLC e biossensores/eletroquímica. A seção de resultados inclui vincristina e metotrexato. O documento se identifica internamente como relatório parcial de setembro/2023 a fevereiro/2024, apesar do nome de arquivo “RELATÓRIO FINAL”.

## Comece por aqui

1. [Demonstração de calibração com dados sintéticos](notebooks/01_calibration_demo.ipynb): executável sem as planilhas da pesquisa.
2. [Leitura e consolidação de sinais](notebooks/02_signal_workflow.ipynb): configuração para os dados originais.
3. [Catálogo dos seis notebooks históricos](docs/curation.md): diferenças, seleção e origem.
4. [Método, resultados registrados e limitações](docs/experiments.md).

## O que foi recuperado

- Consolidação de espectros CSV em UTF-16LE e de planilhas exportadas do NOVA.
- Inspeção de corrente por tempo/potencial, extração de máximos e diferenças entre curvas.
- Regressão linear e cálculo de R² em uma variante do fluxo de calibração.
- Código histórico preservado em cópias limpas, com nomes descritivos e rastreabilidade por hash.

## Executar a versão organizada

Use Python 3.11 ou superior, a partir da raiz deste repositório:

```sh
python -m venv .venv
python -m pip install -e .
python -m ic1 examples/synthetic_calibration.csv --output outputs/synthetic_calibration.json
python -m unittest discover -s tests -v
python scripts/validate_notebooks.py
```

Ative `.venv` antes da instalação (`.venv\Scripts\Activate.ps1` no PowerShell ou `source .venv/bin/activate` no Linux/macOS). Para abrir os notebooks e gerar gráficos: `python -m pip install -e ".[notebooks]"`, seguido de `jupyter lab`.

O CSV de calibração contém `concentration` e `signal`. A unidade e a identidade do composto precisam ser definidas pelo responsável pelos dados. O arquivo em `examples/` é **inteiramente sintético**, usado apenas para demonstrar a execução; seus coeficientes não são resultados da IC.

## Estrutura

```text
src/ic1/                   Leitura, consolidação, picos e calibração
notebooks/                 Demonstrações e fluxo organizado
notebooks/historical/      Seis cadernos recuperados, sem saídas embutidas
docs/                      Método, curadoria e proveniência
results/                   Evidências textuais das saídas históricas
examples/                  Dados sintéticos explicitamente identificados
tests/                     Verificações numéricas e de integridade dos sinais
```

## Estado dos resultados

A série **VIN**, identificada como vincristina pelo contexto do relatório e pelos nomes das amostras, agora pode ser recalculada a partir de seis tabelas instrumentais fornecidas pelo autor. O ajuste aos máximos reproduz **R² = 0,984966**, compatível com o **0,985** salvo em `B01`. Os seis rótulos vão de 200 a 1.200 **nmol**: essa unidade foi preservada como quantidade rotulada, sem conversão em concentração, pois o volume não foi fornecido. O ajuste não estabelece LOD, LOQ ou validação independente. [Dados, método e resultado](docs/report_review.md).

A versão organizada corrige problemas de alinhamento e pareamento encontrados nos protótipos. É uma implementação posterior; a reprodução numérica da série VIN foi verificada separadamente. [Detalhes](docs/experiments.md) · [Origem dos notebooks](docs/provenance.json) · [Origem das tabelas](docs/additional_sources.json) · [Autoria e direitos](RIGHTS.md).

## Reproduzir a série instrumental fornecida

```sh
python -m ic1.reproduce --output outputs/vincristine_001
```

O comando lê as tabelas CSV incluídas em `data/source_tables/vincristine/`, reaplica a janela histórica de potencial e salva sinais selecionados, máximos e ajuste em uma pasta nova. [Notebook com os dados fornecidos](notebooks/03_supplied_vincristine.ipynb).

O repositório contém ainda seis espectros CSV com desvio-padrão e uma série suplementar rotulada IMT/SRF. O composto dos espectros numerados e o significado de IMT/SRF continuam sem confirmação; eles não são apresentados como medições identificadas de metotrexato.
