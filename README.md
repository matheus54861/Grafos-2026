# Projeto Prático: Coloração de Mapas e Grafos (Tema 8)

## Integrantes

- Nome do Integrante 1 (RA: ...)
- Nome do Integrante 2 (RA: ...)
- Nome do Integrante 3 (RA: ...)
- Nome do Integrante 4 (RA: ...)

## Descrição do Problema

O projeto resolve o problema de coloração de mapas geográficos (como os estados do Brasil), garantindo que regiões fronteiriças não recebam a mesma cor utilizando o menor número possível de cores (Teorema das 4 Cores).

## Como Instalar e Executar

1. Instancie o ambiente virtual: `python -m venv venv` e ative-o.
2. Instale as dependências: `pip install -r requirements.txt`
3. Execute a aplicação: `streamlit run app.py`

## Algoritmos Implementados

- **Welsh-Powell**: Abordagem gulosa baseada na ordenação decrescente de graus.
- **DSATUR**: Heurística avançada baseada no grau de saturação de cores vizinhas.
