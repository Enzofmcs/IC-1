# Método e leitura crítica dos experimentos

## Ordem de leitura

1. `B02`: importar espectros CSV, unir colunas e recortar comprimentos de onda até 400.
2. `B00`: explorar a subtração entre curvas e a suavização apenas para visualização.
3. `A03` e `B01`: comparar as variantes do processamento de planilhas NOVA.
4. `A10`: inspecionar sinais e o ponto máximo de uma série.
5. `C26`: consultar como material relacionado de vínculo ainda não confirmado.

Essa sequência é conceitual; os arquivos não comprovam a ordem cronológica dos experimentos.

## Diferenças recuperadas

`A03` define `NOVAsheet` duas vezes; a definição final altera o formato esperado. `B01` usa ordenação natural dos nomes, inclui a janela `Potential applied (V) >= -0.025177002`, cria uma tabela de máximos e acrescenta R². Na tabela de máximos, a escrita em A1/B1 sobrepõe o cabeçalho da primeira linha. Nenhuma dessas decisões deve ser assumida adequada a outros dados sem revisar o protocolo.

`B00` usa colunas chamadas `IMT 1uM` e `IMT 1uM SRF 8uM`. O significado de IMT/SRF não foi identificado. `C26` lê uma planilha com enzima e anticorpo; também não há evidência suficiente para associá-la a metotrexato ou vincristina. O autor informou não reconhecer essas siglas no momento da curadoria; o relatório integral da IC ainda não foi fornecido.

## Problemas que motivaram a versão organizada

- Unir correntes por índice pode combinar grades de potencial diferentes silenciosamente. `consolidate_signals` agora exige grades compatíveis.
- Em `B00`, ordenar apenas x perde a correspondência com y. `subtract_signals` preserva os pares e recusa grades incompatíveis.
- Em `C26`, ordenar apenas os máximos antes da regressão destrói o pareamento concentração/resposta. O novo ajuste recebe explicitamente os pares.
- Planilhas ausentes, variáveis herdadas e chamadas fora de ordem impedem uma execução limpa dos cadernos históricos.
- A nova API recusa valores não finitos, concentrações constantes e extrapolação implícita. Não altera sinais por suavização antes de encontrar picos.

## Evidência histórica

Consulte `results/historical_evidence.json`: cada trecho indica notebook e número da célula original, antes da adição da nota de curadoria.

| Origem | Registro salvo | Interpretação permitida |
|---|---|---|
| A03 | y = 2,81e-07 x + 5,11e-05 | Coeficientes de uma execução registrada; conjunto e unidade não recuperados |
| B01 | y = 3,20e-09 x + 5,07e-05; R² = 0,985 | Ajuste registrado de outra variante; não comparar inclinações sem os dados |

Os registros não comprovam precisão de estimação de concentração, seletividade, recuperação, estabilidade, LOD ou LOQ. Essas propriedades não foram recalculadas.

## Como adicionar os dados reais

Guarde os arquivos autorizados em `data/raw/` (ignorado pelo Git), registre composto, unidade de concentração, branco, repetições, protocolo e janela de potencial. Não misture séries de compostos ou unidades diferentes. Conserve a associação entre cada concentração e sua medição; não ordene os dois vetores separadamente.

A função `fit_calibration` calcula OLS, R² e RMSE no próprio conjunto de ajuste. Separe amostras independentes para avaliação se disponíveis. O procedimento não seleciona automaticamente o modelo químico mais apropriado.
