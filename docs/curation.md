# Catálogo dos notebooks históricos

A sequência abaixo é uma **ordem de leitura proposta**, inferida pelo conteúdo. Não é uma cronologia comprovada dos experimentos. Os códigos A/B/C distinguem as três exportações fornecidas.

| ID | Arquivo organizado | Conteúdo e diferenças | Limitações |
|---|---|---|---|
| B02 | [01_spectra_csv](../notebooks/historical/01_spectra_csv.ipynb) | Consolidação de espectros CSV UTF-16LE; absorção por comprimento de onda. | Os seis CSVs chegaram na complementação; o composto das séries numeradas permanece sem identificação. O CSV 1 aparece somente em uma consolidação. |
| B00 | [02_spectral_difference](../notebooks/historical/02_spectral_difference.ipynb) | Diferença de curvas e interpolação cúbica. | ALL SRF & IMT.xlsx fornecida na complementação; siglas não identificadas. Ordena x sem reordenar y; a fórmula da planilha usa outra referência de subtração. |
| A03 | [03_nova_initial](../notebooks/historical/03_nova_initial.ipynb) | Primeira variante de consolidação NOVA e ajuste linear. | Duas definições de NOVAsheet; chamada de análise antes da geração e exemplo final incompleto. |
| B01 | [04_nova_calibration](../notebooks/historical/04_nova_calibration.ipynb) | Variante com ordenação natural, filtro de potencial e R². | As seis tabelas VIN e os derivados foram fornecidos; a curva foi recalculada. Persistem erros de cabeçalho e chamadas fora de ordem no original; use ic1.reproduce. |
| A10 | [05_peak_exploration](../notebooks/historical/05_peak_exploration.ipynb) | Inspeção de corrente por tempo/potencial e localização do máximo. | Planilha sla.xlsx não fornecida; composto não identificado. |
| C26 | [06_antibody_exploration](../notebooks/historical/06_antibody_exploration.ipynb) | Exploração de máximos de enzima/anticorpo e regressão. | Vínculo com a IC-1 pendente; ordena sinais independentemente das concentrações e lê arquivo antes de gerá-lo. Não usar como curva validada. |

## Critérios de seleção

Foram inspecionadas 104 entradas dos três ZIPs. Arquivos vazios, exercícios de disciplinas e projetos sem relação demonstrada com estas pesquisas ficaram fora dos repositórios. Arquivos de nomes iguais em exportações diferentes não foram tratados automaticamente como duplicatas. Hashes e origem permitem rastrear a seleção.

As saídas embutidas, imagens e metadados de sessão foram removidos das cópias públicas. Nenhuma execução histórica foi simulada ou reconstituída. Trechos de métricas efetivamente salvos foram transcritos em um arquivo de evidência separado.

## Complementação com relatórios e dados

As notas de B02, B00 e B01 foram atualizadas após o recebimento das planilhas. B01 agora tem reprodução numérica documentada. O contexto de MTX/VIN está confirmado pelo relatório, mas IMT/SRF e C26 continuam sem identificação específica. Veja [revisão das evidências](report_review.md).
