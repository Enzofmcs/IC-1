# Evidências adicionais da IC-1

## Identificação e contribuição

O documento fornecido tem o título “Otimização da coleta de dados de métodos analíticos desenvolvidos para a detecção do antitumoral metotrexato”. Identifica Enzo Souza como bolsista Fapic e Augusto Etchegaray Júnior como orientador. O projeto do orientador trata de surfactinas e resistência a múltiplas drogas. Isso contextualiza o laboratório, mas não basta para expandir as siglas IMT/SRF dos arquivos.

O cabeçalho do documento diz **relatório parcial**, referente a setembro/2023–fevereiro/2024, datado de março/2024. O cronograma inclui atividades previstas até agosto/2024; isso não comprova execução de todas elas. O nome do arquivo diz “FINAL”, divergindo do conteúdo. Não se atribuiu uma data final à IC com base apenas no nome.

Nas seções Objetivos e Metodologia, a contribuição é auxiliar na coleta e análise de dados de HPLC e biossensores, automatizar planilhas e gráficos com Python. Os equipamentos descritos são HPLC Perkin Elmer Flexar/Chromera e potenciostato AUTOLAB PGSTAT 204/NOVA. Há duas versões do NOVA citadas no texto, 2.1.2 e 2.1.4; a versão exata por ensaio não foi comprovada.

Resultados Obtidos descreve `printagraf` e `plotTxA`. As figuras mostram chamadas e gráficos de corrente/potencial e corrente/tempo, inclusive rótulos de MTX. As implementações completas dessas duas funções não foram encontradas nos 104 notebooks ou no ZIP adicional. Não se afirma que `NOVAsheet` seja a mesma função nem que os sinais VIN reproduzam os gráficos de MTX.

## Reprodução numérica da série VIN

O ZIP adicional contém seis exportações NOVA `VIN-200nmol.xlsx` a `VIN-1200nmol.xlsx`, a consolidação `tesss2/novaplanilha.xlsx` e a tabela de máximos `tesss2/novaplanilha2.xlsx`. As cópias CSV preservam os valores e os cabeçalhos numéricos; originais e hashes estão em `additional_sources.json`.

- Cada exportação contém 74 medições e 7 colunas. O XML de dimensão declara apenas A1; leitores que respeitam esse limite podem mostrar o arquivo como quase vazio. Os dados foram lidos integralmente sem modificar a fonte.
- Aplicou-se a mesma condição de B01: potencial >= -0,025177002 V. Permanecem 69 medições por amostra.
- A consolidação recalculada confere com os 69 registros de `novaplanilha.xlsx`; os seis máximos conferem com `novaplanilha2.xlsx`, que não tem cabeçalho.
- Ajustou-se `corrente máxima = a * quantidade rotulada + b`, mantendo o pareamento de cada amostra.

| Parâmetro | Recalculado |
|---|---|
| Número de pontos de ajuste | 6 |
| Inclinação | 3,1991141183e-09 A por unidade rotulada nmol |
| Intercepto | 5,0739746094e-05 A |
| R² | 0,9849660358 |
| RMSE no ajuste | 1,3499859733e-07 A |

O R² arredondado reproduz 0,985 de B01. Os rótulos `nmol` indicam quantidade, e não foram reinterpretados como nM ou nmol/L. Não há volume, réplicas independentes, branco validado ou conjunto externo suficiente para estimar desempenho analítico ou concentração em amostra desconhecida.

## Espectros e materiais relacionados

Os seis CSVs numerados possuem 911 medições entre 190 e 1.100 nm, com absorbância e desvio-padrão. Sua consolidação de 190 a 400 nm confere com `newsheet/test1.xlsx`. `12-12-23-ALL.xlsx` contém ainda a coluna `1.CSV`, cuja fonte não está no ZIP; ela não foi inventada nem reconstruída.

`ALL SRF & IMT.xlsx` foi transcrito apenas nas colunas A:G, de observações. A fórmula da coluna H usa G-D, enquanto B00 subtrai G-C; a coluna J contém valores derivados. Não se escolheu silenciosamente uma dessas diferenças como resultado analítico correto. O gráfico PNG fornecido é compatível com a comparação rotulada de B00, mas não identifica quimicamente IMT/SRF.

Arquivos `~$` são bloqueios temporários de Excel e ficaram fora. `testes/teste32/X.xlsx` não identifica o composto/quantidade e não entrou no ajuste VIN. Os três notebooks do ZIP novo são idênticos por hash a B02, B00 e B01; não foram duplicados.
