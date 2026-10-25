# Validação da curadoria

Verificação local em 25/10/2026: Python 3.12.14, Pandas 3.0.1 e Openpyxl 3.1.5.

- 10 testes automatizados passaram: ajuste e inversão de curva conhecida, dados degenerados, preservação de pares, janela de pico, rejeição de grades incompatíveis, leitura CSV UTF-16LE/XLSX, nomes de amostra e três verificações dos dados fornecidos.
- Os 9 notebooks passaram pela validação de estrutura; as células Python sem comandos mágicos passaram pela análise sintática.
- A demonstração sintética e a interface de calibração foram executadas e verificadas.
- As células dos 6 notebooks históricos foram comparadas com os originais: código e texto preservados, saídas e metadados de execução removidos.
- Links locais da documentação verificados; não foram encontrados padrões comuns de credenciais no conteúdo publicado.

Na complementação chegaram seis séries instrumentais VIN e suas planilhas derivadas. A consolidação de 69 linhas, os seis máximos e o ajuste foram recalculados; R² = 0,9849660358 coincide com o valor histórico arredondado. A regressão também foi conferida com NumPy, por implementação independente. Os espectros foram comparados à consolidação histórica de 190 a 400 nm.

Os scripts originais dos notebooks históricos não foram executados sobre as fontes. Não se reproduziram os experimentos de MTX/tempo, cujas planilhas não foram identificadas no ZIP. Os arquivos originais permanecem intactos. O GitHub Actions repete os testes e a validação estrutural; consulte o PR para o status remoto.
