# IC-1 · Análise de sinais e curvas de calibração

**Python · Pandas · tratamento de sinais · automação de planilhas · regressão linear**

Repositório de iniciação científica de **Enzo Souza**, com ferramentas para organizar medições experimentais, extrair máximos de corrente e ajustar relações entre concentração e resposta instrumental.

O objetivo informado pelo autor é a medição da concentração de **metotrexato ou vincristina**. Os notebooks recuperados incluem sinais eletroquímicos, espectros e uma exploração de enzima/anticorpo; os arquivos disponíveis não permitem associar cada série a um desses compostos. Essa identificação aguarda o relatório da pesquisa e as planilhas de origem.

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

Há uma saída histórica de R² = **0,985** na variante `B01`. Trata-se de um ajuste registrado, **não reexecutado**: faltam os dados brutos, a identificação do composto, as unidades completas e uma avaliação independente. O repositório não estabelece limite de detecção, limite de quantificação ou validação analítica.

A versão organizada corrige problemas de alinhamento e pareamento encontrados nos protótipos. Ela é uma implementação posterior, não uma reprodução automática das saídas históricas. [Detalhes](docs/experiments.md) · [Origem](docs/provenance.json) · [Autoria e direitos](RIGHTS.md).
