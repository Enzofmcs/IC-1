# Validação da curadoria

Verificação local em 25/10/2026: Python 3.12.14, Pandas 3.0.1 e Openpyxl 3.1.5.

- 7 testes automatizados passaram: ajuste e inversão de curva conhecida, dados degenerados, preservação de pares, janela de pico, rejeição de grades incompatíveis, leitura CSV UTF-16LE/XLSX e nomes de amostra.
- Os 8 notebooks passaram pela validação de estrutura; as células Python sem comandos mágicos passaram pela análise sintática.
- A demonstração sintética e a interface de calibração foram executadas e verificadas.
- As células dos 6 notebooks históricos foram comparadas com os originais: código e texto preservados, saídas e metadados de execução removidos.
- Links locais da documentação verificados; não foram encontrados padrões comuns de credenciais no conteúdo publicado.

As planilhas experimentais não estavam nos ZIPs. Os resultados históricos não foram recalculados. O fluxo que depende dessas planilhas não foi executado. O GitHub Actions configura a repetição dos testes e da validação estrutural em um ambiente limpo; o status de cada execução deve ser consultado no PR.
